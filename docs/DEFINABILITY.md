# Definability Modes in Nice Connectives

This document explains the two definability modes available in the nice_connectives project: **truth-functional** (default) and **syntactic**. Understanding these modes is crucial for choosing the appropriate definability notion for your research.

## Contents

- [Mathematical Foundations](#mathematical-foundations)
- [Truth-Functional Mode (Default)](#truth-functional-mode-default)
- [Syntactic Mode](#syntactic-mode)
- [Mode Comparison](#mode-comparison)
- [CLI Usage](#using-definability-modes-in-commands)
- [Implementation Details](#implementation-details)
- [Related Documentation](#related-documentation)
- [FAQ](#frequently-asked-questions)

## Mathematical Foundations

### What is Definability?

In the context of logical connectives, **definability** answers the question: "Can function f be expressed using only functions from basis B?"

Formally, a connective f is **definable** from basis B if there exists a composition tree using only functions from B (and variable bindings) that evaluates to f on all inputs.

**Key Concepts:**
- **Composition**: Applying functions to results of other functions
  - Example: `NOT(AND(x,y))` composes NOT with AND
- **Depth**: Maximum nesting level in a composition tree
  - Depth 1: `AND(x,y)` - direct function application
  - Depth 2: `NOT(AND(x,y))` - one level of nesting
  - Depth 3: `OR(NOT(x), NOT(y))` - deeper nesting
- **Basis**: The set of functions available for composition

**Connection to Nice Sets:**

Nice sets require both **completeness** and **independence**:
- **Completeness**: The set can express all possible connectives (via composition)
- **Independence**: No function in the set is definable from the others

Definability directly affects independence checking. A set is independent only if each function requires all others - none can be expressed using just the remaining functions.

**Example - NAND from {NOT, AND}:**
```
NAND(x,y) = NOT(AND(x,y))

Truth table verification:
  x | y | AND | NOT(AND) | NAND
  0 | 0 |  0  |    1     |  1   ✓
  0 | 1 |  0  |    1     |  1   ✓
  1 | 0 |  0  |    1     |  1   ✓
  1 | 1 |  1  |    0     |  0   ✓

Conclusion: NAND is definable from {NOT, AND}
```

### Two Notions of Definability

This project implements two distinct notions of definability:

1. **Truth-Functional (Clone-Theoretic)** (Default): Includes universal rules for projections and cross-arity constants. Based on truth-functional equivalence.

2. **Syntactic (Composition-Based)**: Requires explicit construction via composition trees with bounded depth. Arity-sensitive and conservative.

**Why Two Notions?**

Different research traditions have different conventions:
- **Universal Algebra**: Typically use truth-functional (clone-theoretic) definability (default in this project)
- **Logic and Computation**: Typically use syntactic (composition-based) definability

Neither is inherently "more correct" - the choice depends on your research question and which properties matter for your analysis.

## Truth-Functional Mode (Default)

### Mathematical Definition

A connective f is **syntactically definable** from basis B at depth d if:

```
∃ composition tree T where:
  - All leaf nodes are from B ∪ {variable bindings}
  - Tree depth ≤ d (default: 3)
  - T evaluates to f on all inputs
  - Arity constraints: compositions respect function arities
```

### Key Characteristics

1. **Depth-Bounded**: Only checks compositions up to `max_depth` (default: 3)
   - Tradeoff: deeper = more thorough but exponentially slower
   - Depth 3 is sufficient for most classical results

2. **Arity-Sensitive**: Functions of different arities are treated as distinct
   - `TRUE₀` (nullary constant) ≠ `TRUE₂` (binary constant)
   - Cannot compose arity-0 functions to create arity-2 functions

3. **No Implicit Projections**: Projection functions must be composed from basis
   - `PROJ_X(x,y) = x` is not "free"
   - Can be expressed as `AND(x, OR(x,y))` if {AND, OR} are available

4. **Composition-Only**: No special universal assumptions
   - Every definability claim requires an explicit composition witness

### Examples

#### Example 1: NAND from {NOT, AND}

```
Target: NAND(x,y)
Basis: {NOT, AND}
Depth: 2

Composition tree:
  NOT
   |
  AND
  / \
 x   y

Evaluation: NOT(AND(x,y))
  - Depth 1: Compute AND(x,y)
  - Depth 2: Apply NOT to result
  - Truth table matches NAND ✓

Conclusion: NAND is syntactically definable from {NOT, AND} at depth 2
```

#### Example 2: Projection from {AND, OR}

```
Target: PROJ_X(x,y) = x
Basis: {AND, OR}
Depth: 2

Composition tree (using absorption law):
  AND
  / \
 x  OR
    / \
   x   y

Evaluation: AND(x, OR(x,y))
  Truth table:
    x | y | OR(x,y) | AND(x, OR) | PROJ_X
    0 | 0 |    0    |     0      |   0   ✓
    0 | 1 |    1    |     0      |   0   ✓
    1 | 0 |    1    |     1      |   1   ✓
    1 | 1 |    1    |     1      |   1   ✓

Conclusion: PROJ_X is syntactically definable from {AND, OR} at depth 2
```

#### Example 3: Cross-Arity Constants are Independent

```
Target: TRUE₂(x,y) = 1  (binary constant)
Basis: {TRUE₀}          (nullary constant, value = 1)
Depth: 3

Attempt 1: Direct application?
  - TRUE₀ has arity 0, cannot apply to arguments (x,y)
  - Not a valid composition ✗

Attempt 2: Nest TRUE₀?
  - TRUE₀() returns 1 (no arguments)
  - Cannot bind result to (x,y) parameters
  - Still not valid ✗

Attempt 3: Multiple TRUE₀ compositions?
  - TRUE₀(TRUE₀(TRUE₀())) = 1 (but still arity 0)
  - Cannot change arity through composition
  - Not valid ✗

Conclusion: TRUE₂ is NOT syntactically definable from {TRUE₀}
Reason: Different arities, no arity-changing operations allowed
```

### When to Use Syntactic Mode

**Recommended Use Cases:**

- **Default choice for most research** (conservative, widely accepted)
- Studying composition-based definability and construction proofs
- Reproducing classical logic results (e.g., binary-only maximum = 3)
- Research on bounded composition depth and computational complexity
- Conservative estimates of independence (fewer assumptions = stricter)

**Typical Results:**

- Binary connectives only: maximum nice set size = 3
- Unary + Binary: maximum ≈ 5
- With ternary connectives: maximum ≥ 35
- Generally produces **larger nice sets** (stricter independence criterion)

**Research Alignment:**

Most classical logic literature uses syntactic (composition-based) definability, so results will be directly comparable to existing work.

## Truth-Functional Mode

### Mathematical Definition

A connective f is **truth-functionally definable** from basis B if:

```
(f is a projection function) OR
(f and some g ∈ B are constants with same truth value) OR
(f is syntactically definable from B via composition)
```

This mode adds two **special rules** to the standard composition-based checking:

1. **Universal Projection Rule**: All projections are universally definable
2. **Cross-Arity Constant Equivalence**: Constants with same truth value are equivalent

### Key Characteristics

1. **Universal Projections**: All `PROJ_i` functions are automatically definable
   - Rationale: Projections are "identity operations" that don't transform values
   - In clone theory, projections are considered universally available

2. **Cross-Arity Constant Equivalence**: Constants with same output are equivalent
   - `TRUE₀ ≡ TRUE₁ ≡ TRUE₂ ≡ TRUE₃` (all always return 1)
   - `FALSE₀ ≡ FALSE₁ ≡ FALSE₂ ≡ FALSE₃` (all always return 0)
   - Rationale: Same semantic meaning despite different syntactic arities

3. **Clone-Theoretic**: Based on truth-functional equivalence classes
   - Aligns with universal algebra tradition
   - Focus on semantic properties rather than syntactic construction

4. **Permissive**: Detects more dependencies than syntactic mode
   - More things are definable → harder to maintain independence
   - Typically produces smaller maximum nice set sizes

### Special Rules

#### Rule 1: Universal Projection Definability

```
For any basis B and any projection PROJ_i:
  is_definable(PROJ_i, B, mode=truth-functional) = True
```

**Rationale**: In clone theory, projections represent identity operations that are semantically "free" - they select inputs without transformation. Since they're the fundamental building blocks of any function composition, they're treated as universally available.

**Example:**
```
Target: PROJ_X(x,y) = x
Basis: {AND}  (any basis works)
Mode: truth-functional

Check:
  1. Is PROJ_X a projection? YES
  2. Return True immediately (universal projection rule)

Conclusion: PROJ_X is truth-functionally definable from ANY basis
```

#### Rule 2: Cross-Arity Constant Equivalence

```
If f and g are constants with the same truth value:
  is_definable(f, [g], mode=truth-functional) = True

Truth value equivalence classes:
  - All-True class: {TRUE₀, TRUE₁, TRUE₂, TRUE₃, ...}
  - All-False class: {FALSE₀, FALSE₁, FALSE₂, FALSE₃, ...}
```

**Rationale**: Constants represent semantic values (always-true or always-false) independent of their syntactic arity. From a truth-functional perspective, `TRUE₂(x,y)` and `TRUE₀` both represent the same proposition: "always true".

**Example:**
```
Target: TRUE₂(x,y) = 1
Basis: {TRUE₀}  (nullary constant, value = 1)
Mode: truth-functional

Check:
  1. Is TRUE₂ a projection? NO
  2. Is TRUE₂ a constant? YES (outputs 1 for all inputs)
  3. Is TRUE₀ a constant? YES (outputs 1)
  4. Same truth value? YES (both always return 1)
  5. Return True (cross-arity constant equivalence rule)

Conclusion: TRUE₂ is truth-functionally definable from {TRUE₀}
```

### Examples

#### Example 1: Universal Projection

```
Target: PROJ_Y(x,y) = y
Basis: {XOR}
Mode: truth-functional

Check:
  1. Is PROJ_Y a projection? YES
  2. Apply universal projection rule → return True immediately
  3. (No composition checking needed)

Conclusion: PROJ_Y is truth-functionally definable from {XOR}

Note: In syntactic mode, this would require finding a composition like:
  XOR(y, XOR(x,y)) = y  (requires depth 2 and both variables)
```

#### Example 2: Cross-Arity Constants

```
Target: FALSE₃(x,y,z) = 0  (ternary constant)
Basis: {FALSE₀}             (nullary constant)
Mode: truth-functional

Check:
  1. Is FALSE₃ a projection? NO
  2. Is FALSE₃ a constant? YES (all outputs = 0)
  3. Any basis element also constant with same value?
     - FALSE₀ is constant (output = 0)
     - Same truth value (both always 0)
  4. Return True (cross-arity constant rule)

Conclusion: FALSE₃ is truth-functionally definable from {FALSE₀}

Note: In syntactic mode, FALSE₃ would NOT be definable from {FALSE₀}
      (different arities, cannot compose)
```

#### Example 3: Non-Special Cases Still Require Composition

```
Target: NAND(x,y)
Basis: {NOT, AND}
Mode: truth-functional

Check:
  1. Is NAND a projection? NO
  2. Is NAND a constant? NO (outputs vary with inputs)
  3. Fall back to standard composition checking
  4. Find composition: NOT(AND(x,y)) at depth 2 ✓

Conclusion: NAND is truth-functionally definable from {NOT, AND}

Note: Same result as syntactic mode for non-special cases
```

### When to Use Truth-Functional Mode

**Recommended Use Cases:**

- Studying clone theory or universal algebra
- Research on truth-functional equivalence and semantic properties
- When projections should be treated as "free" (universally available)
- Cross-arity constant studies and equivalence class analysis
- Permissive definability (detecting maximum dependencies)

**Typical Results:**

- **Smaller maximum nice set sizes** (more dependencies detected)
- Cross-arity constants collapse into equivalence classes
- Sets containing projections often become dependent
- Aligns with universal algebra tradition

**Research Alignment:**

Universal algebra and clone theory literature typically use truth-functional (or equivalent) definability notions. Results will be comparable to this research tradition.

## Mode Comparison

### Side-by-Side Comparison

| Aspect | Syntactic | Truth-Functional |
|--------|-----------|------------------|
| **Projection definability** | Requires explicit composition (e.g., x∧(x∨y)=x) | Universal (always definable from any basis) |
| **Cross-arity constants** | Independent (TRUE₀ ≠ TRUE₂) | Equivalent (TRUE₀ ≡ TRUE₂) |
| **Definability strictness** | Strict (fewer assumptions) | Permissive (more universal rules) |
| **Nice set sizes** | Larger (fewer dependencies detected) | Smaller (more dependencies detected) |
| **Research tradition** | Logic, composition theory, computability | Universal algebra, clone theory |
| **Use case** | Composition-based research | Clone-theoretic research |
| **Default mode** | ✓ Yes | No |
| **Implementation** | Pattern enumeration up to depth | Special rules + pattern enumeration |
| **Performance** | Baseline | Slightly faster (special rules shortcut) |

### Example: Same Set, Different Modes

Consider the set: `{AND, OR, PROJ_X, TRUE₀, TRUE₂}`

#### Syntactic Mode Analysis

```
Check independence (each function against the others):

1. Is AND definable from {OR, PROJ_X, TRUE₀, TRUE₂}?
   - Pattern enumeration up to depth 3
   - No composition found → NOT definable ✓

2. Is OR definable from {AND, PROJ_X, TRUE₀, TRUE₂}?
   - Pattern enumeration up to depth 3
   - No composition found → NOT definable ✓

3. Is PROJ_X definable from {AND, OR, TRUE₀, TRUE₂}?
   - Check composition: AND(x, OR(x,y))
   - Truth table matches PROJ_X → definable ✗

Result: NOT INDEPENDENT in syntactic mode
Reason: PROJ_X = AND(x, OR(x,y)) - composition dependency at depth 2
```

#### Truth-Functional Mode Analysis

```
Check independence:

1. Is AND definable from {OR, PROJ_X, TRUE₀, TRUE₂}?
   - Is AND a projection? NO
   - Is AND a constant? NO
   - Check compositions from {OR, PROJ_X, TRUE₀, TRUE₂}
   - PROJ_X cannot create AND (no transformation)
   - TRUE₀, TRUE₂ are constants (cannot create varying function)
   - OR alone insufficient
   - NOT definable ✓

2. Is PROJ_X definable from {AND, OR, TRUE₀, TRUE₂}?
   - Is PROJ_X a projection? YES
   - Apply universal projection rule → definable ✗

3. Is TRUE₂ definable from {AND, OR, PROJ_X, TRUE₀}?
   - Is TRUE₂ a constant? YES (always 1)
   - Is TRUE₀ a constant with same value? YES (always 1)
   - Apply cross-arity constant rule → definable ✗

Result: NOT INDEPENDENT in truth-functional mode
Reason: Multiple dependencies via special rules
  - PROJ_X definable (universal projection)
  - TRUE₂ definable from TRUE₀ (cross-arity constants)
```

**Key Insight**: Both modes detect that this set is NOT independent, but for different reasons:
- **Syntactic**: Finds explicit composition dependency (PROJ_X = AND(x, OR(x,y)))
- **Truth-functional**: Finds multiple dependencies via universal rules

### Binary-Only Comparison

**Setup**: Searching for maximum nice sets using only binary (arity-2) connectives.

#### Syntactic Mode

```bash
python -m src.cli search binary --definability-mode syntactic
```

**Expected Results:**
- Maximum nice set size: **3**
- Example nice set: `{XOR, AND, TRUE}` or `{NAND, NOR, PROJ_X}`
- Approximately 76 nice sets of size 3
- Matches classical results from logic literature

**Independence Example:**
```
Set: {XOR, AND, TRUE}

Checks:
  - XOR from {AND, TRUE}? NO (depth 3 insufficient)
  - AND from {XOR, TRUE}? NO
  - TRUE from {XOR, AND}? NO (constants not composable)

Result: Independent ✓
```

#### Truth-Functional Mode

```bash
python -m src.cli search binary --definability-mode truth-functional
```

**Expected Results:**
- Maximum nice set size: **Potentially different** from syntactic
- Projection-containing sets become dependent (universal projection rule)
- Fewer total nice sets due to stricter dependencies

**Dependency Example:**
```
Set: {XOR, AND, PROJ_X}

Checks:
  - XOR from {AND, PROJ_X}? NO
  - AND from {XOR, PROJ_X}? NO
  - PROJ_X from {XOR, AND}? YES (universal projection rule) ✗

Result: NOT Independent
```

### Practical Impact Summary

**Syntactic Mode:**
- Stricter independence (fewer things definable)
- Larger maximum nice sets
- More nice sets overall
- Conservative estimates

**Truth-Functional Mode:**
- Permissive independence (more things definable)
- Smaller maximum nice sets
- Fewer nice sets overall
- Detects semantic equivalences

**Neither is Wrong**: They measure different properties. Choose based on your research question:
- Want composition-based results? → Syntactic
- Want clone-theoretic results? → Truth-functional

## Using Definability Modes in Commands

### Specifying Mode via Flag

All CLI commands support the `--definability-mode` flag:

```bash
# Default: syntactic mode (no flag needed)
python -m src.cli search binary

# Explicit syntactic mode (same as default)
python -m src.cli search binary --definability-mode syntactic

# Truth-functional mode
python -m src.cli search binary --definability-mode truth-functional
```

### Mode Works with All Commands

#### Search Commands

```bash
# Enumeration search with truth-functional mode
python -m src.cli search binary --definability-mode truth-functional

# Full arity search with syntactic mode (default)
python -m src.cli search full --max-arity 3 --definability-mode syntactic

# Compare modes by running both
python -m src.cli search binary --definability-mode syntactic > results_syntactic.txt
python -m src.cli search binary --definability-mode truth-functional > results_tf.txt
```

#### Proof Commands

```bash
# Z3 proof with truth-functional mode
python -m src.cli prove z3 --target-size 17 --definability-mode truth-functional

# Enumeration proof with syntactic mode (default)
python -m src.cli prove enum --binary-only --definability-mode syntactic
```

#### Validation Commands

```bash
# Validate results with both modes to compare
python -m src.cli validate binary --definability-mode syntactic
python -m src.cli validate binary --definability-mode truth-functional

# Validate ternary results
python -m src.cli validate ternary --definability-mode truth-functional
```

#### Benchmark Commands

```bash
# Benchmark with different modes
python -m src.cli benchmark quick --definability-mode syntactic
python -m src.cli benchmark quick --definability-mode truth-functional

# Compare performance between modes
python -m src.cli benchmark full --definability-mode syntactic
python -m src.cli benchmark full --definability-mode truth-functional
```

### Interpreting Results Across Modes

**Key Points:**

- Same command + different mode → potentially different results
- Syntactic typically finds **larger** nice sets (fewer dependencies)
- Truth-functional typically finds **smaller** nice sets (more dependencies)
- Neither result is "wrong" - they measure different properties

**Example Output Comparison:**

```bash
# Syntactic mode
python -m src.cli search binary --definability-mode syntactic
# Output: Maximum nice set size: 3
#         Found 76 nice sets of size 3
#         Example: {XOR, AND, TRUE}

# Truth-functional mode
python -m src.cli search binary --definability-mode truth-functional
# Output: Maximum nice set size: [potentially different]
#         [Different number] nice sets found
#         Projection-containing sets are dependent
```

**Interpretation:**

If truth-functional mode gives a smaller maximum:
- **Reason**: Cross-arity constants collapse to equivalence classes, or projections are universally definable
- **Implication**: More semantic dependencies detected
- **Research Note**: Document which mode was used for all results

## Implementation Details

### Source Code

The definability modes are implemented in the codebase at the following locations:

#### Primary Implementation: `src/independence.py`

**DefinabilityMode Enum** (lines 16-19):
```python
class DefinabilityMode(Enum):
    SYNTACTIC = "syntactic"
    TRUTH_FUNCTIONAL = "truth-functional"
```

**Main Entry Point: `is_definable()`** (lines 22-65):
```python
def is_definable(
    target: Connective,
    basis: List[Connective],
    max_depth: int = 3,
    mode: DefinabilityMode = DefinabilityMode.SYNTACTIC,
    memo: Optional[Dict] = None
) -> bool:
    """
    Check if target is definable from basis under the specified mode.

    Modes:
    - SYNTACTIC: Composition-based, depth-bounded, arity-sensitive
    - TRUTH_FUNCTIONAL: Universal projections + cross-arity constants + composition
    """
```

**Helper Functions**:
- `_is_projection()` (line 181): Identifies projection functions
- `_get_truth_function_signature()` (line 208): Extracts constant truth values
- `_check_composition_enumeration()` (lines 68-173): Pattern enumeration logic

**Mode-Specific Logic Branches**:
- **Universal projection check** (line 51): Truth-functional mode only
- **Cross-arity constant check** (lines 54-59): Truth-functional mode only
- **Pattern enumeration** (line 65): Both modes (fallback for truth-functional)

#### CLI Integration: `src/cli.py`

The `--definability-mode` flag is added to all relevant commands:

```python
parser.add_argument(
    '--definability-mode',
    choices=['syntactic', 'truth-functional'],
    default='syntactic',
    help='Definability mode for independence checking'
)

# String-to-enum conversion
mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
```

**Commands with Mode Support:**
- `prove z3` - Z3-based proofs
- `prove enum` - Enumeration proofs
- `validate binary` - Binary connective validation
- `validate ternary` - Ternary connective validation
- `search binary` - Binary-only search
- `search full` - Full arity search
- `benchmark` - Performance benchmarking

### Test Coverage

**Test File**: `tests/test_definability_modes.py` (236 lines, 28 tests)

#### Test Classes

1. **`TestUniversalProjections`** (lines 12-42)
   - Tests universal projection rule in truth-functional mode
   - Verifies projections definable from any basis
   - Confirms syntactic mode does NOT have universal projections

2. **`TestCrossArityConstants`** (lines 44-84)
   - Tests cross-arity constant equivalence
   - Verifies TRUE_n ≡ TRUE_m and FALSE_n ≡ FALSE_m
   - Confirms syntactic mode treats different arities as independent

3. **`TestPermutationConsistency`** (lines 86-106)
   - Tests consistent behavior across permutation-equivalent functions
   - Verifies mode choice doesn't break permutation handling

4. **`TestBackwardCompatibility`** (lines 108-136)
   - Ensures syntactic mode matches original (pre-mode) behavior
   - Regression tests for existing results

5. **`TestNiceSetSizeDifference`** (lines 138-188)
   - Tests mode impact on nice set maximum sizes
   - Verifies truth-functional finds different (typically smaller) results

6. **`TestModeEnumValues`** (lines 190-211)
   - Tests enum correctness and string representations
   - Verifies mode parameter handling

7. **`TestEdgeCasesWithModes`** (lines 213-236)
   - Tests edge cases (nullary functions, deep compositions)
   - Verifies robustness across modes

#### Key Test Examples

```python
# Universal projection (truth-functional mode)
def test_projection_x_definable_from_any_in_truth_functional(self):
    assert is_definable(
        PROJECT_X,
        [AND],
        mode=DefinabilityMode.TRUTH_FUNCTIONAL
    )

# Cross-arity constants (truth-functional mode)
def test_true_constants_equivalent_across_arities(self):
    TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')
    assert is_definable(
        CONST_TRUE_BIN,  # TRUE_2
        [TRUE_3],
        mode=DefinabilityMode.TRUTH_FUNCTIONAL
    )

# Syntactic mode does NOT have universal projections
def test_projection_not_universally_definable_in_syntactic(self):
    assert not is_definable(
        PROJECT_X,
        [AND],
        mode=DefinabilityMode.SYNTACTIC
    )
```

#### Running Tests

```bash
# Run all definability mode tests
pytest tests/test_definability_modes.py -v

# Run specific test class
pytest tests/test_definability_modes.py::TestUniversalProjections -v

# Check test coverage
pytest tests/test_definability_modes.py --cov=src.independence --cov-report=term-missing

# Run tests with detailed output
pytest tests/test_definability_modes.py -vv --tb=short
```

## Related Documentation

### Core Concepts

- **[README.md](../README.md#problem-statement)** - Definition of "nice" sets (completeness + independence)
- **[README.md](../README.md#technical-approach)** - Pattern enumeration for independence checking
- **[USAGE.md](USAGE.md#definability-modes)** - CLI usage and practical examples (lines 556-659)

### Implementation

- **[src/independence.py](../src/independence.py)** - Full implementation (lines 1-1086)
  - `DefinabilityMode` enum (lines 16-19)
  - `is_definable()` function (lines 22-65)
  - Helper functions (lines 181-241)
- **[tests/test_definability_modes.py](../tests/test_definability_modes.py)** - Comprehensive test suite (236 lines, 28 tests)
- **[src/cli.py](../src/cli.py)** - CLI integration with `--definability-mode` flag

### Research Context

- **[RESULTS.md](RESULTS.md)** - Research findings (all use syntactic mode by default unless specified)
- **[specs/reports/016_definability_notion_analysis.md](../specs/reports/016_definability_notion_analysis.md)** - Detailed definability analysis that inspired this implementation
- **[specs/plans/012_definability_mode_cli_flag.md](../specs/plans/012_definability_mode_cli_flag.md)** - Implementation plan for definability modes

### Related Concepts

**Completeness:**
- Completeness checking is **NOT** affected by definability mode
- Uses Post's Completeness Theorem (escaping all 5 Post classes: T0, T1, M, D, A)
- Both modes use identical completeness checking
- See [README.md Technical Approach](../README.md#technical-approach) (lines 184-186)

**Independence:**
- Independence = no function in set is definable from others
- **Definability mode directly affects independence checking**
- Syntactic: stricter (fewer things definable → easier to maintain independence)
- Truth-functional: permissive (more things definable → harder to maintain independence)

**Depth Parameter:**
- Both modes use depth-bounded composition checking
- Special rules (projections, constants) in truth-functional mode apply BEFORE depth checking
- Higher depth → more thorough but exponentially slower
- Default depth = 3 (sufficient for most classical results)
- See [USAGE.md Advanced Usage](USAGE.md#advanced-usage) (lines 796-803)

## Frequently Asked Questions

### Q1: Which mode should I use for my research?

**Use syntactic mode (default) if:**
- Studying composition-based definability
- Want conservative independence estimates
- Reproducing classical logic results
- Unsure which to choose (default is safer)
- Research aligns with logic/computation tradition

**Use truth-functional mode if:**
- Studying clone theory or universal algebra
- Want projections treated as "free" (universally available)
- Researching cross-arity constant relationships
- Need permissive definability (detecting maximum dependencies)
- Research aligns with universal algebra tradition

**General Advice**: Start with syntactic mode (default) unless you have a specific reason to use truth-functional. Most classical results use syntactic semantics.

### Q2: Do the modes affect completeness checking?

**NO.** Definability modes **only** affect independence checking.

Completeness uses Post's Completeness Theorem, which checks if a set escapes all 5 maximal clones (T0, T1, M, D, A). This checking is identical across both modes.

**Example:**
```python
# Completeness check - same result regardless of mode
is_complete({AND, OR, NOT})  # True (escapes all Post classes)

# Independence check - may differ by mode
is_independent({AND, OR, PROJ_X}, mode=SYNTACTIC)         # ?
is_independent({AND, OR, PROJ_X}, mode=TRUTH_FUNCTIONAL)  # False (proj universal)
```

### Q3: Why does truth-functional mode give smaller nice sets?

Truth-functional mode detects **MORE dependencies**:

1. **Universal projection rule**: All projection functions are automatically definable from any basis
   - Any set containing a projection becomes dependent in truth-functional mode

2. **Cross-arity constant equivalence**: Constants with same truth value are equivalent
   - TRUE₀ ≡ TRUE₂ ≡ TRUE₃ (all collapse to "always true")
   - FALSE₀ ≡ FALSE₂ ≡ FALSE₃ (all collapse to "always false")
   - Sets with multiple cross-arity constants become dependent

**More dependencies** → harder to maintain independence → smaller maximum nice set sizes

**Example:**
```
Set: {TRUE₀, TRUE₂, AND, OR}

Syntactic mode:
  - TRUE₀ and TRUE₂ have different arities → independent ✓
  - Result: Potentially independent (if no composition dependencies)

Truth-functional mode:
  - TRUE₂ definable from TRUE₀ (cross-arity constant rule) ✗
  - Result: NOT independent
```

### Q4: Are the classical binary-only results (max=3) mode-dependent?

**Partially.** The classical result (maximum nice set size = 3 for binary-only) uses composition-based definability, which corresponds to **syntactic mode**.

Truth-functional mode might give **different results** due to:
- Universal projection rule (projection-containing sets become dependent)
- More permissive definability overall

**Recommendation**: When citing classical results, use syntactic mode for direct comparability. If using truth-functional mode, clearly document this and explain why results may differ.

### Q5: Can I switch modes mid-research?

Yes, but results **aren't directly comparable**:

- Syntactic nice set ≠ Truth-functional nice set (different definitions of independence)
- Maximum sizes may differ between modes
- Specific nice sets may differ

**Best Practices:**
1. **Choose one mode** for the primary research
2. **Document mode choice** clearly in writeups
3. If comparing modes, **run experiments with both** and explicitly note differences
4. **Don't mix results** from different modes in the same analysis

**Example Research Note:**
```
"All results reported use syntactic mode (default). Truth-functional mode
was also tested and gave a maximum nice set size of [N], demonstrating
[comparison insight]."
```

### Q6: What's the performance difference between modes?

Truth-functional mode is typically **slightly faster** (< 5% improvement):

**Reasons:**
- Special rules (projections, constants) return immediately without composition checking
- Avoids expensive pattern enumeration for special cases
- Early termination when special rules apply

**But**: The difference is usually negligible for most practical purposes. **Choose mode based on research question, not performance.**

**Benchmark Example:**
```bash
# Time both modes
time python -m src.cli search binary --definability-mode syntactic
# ~10.5 seconds

time python -m src.cli search binary --definability-mode truth-functional
# ~10.1 seconds (slightly faster due to special rules)
```

### Q7: Are there cases where modes give the same result?

**Yes!** For sets **without**:
- Projection functions (PROJ_X, PROJ_Y, etc.)
- Cross-arity constants (e.g., both TRUE₀ and TRUE₂ in same set)

Modes will often give **identical results**.

**Example: {AND, OR, XOR}**
```
No projections: ✓
No cross-arity constants: ✓

Syntactic mode:
  - Check compositions up to depth 3
  - No function definable from others → Independent ✓

Truth-functional mode:
  - No special rules apply (not projections, not constants)
  - Fall back to standard composition checking
  - Same result as syntactic → Independent ✓

Conclusion: Modes agree for this set
```

**Example: {NAND, NOR, XOR}**
```
Syntactic: Independent (classical result)
Truth-functional: Independent (same result - no special cases)
```

### Q8: How do I cite which mode I used in a paper?

**Recommended Citation Format:**

**Method Section:**
```
"Independence was checked using [syntactic/truth-functional] definability
with depth bound 3. Syntactic definability requires explicit composition
trees bounded by depth, while truth-functional definability additionally
treats all projections as universally definable and cross-arity constants
as equivalent."
```

**Results Section:**
```
"Using syntactic definability (default), the maximum nice set size for
binary connectives is 3, matching classical results. Truth-functional
definability gives [result], reflecting its more permissive notion of
definability."
```

**Tool Reference:**
```
"Computations performed using nice_connectives toolkit with
--definability-mode [syntactic/truth-functional] flag."
```

## Summary

### Key Takeaways

1. **Two definability modes available:**
   - **Syntactic (default)**: Composition-based, depth-bounded, arity-sensitive
   - **Truth-functional**: Universal projections + cross-arity constant equivalence + composition

2. **Mode choice affects independence checking:**
   - Syntactic: stricter (fewer definability assumptions → larger nice sets)
   - Truth-functional: permissive (more universal rules → smaller nice sets)
   - Completeness checking is **NOT** affected (same for both modes)

3. **Different use cases:**
   - Syntactic: Classical logic, composition research, conservative estimates
   - Truth-functional: Clone theory, universal algebra, semantic equivalence

4. **Both modes are valid:**
   - Neither is inherently "more correct"
   - Choose based on research question and which properties matter
   - Document mode choice clearly in research outputs

5. **Easy to use:**
   - Single flag: `--definability-mode [syntactic|truth-functional]`
   - Works with all CLI commands (search, prove, validate, benchmark)
   - Default (syntactic) matches classical results

### Next Steps

**Try Both Modes:**
```bash
# Compare syntactic and truth-functional modes
python -m src.cli search binary --definability-mode syntactic
python -m src.cli search binary --definability-mode truth-functional
```

**Understand the Differences:**
- Run the same searches with both modes
- Compare maximum nice set sizes
- Examine which sets are considered independent in each mode
- Understand why differences occur (projections, constants)

**Read the Implementation:**
- **Source**: [`src/independence.py`](../src/independence.py) (lines 16-65)
- **Tests**: [`tests/test_definability_modes.py`](../tests/test_definability_modes.py)
- Understand the special rules in truth-functional mode
- See how pattern enumeration works in both modes

**Explore Related Topics:**
- **[USAGE.md](USAGE.md)** - Practical CLI usage and workflows
- **[README.md](../README.md)** - Project overview and mathematical background
- **[RESULTS.md](RESULTS.md)** - Research findings with definability modes

### Further Reading

- **[USAGE.md § Definability Modes](USAGE.md#definability-modes)** - Practical CLI usage and examples (lines 556-659)
- **[README.md § Technical Approach](../README.md#technical-approach)** - Pattern enumeration and Post's theorem
- **[RESULTS.md](RESULTS.md)** - Research findings (syntactic mode used by default)
- **[src/independence.py](../src/independence.py)** - Complete implementation with inline documentation

---

**Questions or Issues?**

If you encounter unexpected behavior or have questions about definability modes, please:
1. Check the [FAQ](#frequently-asked-questions) above
2. Review the [test suite](../tests/test_definability_modes.py) for examples
3. Examine the [implementation](../src/independence.py) for technical details
4. Refer to the [original analysis report](../specs/reports/016_definability_notion_analysis.md) for theoretical background
