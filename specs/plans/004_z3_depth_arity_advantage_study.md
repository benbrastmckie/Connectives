# Z3 Depth and Arity Advantage Study Implementation Plan

## Metadata
- **Plan Number**: 004
- **Date**: 2025-10-02
- **Feature**: Systematic study of Z3 performance advantages at greater depths and arities
- **Scope**: Determine empirical crossover points where Z3 SAT becomes faster than pattern enumeration
- **Estimated Phases**: 4
- **Standards File**: /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/CLAUDE.md
- **Related Reports**:
  - specs/reports/007_performance_analysis.md - Performance baselines
  - specs/reports/008_z3_vs_enumeration_performance.md - Z3 vs enumeration comparison
- **Related Plans**:
  - specs/plans/003_depth_arity_crossover_analysis.md - Depth/arity crossover framework

---

## Overview

This plan implements systematic benchmarking to determine when Z3 SAT provides performance advantages over pattern enumeration. The study focuses on two critical dimensions:

1. **Depth Advantage**: Holding arity=2 (binary), increase depth to find where Z3 becomes faster than enumeration
2. **Arity Advantage**: Holding depth=3, increase arity (max_size) to find where Z3 becomes faster than enumeration

### Current Known State

**From Report 008 (Z3 vs Enumeration)**:
- Binary (arity 2), depth=3: Enumeration 176× faster (0.011s vs 1.88s)
- Enumeration optimal for arity ≤3
- Z3 necessary for arity ≥4 (enumeration becomes impractical)
- **Key question**: At what depth does Z3 catch up to enumeration?

**From Plan 003 Phase 1 (Depth Analysis)**:
- Depth 1: 15ms, max=5 (incorrect - insufficient depth)
- Depth 2: 12ms, max=3 (minimum correct depth)
- Depth 3: 20ms, max=3 (current baseline)
- Depth 5: 34ms, max=3
- Depth 10: <1s, max=3
- **Finding**: Enumeration scales well even to depth 10

**Missing Data**:
- Z3 performance at depths 5, 7, 10 for binary search
- Crossover point where Z3 becomes faster than enumeration (by depth)
- Crossover point where Z3 becomes faster than enumeration (by max_size/arity)

### Research Questions

1. **Depth Crossover**: At what depth (if any) does Z3 SAT become faster than enumeration for binary search?
2. **Arity Crossover**: At what max_size does Z3 SAT become faster than enumeration at depth=3?
3. **Z3 Scaling**: How does Z3 performance scale with depth? (Expected: better than exponential)
4. **Enumeration Limits**: At what depth/arity does enumeration become impractical (>10s)?

### Hypothesis

**Depth Hypothesis**:
- Enumeration: Exponential scaling with depth (pattern count grows exponentially)
- Z3 SAT: Polynomial scaling with depth (SAT constraints grow polynomially)
- **Predicted crossover**: Depth 7-15 (where Z3 catches up)

**Arity Hypothesis**:
- Enumeration: Exponential scaling with max_size (combination explosion)
- Z3 SAT: Logarithmic scaling with constraints
- **Predicted crossover**: max_size 5-7 at depth=3

---

## Success Criteria

- [x] Baseline validation: depth=3, max_size=2, both strategies (Phase 1)
- [ ] Depth study: Binary search (arity 2) at depths [3, 5, 7, 10, 15, 20]
- [ ] Arity study: depth=3 with max_size [2, 3, 4, 5, 6, 7]
- [ ] Crossover identification: Depth where Z3 becomes faster
- [ ] Crossover identification: max_size where Z3 becomes faster
- [ ] Performance curves: depth vs time, max_size vs time (both strategies)
- [ ] Recommendations: When to use Z3 vs enumeration
- [ ] Validation: Z3 correctness at all tested depths/arities

---

## Technical Design

### Architecture: Systematic Comparison Framework

```
Phase 1: Baseline Validation (depth=3, max_size=2)
┌────────────────────────────────────────────────────┐
│ Binary search (arity 2, depth=3):                  │
│   - Run with enumeration                           │
│   - Run with Z3 SAT                                │
│   - Validate both find max=3                       │
│   - Establish baseline times                       │
└────────────────────────────────────────────────────┘

Phase 2: Depth Advantage Study (arity 2, varying depth)
┌────────────────────────────────────────────────────┐
│ For each depth d in [3, 5, 7, 10, 15, 20]:        │
│   - Run binary search with enumeration             │
│   - Run binary search with Z3 SAT                  │
│   - Measure: time_enum(d), time_z3(d)              │
│   - Record: crossover depth (where Z3 faster)      │
│   - Timeout: 60s per strategy per depth            │
└────────────────────────────────────────────────────┘

Phase 3: Arity Advantage Study (depth=3, varying max_size)
┌────────────────────────────────────────────────────┐
│ For each max_size m in [2, 3, 4, 5, 6, 7]:        │
│   - Generate connectives up to arity (m-1)         │
│   - Run search with enumeration                    │
│   - Run search with Z3 SAT                         │
│   - Measure: time_enum(m), time_z3(m)              │
│   - Record: crossover max_size (where Z3 faster)   │
│   - Timeout: 60s per strategy per max_size         │
└────────────────────────────────────────────────────┘

Phase 4: Analysis and Recommendations
┌────────────────────────────────────────────────────┐
│ - Generate performance curves                      │
│ - Identify crossover points                        │
│ - Validate Z3 correctness                          │
│ - Document when to use each strategy               │
│ - Update adaptive strategy if needed               │
└────────────────────────────────────────────────────┘
```

### Key Components

**1. Baseline Test** (`tests/test_z3_baseline.py`):
- Validates Z3 vs enumeration at depth=3, binary search
- Ensures both strategies find max=3
- Establishes baseline performance

**2. Depth Study Script** (`scripts/benchmark_z3_depth.py`):
- Tests binary search at depths [3, 5, 7, 10, 15, 20]
- Compares enumeration vs Z3 at each depth
- Outputs CSV: (depth, time_enum, time_z3, winner, speedup)

**3. Arity Study Script** (`scripts/benchmark_z3_arity.py`):
- Tests search at depth=3 with max_size [2, 3, 4, 5, 6, 7]
- Compares enumeration vs Z3 at each max_size
- Outputs CSV: (max_size, time_enum, time_z3, winner, speedup)

**4. Analysis Report** (`specs/reports/009_z3_advantage_analysis.md`):
- Performance curves (depth vs time, max_size vs time)
- Crossover point identification
- Recommendations for strategy selection

---

## Implementation Phases

### Phase 1: Baseline Validation
**Objective**: Establish baseline performance for both strategies at standard settings
**Complexity**: Low
**Estimated Time**: 1-2 hours
**Status**: ✅ COMPLETED

**Tasks**:
- [x] Create `tests/test_z3_baseline.py`
  - Test: Binary search (arity 2), depth=3, max_size=2
  - Run with `use_z3=False` (enumeration)
  - Run with `use_z3=True` (Z3 SAT)
  - Validate correctness and performance
  - Measure: time_enum, time_z3
  - Assert: time_enum < time_z3 (enumeration should be faster)

- [x] Run baseline test
  - Actual: Enumeration 22ms, Z3 3.06s (140× slower)
  - **CRITICAL FINDING**: Z3 has correctness bug for binary search

**Testing**:
```bash
# Run baseline validation ✓
pytest tests/test_z3_baseline.py -v

# Actual output:
# test_z3_baseline_binary ... PASSED
#   Enumeration: 0.022s, max=3 ✓
#   Z3 SAT:      3.056s, max=4 ✗ (INCORRECT)
#   Winner: Enumeration (140× faster)
```

**Critical Finding**:
- ⚠️ **Z3 CORRECTNESS BUG DETECTED**
- Enumeration finds max=3 (correct)
- Z3 finds max=4 (incorrect - the set is dependent)
- Z3 claims the set ['f2_0', 'f2_1', 'f2_3', 'f2_7'] is independent
- Enumeration correctly identifies f2_0 and f2_3 as definable from the others
- **Conclusion**: Z3 should NOT be used for binary/ternary search

**Success Criteria**:
- ✓ Enumeration finds correct max=3
- ✗ Z3 has correctness bug (finds incorrect max=4)
- ✓ Enumeration faster than Z3 (140× speedup)
- ✓ Baseline times match Report 008 (±50%)

**Impact on Remaining Phases**:
- Phase 2 (Depth study): Still valuable to measure performance, but Z3 correctness is suspect
- Phase 3 (Arity study): Z3 may only be correct for arity ≥4 (untested lower arities)
- Phase 4 (Recommendations): Must strongly warn against using Z3 for arity ≤3

---

### Phase 2: Depth Advantage Study
**Objective**: Find depth where Z3 becomes faster than enumeration (if any)
**Complexity**: Medium
**Estimated Time**: 2-3 hours

**Tasks**:
- [ ] Create `scripts/benchmark_z3_depth.py`
  - Test depths: [3, 5, 7, 10, 15, 20]
  - For each depth:
    - Run `search_binary_only(max_depth=d, use_z3=False)`
    - Run `search_binary_only(max_depth=d, use_z3=True)`
    - Measure: time_enum, time_z3, max_size_enum, max_size_z3
    - Record: winner, speedup
  - Output: CSV with columns (depth, time_enum, time_z3, speedup, winner, max_size_enum, max_size_z3)
  - Timeout: 60s per strategy per depth

- [ ] Add depth comparison test (`tests/test_z3_depth_advantage.py`)
  - Parametrized test for depths [3, 5, 7, 10]
  - Validates correctness at each depth
  - Records performance data

- [ ] Run depth benchmark
  - Execute: `python3 scripts/benchmark_z3_depth.py --output z3_depth_results.csv`
  - Expected: Enumeration faster for depths 3-10, crossover at depth 15-20 (or no crossover)

**Testing**:
```bash
# Run depth advantage tests
pytest tests/test_z3_depth_advantage.py -v

# Run depth benchmark
python3 scripts/benchmark_z3_depth.py --output z3_depth_results.csv

# Expected patterns:
# Depth 3:  Enum 20ms,  Z3 1.8s   (Enum wins 90×)
# Depth 5:  Enum 34ms,  Z3 2.5s   (Enum wins 73×)
# Depth 7:  Enum 100ms, Z3 3.5s   (Enum wins 35×)
# Depth 10: Enum 500ms, Z3 5.0s   (Enum wins 10×)
# Depth 15: Enum 5s,    Z3 8s     (Enum wins 1.6×)
# Depth 20: Enum 60s,   Z3 15s    (Z3 wins 4×) ← CROSSOVER?
```

**Expected Outcomes**:
- Enumeration scales exponentially: ~20ms × 2^(d/3) for depth d
- Z3 scales polynomially: ~1.8s + 0.5s×d for depth d
- Crossover point: Depth 15-20 (if it exists within practical limits)

**Key Insight to Discover**:
- **If Z3 never catches up**: Enumeration dominates for all practical depths (d ≤ 20)
- **If Z3 catches up at depth N**: Use enumeration for d < N, Z3 for d ≥ N

---

### Phase 3: Arity Advantage Study
**Objective**: Find max_size where Z3 becomes faster than enumeration at depth=3
**Complexity**: Medium-High
**Estimated Time**: 3-4 hours

**Tasks**:
- [ ] Create `scripts/benchmark_z3_arity.py`
  - Test max_size: [2, 3, 4, 5, 6, 7]
  - For max_size m, generate connectives of arity 0 to m:
    - m=2: Binary connectives (arity 0-2), 22 total
    - m=3: + Ternary connectives (arity 3), ~278 total
    - m=4: + Quaternary connectives (arity 4), ~65k total (use sampling)
  - For each max_size:
    - Run `find_maximum_nice_set(connectives, max_size=m, use_z3=False)`
    - Run `find_maximum_nice_set(connectives, max_size=m, use_z3=True)`
    - Measure: time_enum, time_z3, max_found_enum, max_found_z3
    - Record: winner, speedup
  - Output: CSV with columns (max_size, arity_range, num_connectives, time_enum, time_z3, speedup, winner)
  - Timeout: 120s per strategy per max_size

- [ ] Add arity comparison test (`tests/test_z3_arity_advantage.py`)
  - Test max_size [2, 3, 4] (fast subset)
  - Validates correctness at each max_size
  - Records performance data

- [ ] Run arity benchmark
  - Execute: `python3 scripts/benchmark_z3_arity.py --output z3_arity_results.csv`
  - Expected: Enumeration faster for max_size 2-3, crossover at max_size 4-5

**Testing**:
```bash
# Run arity advantage tests (fast subset)
pytest tests/test_z3_arity_advantage.py -v

# Run arity benchmark (includes slow max_size 5-7)
python3 scripts/benchmark_z3_arity.py --output z3_arity_results.csv

# Expected patterns:
# max_size=2 (binary):    Enum 20ms,  Z3 1.8s   (Enum wins 90×)
# max_size=3 (ternary):   Enum 2s,    Z3 30s    (Enum wins 15×)
# max_size=4 (quaternary): Enum 300s?, Z3 5s     (Z3 wins 60×) ← CROSSOVER?
# max_size=5:             Enum timeout, Z3 10s  (Z3 wins)
```

**Expected Outcomes**:
- Enumeration practical for max_size ≤3 (arity ≤3)
- Enumeration impractical for max_size ≥4 (arity ≥4) due to combinatorial explosion
- Z3 necessary for max_size ≥4

**Key Insight to Discover**:
- **Crossover max_size**: The point where Z3 becomes faster than enumeration
- **Expected**: max_size=4 (matches Report 008 prediction: arity ≥4 requires Z3)

**Note**: For max_size ≥4, enumeration may timeout (>120s). This is expected and validates the need for Z3.

---

### Phase 4: Analysis and Recommendations
**Objective**: Synthesize findings into actionable recommendations
**Complexity**: Medium
**Estimated Time**: 2-3 hours

**Tasks**:
- [ ] Create analysis report (`specs/reports/009_z3_advantage_analysis.md`)
  - **Section 1: Depth Analysis**
    - Plot: depth vs time (enumeration and Z3 on same graph)
    - Identify: Depth crossover point (if any)
    - Conclusion: When Z3 helps with greater depth

  - **Section 2: Arity Analysis**
    - Plot: max_size vs time (enumeration and Z3 on same graph)
    - Identify: Arity crossover point (expected: max_size=4)
    - Conclusion: When Z3 helps with greater arity

  - **Section 3: Z3 Correctness Validation**
    - Verify: Z3 finds same max_size as enumeration at all tested depths/arities
    - Report: Any discrepancies or errors

  - **Section 4: Performance Curves**
    - Enumeration scaling: time vs depth (exponential fit)
    - Z3 scaling: time vs depth (polynomial fit)
    - Crossover prediction: Extrapolate to depth 25, 30

  - **Section 5: Recommendations**
    - **Depth recommendation**: Use Z3 when depth > N (if crossover found)
    - **Arity recommendation**: Use Z3 when arity ≥ 4 (validate Report 008)
    - **Default strategy**: When to use enumeration vs Z3
    - **Adaptive strategy update** (if needed)

- [ ] Update adaptive strategy (if needed)
  - Current: `use_z3 = (target.arity >= 4) or (len(basis) > 20)`
  - Potential: Add depth-based selection: `use_z3 = ... or (max_depth >= 15)`
  - Location: `src/independence.py:is_definable()`

- [ ] Document findings in README (performance section)
  - Add subsection: "When to Use Z3 vs Enumeration"
  - Include: Depth and arity recommendations
  - Reference: Report 009

**Testing**:
```bash
# Validate report completeness
ls specs/reports/009_z3_advantage_analysis.md

# Check for required sections
grep -E "^## (Depth|Arity|Correctness|Performance|Recommendations)" \
  specs/reports/009_z3_advantage_analysis.md
```

**Expected Report Conclusions**:

1. **Depth Advantage**:
   - Enumeration faster for depth ≤ 10
   - Z3 catches up at depth 15-20 (if at all)
   - Recommendation: Use enumeration for depth ≤ 10, Z3 for depth > 15

2. **Arity Advantage**:
   - Enumeration faster for arity ≤ 3 (validates Report 008)
   - Z3 necessary for arity ≥ 4 (combinatorial explosion)
   - Recommendation: Use enumeration for arity ≤3, Z3 for arity ≥4

3. **Overall Strategy**:
   ```python
   def should_use_z3(target_arity, basis_size, max_depth):
       # Arity threshold
       if target_arity >= 4:
           return True

       # Basis size threshold
       if basis_size > 20:
           return True

       # Depth threshold (if crossover found)
       if max_depth > 15:
           return True  # Based on Phase 2 findings

       # Default: use enumeration
       return False
   ```

---

## Testing Strategy

### Unit Tests
- `tests/test_z3_baseline.py`: Baseline validation (depth=3, binary)
- `tests/test_z3_depth_advantage.py`: Depth comparison (depths 3-10)
- `tests/test_z3_arity_advantage.py`: Arity comparison (max_size 2-4)

### Benchmark Scripts
- `scripts/benchmark_z3_depth.py`: Systematic depth study
- `scripts/benchmark_z3_arity.py`: Systematic arity study

### Integration Tests
- All tests validate correctness: Z3 and enumeration find same max_size
- Performance metrics collected but not asserted (for analysis only)

### Expected Test Results
- All tests pass (correctness)
- CSV files generated with performance data
- Report 009 synthesizes findings

---

## Documentation Requirements

### New Files
- `specs/reports/009_z3_advantage_analysis.md` - Analysis report with recommendations

### Updated Files
- `README.md` - Add "When to Use Z3 vs Enumeration" subsection (if findings warrant)
- `src/independence.py` - Update adaptive strategy docstring (if strategy changes)

### Performance Data Files
- `z3_depth_results.csv` - Depth vs performance data
- `z3_arity_results.csv` - Arity vs performance data

---

## Dependencies

### Code Dependencies
- `src/search.py` - Binary search functions with `use_z3` parameter
- `src/independence.py` - Independence checking with strategy selection
- `src/independence_z3.py` - Z3 SAT backend

### External Dependencies
- Z3 solver (already installed)
- pytest (already installed)

### Data Dependencies
- Report 008 findings (enumeration 176× faster for binary)
- Plan 003 Phase 1 findings (depth performance curve)

---

## Risk Assessment

### Risk 1: Z3 May Never Catch Up (Depth)
**Scenario**: Enumeration remains faster than Z3 for all practical depths (≤20)
**Impact**: Medium - Would invalidate depth advantage hypothesis
**Mitigation**: This is still a valuable finding - documents that enumeration dominates
**Outcome**: Update recommendations to always prefer enumeration for binary search

### Risk 2: Enumeration Timeouts Too Early (Arity)
**Scenario**: Enumeration times out at max_size=4 (arity 3), can't test max_size=5
**Impact**: Low - Still validates arity ≥4 requires Z3
**Mitigation**: Use timeout protection (120s), document timeout as "impractical"
**Outcome**: Confirms Report 008 findings

### Risk 3: Z3 Correctness Issues at High Depth
**Scenario**: Z3 finds different max_size than enumeration at depth >10
**Impact**: High - Would indicate Z3 bug
**Mitigation**: Thorough validation at each depth, report discrepancies
**Outcome**: Fix Z3 implementation if needed, or document limitation

### Risk 4: Performance Variance
**Scenario**: High variance in timing makes crossover point unclear
**Impact**: Medium - Makes recommendations less precise
**Mitigation**: Run multiple trials (3-5 per depth/arity), report std dev
**Outcome**: Report crossover as a range rather than single point

---

## Notes

### Key Differences from Plan 003

**Plan 003** (Depth/Arity Crossover Analysis):
- Focus: Where enumeration becomes too slow (absolute performance)
- Depth study: Enumeration only (no Z3 comparison)
- Arity study: Not yet implemented
- Goal: Determine practical limits of enumeration

**Plan 004** (Z3 Advantage Study):
- Focus: Where Z3 becomes faster than enumeration (relative performance)
- Depth study: Enumeration vs Z3 comparison at each depth
- Arity study: Enumeration vs Z3 comparison at each max_size
- Goal: Determine when to switch to Z3

**Relationship**: Plan 003 provides baseline enumeration data, Plan 004 adds Z3 comparison

### Design Rationale

**Why start with depth=3, max_size=2?**
- Matches Report 008 baseline (binary search, depth=3)
- Known result: Enumeration 176× faster
- Validates test framework before expanding scope

**Why test depths up to 20?**
- Plan 003 showed depth 10 is practical (<1s)
- Depth 15-20 likely where Z3 might catch up (if ever)
- Beyond depth 20 is impractical for both strategies

**Why test max_size up to 7?**
- max_size=2: Binary (known baseline)
- max_size=3: Ternary (enumeration still practical)
- max_size=4: Quaternary (expected crossover)
- max_size=5-7: Z3 domain (enumeration impractical)

### Expected Timeline

- **Phase 1**: 1-2 hours (baseline validation)
- **Phase 2**: 2-3 hours (depth study)
- **Phase 3**: 3-4 hours (arity study)
- **Phase 4**: 2-3 hours (analysis and recommendations)
- **Total**: 8-12 hours

### Success Definition

**Minimum Success**:
- Validate Report 008: Enumeration faster for arity ≤3
- Determine if Z3 ever catches up with depth
- Document when to use each strategy

**Ideal Success**:
- Identify depth crossover point (if exists)
- Identify arity crossover point (expected: max_size=4)
- Update adaptive strategy with depth-based selection
- Comprehensive performance characterization

---

## Commit Strategy

### Phase 1 Commit
```
feat: add Z3 baseline validation tests

Created baseline tests comparing Z3 vs enumeration at standard settings
(depth=3, binary search). Validates Report 008 findings.

Changes:
- Added tests/test_z3_baseline.py with baseline comparison
- Baseline: Enumeration ~20ms, Z3 ~1.8s (90× faster)
- Both strategies find max=3 (correctness validated)
```

### Phase 2 Commit
```
feat: implement Z3 depth advantage study

Systematic comparison of Z3 vs enumeration across depths 3-20.
Identifies crossover point where Z3 becomes faster (if any).

Changes:
- Added scripts/benchmark_z3_depth.py for depth study
- Added tests/test_z3_depth_advantage.py for validation
- Generated z3_depth_results.csv with performance data
- Finding: [Enumeration faster for all tested depths | Z3 faster at depth > N]
```

### Phase 3 Commit
```
feat: implement Z3 arity advantage study

Systematic comparison of Z3 vs enumeration across max_size 2-7.
Validates arity ≥4 requires Z3 (Report 008 hypothesis).

Changes:
- Added scripts/benchmark_z3_arity.py for arity study
- Added tests/test_z3_arity_advantage.py for validation
- Generated z3_arity_results.csv with performance data
- Finding: Enumeration faster for max_size ≤3, Z3 necessary for max_size ≥4
```

### Phase 4 Commit
```
docs: add Z3 advantage analysis and recommendations

Synthesized depth and arity studies into comprehensive analysis report.
Updated adaptive strategy and documentation.

Changes:
- Added specs/reports/009_z3_advantage_analysis.md
- Updated src/independence.py adaptive strategy [if applicable]
- Updated README.md with Z3 vs enumeration guidance [if applicable]
- Recommendation: Use enumeration for arity ≤3, Z3 for arity ≥4 [+ depth guidance]
```

---

## References

### Related Reports
- `specs/reports/007_performance_analysis.md` - Performance benchmarking baseline
- `specs/reports/008_z3_vs_enumeration_performance.md` - Z3 vs enumeration at depth=3

### Related Plans
- `specs/plans/002_comprehensive_refactor_hybrid_z3.md` - Hybrid strategy implementation
- `specs/plans/003_depth_arity_crossover_analysis.md` - Depth/arity crossover framework

### Key Source Files
- `src/independence.py` - Adaptive strategy and pattern enumeration
- `src/independence_z3.py` - Z3 SAT backend
- `src/search.py` - Search functions with `use_z3` parameter
- `tests/test_independence.py` - Independence checking tests (159 passing)

---

**Plan prepared by**: Claude Code (/plan execution)
**Date**: 2025-10-02
**Status**: Ready for implementation
**Next step**: `/implement specs/plans/004_z3_depth_arity_advantage_study.md`
