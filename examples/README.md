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
- **[z3_nice_set_30.md](z3_nice_set_30.md)** - **Current verified maximum**: size-30 nice set (245.75s)

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
| Z3: Mixed arity | **17** | 0,2,3 | 0.69s | Verified | [Details](z3_nice_set_17.md) |
| Z3: Size 29 | **29** | 0,2,3 | 3.17s | Verified | [Details](z3_nice_set_29.md) |
| **Z3: Current maximum** | **30** | 0,2,3 | 245.75s | **Largest verified** | [Details](z3_nice_set_30.md) |

### Key Finding

**Classical result**: Binary-only maximum = 3 (proven)
**Unary + Binary**: Maximum = 5 (proven, 67% larger than binary-only)
**This implementation**: Mixed-arity maximum ≥ 30 (900% larger than binary-only)
**Status**: Size 31+ unknown (timed out after 5 minutes)

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
- Small pools (≤25 connectives)
- Small target sizes (≤6)
- Finding ALL nice sets (complete census)
- Educational/exploratory purposes

### Z3 Constraint Solving

**How it works**:
1. Encode completeness and independence as logical constraints
2. Use SMT solver with symmetry breaking to prune search space
3. Find **ONE** nice set (existence proof)

**Characteristics**:
- ✓ Scales to huge search spaces (278+ connectives)
- ✓ Uses logical constraints to avoid redundant checks
- ✓ Essential for ternary/quaternary functions
- ✗ Only finds one solution (not complete census)
- ✗ Specific set found varies between runs

**Best for**:
- Large pools (100+ connectives)
- Large target sizes (20+)
- Existence proofs (just need to know one solution exists)
- Production searches

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

### 3. Z3-Discovered Size-29 Nice Set

**File**: [z3_nice_set_29.md](z3_nice_set_29.md)

A size-29 nice set discovered using Z3. Significantly larger than binary-only maximum (3) but superseded by size-30.

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
- Superseded by size-30 discovery

### 4. Z3-Discovered Size-30 Nice Set (Current Verified Maximum)

**File**: [z3_nice_set_30.md](z3_nice_set_30.md)

The current verified maximum nice set size.

**Contains**:
- Complete set listing: FALSE + PROJ_X + 28 ternary functions
- Detailed completeness and independence verification
- Comparison with smaller sizes (900% larger than binary-only)
- Search performance: 245.75 seconds

**Key Insights**:
- **93% ternary**: 28 of 30 connectives are ternary
- Search for size 31 timed out after 5 minutes
- Likely close to theoretical maximum for depth-3 independence
- Demonstrates power of mixed-arity connective sets

**Major Implications**:
- Higher arities provide far more room for independence than binary-only
- Ternary functions enable sets 10× larger than binary-only maximum
- Size 30 represents current state-of-the-art for verified nice sets
- Theoretical upper bound remains an open problem

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

#### Size-30 Nice Set (Current Verified Maximum)
```bash
python -m src.cli prove z3 --target-size 30 --max-depth 3
# Expected: ~245s (~4 minutes)
```

**Note:**
- Enumeration times are consistent (exhaustive search)
- Z3 times and specific sets found may vary between runs
- Maximum sizes should be consistent across all runs

---

## Navigation

- [← Project README](../README.md)
- [CLI Documentation](../src/README.md)
- [Research Reports](../specs/README.md)
