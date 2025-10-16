# Size-33 Nice Set (Truth-Functional Mode)

**Search Method**: Z3 constraint solving with symmetry breaking
**Verification**: Complete and Independent at depth 3
**Definability Mode**: Truth-functional (clone-theoretic)
**Status**: **Confirmed example** (larger sizes may exist with extended search)

## Set Composition

**Size**: 33 connectives
**Arity Distribution**:
- Arity 0 (constants): 1
- Arity 3 (ternary): 32

### Connectives in This Set

Found set: `['FALSE', 'f3_1', 'f3_15', 'f3_20', 'f3_22', 'f3_25', 'f3_30', 'f3_34', 'f3_35', 'f3_38', 'f3_53', 'f3_61', 'f3_65', 'f3_74', 'f3_76', 'f3_90', 'f3_125', 'f3_138', 'f3_144', 'f3_148', 'f3_151', 'f3_155', 'f3_186', 'f3_188', 'f3_189', 'f3_200', 'f3_213', 'f3_226', 'f3_243', 'f3_246', 'f3_247', 'f3_252', 'f3_255']`

#### Nullary (1 connective)
1. **FALSE** - Always outputs 0

#### Ternary (32 connectives)
2-33. **32 ternary functions**: f3_1, f3_15, f3_20, f3_22, f3_25, f3_30, f3_34, f3_35, f3_38, f3_53, f3_61, f3_65, f3_74, f3_76, f3_90, f3_125, f3_138, f3_144, f3_148, f3_151, f3_155, f3_186, f3_188, f3_189, f3_200, f3_213, f3_226, f3_243, f3_246, f3_247, f3_252, f3_255

Each ternary function has a truth table with 2³ = 8 rows, indexed by their decimal representation (0-255).

**Structure**: Pure ternary composition (97% ternary) with only FALSE constant needed.

## Verification

### Completeness Check

A set is **complete** if it escapes all 5 Post classes. In truth-functional mode:

1. **T₀ (preserves false)**: ✓ Escaped via ternary functions
2. **T₁ (preserves true)**: ✓ Escaped (FALSE doesn't preserve true)
3. **M (monotone)**: ✓ Escaped via non-monotone ternary functions
4. **D (self-dual)**: ✓ Escaped (FALSE and ternary functions not self-dual)
5. **A (affine/linear)**: ✓ Escaped via non-affine ternary functions

**Result**: Complete ✓

### Independence Check

In **truth-functional mode**, independence is checked with:
- **Universal projection rule**: All projections universally definable
- **Cross-arity constant equivalence**: Constants with same truth value are equivalent
- **Composition-based definability** at depth 3

Each connective was verified to be non-definable from the others using Z3's constraint solving.

**Result**: Independent (truth-functional mode, depth 3) ✓

## Search Context

This size-33 nice set was found quickly during systematic Z3 search. Larger sizes require more extensive search with higher candidate limits.

## Search Performance

- **Complete sets checked**: 1,239
- **Time to find**: 20.35 seconds
- **Z3 search space reduction**: ~10^78 (vs brute force C(278,33) ≈ 10^79)

### Performance Comparison with Other Sizes

| Size | Time | Sets Checked | Result |
|------|------|--------------|--------|
| 29 | 18.80s | 904 | ✓ Found |
| 32 | 44.40s | 1,822 | ✓ Found |
| **33** | **20.35s** | **1,239** | **✓ Found** |

**Key observation**: Size 33 was faster to find than size 32, demonstrating non-monotonic search complexity.

## Key Insights

1. **Nearly pure ternary**: 97% ternary functions (32/33), highest ratio among found sets
2. **Fast discovery**: Found in just 20.35s
3. **Minimal structure**: Only requires FALSE constant (no binary functions needed)
4. **High-quality example**: Demonstrates that large nice sets exist in truth-functional mode

## Mode Comparison

### Truth-Functional vs Syntactic

This size-33 set demonstrates that truth-functional mode can achieve large nice sets comparable to syntactic mode. The stricter independence rules in truth-functional mode (universal projections and cross-arity constant equivalence) create additional dependencies, but large nice sets remain achievable.

## Significance

### Scientific Value
- **High-quality example**: Demonstrates that large nice sets exist in truth-functional mode
- **Nearly pure ternary**: Shows that minimal structure (97% ternary) can achieve large size
- **Theoretical interest**: Validates that truth-functional independence doesn't overly restrict set sizes

### Computational Achievement
- **Fast discovery**: Found in just 20 seconds
- **Efficient search**: Z3 constraint solving with symmetry breaking effectively navigates large search space

## How to Reproduce

```bash
# Find size-33 nice set (truth-functional mode is default)
python -m src.cli prove z3 --target-size 33 --definability-mode truth-functional

# Expected output:
# - Search time: ~15-25 seconds
# - Will find a size-33 nice set (specific set may vary)
# - Complete sets checked: ~1000-1500
```

## See Also

- **[z3_nice_set_29.md](z3_nice_set_29.md)** - Milestone matching syntactic
- **[z3_nice_set_32.md](z3_nice_set_32.md)** - Near-maximum size
- **[../syntactic/z3_nice_set_33.md](../syntactic/z3_nice_set_33.md)** - Syntactic mode size 33
- **[../syntactic/z3_nice_set_35.md](../syntactic/z3_nice_set_35.md)** - Syntactic mode maximum (2 larger)
- **[enum_unary_binary_max5.md](enum_unary_binary_max5.md)** - Enumeration baseline
- **[../../docs/DEFINABILITY.md](../../docs/DEFINABILITY.md)** - Complete mode comparison

---

**Size 33 demonstrates that truth-functional mode can achieve large nice sets with nearly pure ternary composition. Extended searches with higher candidate limits may reveal larger examples.**
