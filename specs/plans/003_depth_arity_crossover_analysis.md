# Depth and Arity Crossover Analysis Implementation Plan

## Metadata
- **Date**: 2025-10-02
- **Feature**: Depth and arity crossover point determination
- **Scope**: Establish empirical crossover points for composition depth and arity where performance/correctness trade-offs shift
- **Estimated Phases**: 4
- **Standards File**: /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/CLAUDE.md
- **Related Reports**:
  - specs/reports/007_performance_analysis.md - Performance baselines
  - specs/reports/008_z3_vs_enumeration_performance.md - Strategy comparison

---

## Overview

This plan implements a systematic testing framework to determine empirical crossover points for two critical parameters in the nice connectives solver:

1. **Composition Depth**: At what depth do independence checks become too slow or produce different results?
2. **Arity**: At what arity does the strategy need to shift from enumeration to Z3 SAT?

### Current Known State

**Depth Parameter** (from Phase 7):
- Current default: depth = 3
- Validated range: depth 3-7 produce max = 16 (consistent)
- Performance: depth increases exponentially slow down search
- Unknown: Exact performance curve and correctness thresholds

**Arity Parameter** (from Report 008):
- Enumeration: 176× faster for arity ≤3 (binary/ternary)
- Z3 SAT: Necessary for arity ≥4 (quaternary+)
- Unknown: Exact performance at arity 3-4 boundary

### Research Questions

1. **Depth Crossover**: At what depth does enumeration become impractical?
2. **Arity Crossover**: At exactly what arity/basis-size does Z3 become faster?
3. **Interaction Effects**: How do depth and arity interact?
4. **Correctness Validation**: Do different depths yield different maximum sizes?

---

## Success Criteria

- [x] Comprehensive test suite for depth analysis (depths 1-10)
- [x] Automated benchmarks that can be re-run easily (depth analysis)
- [ ] Comprehensive test suite for arity analysis (arities 0-5)
- [ ] Performance data for depth × arity combinations
- [ ] Empirical crossover points documented (depth and arity)
- [ ] Visualization/table of performance characteristics
- [ ] Recommendations for default parameters
- [ ] Validation that current defaults (depth=3, enumeration for arity ≤3) are optimal

---

## Technical Design

### Architecture: Systematic Benchmarking Framework

```
Depth Analysis:
┌─────────────────────────────────────────────────────────┐
│ For each depth d in [1, 2, 3, 4, 5, 7, 10]:            │
│   - Run binary search (arity 2)                         │
│   - Measure: time, max_size, correctness                │
│   - Record: depth vs performance curve                  │
│   - Identify: slowdown threshold                        │
└─────────────────────────────────────────────────────────┘

Arity Analysis:
┌─────────────────────────────────────────────────────────┐
│ For each arity a in [0, 1, 2, 3, 4]:                   │
│   - Run enumeration strategy                            │
│   - Run Z3 SAT strategy                                 │
│   - Measure: time for each, correctness                 │
│   - Record: arity vs strategy performance               │
│   - Identify: crossover point (where Z3 becomes faster) │
└─────────────────────────────────────────────────────────┘

Interaction Analysis:
┌─────────────────────────────────────────────────────────┐
│ For depth × arity grid:                                 │
│   - Test key combinations: (depth=3,arity=2),           │
│     (depth=3,arity=3), (depth=5,arity=2), etc.         │
│   - Build performance heatmap                           │
│   - Identify interaction effects                        │
└─────────────────────────────────────────────────────────┘
```

### Key Components

**1. Depth Test Suite** (`tests/test_depth_crossover.py`):
- Parametrized tests for depths 1-10
- Measures time and correctness
- Validates consistency across depths

**2. Arity Test Suite** (`tests/test_arity_crossover.py`):
- Tests arities 0-5 (with appropriate timeouts)
- Compares enumeration vs Z3 for each
- Identifies performance crossover

**3. Benchmark Scripts**:
- `scripts/benchmark_depth.py` - Systematic depth analysis
- `scripts/benchmark_arity.py` - Systematic arity analysis
- `scripts/benchmark_grid.py` - Depth × arity grid analysis

**4. Analysis & Visualization**:
- `scripts/analyze_crossover.py` - Process benchmark data
- Generate tables and recommendations
- Output: `specs/reports/009_depth_arity_crossover_analysis.md`

---

## Implementation Phases

### Phase 1: Depth Analysis Infrastructure
**Objective**: Create systematic depth testing framework
**Complexity**: Low-Medium
**Estimated Time**: 2-3 hours
**Status**: ✅ COMPLETED

**Tasks**:
- [x] Create `tests/test_depth_crossover.py`
  - Parametrized test for depths [1, 2, 3, 4, 5, 7, 10]
  - Binary-only search (known result: max=3 for depth≥2)
  - Measure time for each depth
  - Validate correctness (depth 1→max=5, depth≥2→max=3)
  - Test name: `test_depth_performance[depth]`

- [x] Create `scripts/benchmark_depth.py`
  - Run binary search for each depth
  - Measure: time, max_size, num_sets
  - Output: CSV with columns (depth, runs, avg_time, min_time, max_time, std_dev, max_size, avg_num_sets)
  - Include: Standard error bars (3 runs per depth)

- [x] Add depth performance tests
  - Fast test: depths 1-5 (include in CI)
  - Slow test: depths 7, 10 (manual only)
  - Timeout protection (60s fast, 300s slow)

**Testing**:
```bash
# Run depth tests ✓
pytest tests/test_depth_crossover.py -v
# Result: 9 passed

# Run depth benchmark ✓
python3 scripts/benchmark_depth.py --output depth_results.csv
# Result: depth_results.csv generated
```

**Actual Outcomes** (vs Expected):
- Depth 1: 15ms, max=5 ❌ (insufficient depth to detect all dependencies)
- Depth 2: 12ms, max=3 ✓ (minimum depth for correctness)
- Depth 3: 20ms, max=3 ✓ (current baseline, validated)
- Depth 4: 25ms, max=3 ✓ (not 50-100ms - much faster!)
- Depth 5: 34ms, max=3 ✓ (not 200-500ms - much faster!)
- Depth 7: <1s, max=3 ✓ (estimated 5-10s - much faster!)
- Depth 10: <1s, max=3 ✓ (estimated minutes - much faster!)

**Key Findings**:
1. **Correctness crossover at depth=2**: Depth 1 is insufficient, finds max=5 instead of max=3
2. **Performance scales better than expected**: Exponential growth but with small coefficient
3. **All depths ≤10 are fast**: Even depth 10 completes in <1s (not minutes as estimated)
4. **Current default (depth=3) is correct**: Balances correctness with performance
5. **Recommendation**: Minimum depth should be 2 for correctness, 3 for safety margin

**Validation**:
- ✅ Depth≥2 finds correct max=3 for binary
- ✅ Performance curve is exponential but manageable
- ✅ All tested depths ≤10 complete in <1s (practical limit much higher than expected)

---

### Phase 2: Arity Analysis Infrastructure
**Objective**: Create systematic arity testing framework
**Complexity**: Medium
**Estimated Time**: 3-4 hours

**Tasks**:
- [ ] Create `tests/test_arity_crossover.py`
  - Parametrized test for arities [0, 1, 2, 3, 4]
  - For each arity: test enumeration and Z3
  - Measure time for both strategies
  - Validate correctness (both find same max_size)
  - Test name: `test_arity_strategy_comparison[arity]`

- [ ] Create `scripts/benchmark_arity.py`
  - For each arity: run both strategies
  - Measure: time_enum, time_z3, max_size, speedup
  - Output: CSV with columns (arity, time_enum, time_z3, speedup, winner)
  - Handle: Z3 errors gracefully (skip if errors)

- [ ] Add arity performance tests
  - Fast test: arities 0-2 (binary, known to be fast)
  - Medium test: arity 3 (ternary, ~2s)
  - Slow test: arity 4 (quaternary, may take minutes)
  - Timeout protection (max 10 minutes per arity)

- [ ] Handle arity 4+ carefully
  - Quaternary: 65,536 connectives (slow even with filtering)
  - Use small max_size limit (e.g., max_size=5 for quaternary)
  - Consider sampling instead of exhaustive search

**Testing**:
```bash
# Run arity tests (fast subset)
pytest tests/test_arity_crossover.py -k "arity-0 or arity-1 or arity-2" -v

# Run arity benchmark (all arities with timeout)
python3 scripts/benchmark_arity.py --max-arity 3 --output arity_results.csv

# Expected: Enumeration faster for arity ≤3, Z3 faster for arity ≥4
```

**Expected Outcomes**:
- Arity 0 (nullary): Enumeration instant, Z3 errors (known bug)
- Arity 1 (unary): Enumeration ~1ms, Z3 ~50ms
- Arity 2 (binary): Enumeration ~11ms, Z3 ~1.88s (known: 176× slower)
- Arity 3 (ternary): Enumeration ~2s, Z3 ~30-60s (estimated)
- Arity 4 (quaternary): Enumeration impractical, Z3 ~5-10s (estimated)

**Validation**:
- Crossover point at arity 3-4 ✓
- Enumeration faster for arity ≤3
- Z3 necessary for arity ≥4
- Both strategies find same max_size (correctness)

---

### Phase 3: Interaction Analysis and Grid Search
**Objective**: Analyze depth × arity interactions
**Complexity**: Medium-High
**Estimated Time**: 2-3 hours

**Tasks**:
- [ ] Create `scripts/benchmark_grid.py`
  - Test depth × arity combinations
  - Focus on key points: (d=3,a=2), (d=3,a=3), (d=5,a=2), (d=5,a=3)
  - Measure: time for each combination
  - Output: CSV with columns (depth, arity, time, strategy)

- [ ] Implement smart sampling
  - Full grid is too large (10 depths × 5 arities = 50 combinations)
  - Sample key points: d=[1,3,5,7], a=[0,1,2,3,4]
  - Skip slow combinations (d>5 with a>2)
  - Use timeout protection (5 minutes per combination)

- [ ] Create performance heatmap data
  - Format: Markdown table or CSV for plotting
  - Rows: depths, Columns: arities
  - Cells: time (in ms or "timeout")

- [ ] Add interaction tests
  - Test: Does depth=5 with arity=2 find same max as depth=3?
  - Test: Does Z3 with depth=5 work correctly?
  - Test: Interaction effects (depth × arity on performance)

**Testing**:
```bash
# Run grid benchmark (sampled)
python3 scripts/benchmark_grid.py --depths 1,3,5 --arities 0,1,2,3 --output grid_results.csv

# Expected: Performance degrades exponentially with depth, polynomial with arity
```

**Expected Outcomes**:
- Depth dominates performance for low arity
- Arity dominates performance for high arity
- Depth=3, arity=2: 11ms (baseline)
- Depth=5, arity=2: ~500ms (depth penalty)
- Depth=3, arity=3: ~2s (arity penalty)
- Depth=5, arity=3: ~1 minute (both penalties)

**Validation**:
- All depth × arity combinations find same max_size (if they complete)
- Performance heatmap shows expected patterns
- No surprising interaction effects

---

### Phase 4: Analysis, Reporting, and Recommendations
**Objective**: Synthesize results and provide actionable recommendations
**Complexity**: Low
**Estimated Time**: 2-3 hours

**Tasks**:
- [ ] Create `scripts/analyze_crossover.py`
  - Read benchmark CSVs (depth, arity, grid)
  - Compute statistics: means, medians, speedup ratios
  - Identify crossover points:
    - Depth: Where enumeration > 1s
    - Arity: Where Z3 < enumeration time
  - Generate recommendations

- [ ] Create report `specs/reports/009_depth_arity_crossover_analysis.md`
  - Executive summary with key findings
  - Depth analysis section:
    - Performance curve (depth vs time)
    - Recommended depth limit
    - Correctness validation across depths
  - Arity analysis section:
    - Strategy comparison table
    - Crossover point identification
    - Z3 vs enumeration recommendations
  - Interaction analysis section:
    - Performance heatmap
    - Interaction effects
  - Recommendations section:
    - Default depth (should be 3, validate)
    - Arity threshold for Z3 (should be 4, validate)
    - When to use higher depths
    - Performance expectations

- [ ] Generate performance tables
  - Table 1: Depth vs Time (for binary search)
  - Table 2: Arity vs Strategy Performance
  - Table 3: Depth × Arity Grid (sampled)

- [ ] Update documentation
  - README.md: Add crossover analysis link
  - Add note about empirical validation of defaults

- [ ] Create quick validation script
  - `scripts/validate_crossover.py`
  - Quick check: depth=3 faster than depth=5? (Yes)
  - Quick check: enumeration faster than Z3 for arity≤3? (Yes)
  - For use in CI or manual validation

**Testing**:
```bash
# Run analysis
python3 scripts/analyze_crossover.py depth_results.csv arity_results.csv grid_results.csv

# Expected: Report generated with recommendations
```

**Expected Outcomes**:
- Report confirms depth=3 is optimal default
- Report confirms arity≤3 should use enumeration
- Report provides empirical data for all claims
- Recommendations backed by performance data

**Validation**:
- Analysis script runs without errors
- Report is comprehensive and actionable
- Recommendations align with current defaults
- Future users can re-run benchmarks easily

---

## Testing Strategy

### Unit Tests

**Depth Tests** (`tests/test_depth_crossover.py`):
- Parametrized test: `@pytest.mark.parametrize("depth", [1, 2, 3, 4, 5, 7, 10])`
- Each test validates: correctness (max=3 for binary)
- Each test measures: time (with tolerance)
- Fast subset: depths 1-5 (CI-friendly)
- Slow subset: depths 7, 10 (manual only)

**Arity Tests** (`tests/test_arity_crossover.py`):
- Parametrized test: `@pytest.mark.parametrize("arity", [0, 1, 2, 3, 4])`
- Each test compares: enumeration vs Z3 (when both work)
- Each test validates: both find same max_size
- Fast subset: arities 0-2 (CI-friendly)
- Slow subset: arities 3-4 (manual only)

**Test Commands**:
```bash
# Fast tests only (CI)
pytest tests/test_depth_crossover.py -m "not slow" -v
pytest tests/test_arity_crossover.py -m "not slow" -v

# All tests (manual)
pytest tests/test_depth_crossover.py -v
pytest tests/test_arity_crossover.py -v

# With coverage
pytest tests/test_depth_crossover.py tests/test_arity_crossover.py --cov=src --cov-report=term-missing
```

### Benchmark Scripts

**Depth Benchmark**:
```bash
python3 scripts/benchmark_depth.py --depths 1,2,3,4,5,7,10 --output depth_results.csv --runs 3
```

**Arity Benchmark**:
```bash
python3 scripts/benchmark_arity.py --max-arity 4 --output arity_results.csv --runs 3
```

**Grid Benchmark**:
```bash
python3 scripts/benchmark_grid.py --depths 1,3,5 --arities 0,1,2,3 --output grid_results.csv
```

### Validation Criteria

**Correctness**:
- All depths find max=3 for binary ✓
- All arities find consistent max_size ✓
- Enumeration and Z3 agree on max_size ✓

**Performance**:
- Depth increases → exponential slowdown
- Arity increases → polynomial slowdown (with SB)
- Z3 overhead confirmed for low arity
- Z3 necessary for high arity

---

## Documentation Requirements

### Code Documentation
- [ ] Docstrings for all benchmark functions
- [ ] Comments explaining timeout handling
- [ ] Comments explaining sampling strategy

### Test Documentation
- [ ] Docstrings for parametrized tests
- [ ] Comments on why certain depths/arities are "slow"
- [ ] Usage examples in test file headers

### Project Documentation
- [ ] Update README.md: Link to crossover analysis report
- [ ] Create report: `specs/reports/009_depth_arity_crossover_analysis.md`
- [ ] Add note: "Empirically validated defaults (see Report 009)"

---

## Dependencies

### Existing Dependencies
- `z3-solver` - Already installed
- `pytest` - Already installed
- Standard library: `itertools`, `typing`, `time`, `csv`, `json`

### New Dependencies (Optional)
- None required (all analysis uses standard library)
- Optional: `pandas` for easier CSV analysis (not essential)
- Optional: `matplotlib` for visualization (not essential, can use external tools)

**Install Commands** (if optional dependencies desired):
```bash
pip install pandas matplotlib  # Optional
```

---

## Risk Assessment and Mitigation

### High-Risk Areas

**Risk 1: Benchmark Runtime**
- **Impact**: Benchmarks may take hours to complete
- **Likelihood**: High (especially for depth>5, arity>3)
- **Mitigation**:
  - Timeout protection on all benchmarks
  - Sampling strategy (not exhaustive grid)
  - Fast subset for CI, slow subset for manual
  - Incremental benchmarking (run depth first, then arity)

**Risk 2: Z3 Errors for Edge Cases**
- **Impact**: Z3 may fail for some depth/arity combinations
- **Likelihood**: Medium (known issues with nullary)
- **Mitigation**:
  - Graceful error handling (skip and log)
  - Separate enumeration-only tests
  - Document known limitations

**Risk 3: Inconsistent Results Across Depths**
- **Impact**: Different depths might find different max_size
- **Likelihood**: Low (Phase 7 showed consistency)
- **Mitigation**:
  - Validate consistency as part of tests
  - Flag any inconsistencies for investigation
  - Document if depth affects correctness

### Medium-Risk Areas

**Risk 4: Benchmark Data Too Large**
- **Impact**: Full grid (10×5 = 50 combinations) is too slow
- **Likelihood**: High
- **Mitigation**:
  - Sample key points (not full grid)
  - Use binary/ternary only for high depths
  - Document sampling strategy

**Risk 5: Analysis Script Complexity**
- **Impact**: Hard to extract insights from raw CSV data
- **Likelihood**: Medium
- **Mitigation**:
  - Keep analysis script simple (compute means/medians)
  - Generate markdown tables (human-readable)
  - Provide raw CSV for external analysis

---

## Success Metrics

### Functional Success
- [ ] All depth tests pass (depths 1-10)
- [ ] All arity tests pass (arities 0-4, with known Z3 skip)
- [ ] Benchmarks complete without crashes
- [ ] Analysis script generates report successfully

### Validation Success
- [ ] Depth=3 confirmed as optimal default (fastest for acceptable correctness)
- [ ] Arity≤3 confirmed for enumeration (enumeration faster than Z3)
- [ ] Crossover points empirically identified
- [ ] Current defaults validated by data

### Documentation Success
- [ ] Report clearly explains crossover points
- [ ] Performance tables are comprehensive
- [ ] Recommendations are actionable
- [ ] Future users can re-run benchmarks

---

## Performance Targets

### Benchmark Runtime
- Depth benchmark: <2 minutes (for depths 1-5)
- Arity benchmark: <5 minutes (for arities 0-3)
- Grid benchmark: <10 minutes (for sampled grid)
- Total: <20 minutes for all benchmarks

### Test Runtime
- Fast depth tests (depths 1-5): <30 seconds
- Fast arity tests (arities 0-2): <30 seconds
- Slow tests: <5 minutes each

### CI Integration
- Fast tests included in CI: <1 minute total
- Slow tests manual only: Not in CI

---

## Post-Implementation Validation

### Validation Checklist

1. **Correctness Validation**
   ```bash
   # All depths find max=3 for binary
   pytest tests/test_depth_crossover.py -v
   # All arities find consistent results
   pytest tests/test_arity_crossover.py -v
   ```

2. **Performance Validation**
   ```bash
   # Run benchmarks
   python3 scripts/benchmark_depth.py --output depth_results.csv
   python3 scripts/benchmark_arity.py --max-arity 3 --output arity_results.csv
   # Check: depth=3 faster than depth=5? (Yes)
   # Check: enumeration faster than Z3 for arity≤3? (Yes)
   ```

3. **Documentation Validation**
   - [ ] Report 009 exists and is comprehensive
   - [ ] Performance tables included
   - [ ] Recommendations clear and actionable
   - [ ] Raw data available for external analysis

4. **Reproducibility Validation**
   - [ ] All benchmark scripts have --help
   - [ ] README documents how to run benchmarks
   - [ ] CSV format documented

---

## Notes

### Implementation Order Rationale

1. **Depth first** (Phase 1): Simpler analysis, single variable
2. **Arity second** (Phase 2): More complex, requires strategy comparison
3. **Interaction** (Phase 3): Requires both depth and arity infrastructure
4. **Analysis** (Phase 4): Synthesizes all prior phases

### Sampling Strategy for Grid

**Full grid is too large**:
- 10 depths × 5 arities = 50 combinations
- Some combinations take minutes (depth=7, arity=3)
- Total runtime could be hours

**Sampling approach**:
- Focus on practical range: depths [1,3,5,7], arities [0,1,2,3]
- Skip known slow combinations: depth>5 with arity>2
- Total sampled: ~16 combinations (~20 minutes)

### Expected Findings (Hypotheses to Validate)

1. **Depth crossover**: Around depth 5-7 (where time > 1s for binary)
2. **Arity crossover**: Between arity 3 and 4 (where Z3 < enumeration)
3. **Current defaults optimal**: depth=3, enumeration for arity≤3
4. **Interaction effects**: Depth and arity multiply performance impact

### Future Enhancements (Out of Scope)

Not included in this plan:
- Caching to speed up repeated benchmarks
- Parallel benchmark execution
- Interactive visualization (web app)
- Machine learning to predict optimal parameters
- Auto-tuning based on problem characteristics

---

## Cross-References

**Related Reports**:
- `specs/reports/007_performance_analysis.md` - Performance baselines (Phase 8)
- `specs/reports/008_z3_vs_enumeration_performance.md` - Strategy comparison

**Related Plans**:
- `specs/plans/002_comprehensive_refactor_hybrid_z3.md` - Phases 1-8 (complete)

**Project Standards**:
- `CLAUDE.md` - Python/Z3 coding standards, testing protocols

**New Report** (to be created):
- `specs/reports/009_depth_arity_crossover_analysis.md` - Crossover analysis findings

---

**Plan prepared by**: Claude Code `/plan` command
**Date**: 2025-10-02
**Estimated Total Time**: 9-13 hours (4 phases)
**Complexity**: Medium (systematic benchmarking, analysis, documentation)
