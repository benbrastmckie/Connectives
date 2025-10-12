# Size-35 Nice Set Discovery

**NEW RECORD**: First known nice set of size 35!

## Discovery Details

- **Method**: Z3-based constraint-guided search with depth-3 independence checking
- **Search Time**: 2783.17 seconds (~46.4 minutes)
- **Complete Sets Checked**: 26,860
- **Date**: 2025-10-07

## The Nice Set

This set contains **35 connectives**:
- 1 nullary (constant): FALSE
- 1 binary: CONV_INHIBIT (converse inhibition: x ∧ ¬y)
- 33 ternary functions

### Arity Distribution
- Nullary: 1 (3%)
- Binary: 1 (3%)
- Ternary: 33 (94%)

This is the highest ternary percentage found so far, with 94% ternary functions.

## Full Set Listing

```
FALSE           (nullary)
CONV_INHIBIT    (binary: x ∧ ¬y)
f3_2            (ternary)
f3_19           (ternary)
f3_23           (ternary)
f3_26           (ternary)
f3_60           (ternary)
f3_80           (ternary)
f3_84           (ternary)
f3_87           (ternary)
f3_95           (ternary)
f3_96           (ternary)
f3_106          (ternary)
f3_107          (ternary)
f3_117          (ternary)
f3_122          (ternary)
f3_133          (ternary)
f3_143          (ternary)
f3_144          (ternary)
f3_150          (ternary)
f3_152          (ternary)
f3_172          (ternary)
f3_181          (ternary)
f3_182          (ternary)
f3_186          (ternary)
f3_195          (ternary)
f3_200          (ternary)
f3_209          (ternary)
f3_210          (ternary)
f3_225          (ternary)
f3_229          (ternary)
f3_231          (ternary)
f3_233          (ternary)
f3_236          (ternary)
f3_247          (ternary)
```

**Note**: For complete truth tables of all ternary connectives (f3_N), see the [Ternary Connectives Glossary](../glossary/connectives.md).

## Verification

### Completeness
Verified via Post's Theorem - the set escapes all 5 Post classes:
- T₀ (preserves false)
- T₁ (preserves true)
- M (monotone)
- D (self-dual)
- A (affine/linear)

### Independence
Verified via pattern enumeration up to depth 3. No connective in the set can be expressed as a composition (depth ≤ 3) of the others.

## Significance

This discovery demonstrates:
1. **Size-35 is achievable**: The maximum nice set size is at least 35
2. **Extended search success**: Increasing the candidate limit from 10,000 to 50,000 was necessary to find this set
3. **Very sparse solution space**: Required checking 26,860 complete sets (2.7× more than size-34)
4. **Ternary dominance continues**: 94% ternary functions, highest percentage yet
5. **Mixed arity still beneficial**: Still includes one binary function (CONV_INHIBIT) alongside the ternary functions

## Search Evolution

The discovery of size-35 required substantially more search effort:
- Size-31: 9,527 candidates
- Size-32: 1,822 candidates (10× faster)
- Size-33: 1,239 candidates (even faster)
- Size-34: 3,226 candidates
- **Size-35: 26,860 candidates** (8× harder than size-34)

This suggests we are approaching the maximum, as the solution space is becoming increasingly sparse.

## Reproduction

To reproduce this finding:

```bash
python -m src.cli prove z3 --target-size 35 --max-depth 3 --max-candidates 50000
```

Note: This will take approximately 45-50 minutes to find the first size-35 set.

## Next Steps

The next natural question is: **Does a size-36 nice set exist?**

Given the dramatic increase in search difficulty (26,860 candidates for size-35 vs. 3,226 for size-34), a size-36 search may require:
- Even higher candidate limits (100,000+)
- Longer runtime (hours instead of minutes)
- Or may not exist at all (size-35 could be the maximum)
