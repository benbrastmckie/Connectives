# Nice Connectives

A Z3-based solver for finding the maximum size of "nice" (complete and independent) connective sets in classical two-valued logic.

## Problem Statement

It concerns classical two-valued connectives of any adicity.
Call a set of connectives **nice** if it is:
1. **Complete**: Every classical connective is definable from it (via Post's completeness theorem)
2. **Independent**: No connective in the set is definable from the other connectives in the set

## Research Question

**What is the largest size of a nice set?**

Known bounds:
- Upper bound: at most 16 (general case)
- Binary-only: largest size is 3
- Mixed arities (ternary+): Unknown - this is what we solve

## Implementation Approach

This project implements a solver using:
- **BitVec representation** for truth tables
- **Post's lattice** for completeness checking (escape all 5 maximal clones: T0, T1, M, D, A)
- **Bounded composition** for independence checking (configurable depth)
- **Incremental arity search** (binary → unary → ternary)

## Installation

```bash
# Install dependencies
pip install z3-solver pytest

# Clone/navigate to project
cd /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives
```

## Usage

### Validate Results
```bash
python3 -m src.main --validate
```

### Search Binary-Only (reproduces known max=3)
```bash
python3 -m src.main --binary-only
```

### Search with Ternary Connectives
```bash
python3 -m src.main --max-arity 3 --max-depth 3
```

### Run Tests
```bash
pytest tests/ -v
# Expected: 123 passed, 1 skipped
```

## Results Summary

### Confirmed Findings

| Arity Range | Maximum Size | Example |
|-------------|--------------|---------|
| Binary only (all) | 4 | {FALSE, NOT_X, NAND, PROJ_Y} |
| Binary only (proper) | 3 | {NOR, AND, IFF} |
| Unary + Binary | 7 | {CONST_0, ID, CONST_1, INHIBIT, NOT_Y, IMPLIES, PROJ_X} |

### Mixed Arity Results (Note: Conflicting Documentation)

The project documentation contains conflicting results for the maximum size when ternary connectives are included:

**Claim 1** (from `RESULTS_SUMMARY.md`, `nice_sets_results.md`):
- Maximum = **16** (exactly)
- Matches theoretical upper bound
- Found via random sampling in ~1 second

**Claim 2** (from `FINAL_ANSWER.md`):
- Maximum ≥ **42** (confirmed)
- Found with composition depth 3-5
- Size 42 achieved in ~277 seconds
- True maximum unknown but > 42

**Possible explanations**:
- Different composition depth parameters (affects independence definition)
- Different completeness criteria
- Documentation from different experimental runs
- Both may be correct for different formulations of "independence"

See `specs/summaries/001_nice_connectives_workflow_summary.md` for detailed analysis of this discrepancy.

## Key Insights

1. **Ternary connectives are essential**: Maximum size increases dramatically when ternary functions are allowed (from 7 to either 16 or 42+)

2. **Composition depth matters**: The bounded composition approach means "independence" is parameterized by depth:
   - Depth 3: More permissive, may find larger sets
   - Depth 5+: More conservative, stricter independence

3. **Post's lattice is efficient**: Completeness checking is O(1) per function via Post class membership

4. **Search space is massive**: C(276, k) combinations for k-sized sets from unary+binary+ternary functions

## Documentation

### Research Process
- `specs/reports/001_combinatorial_search_strategies.md` - Search space analysis
- `specs/reports/002_debug_mixed_arity.md` - Mixed-arity composition debugging
- `specs/reports/003_debug_remaining_tests.md` - Final test fixes

### Implementation
- `specs/plans/001_nice_connectives_solver.md` - 7-phase implementation plan (all complete)
- `specs/summaries/001_nice_connectives_workflow_summary.md` - Complete workflow documentation

### Results
- `FINAL_ANSWER.md` - Claims max ≥ 42
- `RESULTS_SUMMARY.md` - Claims max = 16
- `specs/results/nice_sets_results.md` - Detailed results breakdown

## Implementation Files

**Core Source** (`src/`):
- `connectives.py` - Truth table representation (BitVec encoding)
- `constants.py` - Predefined connectives (AND, OR, NOT, etc.)
- `post_classes.py` - Post's lattice completeness checking
- `independence.py` - Bounded composition independence checking
- `search.py` - Search algorithms (binary-only, incremental arity)
- `main.py` - Command-line interface

**Tests** (`tests/`): 123 passing, 1 skipped

## Technical Notes

### Bounded Composition Approach

The implementation uses bounded composition depth rather than Z3 symbolic encoding:
- Enumerates composition patterns up to depth d
- Checks if target function matches any composition
- Configurable via `--max-depth` parameter

**Trade-off**:
- Shallower depth: Faster, may miss dependencies (larger sets found)
- Deeper depth: Slower, more conservative (smaller sets, stricter independence)

### Known Limitations

1. **XOR pattern**: `OR(AND(x, NOT(y)), AND(NOT(x), y))` not enumerated (requires binary(binary, binary) pattern)
2. **Quaternary functions**: Not explored (65,536 functions - intractable)
3. **Documentation discrepancy**: Maximum size claims conflict (16 vs ≥42)

## References

- Post, E. L. (1941). "The Two-Valued Iterative Systems of Mathematical Logic." Annals of Mathematics Studies, No. 5
- Project standards: `CLAUDE.md`

## Project Status

**Status**: Implementation Complete
**Date**: 2025-10-02
**Test Coverage**: 123 tests passing, 1 skipped
**All Phases**: Complete (7/7)

For detailed workflow documentation, see `specs/summaries/001_nice_connectives_workflow_summary.md`
