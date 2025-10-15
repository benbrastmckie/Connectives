# Syntactic Mode Test Results

This directory contains test results generated using **syntactic definability mode** (composition-based, depth-bounded).

## About Syntactic Mode

**Syntactic definability** requires explicit construction via composition trees with bounded depth. A connective f is definable from basis B if there exists a composition tree using only functions from B that evaluates to f.

### Key Characteristics

1. **Depth-Bounded**: Only checks compositions up to max_depth (default: 3)
2. **Arity-Sensitive**: Functions of different arities are treated as distinct
3. **No Implicit Projections**: Projection functions must be composed from basis
4. **Composition-Only**: No special universal assumptions

### Expected Results

Syntactic mode typically produces:
- **Larger maximum nice set sizes** (fewer dependencies detected)
- More total nice sets overall
- Conservative independence estimates
- Results comparable to classical logic literature

## Test Files

### Enumeration Tests

- **[enum_binary_only_max3.md](enum_binary_only_max3.md)** - Binary-only search via brute-force enumeration
  - Maximum: 3
  - Nice sets found: 76 (size 3)
  - Search time: 5.17s

- **[enum_classical_binary_max3.md](enum_classical_binary_max3.md)** - Detailed walkthrough of classical binary result
  - Maximum: 3
  - Classical result verification

- **[enum_unary_binary_max5.md](enum_unary_binary_max5.md)** - Unary + binary connectives search
  - Maximum: 5
  - Demonstrates benefit of mixed arities

### Z3 Constraint-Based Tests

- **[z3_unary_binary_max5.md](z3_unary_binary_max5.md)** - Z3 proof for unary + binary
  - Maximum: 5
  - Fast constraint-solving approach

- **[z3_nice_set_17.md](z3_nice_set_17.md)** - Size-17 nice set discovery
  - First known size-17 nice set
  - Mixed arity (nullary, unary, binary, ternary)

- **[z3_nice_set_29.md](z3_nice_set_29.md)** through **[z3_nice_set_35.md](z3_nice_set_35.md)** - Large nice sets
  - Progressive discoveries of sizes 29-35
  - Predominantly ternary connectives
  - Size 35 is current known maximum in syntactic mode

## Mode Comparison

For equivalent results in **truth-functional mode**, see:
- [../truth_functional/](../truth_functional/) - Truth-functional mode test directory
- [../../docs/DEFINABILITY.md](../../docs/DEFINABILITY.md) - Complete mode comparison

### Syntactic vs Truth-Functional

| Aspect | Syntactic (This Directory) | Truth-Functional |
|--------|----------------------------|------------------|
| Projections | Must compose explicitly | Universally definable |
| Cross-arity constants | Independent | Equivalent if same truth value |
| Nice set sizes | Typically larger | Typically smaller |
| Research tradition | Logic, computability | Universal algebra, clone theory |

## Legacy Note

These tests were generated when syntactic mode was the default (before 2025-10-15). The project has since switched to truth-functional mode as the default, but these results remain valid and useful for:
- Comparing definability modes
- Reproducing classical logic results
- Conservative independence estimates

## Related Documentation

- **[../truth_functional/README.md](../truth_functional/README.md)** - Truth-functional mode results
- **[../README.md](../README.md)** - Examples directory overview
- **[../../docs/DEFINABILITY.md](../../docs/DEFINABILITY.md)** - Complete mode documentation
- **[../../README.md](../../README.md)** - Project overview

## Reproducing Results

All tests can be reproduced using the syntactic mode flag:

```bash
# Binary-only enumeration
python -m src.cli search binary --definability-mode syntactic

# Unary+binary enumeration
python -m src.cli search full --max-arity 2 --definability-mode syntactic

# Z3 search for size N
python -m src.cli prove z3 --target-size N --definability-mode syntactic
```

---

**All results in this directory use syntactic (composition-based) definability mode.**
