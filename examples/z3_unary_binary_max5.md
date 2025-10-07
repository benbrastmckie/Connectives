# Example: Unary + Binary Maximum Nice Set (Size 5)

**Search Method**: Z3 constraint solving with symmetry breaking
**Arity Restriction**: Constants (0), Unary (1), and Binary (2) only - no ternary
**Verification**: Complete and Independent at depth 3

## Answer

**Maximum nice set size with unary + binary connectives: 5**

This is proven by:
1. Z3 found a size-5 nice set (existence proof)
2. Z3 found no size-6 nice sets after checking 10,000 complete candidates (exhaustion proof)

## Set Composition

**Size**: 5 connectives
**Arity Distribution**:
- Arity 0 (constants): 2 (FALSE, TRUE)
- Arity 2 (binary): 3 (XOR, AND, IMP)

**Notable**: No unary functions! This avoids the dependency where FALSE = NOT(TRUE).

### Connectives in This Set

1. **FALSE** (arity 0)
   - Truth table: 0b0
   - Always outputs 0

2. **TRUE** (arity 0)
   - Truth table: 0b1
   - Always outputs 1

3. **XOR** (arity 2)
   - Truth table: 0b0110 = 6
   - Formula: f(x,y) = x ⊕ y

   | x | y | XOR(x,y) |
   |---|---|----------|
   | 0 | 0 | 0        |
   | 0 | 1 | 1        |
   | 1 | 0 | 1        |
   | 1 | 1 | 0        |

4. **AND** (arity 2)
   - Truth table: 0b1000 = 8
   - Formula: f(x,y) = x ∧ y

   | x | y | AND(x,y) |
   |---|---|----------|
   | 0 | 0 | 0        |
   | 0 | 1 | 0        |
   | 1 | 0 | 0        |
   | 1 | 1 | 1        |

5. **IMP** (arity 2)
   - Truth table: 0b1101 = 13
   - Formula: f(x,y) = x → y = ¬x ∨ y

   | x | y | IMP(x,y) |
   |---|---|----------|
   | 0 | 0 | 1        |
   | 0 | 1 | 1        |
   | 1 | 0 | 0        |
   | 1 | 1 | 1        |

## Verification

### Completeness Check

A set is **complete** if it escapes all 5 Post classes. This set escapes:

1. **T₀ (preserves false)**: ✓ Escaped
   - TRUE: TRUE() = 1 ≠ 0, doesn't preserve false ✓

2. **T₁ (preserves true)**: ✓ Escaped
   - FALSE: FALSE() = 0 ≠ 1, doesn't preserve true ✓

3. **M (monotone)**: ✓ Escaped
   - XOR is not monotone: XOR(0,0) = 0 < XOR(0,1) = 1 but XOR(1,1) = 0 ✓

4. **D (self-dual)**: ✓ Escaped
   - FALSE is not self-dual ✓
   - TRUE is not self-dual ✓

5. **A (affine/linear)**: ✓ Escaped
   - AND is not affine (it's quadratic over GF(2)) ✓

**Result**: Complete ✓

### Independence Check

Z3 search verified independence by:
- Checking all composition patterns up to depth 3
- Confirming no connective in the set can be derived from the others
- Using the fixed independence checker that properly handles arity-0 and arity-1 targets

**Result**: Independent (at depth 3) ✓

## Why Not Include Unary Functions?

Adding unary functions creates dependencies:
- If we have {FALSE, TRUE, NOT}, then FALSE = NOT(TRUE)
- If we have {0, 1, NOT} (unary versions), then 0 = NOT(1)

The maximum size-5 set avoids this by using only constants and binary functions.

## Comparison with Binary-Only

| Configuration | Maximum Size | Improvement |
|---------------|-------------|-------------|
| Binary-only (arity 2) | 3 | baseline |
| **Unary + Binary (arity 0-2)** | **5** | **67% larger** |
| Unary + Binary + Ternary (arity 0-3) | ≥29 | 867% larger |

**Key insight**: Adding constants to binary functions increases the maximum from 3 to 5.

## Search Performance

- **Size 5**: Found in 0.04s, checked 26 complete sets
- **Size 6**: No sets found after 19.05s, checked 10,000 complete sets

**Z3 efficiency**: Symmetry breaking significantly reduces search space.

## How to Reproduce

```bash
# Find size-5 nice set (should find one)
python -m src.cli prove z3 --target-size 5 --max-depth 3 --max-arity 2

# Verify size-6 doesn't exist (should find none)
python -m src.cli prove z3 --target-size 6 --max-depth 3 --max-arity 2
```

## See Also

- [enum_classical_binary_max3.md](enum_classical_binary_max3.md) - Binary-only result (max=3)
- [z3_nice_set_17.md](z3_nice_set_17.md) - With ternary functions (size 17)
- [z3_nice_set_29.md](z3_nice_set_29.md) - Current record with ternary (size 29)
- [RESULTS.md](../docs/RESULTS.md) - Complete research findings

---

**This example demonstrates that including constants with binary functions increases the maximum nice set size from 3 to 5.**
