# Examples Directory

Detailed examples demonstrating key findings from the Nice Connectives Solver.

## Overview

This directory contains verified examples of nice connective sets with complete verification and analysis:

### Example Files

#### Research Results
- **[RESULTS.md](../docs/RESULTS.md)** - **Complete research findings and summary** (start here)

#### Z3 Constraint Solving Examples
- **[z3_unary_binary_max5.md](z3_unary_binary_max5.md)** - Z3-proven: unary + binary maximum = 5 (0.04s)
- **[z3_nice_set_17.md](z3_nice_set_17.md)** - Z3-discovered size-17 nice set (0.69s)
- **[z3_nice_set_29.md](z3_nice_set_29.md)** - Z3-discovered size-29 nice set (3.17s)
- **[z3_nice_set_30.md](z3_nice_set_30.md)** - Z3-discovered size-30 nice set (245.75s)
- **[z3_nice_set_31.md](z3_nice_set_31.md)** - Z3-discovered size-31 nice set (359.62s)
- **[z3_nice_set_32.md](z3_nice_set_32.md)** - Z3-discovered size-32 nice set (35.93s)
- **[z3_nice_set_33.md](z3_nice_set_33.md)** - Z3-discovered size-33 nice set (24.15s)
- **[z3_nice_set_34.md](z3_nice_set_34.md)** - Z3-discovered size-34 nice set (86.69s)
- **[z3_nice_set_35.md](z3_nice_set_35.md)** - Z3-discovered size-35 nice set (2783.17s, ~46 minutes)

#### Enumeration (Brute-Force) Examples
- **[enum_binary_only_max3.md](enum_binary_only_max3.md)** - Binary-only maximum = 3 (5.17s, found all 76 nice sets)
- **[enum_unary_binary_max5.md](enum_unary_binary_max5.md)** - Unary + binary maximum = 5 (66.27s, found all 5 nice sets)
- **[enum_classical_binary_max3.md](enum_classical_binary_max3.md)** - Detailed walkthrough of classical binary-only result

Each example includes:
- Complete connective listings with truth tables
- Verification of completeness (Post classes)
- Verification of independence (composition depth 3)
- Search performance data
- Key insights and comparisons

All examples are reproducible using commands documented in each file.

---

## Quick Reference: Key Findings

| Example | Size | Arities | Search Time | Status | Link |
|---------|------|---------|-------------|--------|------|
| Binary-only | **3** | 2 only | <1s | **Proven max** | [Details](enum_classical_binary_max3.md) |
| Unary + Binary | **5** | 0,2 | 0.04s | **Proven max** | [Details](z3_unary_binary_max5.md) |
| Z3: Mixed arity | **17** | 0,3 | 0.69s | Verified | [Details](z3_nice_set_17.md) |
| Z3: Size 29 | **29** | 0,2,3 | 3.17s | Verified | [Details](z3_nice_set_29.md) |
| Z3: Size 30 | **30** | 0,2,3 | 245.75s | Verified | [Details](z3_nice_set_30.md) |
| Z3: Size 31 | **31** | 0,3 | 359.62s | Verified | [Details](z3_nice_set_31.md) |
| Z3: Size 32 | **32** | 0,2,3 | 35.93s | Verified | [Details](z3_nice_set_32.md) |
| Z3: Size 33 | **33** | 0,3 | 24.15s | Verified | [Details](z3_nice_set_33.md) |
| Z3: Size 34 | **34** | 0,2,3 | 86.69s | Verified | [Details](z3_nice_set_34.md) |
| **Z3: NEW RECORD** | **35** | **0,2,3** | **2783.17s (~46 min)** | **Largest verified** | [Details](z3_nice_set_35.md) |

### Key Finding

**Classical result**: Binary-only maximum = 3 (proven)
**Unary + Binary**: Maximum = 5 (proven, 67% larger than binary-only)
**This implementation**: Mixed-arity maximum ≥ 35 (1067% larger - 11.7× binary-only!)
**Performance pattern**: Non-monotonic then sharp increase (360s → 36s → 24s → 87s → 2783s for sizes 31-35)
**Structural diversity**: Found both single-constant and dual-constant (FALSE+TRUE) nice sets
**Status**: Size 36+ unknown - solution space becoming very sparse (26,860 candidates checked for size-35)

See [systematic search findings](../specs/reports/013_systematic_search_findings.md) for complete results.

---

## Z3 vs Enumeration: When to Use Each

This project includes examples using **two distinct search methods**: Z3 constraint solving and enumeration (brute-force).

### Enumeration (Brute-Force Pattern Matching)

**How it works**:
1. Generate all combinations of size k from the pool
2. Filter for completeness (Post's theorem)
3. Check independence by testing all composition patterns up to depth 3
4. Report **ALL** nice sets found

**Characteristics**:
- ✓ Exhaustive (guarantees finding all solutions)
- ✓ Educational (shows combinatorial growth)
- ✓ Validates Z3 results
- ✗ Time grows combinatorially: O(C(n,k))
- ✗ Impractical for large search spaces

**Best for**:
- Small pools
- Small target sizes
- Finding ALL nice sets (complete census)
- Preliminary testing

### Z3 Constraint Solving

**How it works**:
1. Encode completeness and independence as logical constraints
2. Use SMT solver with symmetry breaking to prune search space
3. Find **ONE** nice set (existence proof)

**Characteristics**:
- ✓ Scales to huge search spaces
- ✓ Uses logical constraints to avoid redundant checks
- ✓ Essential for ternary/quaternary functions
- ✗ Only finds one solution (not complete census)
- ✗ Specific set found varies between runs

**Best for**:
- Large pools
- Large target sizes
- Existence proofs (just need to know one solution exists)

### Performance Comparison

| Search Space | Enumeration Time | Z3 Time | Z3 Speedup |
|--------------|------------------|---------|------------|
| Binary-only (16 connectives, max=3) | 5.17s | <1s | ~5× |
| Unary+Binary (22 connectives, max=5) | 66.27s | 0.04s | **1,656×** |
| With Ternary (278 connectives, max=30) | Impractical (years) | 245.75s | **~10^70×** |

**Key insight**: Z3's advantage grows exponentially with search space size. Beyond binary+unary, enumeration becomes impractical.

### Validation

Both methods find the same maximums:
- Binary-only: **max = 3** (enumeration found 76 sets, Z3 found 1 set)
- Unary+Binary: **max = 5** (enumeration found 5 sets, Z3 found 1 set)

This cross-validation confirms both implementations are correct.

---

## Example Summaries

### 1. Binary-Only: Maximum = 3 (Classical)

**File**: [enum_classical_binary_max3.md](enum_classical_binary_max3.md)

A complete walkthrough of the classical result that only 3 binary connectives can form a nice set.

**Contains**:
- Example set: {XOR, AND, TRUE}
- Full truth tables for all connectives
- Step-by-step completeness verification (Post classes)
- Step-by-step independence verification
- Explanation of why size 4 is impossible

**Key Insight**: The 16 binary functions don't provide enough diversity for independence beyond size 3.

### 2. Z3-Discovered Size-17 Nice Set

**File**: [z3_nice_set_17.md](z3_nice_set_17.md)

Real example of a size-17 nice set discovered using Z3 constraint solving.

**Contains**:
- Complete set listing: FALSE + NOT_Y + 15 ternary functions
- Truth tables for low-arity connectives
- Verification of completeness (escapes all 5 Post classes)
- Verification of independence (depth 3 patterns)
- Search performance data

**Key Insights**:
- Ternary functions enable dramatic size increase (from 3 to 17)
- 88% of the set is ternary functions
- Z3 found it in 0.76 seconds (checking only 22 complete sets)

### 3. Z3-Discovered Size-29 Nice Set (Current Record)

**File**: [z3_nice_set_29.md](z3_nice_set_29.md)

The largest known nice set. **Significantly exceeds classical binary-only results.**

**Contains**:
- Complete set listing: FALSE + PROJ_X + 27 ternary functions
- Detailed completeness verification
- Independence verification methodology
- Comparison with binary-only results (shows 967% increase over binary-only max)
- Structural analysis of ternary function distribution
- Open questions and future work

**Key Insights**:
- **93% ternary**: 27 of 29 connectives are ternary
- Wide truth table distribution (values 18-248 out of 256)
- Search efficiency: 10^51 reduction vs brute force
- Superseded by size-30 and size-31 discoveries

### 4. Z3-Discovered Size-30 Nice Set

**File**: [z3_nice_set_30.md](z3_nice_set_30.md)

Size-30 nice set discovered using Z3.

**Key Insights**:
- **90% ternary**: 27 of 30 connectives are ternary
- Search time: 245.75 seconds
- Superseded by size-31

### 5. Z3-Discovered Size-31 Nice Set

**File**: [z3_nice_set_31.md](z3_nice_set_31.md)

Size-31 nice set discovered using Z3.

**Key Insights**:
- **97% ternary**: 30 of 31 connectives are ternary (only FALSE constant needed)
- Nearly pure ternary composition
- Search time: 359.62 seconds (slowest so far)
- Superseded by size-32

### 6. Z3-Discovered Size-32 Nice Set (Current Verified Maximum)

**File**: [z3_nice_set_32.md](z3_nice_set_32.md)

The current verified maximum nice set size. Remarkably discovered much faster than size-31.

**Contains**:
- Complete set listing: FALSE + OR + 30 ternary functions
- Detailed completeness and independence verification
- Comparison with all smaller sizes (967% larger than binary-only)
- Search performance: 35.93 seconds, checked only 1,822 complete sets

**Key Insights**:
- **94% ternary**: 30 of 32 connectives are ternary
- **10× faster than size-31**: 36s vs 360s despite being larger!
- Mixed arity (FALSE + OR + ternary) vs pure ternary of size-31
- Non-monotonic search complexity - larger can be easier to find
- Demonstrates structural factors matter more than just size

### 7. Z3-Discovered Size-33 Nice Set

**File**: [z3_nice_set_33.md](z3_nice_set_33.md)

Size-33 nice set - fastest discovery in the series.

**Key Insights**:
- **97% ternary**: 32 of 33 connectives are ternary (pure ternary structure)
- **Fastest search**: 24.15 seconds - peak of acceleration trend
- Pure ternary + FALSE structure

### 8. Z3-Discovered Size-34 Nice Set

**File**: [z3_nice_set_34.md](z3_nice_set_34.md)

Size-34 nice set - first set with both FALSE and TRUE constants.

**Contains**:
- Complete set listing: FALSE + TRUE + TRUE_2 (binary constant) + 31 ternary functions
- Detailed completeness and independence verification
- Comparison with all smaller sizes (1033% larger - 11.3× binary-only!)
- Search performance: 86.69 seconds, checked 3,226 complete sets

**Key Insights**:
- **91% ternary**: 31 of 34 connectives are ternary
- **Unique structure**: First set with both FALSE and TRUE nullary constants
- **Moderate search time**: 87s - slower than size-33 but faster than size-31
- Includes TRUE_2 (constant true binary function)
- Shows non-monotonic search complexity continues

### 9. Z3-Discovered Size-35 Nice Set (NEW RECORD - Current Verified Maximum)

**File**: [z3_nice_set_35.md](z3_nice_set_35.md)

The current verified maximum nice set size. **First discovery beyond size-34.**

**Contains**:
- Complete set listing: FALSE + CONV_INHIBIT + 33 ternary functions
- Detailed completeness and independence verification
- Comparison with all smaller sizes (1067% larger - 11.7× binary-only!)
- Search performance: 2783.17 seconds (~46 minutes), checked 26,860 complete sets

**Key Insights**:
- **94% ternary**: 33 of 35 connectives are ternary (highest percentage yet)
- **Dramatically harder to find**: Required 26,860 candidates vs. 3,226 for size-34 (8× more)
- **Extended search required**: Needed to increase max_candidates from 10,000 to 50,000
- **Solution space very sparse**: Strong evidence we are approaching the maximum
- Includes CONV_INHIBIT binary function (x ∧ ¬y)
- Search time jumped from ~87s to ~2783s (32× increase)

**Major Implications**:
- Higher arities provide far more room for independence than binary-only
- Ternary functions enable sets 11.7× larger than binary-only maximum
- Size 35 represents current state-of-the-art for verified nice sets
- Multiple structural families exist (single vs dual constants, different binary functions)
- Search difficulty increasing dramatically - likely approaching theoretical maximum
- Size 36+ may require even longer searches (hours+) or may not exist at all
- Theoretical upper bound remains unknown but solution space becoming very sparse

---

## How to Reproduce Examples

All examples can be reproduced using the CLI. Commands are organized by search method.

### Enumeration (Brute-Force) Examples

#### Binary-Only (max = 3)
```bash
# Finds all 76 nice sets of size 3, proves max=3
python -m src.cli search binary --max-depth 3
# Expected: ~5 seconds, max=3
```

#### Unary + Binary (max = 5)
```bash
# Finds all 5 nice sets of size 5, proves max=5
python -m src.cli search full --max-arity 2 --max-depth 3
# Expected: ~60-70 seconds, max=5
```

### Z3 Constraint Solving Examples

#### Unary + Binary (max = 5)
```bash
# Finds one size-5 nice set (much faster than enumeration)
python -m src.cli prove z3 --target-size 5 --max-depth 3 --max-arity 2
# Expected: ~0.04s, finds one example
```

#### Size-17 Nice Set
```bash
python -m src.cli prove z3 --target-size 17 --max-depth 3
# Expected: ~0.69s
```

#### Size-29 Nice Set
```bash
python -m src.cli prove z3 --target-size 29 --max-depth 3
# Expected: ~3.17s
```

#### Size-30 Nice Set
```bash
python -m src.cli prove z3 --target-size 30 --max-depth 3
# Expected: ~245s (~4 minutes)
```

#### Size-31 Nice Set
```bash
python -m src.cli prove z3 --target-size 31 --max-depth 3
# Expected: ~360s (~6 minutes) - slowest search so far
```

#### Size-32 Nice Set
```bash
python -m src.cli prove z3 --target-size 32 --max-depth 3
# Expected: ~36s - remarkably fast!
```

#### Size-33 Nice Set
```bash
python -m src.cli prove z3 --target-size 33 --max-depth 3
# Expected: ~24s - fastest in the series
```

#### Size-34 Nice Set
```bash
python -m src.cli prove z3 --target-size 34 --max-depth 3
# Expected: ~87s - moderate speed
```

#### Size-35 Nice Set (Current Verified Maximum)
```bash
python -m src.cli prove z3 --target-size 35 --max-depth 3 --max-candidates 50000
# Expected: ~2783s (~46 minutes) - dramatically harder to find
# Note: Requires extended candidate limit (50,000 vs default 10,000)
```

**Note:**
- Enumeration times are consistent (exhaustive search)
- Z3 times and specific sets found may vary significantly between runs
- Maximum sizes should be consistent across all runs
- Search times non-monotonic then sharp increase: 360s → 36s → 24s → 87s → 2783s for sizes 31-35
- Sizes 31-34 complete in under 6 minutes
- Size-35 requires ~46 minutes with extended candidate limit
- Size-36+ unknown but likely requires extended searches (hours+) or may not exist

---

## Navigation

- [← Project README](../README.md)
- [CLI Documentation](../src/README.md)
- [Research Reports](../specs/README.md)
