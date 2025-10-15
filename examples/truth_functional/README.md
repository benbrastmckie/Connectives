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

### Z3 Constraint-Based Tests

**Status**: Deferred due to time constraints (2-4 hours estimated)

The following tests are planned but not yet generated:
- z3_nice_set_17.md - Size-17 search (if achievable in truth-functional mode)
- z3_nice_set_29.md through z3_nice_set_35.md - Large set searches

These can be generated using:
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
| Unary+binary max | 5 | 5 (partial) | Likely same |

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
