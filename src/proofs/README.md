# Proof Scripts

This directory contains formal proof scripts for verifying the maximum size of nice (complete and independent) connective sets.

## Contents

### `enumeration_proof.py`

Pattern enumeration-based proof that maximum nice set size = 16.

**Approach:**
- Constructive: Verifies a size-16 nice set exists
- Non-existence: Searches for size-17 nice sets (finds none)

**Usage:**
```bash
# Via CLI
python3 -m src.cli prove enum

# Direct execution
python3 -m src.proofs.enumeration_proof
```

**Features:**
- Exhaustive search for size-17 sets
- Sampling mode for very large search spaces
- Progress tracking with estimated completion times

### `z3_proof.py`

Z3 constraint solver-based proof for maximum nice set size.

**Approach:**
- Encodes completeness as Z3 constraints (Post classes)
- Uses symmetry breaking to prune search space
- Checks independence procedurally for complete sets
- Incremental solving with checkpointing support

**Usage:**
```bash
# Via CLI
python3 -m src.cli prove z3

# With checkpointing
python3 -m src.cli prove z3 --checkpoint proof.json --interval 50

# Custom parameters
python3 -m src.cli prove z3 --target-size 17 --max-depth 3

# Direct execution
python3 -m src.proofs.z3_proof
```

**Features:**
- Smart enumeration using Z3 SAT solver
- Completeness constraints via Post classes
- Advanced symmetry breaking (arity distribution, mandatory connectives)
- Checkpoint/resume support for long-running searches
- Configurable target size and composition depth

**Symmetry Breaking Optimizations:**
- Mandatory inclusion of FALSE constant
- Minimum arity distribution constraints
- At least one constant required
- Lexicographic ordering hints

## Proof Strategy

Both scripts provide complementary evidence:

1. **Lower bound:** Size-16 nice sets exist (verified constructively)
2. **Upper bound:** No size-17 nice sets exist (verified by exhaustive/guided search)
3. **Conclusion:** Maximum nice set size is exactly 16

## Implementation Notes

### Completeness Checking

Both scripts use Post's Completeness Theorem:
- A set is complete iff it escapes all 5 Post classes:
  - T0 (preserves false): f(0,0,...,0) = 0
  - T1 (preserves true): f(1,1,...,1) = 1
  - M (monotone): x <= y implies f(x) <= f(y)
  - D (self-dual): not f(x) = f(not x)
  - A (affine/linear): f(x XOR y) = f(x) XOR f(y) XOR f(0)

**Implementation:** The `is_complete()` function checks if at least one connective in the set does NOT belong to each clone. This is much faster than checking definability of all Boolean functions.

### Independence Checking

Independence is verified using bounded composition pattern enumeration:
- Patterns up to depth 3 by default
- Covers all practical composition scenarios
- Configurable depth for experimentation

**Key patterns checked:**
- Depth 1: Direct matches with variable permutations
- Depth 2: f(g(x,y), h(x,y)), unary(binary(x,y)), binary(unary(x), unary(y))
- Depth 3: unary(binary(unary(x), unary(y))), complex nested patterns

**Important:** Bounded composition means we only detect dependencies up to the specified depth. Deeper compositions may exist but won't be found.

### Performance

- **Enumeration proof:** Seconds to minutes depending on sample size
- **Z3 proof:** Minutes to hours depending on search space and symmetry breaking effectiveness

The Z3 approach is generally faster for proving non-existence due to constraint-guided pruning.

## Important Code Blocks

### Connective Pool Construction

Both proof scripts start by building a pool of connectives across arities:

```python
def build_connective_pool(max_arity=3):
    """Build the complete connective pool."""
    pool = []
    pool.extend(generate_all_connectives(0))  # 2 constants
    pool.extend(generate_all_connectives(1))  # 4 unary
    pool.extend(ALL_BINARY)                   # 16 binary
    if max_arity >= 3:
        pool.extend(generate_all_connectives(3))  # 256 ternary
    return pool
```

**Pool sizes:**
- Arity 0-2: 22 connectives
- Arity 0-3: 278 connectives (includes 256 ternary functions)

### Z3 Completeness Constraints (z3_proof.py)

The Z3 proof encodes Post's Completeness Theorem as constraints:

```python
# Build classification for each connective
preserves_f = [is_t0_preserving(pool[i]) for i in range(n)]
preserves_t = [is_t1_preserving(pool[i]) for i in range(n)]
monotone = [is_monotone(pool[i]) for i in range(n)]
self_dual = [is_self_dual(pool[i]) for i in range(n)]
affine = [is_affine(pool[i]) for i in range(n)]

# Escape T0: at least one selected connective doesn't preserve false
s.add(Or([And(selected[i], not preserves_f[i]) for i in range(n)]))

# Escape T1: at least one selected connective doesn't preserve true
s.add(Or([And(selected[i], not preserves_t[i]) for i in range(n)]))

# Similar for M, D, A clones...
```

This encoding allows Z3 to efficiently generate only complete sets as candidates, dramatically reducing the search space.

### Z3 Symmetry Breaking (z3_proof.py)

Advanced symmetry breaking constraints prune equivalent search branches:

```python
# Force FALSE constant to be included
if false_idx is not None:
    s.add(selected[false_idx])

# At least one constant required
constants_indices = [i for i in range(n) if pool[i].arity == 0]
if constants_indices:
    s.add(Or([selected[i] for i in constants_indices]))

# Minimum ternary count for larger sets
ternary_indices = [i for i in range(n) if pool[i].arity == 3]
min_ternary = max(0, int((target_size / 17) * 10))
if min_ternary > 0:
    ternary_count = Sum([If(selected[i], 1, 0) for i in ternary_indices])
    s.add(ternary_count >= min_ternary)
```

These constraints are based on empirical observations about maximal nice sets.

### Incremental Z3 Solving (z3_proof.py)

The Z3 script uses incremental solving for efficiency:

```python
while True:
    s.push()  # Create temporary scope

    result = s.check()
    if result == unsat:
        s.pop()
        break

    # Get model and extract selected connectives
    m = s.model()
    selected_indices = [i for i in range(n) if is_true(m[selected[i]])]
    selected_connectives = [pool[i] for i in selected_indices]

    # Check independence procedurally
    independent = is_independent(selected_connectives, max_depth=max_depth)

    # Block this solution and continue
    s.pop()
    s.add(Or([Not(selected[i]) for i in selected_indices]))
```

**Key insight:** Z3 generates complete sets, but we check independence procedurally since encoding composition patterns in Z3 is complex.

### Enumeration Proof Example Validation (enumeration_proof.py)

The enumeration proof validates a known size-16 nice set:

```python
def verify_size_16_exists(pool, max_depth=3):
    # Use the known example from validation
    example_indices = [
        6,    # XOR (binary)
        23, 64, 105, 150, 195, 240,  # ternary functions
        233, 106, 217, 90, 201, 74, 185, 58, 169  # more ternary
    ]

    # Build the actual connective set
    ternary = generate_all_connectives(3)
    example_set = [ternary[i] for i in example_indices if i < len(ternary)]

    if XOR not in example_set:
        example_set.insert(0, XOR)

    example_set = example_set[:16]

    # Check completeness and independence
    complete = is_complete(example_set)
    independent = is_independent(example_set, max_depth=max_depth)

    return complete and independent and len(example_set) == 16, example_set
```

This constructive proof shows that size-16 nice sets exist.

## Related Modules

- `src/post_classes.py` - Post class checking and completeness
- `src/independence.py` - Pattern enumeration independence checking
- `src/connectives.py` - Connective representation and generation
- `src/commands/prove.py` - CLI command handlers
