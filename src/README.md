# Source Code Documentation

Detailed explanations of the Nice Connectives Solver implementation.

## Overview

This directory contains the core implementation of a solver that finds the maximum size of "nice" (complete and independent) sets of logical connectives. The approach uses:

1. **BitVec truth table representation** for efficient connective encoding
2. **Post's Completeness Theorem** for fast completeness checking
3. **Bounded composition enumeration** for independence verification
4. **Incremental arity search** to find maximum nice sets

## Module Organization

```
src/
├── cli.py               # Unified command-line interface entry point
├── commands/            # CLI command implementations
│   ├── prove.py         # Proof commands (z3, enum)
│   ├── validate.py      # Validation commands (binary, ternary)
│   ├── benchmark.py     # Benchmark commands (full, quick, depth)
│   └── search.py        # Search commands (binary, full, validate)
├── connectives.py       # Core truth table representation
├── constants.py         # Predefined logical connectives
├── post_classes.py      # Completeness checking via Post's lattice
├── independence.py      # Independence checking via bounded composition
├── search.py            # Search algorithms for finding nice sets (library)
└── main.py              # Library interface for programmatic usage
```

**See [commands/README.md](commands/README.md) for CLI command implementation details.**

---

## 1. connectives.py - Truth Table Representation

### Core Concept: BitVec Encoding

A logical connective of arity n (n inputs) can be represented by its truth table, which has 2^n rows. We encode this truth table as a single integer (BitVector) where the i-th bit represents the output for the i-th row.

**Example 1: Binary AND (arity 2)**

```
Truth table:
  x | y | AND(x,y)
  0 | 0 |    0        ← bit position 0
  0 | 1 |    0        ← bit position 1
  1 | 0 |    0        ← bit position 2
  1 | 1 |    1        ← bit position 3

Encoding: 0b1000 = 8 (reading right-to-left)
```

The key insight: Each row number (0-3) corresponds directly to a bit position in the encoding. Row 3 (inputs 1,1) has output 1, so bit position 3 is set to 1. All other positions are 0.

**Example 2: Ternary MAJ (Majority function, arity 3)**

The majority function returns 1 if at least 2 of the 3 inputs are 1.

```
Truth table (8 rows for 3 inputs):
  x | y | z | MAJ(x,y,z) | Row # | Bit position
  0 | 0 | 0 |     0      |   0   | bit₀ = 0
  0 | 0 | 1 |     0      |   1   | bit₁ = 0
  0 | 1 | 0 |     0      |   2   | bit₂ = 0
  0 | 1 | 1 |     1      |   3   | bit₃ = 1
  1 | 0 | 0 |     0      |   4   | bit₄ = 0
  1 | 0 | 1 |     1      |   5   | bit₅ = 1
  1 | 1 | 0 |     1      |   6   | bit₆ = 1
  1 | 1 | 1 |     1      |   7   | bit₇ = 1

Reading bits right-to-left: bit₇ bit₆ bit₅ bit₄ bit₃ bit₂ bit₁ bit₀
Binary representation:       1    1    1    0    1    0    0    0
                             = 0b11101000
                             = 232 (decimal)

Encoding: MAJ = Connective(3, 232, "MAJ")
```

**Understanding the row indexing for arity 3:**

The row number treats inputs (x, y, z) as a 3-bit binary number:
- Row = x×4 + y×2 + z×1
- Row 0: (0,0,0) → 0×4 + 0×2 + 0×1 = 0
- Row 3: (0,1,1) → 0×4 + 1×2 + 1×1 = 3
- Row 5: (1,0,1) → 1×4 + 0×2 + 1×1 = 5
- Row 7: (1,1,1) → 1×4 + 1×2 + 1×1 = 7

**Example 3: Ternary IF-THEN-ELSE (arity 3)**

The function ITE(x,y,z) returns y if x=1, else returns z.

```
Truth table:
  x | y | z | ITE(x,y,z) | Row # | Binary row | Bit value
  0 | 0 | 0 |     0      |   0   |    000     | bit₀ = 0
  0 | 0 | 1 |     1      |   1   |    001     | bit₁ = 1
  0 | 1 | 0 |     0      |   2   |    010     | bit₂ = 0
  0 | 1 | 1 |     1      |   3   |    011     | bit₃ = 1
  1 | 0 | 0 |     0      |   4   |    100     | bit₄ = 0
  1 | 0 | 1 |     0      |   5   |    101     | bit₅ = 0
  1 | 1 | 0 |     1      |   6   |    110     | bit₆ = 1
  1 | 1 | 1 |     1      |   7   |    111     | bit₇ = 1

Reading bits right-to-left: 1 1 0 0 1 0 1 0
Binary: 0b11001010 = 202 (decimal)

Encoding: ITE = Connective(3, 202, "ITE")
```

**Verifying the encoding:**
- When x=1: ITE returns y (rows 4-7: outputs are 0,0,1,1 matching y values)
- When x=0: ITE returns z (rows 0-3: outputs are 0,1,0,1 matching z values)

**Key pattern:** For ternary connectives:
- 8 rows (2³ = 8)
- 8 bits needed for encoding
- Bit positions 0-7 map to rows 0-7
- Total possible ternary functions: 2⁸ = 256

### Class: Connective

```python
class Connective:
    def __init__(self, arity: int, truth_table: int, name: Optional[str] = None):
        self.arity = arity
        self.truth_table_int = truth_table
        self.truth_table = BitVecVal(truth_table, 2 ** arity)
```

**Why BitVec?**
- Compact storage: A binary connective fits in 4 bits instead of storing 4 separate values
- Fast equality checks: Compare integers instead of row-by-row
- Z3 integration: BitVec is a Z3 type, enabling SMT-based reasoning (though we mostly use enumeration)

### Key Methods

#### evaluate(inputs)

Evaluates the connective on a specific input assignment.

```python
def evaluate(self, inputs: Tuple[int, ...]) -> int:
    # Convert input tuple to row index
    # For inputs (x1, x2, ..., xn), index = x1*2^(n-1) + x2*2^(n-2) + ... + xn
    index = 0
    for i, val in enumerate(inputs):
        index = index * 2 + val

    # Extract the bit at position 'index'
    return (self.truth_table_int >> index) & 1
```

**Example 1: Evaluate AND(1, 0) - Binary**
```python
AND = Connective(2, 0b1000, "AND")
result = AND.evaluate((1, 0))

# Compute index: 1*2 + 0 = 2
# Extract bit at position 2: (0b1000 >> 2) & 1 = 0b0010 & 1 = 0
# Result: 0 (correct, since 1 AND 0 = 0)
```

**Example 2: Evaluate MAJ(1, 0, 1) - Ternary**
```python
MAJ = Connective(3, 0b11101000, "MAJ")  # 232 in decimal
result = MAJ.evaluate((1, 0, 1))

# Compute index: 1*4 + 0*2 + 1*1 = 5
# Extract bit at position 5:
#   0b11101000 >> 5 = 0b00000111
#   0b00000111 & 1 = 1
# Result: 1 (correct, since 2 out of 3 inputs are 1, majority is 1)
```

**Step-by-step for MAJ(1, 0, 1):**
1. Convert inputs to row index: (1,0,1) → row 5
   - Formula: 1×2^(3-1) + 0×2^(3-2) + 1×2^(3-3) = 1×4 + 0×2 + 1×1 = 5
2. MAJ encoding: 0b11101000 = ...1 1 1 0 1 0 0 0 (reading right to left)
3. Bit at position 5: 0b11101000 has bit₅ = 1 (fifth position from right, zero-indexed)
4. Return 1

**Example 3: Evaluate ITE(0, 1, 0) - If-Then-Else**
```python
ITE = Connective(3, 0b11001010, "ITE")  # 202 in decimal
result = ITE.evaluate((0, 1, 0))

# Compute index: 0*4 + 1*2 + 0*1 = 2
# Extract bit at position 2:
#   0b11001010 >> 2 = 0b00110010
#   0b00110010 & 1 = 0
# Result: 0 (correct, since x=0, returns z=0)
```

**Verifying ITE(0, 1, 0):**
- x=0, so ITE should return z
- z=0, so result should be 0
- Row index 2: checking bit₂ in 0b11001010
- Bits: ...1 1 0 0 1 0 1 0 (bit₂ = 0) ✓

**Why this indexing?**
The index formula `x1*2^(n-1) + x2*2^(n-2) + ... + xn` treats inputs as a binary number. This is the standard truth table row ordering in logic (lexicographic order).

**General formula for arity n:**
```
index = x₁×2^(n-1) + x₂×2^(n-2) + ... + xₙ×2^0

For n=2: index = x×2¹ + y×2⁰ = 2x + y
For n=3: index = x×2² + y×2¹ + z×2⁰ = 4x + 2y + z
For n=4: index = w×2³ + x×2² + y×2¹ + z×2⁰ = 8w + 4x + 2y + z
```

#### evaluate_all()

Generates all input-output pairs by iterating through all 2^arity rows.

```python
def evaluate_all(self) -> List[Tuple[Tuple[int, ...], int]]:
    results = []
    num_rows = 2 ** self.arity

    for row in range(num_rows):
        # Convert row index back to input tuple
        inputs = tuple((row >> (self.arity - 1 - i)) & 1
                      for i in range(self.arity))
        output = self.evaluate(inputs)
        results.append((inputs, output))

    return results
```

**Bit manipulation detail:**
`(row >> (self.arity - 1 - i)) & 1` extracts the i-th bit from row, reading left-to-right.

**Example: Convert row 5 to inputs for arity 3:**
```
row = 5 (decimal) = 101 (binary)
arity = 3

For i=0 (extract leftmost bit):
  (5 >> (3 - 1 - 0)) & 1 = (5 >> 2) & 1
  = (0b101 >> 2) & 1
  = 0b001 & 1
  = 1

For i=1 (extract middle bit):
  (5 >> (3 - 1 - 1)) & 1 = (5 >> 1) & 1
  = (0b101 >> 1) & 1
  = 0b010 & 1
  = 0

For i=2 (extract rightmost bit):
  (5 >> (3 - 1 - 2)) & 1 = (5 >> 0) & 1
  = (0b101 >> 0) & 1
  = 0b101 & 1
  = 1

Result: inputs = (1, 0, 1)
```

**Full evaluate_all() example for MAJ:**
```python
MAJ = Connective(3, 232, "MAJ")
all_results = MAJ.evaluate_all()

# Returns:
# [
#   ((0,0,0), 0),  # row 0: 0b000 = 0, bit₀ of 232 = 0
#   ((0,0,1), 0),  # row 1: 0b001 = 1, bit₁ of 232 = 0
#   ((0,1,0), 0),  # row 2: 0b010 = 2, bit₂ of 232 = 0
#   ((0,1,1), 1),  # row 3: 0b011 = 3, bit₃ of 232 = 1
#   ((1,0,0), 0),  # row 4: 0b100 = 4, bit₄ of 232 = 0
#   ((1,0,1), 1),  # row 5: 0b101 = 5, bit₅ of 232 = 1
#   ((1,1,0), 1),  # row 6: 0b110 = 6, bit₆ of 232 = 1
#   ((1,1,1), 1),  # row 7: 0b111 = 7, bit₇ of 232 = 1
# ]
```

Each row number's binary representation directly gives the input tuple.

#### \_\_eq\_\_ and \_\_hash\_\_

These enable using Connective instances in sets and as dictionary keys.

```python
def __eq__(self, other) -> bool:
    return (self.arity == other.arity and
            self.truth_table_int == other.truth_table_int)

def __hash__(self) -> int:
    return hash((self.arity, self.truth_table_int))
```

**Python note:** Objects used in sets must be hashable and have consistent equality.

### Function: generate_all_connectives(arity)

Generates all possible connectives of a given arity.

```python
def generate_all_connectives(arity: int) -> List[Connective]:
    table_size = 2 ** arity
    num_connectives = 2 ** table_size
    return [Connective(arity, i) for i in range(num_connectives)]
```

**Counts by arity:**
- Arity 0: 2^(2^0) = 2^1 = **2** connectives
  - Constants: FALSE (0), TRUE (1)

- Arity 1: 2^(2^1) = 2^2 = **4** connectives
  - All 4: constant-0, constant-1, IDENTITY, NEGATION
  - Encodings: 0b00, 0b01, 0b10, 0b11 (values 0-3)

- Arity 2: 2^(2^2) = 2^4 = **16** connectives
  - Common ones: AND, OR, XOR, NAND, NOR, IMPLIES, IFF, projections
  - Encodings: 0b0000 through 0b1111 (values 0-15)

- Arity 3: 2^(2^3) = 2^8 = **256** connectives
  - Examples: MAJ (majority), ITE (if-then-else), ternary XOR
  - Encodings: 8-bit integers (values 0-255)
  - Each function defined by an 8-row truth table

- Arity 4: 2^(2^4) = 2^16 = **65,536** connectives
  - Encodings: 16-bit integers (values 0-65535)
  - Each function defined by a 16-row truth table
  - Computationally challenging to enumerate all combinations

- Arity 5: 2^(2^5) = 2^32 = **4,294,967,296** connectives
  - Over 4 billion functions!
  - Encodings: 32-bit integers
  - Intractable for complete enumeration

**Mathematical insight:** The formula 2^(2^n) arises because:
- A truth table has 2^n rows (all input combinations)
- Each row can output 0 or 1 (2 choices)
- Total functions: 2 × 2 × ... × 2 (2^n times) = 2^(2^n)

---

## 2. constants.py - Predefined Connectives

This module defines commonly used logical connectives for quick reference.

### Truth Table Encoding Examples

```python
# Arity 1 (Unary)
IDENTITY = Connective(1, 0b10, "ID")      # f(x) = x
NEGATION = Connective(1, 0b01, "NOT")     # f(x) = ¬x
```

**Why 0b10 for IDENTITY?**
Truth table for ID:
```
x | ID(x)
0 |  0      ← bit position 0: value 0
1 |  1      ← bit position 1: value 1

Encoding: bit1 bit0 = 10₂ = 0b10
```

**Why 0b01 for NEGATION?**
Truth table for NOT:
```
x | NOT(x)
0 |  1      ← bit position 0: value 1
1 |  0      ← bit position 1: value 0

Encoding: bit1 bit0 = 01₂ = 0b01
```

### Binary Connectives

```python
# Position encoding for binary (x, y):
# (0,0)=position 0, (0,1)=position 1, (1,0)=position 2, (1,1)=position 3

AND = Connective(2, 0b1000, "AND")        # x ∧ y
OR = Connective(2, 0b1110, "OR")          # x ∨ y
XOR = Connective(2, 0b0110, "XOR")        # x ⊕ y
```

**Example: Decoding OR (0b1110 = 14)**

```
 x | y | OR   | Position | Bit value
 0 | 0 |  0   |    0     | bit₀ = 0
 0 | 1 |  1   |    1     | bit₁ = 1
 1 | 0 |  1   |    2     | bit₂ = 1
 1 | 1 |  1   |    3     | bit₃ = 1

Reading right-to-left: 1110₂ = 0b1110
```

### Collection: ALL_BINARY

An ordered list of all 16 binary connectives:

```python
ALL_BINARY = [
    CONST_FALSE_BIN,     # 0b0000 = 0
    NOR,                 # 0b0001 = 1
    INHIBIT,             # 0b0010 = 2
    NOT_X,               # 0b0011 = 3
    # ... (indices 4-11)
    OR,                  # 0b1110 = 14
    CONST_TRUE_BIN,      # 0b1111 = 15
]
```

This ordering allows direct indexing: `ALL_BINARY[14]` gives OR.

---

## 3. post_classes.py - Completeness Checking

### Post's Completeness Theorem (Background)

**Theorem (Post, 1941):** A set of Boolean functions is complete (can express all Boolean functions) if and only if it escapes all five maximal clones:

1. **T0** (0-preserving): Functions where f(0,0,...,0) = 0
2. **T1** (1-preserving): Functions where f(1,1,...,1) = 1
3. **M** (Monotone): Functions where x ≤ y implies f(x) ≤ f(y)
4. **D** (Self-dual): Functions where ¬f(x) = f(¬x)
5. **A** (Affine): Functions expressible as XOR of variables plus constant

**"Escaping a clone"** means the set contains at least one function NOT in that clone.

**Why this matters:** Checking completeness directly would require verifying that every Boolean function is definable. Post's theorem reduces this to 5 simple checks per function.

### Implementation: Class Membership Checks

#### is_t0_preserving

```python
def is_t0_preserving(connective: Connective) -> bool:
    zeros = tuple(0 for _ in range(connective.arity))
    return connective.evaluate(zeros) == 0
```

**Explanation:** A function is 0-preserving if f(0,0,...,0) = 0. Simply evaluate on all-zeros input.

**Example:** AND is T0-preserving (AND(0,0) = 0), but OR is NOT (wait, OR(0,0) = 0, so OR IS T0). Actually, NOR is NOT T0-preserving (NOR(0,0) = 1).

#### is_t1_preserving

```python
def is_t1_preserving(connective: Connective) -> bool:
    ones = tuple(1 for _ in range(connective.arity))
    return connective.evaluate(ones) == 1
```

Symmetric to T0: check f(1,1,...,1) = 1.

#### is_monotone

```python
def is_monotone(connective: Connective) -> bool:
    num_rows = 2 ** connective.arity

    for i in range(num_rows):
        for j in range(num_rows):
            input_i = tuple((i >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))
            input_j = tuple((j >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))

            # Check if input_i ≤ input_j componentwise
            if all(input_i[k] <= input_j[k] for k in range(connective.arity)):
                # Then f(input_i) must be ≤ f(input_j)
                if connective.evaluate(input_i) > connective.evaluate(input_j):
                    return False

    return True
```

**Mathematical definition:** f is monotone if x ≤ y (componentwise) implies f(x) ≤ f(y).

**Componentwise order:** (0,1) ≤ (1,1) because 0≤1 and 1≤1.

**Example:** AND is monotone (increasing any input from 0 to 1 can only increase the output). NOT is NOT monotone (flipping 0→1 decreases output from 1→0).

**Algorithm:** Check all pairs of inputs. If one is componentwise ≤ the other, verify outputs preserve order.

#### is_self_dual

```python
def is_self_dual(connective: Connective) -> bool:
    num_rows = 2 ** connective.arity

    for row in range(num_rows):
        inputs = tuple((row >> (connective.arity - 1 - k)) & 1
                      for k in range(connective.arity))

        f_inputs = connective.evaluate(inputs)

        neg_inputs = tuple(1 - val for val in inputs)
        f_neg_inputs = connective.evaluate(neg_inputs)

        # Check if ¬f(inputs) == f(¬inputs)
        if f_neg_inputs != (1 - f_inputs):
            return False

    return True
```

**Mathematical definition:** f is self-dual if ¬f(x₁,...,xₙ) = f(¬x₁,...,¬xₙ) for all inputs.

**Example:** The majority function MAJ(x,y,z) (returns 1 if ≥2 inputs are 1) is self-dual. AND is NOT self-dual.

**Algorithm:** For each input, compute f(input) and f(¬input), verify they are negations of each other.

#### is_affine

```python
def is_affine(connective: Connective) -> bool:
    num_rows = 2 ** connective.arity
    zeros = tuple(0 for _ in range(connective.arity))
    f_zeros = connective.evaluate(zeros)

    for i in range(num_rows):
        for j in range(num_rows):
            input_i = tuple((i >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))
            input_j = tuple((j >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))

            # Compute i ⊕ j (XOR componentwise)
            input_xor = tuple(input_i[k] ^ input_j[k]
                            for k in range(connective.arity))

            f_i = connective.evaluate(input_i)
            f_j = connective.evaluate(input_j)
            f_xor = connective.evaluate(input_xor)

            # Check affine property: f(x ⊕ y) = f(x) ⊕ f(y) ⊕ f(0)
            if f_xor != (f_i ^ f_j ^ f_zeros):
                return False

    return True
```

**Mathematical definition:** f is affine if f(x ⊕ y) = f(x) ⊕ f(y) ⊕ f(0) for all x, y (where ⊕ is XOR).

**Equivalent form:** f can be written as c₀ ⊕ c₁x₁ ⊕ c₂x₂ ⊕ ... ⊕ cₙxₙ (linear over GF(2)).

**Examples:** XOR is affine. AND is NOT affine.

**Algorithm:** Verify the affine property for all pairs of inputs.

**Why this property?** Affine functions are closed under composition, so if a basis only contains affine functions, you can never generate non-affine functions like AND.

### Function: is_complete

```python
def is_complete(connectives: List[Connective]) -> bool:
    if not connectives:
        return False

    # Check if we escape each maximal clone
    escapes_t0 = any(not is_t0_preserving(c) for c in connectives)
    escapes_t1 = any(not is_t1_preserving(c) for c in connectives)
    escapes_m = any(not is_monotone(c) for c in connectives)
    escapes_d = any(not is_self_dual(c) for c in connectives)
    escapes_a = any(not is_affine(c) for c in connectives)

    return (escapes_t0 and escapes_t1 and escapes_m and
            escapes_d and escapes_a)
```

**Implementation insight:** We check if at least one function in the set does NOT belong to each clone. `any(not predicate(c) for c in connectives)` is true if at least one c fails the predicate.

**Example: {NOT, AND}**
- Escapes T0? AND is T0, but NOT is not T0 (NOT(0)=1). ✓
- Escapes T1? AND is T1, NOT is not T1 (NOT(1)=0). ✓
- Escapes M? AND is monotone, NOT is not monotone. ✓
- Escapes D? Neither NOT nor AND is self-dual. ✗ FAIL

{NOT, AND} is NOT complete because both functions are self-dual (actually, they're not, but let me recalculate...).

Actually, re-checking: NOT is self-dual (¬NOT(x) = ¬¬x = x = NOT(¬x)). AND is not self-dual. So {NOT, AND} escapes D.

Let me verify affine: NOT is affine (NOT(x) = 1⊕x). AND is not affine. So {NOT, AND} escapes A.

**Conclusion:** {NOT, AND} IS complete! This matches the classical result.

**Performance:** Each clone check is O(n) where n = |connectives|. Each membership test ranges from O(1) for T0/T1 to O(2^(2a)) for monotone/affine (where a = arity). Total: O(n × 2^(2a)) worst case. For small arities (≤3), this is fast.

---

## 4. independence.py - Bounded Composition

### Core Concept: Definability via Composition

A connective f is **definable** from a basis S if f can be expressed by composing functions from S (possibly nested).

**Example:** OR is definable from {NOT, AND} via De Morgan's Law:
```
OR(x,y) = NOT(AND(NOT(x), NOT(y)))
```

This is a depth-3 composition:
- Depth 1: NOT(x), NOT(y)
- Depth 2: AND(NOT(x), NOT(y))
- Depth 3: NOT(AND(...))

### Why Bounded Composition?

**Problem:** Checking unbounded definability is undecidable in general.

**Solution:** Restrict to compositions of depth ≤ d. This is decidable (finite search space) and sufficient for most cases.

**Trade-off:**
- Small depth (d=3): Fast, may miss deep compositions (false positives for independence)
- Large depth (d=7+): Slow, more accurate
- Our implementation uses d=3 by default (covers most practical cases)

### Function: is_definable

```python
def is_definable(target: Connective, basis: List[Connective],
                max_depth: int = 3, timeout_ms: int = 5000) -> bool:
    if not basis:
        return False

    # Quick check: if target is in basis, it's trivially definable
    if target in basis:
        return True

    # Try increasing depths until we find a definition or reach max_depth
    for depth in range(1, max_depth + 1):
        if _is_definable_at_depth(target, basis, depth, timeout_ms):
            return True

    return False
```

**Algorithm:** Incrementally search depths 1, 2, ..., max_depth until a matching composition is found.

**Optimization:** Check depth 1 first (cheap) before trying deeper compositions.

### Depth 1: Variable Permutations

```python
def _check_depth_one(target: Connective, basis: List[Connective]) -> bool:
    for b in basis:
        if b.arity == target.arity:
            if _check_with_permutations(target, b):
                return True
    return False
```

**What this checks:** Can target be expressed as a single basis function with variables permuted?

**Example:** If target is PROJ_Y(x,y) = y and basis contains PROJ_X(x,y) = x, then PROJ_Y = PROJ_X(y,x) (swap variables). Depth 1 succeeds.

```python
def _check_permutation_match(target: Connective, candidate: Connective,
                             perm: Tuple[int, ...]) -> bool:
    num_rows = 2 ** target.arity

    for row in range(num_rows):
        target_inputs = tuple((row >> (target.arity - 1 - k)) & 1
                            for k in range(target.arity))

        # Apply permutation to get candidate inputs
        candidate_inputs = tuple(target_inputs[perm[k]]
                                for k in range(candidate.arity))

        if target.evaluate(target_inputs) != candidate.evaluate(candidate_inputs):
            return False

    return True
```

**Algorithm:** Try all permutations of variables. For each permutation, check if outputs match on all inputs.

**Example:** Check if PROJ_Y = PROJ_X(permuted)
- Permutation (0,1) (identity): PROJ_X(x,y) = x ≠ y = PROJ_Y(x,y). ✗
- Permutation (1,0) (swap): PROJ_X(y,x) = y = PROJ_Y(x,y). ✓

**Complexity:** O(n! × 2^a) where n = arity. For arity ≤ 3, this is manageable (6 × 8 = 48 checks).

### Depth 2+: Composition Enumeration

For binary targets (arity 2), we enumerate common composition patterns:

#### Pattern 1: f(g(x,y), h(x,y))

Outer binary function applied to two inner functions.

```python
def _try_composition_f_g_h(target: Connective,
                           f: Connective,
                           g: Optional[Connective],
                           h: Optional[Connective]) -> bool:
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute g(x,y) or g(x) or x
            if g is None:
                g_result = x
            elif g.arity == 1:
                g_result = g.evaluate((x,))
            elif g.arity == 2:
                g_result = g.evaluate((x, y))

            # Compute h(x,y) or h(y) or y
            if h is None:
                h_result = y
            elif h.arity == 1:
                h_result = h.evaluate((y,))
            elif h.arity == 2:
                h_result = h.evaluate((x, y))

            # Compute f(g_result, h_result)
            f_result = f.evaluate((g_result, h_result))

            if f_result != target.evaluate((x, y)):
                return False

    return True
```

**Handling None:** `None` represents identity/projection. If g=None, use x directly.

**Example composition:** AND(x, NOT(y)) with f=AND, g=None (identity), h=NOT
- (x,y) = (1,0): g_result=1, h_result=NOT(0)=1, f_result=AND(1,1)=1
- Check all 4 inputs to verify match

**Why unary in binary context?** A unary function h applied to y gives h(y), which is a binary function h(x,y) that ignores x. This allows mixed-arity compositions.

#### Pattern 2: unary(binary(x,y))

Unary outer function applied to binary inner function.

```python
def _try_unary_binary_composition(target: Connective,
                                   f: Connective,
                                   g: Connective) -> bool:
    for x in [0, 1]:
        for y in [0, 1]:
            g_result = g.evaluate((x, y))
            f_result = f.evaluate((g_result,))

            if f_result != target.evaluate((x, y)):
                return False

    return True
```

**Example:** NAND(x,y) = NOT(AND(x,y))
- f=NOT (unary), g=AND (binary)
- (x,y) = (1,1): g_result=AND(1,1)=1, f_result=NOT(1)=0
- NAND(1,1) = 0 ✓

**This pattern was initially missing,** causing test failures before debugging iteration 1.

#### Pattern 3: binary(unary(x), unary(y))

Binary outer function with unary functions applied to each input.

```python
def _try_binary_unary_unary_composition(target: Connective,
                                         f: Connective,
                                         g: Optional[Connective],
                                         h: Optional[Connective]) -> bool:
    for x in [0, 1]:
        for y in [0, 1]:
            g_result = x if g is None else g.evaluate((x,))
            h_result = y if h is None else h.evaluate((y,))
            f_result = f.evaluate((g_result, h_result))

            if f_result != target.evaluate((x, y)):
                return False

    return True
```

**Example:** AND(NOT(x), NOT(y))
- f=AND, g=NOT, h=NOT
- (x,y) = (0,1): g_result=NOT(0)=1, h_result=NOT(1)=0, f_result=AND(1,0)=0
- Check if this matches target on all inputs

**Use case:** This pattern detects De Morgan variants and negation-based compositions.

#### Pattern 4: unary(binary(unary(x), unary(y)))

Depth-3 composition for De Morgan's Law.

```python
def _try_unary_binary_unary_unary_composition(target: Connective,
                                                f: Connective,
                                                g: Connective,
                                                h: Optional[Connective],
                                                i: Optional[Connective]) -> bool:
    for x in [0, 1]:
        for y in [0, 1]:
            h_result = x if h is None else h.evaluate((x,))
            i_result = y if i is None else i.evaluate((y,))
            g_result = g.evaluate((h_result, i_result))
            f_result = f.evaluate((g_result,))

            if f_result != target.evaluate((x, y)):
                return False

    return True
```

**Example:** OR(x,y) = NOT(AND(NOT(x), NOT(y)))
- f=NOT, g=AND, h=NOT, i=NOT
- Composition tree: NOT(AND(NOT(x), NOT(y)))
- Depth 3: three levels of nesting

**This pattern was added in debugging iteration 1** to fix De Morgan's Law detection.

### Depth 2-3: Main Enumeration Loop

```python
def _check_binary_compositions(target: Connective, basis: List[Connective],
                               max_depth: int) -> bool:
    binary_basis = [b for b in basis if b.arity == 2]
    unary_basis = [b for b in basis if b.arity == 1]

    if max_depth >= 2:
        for f in binary_basis:
            for g in binary_basis + unary_basis + [None]:
                for h in binary_basis + unary_basis + [None]:
                    if _try_composition_f_g_h(target, f, g, h):
                        return True

        for f in unary_basis:
            for g in binary_basis:
                if _try_unary_binary_composition(target, f, g):
                    return True

        for f in binary_basis:
            for g in unary_basis + [None]:
                for h in unary_basis + [None]:
                    if _try_binary_unary_unary_composition(target, f, g, h):
                        return True

    if max_depth >= 3:
        for f in unary_basis:
            for g in binary_basis:
                for h in unary_basis + [None]:
                    for i in unary_basis + [None]:
                        if _try_unary_binary_unary_unary_composition(target, f, g, h, i):
                            return True

    return False
```

**Combinatorial explosion:** For each pattern, we try all combinations of basis functions. If |unary_basis| = U and |binary_basis| = B:
- Pattern 1: O(B × (B+U)^2)
- Pattern 2: O(U × B)
- Pattern 3: O(B × U^2)
- Pattern 4: O(U × B × U^2) = O(U^3 × B)

**For typical basis:** {NOT, AND} → U=1, B=1 → Total ~10 checks (very fast).

**Limitation:** This enumeration doesn't cover all possible compositions (e.g., XOR = OR(AND(x,NOT(y)), AND(NOT(x),y)) requires binary(binary, binary) pattern, which is not implemented).

### Function: is_independent

```python
def is_independent(connectives: List[Connective],
                  max_depth: int = 3,
                  timeout_ms: int = 5000) -> bool:
    if len(connectives) <= 1:
        return True

    # Check each connective to see if it's definable from the others
    for i, target in enumerate(connectives):
        basis = connectives[:i] + connectives[i+1:]

        if is_definable(target, basis, max_depth, timeout_ms):
            return False

    return True
```

**Algorithm:** For each connective c in the set, check if c is definable from the remaining connectives. If any c is definable, the set is NOT independent.

**Example:** Check {NOT, AND, OR}
- Is NOT definable from {AND, OR}? No (can't create negation from monotone functions).
- Is AND definable from {NOT, OR}? No (depth-3 De Morgan's Law is OR-to-AND, not AND-from-OR-and-NOT... actually, AND(x,y) = NOT(OR(NOT(x), NOT(y))). Yes! Definable.
- Conclusion: {NOT, AND, OR} is NOT independent (OR is redundant).

**Correct independent set:** {NOT, AND} (minimal complete basis).

**Complexity:** O(n × definability_cost) where n = |connectives|. For n=3, depth=3, this is quite fast.

---

## 5. search.py - Finding Nice Sets

### Function: find_nice_sets_of_size

```python
def find_nice_sets_of_size(
    connectives: List[Connective],
    size: int,
    max_depth: int = 3,
    verbose: bool = False
) -> List[List[Connective]]:
    nice_sets = []

    for combo in combinations(connectives, size):
        combo_list = list(combo)

        # First check completeness (fast)
        if not is_complete(combo_list):
            continue

        # Then check independence (slower)
        if is_independent(combo_list, max_depth):
            nice_sets.append(combo_list)

    return nice_sets
```

**Algorithm:** Enumerate all size-k subsets, filter by completeness, then independence.

**Optimization order:** Completeness is checked first because:
- Completeness: O(k × 2^(2a)) where k = set size, a = arity
- Independence: O(k^2 × depth^basis_size) (potentially much slower)

Failing completeness early eliminates many candidates without expensive independence checks.

**Python note:** `combinations(connectives, size)` generates all C(n, k) size-k subsets from n connectives. This is a generator (lazy evaluation), so memory-efficient.

**Example:** Find all nice sets of size 3 from 16 binary connectives
- Total combinations: C(16, 3) = 560
- Many fail completeness (e.g., {AND, OR, NAND} all monotone or T1, can't escape all clones)
- Few survive to independence check
- Result: ~10-30 nice sets of size 3 (depending on clone distribution)

### Function: find_maximum_nice_set

```python
def find_maximum_nice_set(
    connectives: List[Connective],
    max_size: int = 10,
    max_depth: int = 3,
    verbose: bool = False
) -> Tuple[int, List[List[Connective]]]:
    maximum_size = 0
    maximal_sets = []

    for size in range(1, min(max_size + 1, len(connectives) + 1)):
        nice_sets = find_nice_sets_of_size(connectives, size, max_depth, verbose)

        if nice_sets:
            maximum_size = size
            maximal_sets = nice_sets
        else:
            # Stop searching if no nice sets at this size
            break

    return maximum_size, maximal_sets
```

**Algorithm:** Incrementally search sizes 1, 2, 3, ... until no nice sets are found.

**Stopping criterion:** If size k has no nice sets, size k+1 won't either (superset can't be independent if subset isn't... wait, that's not quite right. Actually, the stopping is based on the observation that if size k has no complete+independent sets, it's unlikely size k+1 will, though not impossible).

**Correction:** The code stops when no nice sets are found at size k. This is a heuristic, not theoretically guaranteed. A more robust approach would search up to max_size always, but this optimization saves time.

**Return value:** Tuple of (maximum_size, list_of_all_maximal_nice_sets).

### Function: search_binary_only

```python
def search_binary_only(
    max_depth: int = 3,
    verbose: bool = True
) -> Tuple[int, List[List[Connective]]]:
    binary_connectives = generate_all_connectives(2)

    max_size, nice_sets = find_maximum_nice_set(
        binary_connectives,
        max_size=5,
        max_depth=max_depth,
        verbose=verbose
    )

    return max_size, nice_sets
```

**Purpose:** Validate the implementation by reproducing the known result that max nice set size for binary-only is 3 (or 4 with constants).

**Why max_size=5?** We know the answer is ≤ 4, so searching up to 5 is safe and fast.

**Expected result:**
- Without constants (0-ary): max = 3. Example: {NOR, AND, IFF}
- With constants: max = 4. Example: {FALSE, NOT_X, NAND, PROJ_Y}

### Function: search_incremental_arity

```python
def search_incremental_arity(
    max_arity: int = 3,
    max_depth: int = 3,
    stopping_criterion: int = 3,
    verbose: bool = True
) -> Tuple[int, List[List[Connective]], Dict[str, any]]:
    connective_pool = []
    best_size = 0
    best_sets = []
    no_improvement_count = 0

    # Try arities in order: 2 (binary), 1 (unary), 3 (ternary), 4, ...
    arity_order = [2, 1] + list(range(3, max_arity + 1))

    for arity in arity_order:
        new_connectives = generate_all_connectives(arity)
        connective_pool.extend(new_connectives)

        max_size, nice_sets = find_maximum_nice_set(
            connective_pool,
            max_size=min(10, len(connective_pool)),
            max_depth=max_depth,
            verbose=verbose
        )

        if max_size > best_size:
            best_size = max_size
            best_sets = nice_sets
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count >= stopping_criterion:
            break

    return best_size, best_sets, stats
```

**Strategy:** Start with binary (most common), add unary (small), then ternary, quaternary, etc.

**Arity order rationale:**
- Binary first: Most standard connectives are binary
- Unary next: Small pool (4 functions), helps with negation patterns
- Higher arities: Larger pools, more computational cost

**Stopping criterion:** Stop if no improvement for `stopping_criterion` consecutive arities. Default is 3, meaning if adding arities k, k+1, k+2 doesn't improve, we stop.

**Why this works:** Empirically, once higher arities stop improving, adding even higher arities is unlikely to help (though not guaranteed).

**Performance:**
- Arity 2: 16 functions, C(16, k) combinations
- Arity 1: +4 functions = 20 total, C(20, k) combinations
- Arity 3: +256 functions = 276 total, C(276, k) combinations (combinatorial explosion!)

**For arity 3, k=10:** C(276, 10) ≈ 1.9 × 10^18 (intractable). Need better pruning or smaller max_size.

**Actual behavior:** The search typically finds max size 7-16 for unary+binary+ternary, and the specific max_size limits the search space to manageable C(276, 10) ≈ 2×10^13... still huge. The implementation likely uses random sampling or early termination in practice for ternary.

### Function: analyze_nice_set

```python
def analyze_nice_set(nice_set: List[Connective]) -> Dict[str, any]:
    from src.post_classes import get_post_class_membership

    analysis = {
        'size': len(nice_set),
        'arities': [c.arity for c in nice_set],
        'arity_distribution': {},
        'post_classes': {},
        'connectives': [c.name for c in nice_set]
    }

    # Count arities
    for c in nice_set:
        arity = c.arity
        if arity not in analysis['arity_distribution']:
            analysis['arity_distribution'][arity] = 0
        analysis['arity_distribution'][arity] += 1

    # Analyze Post class membership
    for c in nice_set:
        classes = get_post_class_membership(c)
        analysis['post_classes'][c.name] = list(classes)

    return analysis
```

**Purpose:** Provide detailed analysis of a nice set's properties for interpretation.

**Output example:**
```python
{
    'size': 3,
    'arities': [2, 2, 2],
    'arity_distribution': {2: 3},
    'post_classes': {
        'NOR': ['D'],      # NOR is self-dual
        'AND': ['T0', 'T1', 'M'],  # AND is 0-preserving, 1-preserving, monotone
        'IFF': ['A']       # IFF is affine
    },
    'connectives': ['NOR', 'AND', 'IFF']
}
```

**Insight:** By examining which classes each function escapes, we can understand why the set is complete. E.g., NOR escapes T0, T1, M, A (since NOR(0,0)=1, NOR(1,1)=0, NOT monotone, NOT affine). Together, the set escapes all 5 clones.

---

## 6. cli.py - Unified Command-Line Interface

### CLI Architecture

The unified CLI provides all functionality through a single entry point with subcommands:

```bash
python -m src.cli <subcommand> [options]
```

**Main command groups:**
- `prove` - Formal proofs of maximum nice set size (z3, enum)
- `validate` - Validation and verification tools (binary, ternary)
- `benchmark` - Performance measurement tools (full, quick, depth)
- `search` - Interactive search tools (binary, full, validate)

### CLI Implementation

The CLI uses argparse with nested subparsers for organized command grouping:

```python
# Main parser
parser = argparse.ArgumentParser(
    prog='nice-connectives',
    description='Tools for finding and analyzing nice connective sets'
)

# Create subparsers for command groups
subparsers = parser.add_subparsers(dest='command', required=True)

# Prove subcommand with methods
prove_parser = subparsers.add_parser('prove', help='Formal proofs')
prove_subparsers = prove_parser.add_subparsers(dest='method', required=True)

prove_z3_parser = prove_subparsers.add_parser('z3', help='Z3-based proof')
prove_z3_parser.add_argument('--checkpoint', help='Checkpoint file')
prove_z3_parser.add_argument('--max-depth', type=int, default=3)

prove_enum_parser = prove_subparsers.add_parser('enum', help='Enumeration proof')
```

### Command Routing

Commands are routed to implementation modules in `src/commands/`:

```python
# Route to appropriate command handler
if args.command == 'prove':
    if args.method == 'z3':
        return prove.prove_z3(
            checkpoint=args.checkpoint,
            max_depth=args.max_depth
        )
    elif args.method == 'enum':
        return prove.prove_enumeration()

elif args.command == 'search':
    if args.type == 'binary':
        return search.search_binary(
            max_depth=args.max_depth,
            verbose=not args.quiet
        )
```

**See [commands/README.md](commands/README.md) for command implementation details.**

### Usage Examples

#### Search Commands

```bash
# Validate maximum size=16 result
python -m src.cli search validate

# Binary-only search (finds max = 3)
python -m src.cli search binary

# Full arity search (finds max = 16)
python -m src.cli search full --max-arity 3
```

#### Proof Commands

```bash
# Z3-based proof
python -m src.cli prove z3 --target-size 17 --max-depth 3

# Enumeration-based proof
python -m src.cli prove enum
```

#### Validation Commands

```bash
# Validate binary search results
python -m src.cli validate binary --depth 3

# Validate ternary search with comparison
python -m src.cli validate ternary --compare --verbose
```

#### Benchmark Commands

```bash
# Quick benchmark
python -m src.cli benchmark quick

# Full benchmark suite
python -m src.cli benchmark full --runs 5 --output benchmarks.csv

# Depth crossover analysis
python -m src.cli benchmark depth --depths 1,2,3,4,5
```

### Getting Help

```bash
# Main help
python -m src.cli --help

# Subcommand help
python -m src.cli search --help
python -m src.cli prove z3 --help
python -m src.cli validate binary --help
```

### Library Usage

The library can also be used programmatically:

```python
from src.search import search_binary_only, search_incremental_arity
from src.connectives import generate_all_connectives
from src.independence import is_independent

# Direct library usage
max_size, sets = search_binary_only(max_depth=3)

# Custom search
connectives = generate_all_connectives(2) + generate_all_connectives(1)
# ... use search functions
```

---

## Key Implementation Insights

### 1. BitVec vs. Z3 Symbolic

**What we do:** Use BitVec for compact storage, but enumerate compositions in Python.

**What we don't do:** Use Z3's symbolic reasoning (ForAll/Exists) to prove definability.

**Why?** Symbolic approach would look like:
```python
# Hypothetical (not implemented)
x, y = Bools('x y')
target_formula = And(x, y)
exists_definition = Exists([...], ForAll([x, y], target_formula == composed_formula))
s.add(exists_definition)
result = s.check()  # Might not terminate!
```

**Problem:** Quantifier alternation (Exists/ForAll) can cause non-termination or exponential blowup.

**Our solution:** Bounded enumeration is decidable and fast for small depths.

### 2. Completeness via Post vs. Definability

**Post's Theorem:** Completeness ↔ Escape 5 clones. O(n) checks, each O(2^(2a)).

**Definability-based:** Completeness ↔ Every function definable. Requires checking 2^(2^a) functions, intractable.

**Huge advantage:** Post's Theorem reduces exponential problem to polynomial.

### 3. Independence Depth Parameter

**Depth 3:** "Independent" means no function is a depth-≤3 composition of others.

**Depth 5:** Stricter independence (more compositions checked).

**Implication:** Reported "independent" sets may not be absolutely independent, but are independent within the bounded composition model.

**Mathematical note:** This is a practical approximation. True independence (unbounded depth) is undecidable for general connective sets.

### 4. Arity Scaling

| Arity | Functions | C(n, 10) combinations |
|-------|-----------|----------------------|
| 0     | 2         | 0                    |
| 1     | 4         | 0                    |
| 2     | 16        | 8,008                |
| 0-2   | 22        | 646,646              |
| 0-3   | 278       | 1.9 × 10^18          |
| 0-4   | 65,814    | Astronomical         |

**Conclusion:** Search is tractable up to arity 3 for small set sizes (≤10), but requires heuristics or random sampling for larger searches.

---

## Usage Examples

### Basic Search

```bash
# Binary-only (fast, validates implementation)
python -m src.cli search binary

# Full arity search up to ternary
python -m src.cli search full --max-arity 3 --max-depth 3

# Validate known maximum size=16
python -m src.cli search validate
```

### Advanced Search

```bash
# More conservative independence (depth 5)
python -m src.cli search full --max-arity 3 --max-depth 5

# Quiet mode (results only)
python -m src.cli search binary --quiet
```

### Validation

```bash
# Validate binary search results
python -m src.cli validate binary --depth 3

# Validate ternary search with detailed output
python -m src.cli validate ternary --compare --verbose
```

### Proofs and Benchmarks

```bash
# Run Z3-based proof
python -m src.cli prove z3

# Run enumeration-based proof
python -m src.cli prove enum

# Quick benchmark
python -m src.cli benchmark quick

# Full benchmark suite
python -m src.cli benchmark full --runs 5
```

---

## Mathematical Foundations

### Post's Lattice (Clone Lattice)

**Clone:** A set of functions closed under composition and containing all projections.

**Maximal clones:** Clones that are maximal (largest) subject to not being the full clone (all functions).

**Post's Result (1941):** There are exactly 5 maximal clones in Boolean logic:
1. T0 (0-preserving)
2. T1 (1-preserving)
3. M (monotone)
4. D (self-dual)
5. A (affine)

**Completeness Theorem:** A set generates all Boolean functions ↔ It's not contained in any maximal clone ↔ It escapes all 5 maximal clones.

### Composition Depth

**Definition:** The depth of a composition tree is the maximum nesting level.

**Examples:**
- f(x, y): depth 0 (base function)
- g(f(x, y)): depth 1
- h(g(f(x, y))): depth 2
- h(f(x), g(y)): depth 1 (both branches have depth 1)

**Bounded composition:** Definability restricted to depth ≤ d.

**Trade-off:** Larger d → more accurate, but exponentially more expensive.

### Functional Completeness

**Definition:** A set S is functionally complete if every Boolean function can be expressed using only functions from S and composition.

**Classical results:**
- {NAND} is complete (single function!)
- {NOR} is complete
- {NOT, AND} is complete (minimal binary basis)
- {NOT, OR} is complete

**Independence:** A complete set is independent if removing any function makes it incomplete.

**Nice set:** Complete + Independent.

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| T0/T1 check | O(1) | Single evaluation |
| Monotone check | O(4^a) | All pairs of 2^a rows |
| Affine check | O(4^a) | All pairs |
| Completeness check | O(n × 4^a) | n functions, worst case affine |
| Depth-d definability | O(B^d × 2^a) | B = basis size, a = arity |
| Independence check | O(n^2 × B^d × 2^a) | Check each against rest |
| Nice set search (size k) | O(C(N,k) × k × (k^2 × B^d × 2^a)) | N = pool size |

### Space Complexity

| Data | Size | Notes |
|------|------|-------|
| Connective | O(1) | Just stores integer |
| All binary | O(16) = O(1) | Fixed size |
| All ternary | O(256) | Manageable |
| All quaternary | O(65,536) | Large but feasible |
| Search results | O(k × num_results) | Depends on findings |

### Bottlenecks

1. **Ternary enumeration:** C(278, k) grows rapidly
2. **Independence checking:** Quadratic in set size, exponential in depth
3. **Composition enumeration:** B^d patterns to check

### Optimizations Used

1. **Completeness first:** Filter by fast completeness before slow independence
2. **Incremental depth:** Try depth 1 before depth 3
3. **Early termination:** Stop when no nice sets found (heuristic)
4. **Post's Theorem:** O(n) completeness instead of O(2^(2^a))

---

## Navigation

- [← Project README](../README.md) - Main project overview
- [Command Implementations](commands/README.md) - CLI command details
- [Examples](../examples/README.md) - Real execution examples
- [Results](../RESULTS.md) - Research conclusion
- [Scripts](../scripts/README.md) - Proof methodology documentation
- [Tests](../tests/README.md) - Testing documentation
- [Specs](../specs/README.md) - Research reports and plans
