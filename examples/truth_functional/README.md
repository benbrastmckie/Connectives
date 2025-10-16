# Truth-Functional Mode Test Results

This directory contains test results generated using **truth-functional definability mode** (clone-theoretic, the current default).

## About Truth-Functional Mode

**Truth-functional definability** extends composition-based definability with universal rules for projections and cross-arity constants. It aligns with clone theory and universal algebra traditions.

### Key Characteristics

1. **Universal Projections**: All projection functions are universally definable from any basis
2. **Cross-Arity Constant Equivalence**: Constants with same truth value are equivalent across arities
3. **Clone-Theoretic**: Based on truth-functional equivalence classes
4. **More Permissive**: Detects more dependencies than syntactic mode

### Expected Results

Truth-functional mode typically produces:
- **Smaller or equal maximum nice set sizes** (more dependencies detected)
- Fewer total nice sets overall
- Sets with projections often become dependent
- Cross-arity constants collapse to equivalence classes

## Test Files

### Enumeration Tests

- **[enum_binary_only.md](enum_binary_only.md)** - Binary-only search via brute-force enumeration
  - Maximum: 3 (same as syntactic)
  - Nice sets found: 52 (size 3)
  - **31% fewer nice sets** than syntactic mode (52 vs 76)
  - Search time: 6.52s

- **[enum_unary_binary_max5.md](enum_unary_binary_max5.md)** - Unary + binary search via incremental enumeration
  - Maximum: 5 (same as syntactic)
  - Nice sets found: 2 (size 5), 25 (size 4), 118 (size 3)
  - **60% fewer size-5 sets** than syntactic mode (2 vs 5)
  - Search time: 149.20s (2.5 minutes)

### Z3 Constraint-Based Tests

Z3 constraint solving enables efficient search for large nice sets. The following milestone sizes are documented:

- **[z3_nice_set_29.md](z3_nice_set_29.md)** - Size-29 search (matches syntactic mode)
  - Found in 18.80s, arity: 1 + 3 + 25 (nullary + binary + ternary)
  - Demonstrates truth-functional mode scales to large sizes

- **[z3_nice_set_32.md](z3_nice_set_32.md)** - Size-32 search (near-maximum)
  - Found in 44.40s, arity: 1 + 1 + 30
  - One away from the likely maximum

- **[z3_nice_set_33.md](z3_nice_set_33.md)** - Size-33 search (**Likely Maximum**)
  - Found in 20.35s, arity: 1 + 0 + 32 (97% ternary!)
  - **Appears to be maximum** (sizes 34-35: none found in extensive search)

#### Additional Confirmed Sizes

The following sizes were also successfully found but not individually documented:

| Size | Time | Sets Checked | Arity Distribution | Notes |
|------|------|--------------|-------------------|-------|
| 6 | 0.14s | 1 | 1 + 2 + 3 | First with ternary |
| 10 | 0.13s | 1 | 1 + 0 + 9 | All ternary except constant |
| 17 | 0.67s | 22 | 1 + 1 + 15 | Matches syntactic milestone |
| 20 | 2.11s | 80 | 1 + 1 + 18 | - |
| 25 | 4.03s | 187 | 1 + 0 + 24 | - |
| 27 | 88.31s | 3,902 | 1 + 1 + 25 | - |
| 29 | 18.80s | 904 | 1 + 3 + 25 | Documented above |
| 32 | 44.40s | 1,822 | 1 + 1 + 30 | Documented above |
| **33** | **20.35s** | **1,239** | **1 + 0 + 32** | **Likely maximum** (documented above) |

#### Extensive Searches Beyond Size 33

The following sizes show no results after extensive Z3-guided search:

| Size | Candidates Checked | Time | Result |
|------|-------------------|------|--------|
| **34** | 10,000 | 362.89s (~6 min) | **0 nice sets found** |
| **35** | 10,000 | 400.44s (~6.7 min) | **0 nice sets found** |

**Strong evidence suggests maximum = 33** (though not mathematically proven).

All tests can be generated using:
```bash
python -m src.cli prove z3 --target-size N --definability-mode truth-functional
```

## Mode Comparison

For equivalent results in **syntactic mode**, see:
- [../syntactic/](../syntactic/) - Syntactic mode test directory (legacy results)
- [../../docs/DEFINABILITY.md](../../docs/DEFINABILITY.md) - Complete mode comparison

### Key Differences from Syntactic Mode

| Test Type | Syntactic | Truth-Functional | Difference |
|-----------|-----------|------------------|------------|
| Binary-only max | 3 | 3 | Same maximum |
| Binary-only count (size 3) | 76 sets | 52 sets | 31% fewer |
| Unary+binary max | 5 | 5 | Same maximum |
| **Mixed-arity max** | **35** | **33 (likely)** | **-2 (5.7% smaller if confirmed)** |

### Why Fewer Nice Sets?

Truth-functional mode's special rules eliminate additional sets:
1. **Universal projection rule**: Any set where projections can't be composed becomes dependent
2. **Cross-arity constant equivalence**: Sets with TRUE₀ and TRUE₂ (or FALSE₀ and FALSE₂) become dependent

Despite fewer nice sets, the **maximum sizes often remain the same**, as the additional dependencies typically affect boundary cases rather than maximum-size sets.

## Default Mode

As of 2025-10-15, truth-functional mode is the **project default**. This reflects the switch to clone-theoretic definability, aligning with universal algebra conventions.

### When to Use This Mode

Use truth-functional mode (this directory) when:
- Studying clone theory or universal algebra
- Want projections treated as "free" (universally available)
- Research on cross-arity constant relationships
- Need permissive definability detecting maximum dependencies

### When to Use Syntactic Mode

Use syntactic mode (../syntactic/) when:
- Reproducing classical logic results
- Want conservative independence estimates
- Studying composition-based definability
- Research requires explicit construction witnesses

## Related Documentation

- **[../syntactic/README.md](../syntactic/README.md)** - Syntactic mode results (legacy)
- **[../README.md](../README.md)** - Examples directory overview
- **[../../docs/DEFINABILITY.md](../../docs/DEFINABILITY.md)** - Complete mode documentation
- **[../../README.md](../../README.md)** - Project overview

## Reproducing Results

All tests use truth-functional mode (default):

```bash
# Binary-only enumeration (default mode)
python -m src.cli search binary

# Explicit truth-functional flag
python -m src.cli search binary --definability-mode truth-functional

# Unary+binary enumeration
python -m src.cli search full --max-arity 2 --definability-mode truth-functional

# Z3 search for size N
python -m src.cli prove z3 --target-size N --definability-mode truth-functional
```

## Contributing New Tests

To add new truth-functional mode tests:
1. Run the desired command with `--definability-mode truth-functional`
2. Document results following the format in enum_binary_only.md
3. Include "Mode Comparison" section referencing syntactic equivalent
4. Add cross-references to related tests

---

**All results in this directory use truth-functional (clone-theoretic) definability mode (project default).**
