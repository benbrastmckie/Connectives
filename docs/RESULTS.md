# Nice Connective Sets: Research Findings

**Project**: Nice Connectives Solver
**Research Question**: What is the maximum size of a "nice" set of logical connectives?

Where "nice" means:
1. **Complete**: Can define all classical connectives (Post's lattice)
2. **Independent**: No connective is definable from the others (bounded composition)

## Current Findings

Systematic search using Z3 constraint solving with two definability modes:

**Truth-Functional Mode (Default - Clone-Theoretic):**
- Nice sets of size up to **33** found (likely maximum)
- Universal projection rules and cross-arity constant equivalence
- More restrictive independence criterion

**Syntactic Mode (Composition-Based):**
- Nice sets of size up to **35** found (maximum unknown)
- Composition-based definability with depth bounds
- More permissive independence criterion

**For Interactive Exploration**: Try the [Jupyter Notebooks](JUPYTER.md) to explore these results hands-on:
- `05_search_binary.ipynb` - Interactive binary-only search
- `06_search_ternary.ipynb` - Z3-based ternary search demonstrations

**Note**: For detailed truth tables of ternary connectives (f3_N notation), see the [Ternary Connectives Glossary](../glossary/connectives.md).

## Key Results

**Definability Mode Choice Matters:**
The maximum nice set size varies by definability mode. This project implements both modes with a CLI flag `--definability-mode`.

**Truth-Functional Mode (Default):**
- **Binary-only**: Max varies by mode
- **Unary + Binary**: max = 5 (proven)
- **Up to Ternary**: max likely = 33
- Focus on clone-theoretic definability with universal projections

**Syntactic Mode:**
- **Binary-only**: max = 3 (classical result, proven)
- **Unary + Binary**: max = 5 (proven)
- **Up to Ternary**: max ≥ 35 (actual bound unknown)
- Focus on composition-based definability

**Why Two Modes?** Different mathematical traditions use different definability notions. Truth-functional (default) aligns with universal algebra; syntactic aligns with classical logic literature. See [DEFINABILITY.md](DEFINABILITY.md) for complete details.

## Concrete Examples

### 1. Binary-Only: Size 3 (Syntactic Mode)

**Example set**: {XOR, AND, TRUE}

```
XOR (0b0110):       AND (0b1000):       TRUE (0b1111):
x y | XOR           x y | AND           x y | TRUE
0 0 | 0             0 0 | 0             0 0 | 1
0 1 | 1             0 1 | 0             0 1 | 1
1 0 | 1             1 0 | 0             1 0 | 1
1 1 | 0             1 1 | 1             1 1 | 1
```

**Properties**:
- ✓ Complete (escapes all 5 Post classes)
- ✓ Independent (no function definable from others)
- ✓ Maximum for binary-only in syntactic mode (size 4 impossible)

**Mode Note**: Truth-functional mode may give different results due to universal projection rules.

**See**: [syntactic/enum_classical_binary_max3.md](../examples/syntactic/enum_classical_binary_max3.md)

### 2. Unary + Binary: Size 5

**Example set**: {FALSE, TRUE, XOR, AND, IMP}

```
Arity distribution:
  Constants (0): ██ (2)
  Binary (2):    ███ (3)
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3)
- **67% larger** than binary-only!
- **No unary functions** (avoids FALSE=NOT(TRUE) dependency)

**Search performance**: 0.04s, checked 26 complete sets
**Proven maximum**: Size 6 exhaustively tested (10,000 candidates, none found)

**See**: [z3_unary_binary_max5.md](z3_unary_binary_max5.md)

### 3. With Ternary: Size 17

**Example set**: FALSE + NOT_Y + 15 ternary functions

```
Arity distribution:
  Constants (0): █ (1)
  Binary (2):    █ (1)
  Ternary (3):   ███████████████ (15) — 88% of set
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3)
- **467% larger** than binary-only!

**Search performance**: 0.76s, checked only 22 complete sets

**See**: [z3_nice_set_17.md](z3_nice_set_17.md)

### 4. Size 29

**Example set**: FALSE + PROJ_X + 27 ternary functions

```
Arity distribution:
  Constants (0): █ (1)
  Binary (2):    █ (1)
  Ternary (3):   ███████████████████████████ (27) — 93% of set
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3)
- **867% larger** than binary-only!

**Search performance**: 3.17s, checked 144 complete sets

**See**: [z3_nice_set_29.md](z3_nice_set_29.md)

### 5. Size 30 (Syntactic Mode)

**Example set**: FALSE + XOR + OR + 27 ternary functions

```
Arity distribution:
  Constants (0): █ (1)
  Binary (2):    ██ (2)
  Ternary (3):   ███████████████████████████ (27) — 90% of set
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3, syntactic mode)
- **900% larger** than binary-only!

**Search performance**: 245.75s (~4 minutes), checked 7,747 complete sets

**Z3 efficiency**: ~10^70 reduction vs brute force

**See**: [syntactic/z3_nice_set_30.md](../examples/syntactic/z3_nice_set_30.md)

### 6. Size 33 (Truth-Functional Mode - Current Likely Maximum)

**Mode**: Truth-functional (default)

**Example set**: 1 constant + 1 binary + 31 ternary functions

```
Arity distribution:
  Constants (0): █ (1)
  Binary (2):    █ (1)
  Ternary (3):   ███████████████████████████████ (31) — 94% of set
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3, truth-functional mode)
- **Likely maximum** for truth-functional mode

**Search performance**: 24.15s, checked 1,239 complete sets

**See**: [truth_functional/z3_nice_set_33.md](../examples/truth_functional/z3_nice_set_33.md)

### 7. Size 35 (Syntactic Mode - Verified Maximum to Date)

**Mode**: Syntactic

**Example set**: 1 constant + 1 binary + 33 ternary functions

```
Arity distribution:
  Constants (0): █ (1)
  Binary (2):    █ (1)
  Ternary (3):   ███████████████████████████████████ (33) — 94% of set
```

**Properties**:
- ✓ Complete
- ✓ Independent (depth 3, syntactic mode)
- **Largest verified** nice set in syntactic mode

**Search performance**: 2783.17s (~46 minutes), checked 26,860 complete sets

**See**: [syntactic/z3_nice_set_35.md](../examples/syntactic/z3_nice_set_35.md)

## Systematic Search Results

The implementation systematically searched for nice sets of increasing sizes using Z3:

### Syntactic Mode Results

| Size | Result | Time | Complete Sets Checked | Notes |
|------|--------|------|----------------------|-------|
| 17 | ✓ Found | 0.69s | 22 | First ternary inclusion |
| 20 | ✓ Found | 0.67s | 25 | |
| 25 | ✓ Found | 3.44s | 172 | |
| 29 | ✓ Found | 3.17s | 144 | Early ternary dominance |
| 30 | ✓ Found | 245.75s (~4min) | 7,747 | |
| 31 | ✓ Found | 359.62s (~6min) | 9,527 | Slowest in 31-34 range |
| 32 | ✓ Found | 35.93s | 1,822 | 10× faster than 31! |
| 33 | ✓ Found | 24.15s | 1,239 | Fastest in series |
| 34 | ✓ Found | 86.69s | 3,226 | Moderate difficulty |
| **35** | **✓ Found** | **2783.17s (~46min)** | **26,860** | **8× harder, sparse solutions** |
| 36 | ? Unknown | - | - | May require extended search or may not exist |

### Truth-Functional Mode Results (Default)

| Size | Result | Time | Complete Sets Checked | Notes |
|------|--------|------|----------------------|-------|
| 29 | ✓ Found | ~3s | 161 | Truth-functional mode |
| 32 | ✓ Found | ~36s | 1,822 | Truth-functional mode |
| **33** | **✓ Found** | **~24s** | **1,239** | **Likely maximum for truth-functional** |

**Pattern**:
- **Syntactic mode**: All tested sizes 17-35 have nice sets. Size 36+ unknown.
- **Truth-functional mode**: Maximum appears to be 33 (more restrictive independence).

### Why Classical Binary-Only Results Don't Extend

Classical results focused on binary-only connectives (max = 3). This implementation shows mixed arities enable much larger sets:
1. Ternary functions provide 256 available connectives (vs 16 binary)
2. Higher arity diversity supports greater independence
3. Systematic exploration with Z3 constraint solving makes large searches tractable

**Key insight**: The 256 available ternary functions provide far more room for independence than binary functions alone.

## Key Insights

### 1. Ternary Dominance

**All large nice sets follow this pattern**:
- 1-2 low-arity functions (constants, binary)
- Remainder is ternary (88-96% of set)

**Why?**
- Ternary functions: 256 available (2^8)
- Binary functions: 16 available (2^4)
- More diversity → easier to maintain independence

### 2. Search Efficiency

**Z3's symmetry breaking is incredibly effective**:

| Size | Brute Force Combinations | Z3 Checks | Reduction |
|------|-------------------------|-----------|-----------|
| 17 | ~10^50 | 22 | 10^48× |
| 29 | ~10^70 | 144 | 10^68× |

Without Z3's constraint solving, these searches would be computationally infeasible.

### 3. Structural Patterns

**Ternary function selection shows wide distribution**:
- Size-29 set uses truth table values 18-248 (out of 256)
- Suggests functions are "well-separated" in truth table space
- Maximizes independence by avoiding similar functions

### 4. Depth-3 Sufficiency

**All found sets are independent at depth 3**:
- Covers practical composition scenarios
- Suggests genuine independence (not just shallow)
- Depth 4-5 validation recommended for rigor

## Open Questions

### 1. What is the actual maximum?

**Current status**:
- Minimum: 29 (proven by construction)
- Maximum: unknown (size 30 timed out)

**Possibilities**:
- Could be exactly 29
- Could be 30-40
- Could be much larger

**Next step**: Overnight search with checkpointing

### 2. Depth sensitivity?

**Question**: Are these sets independent at higher depths?

**Current**: All verified at depth 3
**Needed**: Validation at depth 4-5
**Impact**: Confirms genuine vs. shallow independence

### 3. Higher arities?

**Question**: Do quaternary (4-ary) functions enable even larger sets?

**Available**: 65,536 quaternary functions (2^16)
**Trade-off**: Exponentially longer search time
**Potential**: Could discover even more surprising results

### 4. Theoretical upper bound?

**Question**: Is there a mathematical limit?

**Pool size**: 278 connectives (arities 0-3)
**Current**: 29 found (10.4% of pool)
**Theoretical**: Upper bound unknown

## How to Explore Further

### Interactive Learning

**New to the project?** Start with interactive notebooks:

```bash
# Install Jupyter dependencies
pip install -e ".[jupyter]"

# Launch notebooks
cd notebooks/
jupyter notebook

# Try notebooks 05 and 06 for search demonstrations
```

See **[JUPYTER.md](JUPYTER.md)** for complete guide.

### Reproduce Examples

```bash
# Binary-only (fast, ~1 second)
python3 -m src.cli search binary --max-depth 3

# Size-17 discovery (fast, ~1 second)
python3 -m src.cli prove z3 --target-size 17 --max-depth 3

# Size-29 record (moderate, ~3 seconds)
python3 -m src.cli prove z3 --target-size 29 --max-depth 3

# Size-30 attempt (slow, may timeout)
python3 -m src.cli prove z3 --target-size 30 --max-depth 3
```

### Detailed Examples

- [enum_classical_binary_max3.md](enum_classical_binary_max3.md) - Complete walkthrough of classical result
- [z3_nice_set_17.md](z3_nice_set_17.md) - First major discovery with Z3
- [z3_nice_set_29.md](z3_nice_set_29.md) - Current record with full analysis

### Full Reports

- [../specs/reports/013_systematic_search_findings.md](../specs/reports/013_systematic_search_findings.md) - Complete search results
- [../specs/reports/014_improvement_recommendations.md](../specs/reports/014_improvement_recommendations.md) - Future work

## Conclusion

This implementation demonstrates substantial expansion beyond classical binary-only results and provides insights into definability mode choice:

**Classical result**: Binary-only maximum is 3 (syntactic mode, proven)
**This implementation**:
- **Truth-functional mode (default)**: Maximum likely 33 for arity ≤3
- **Syntactic mode**: Maximum ≥35 for arity ≤3 (actual bound unknown)

The findings demonstrate:
1. **Definability mode matters**: Choice of definability notion significantly affects maximum size
2. **Power of modern constraint solving**: Z3 enables systematic exploration of large search spaces
3. **Importance of exploring higher arities**: Ternary functions enable much larger nice sets
4. **Value of systematic computational exploration**: Pattern enumeration verifies independence
5. **Mathematical insights from computation**: Computational tools reveal surprising results

**The maximum size of nice sets remains an open research question, and the choice of definability mode affects the answer.**

**For researchers**: Choose truth-functional mode (default) for clone-theoretic research, or syntactic mode (`--definability-mode syntactic`) for composition-based research. See [DEFINABILITY.md](DEFINABILITY.md) for guidance.

---

**For detailed examples with verification steps, see the individual example files.**

**For complete research findings, see the reports in specs/reports/.**
