# Comprehensive Refactor: Hybrid Z3-Enhanced Nice Connectives Solver

## Metadata
- **Date**: 2025-10-02
- **Feature**: Comprehensive refactor to address all identified deficits with hybrid SAT-based Z3 approach
- **Scope**: Fix incomplete independence checking, add Z3 SAT backend, resolve documentation discrepancies, implement missing features
- **Estimated Phases**: 8
- **Standards File**: /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/CLAUDE.md
- **Research Reports**:
  - specs/reports/004_comprehensive_project_analysis.md (Identifies all deficits)
  - specs/reports/005_z3_smt_application_analysis.md (Recommends Approach 4: SAT-based)

---

## Overview

This refactoring plan systematically addresses all critical issues identified in the comprehensive project analysis (Report 004) while incorporating the recommended SAT-based Z3 approach (Report 005, Approach 4) for enhanced completeness and performance.

### Critical Issues to Resolve

**From Report 004**:
1. **Incomplete Independence Checker** (High Priority)
   - Missing unary-outer patterns: `NOT(AND(x,y))`
   - Missing ternary composition patterns
   - Conservative false negatives for non-binary arities

2. **Documentation Discrepancy** (High Priority)
   - FINAL_ANSWER.md claims max ≥42
   - Validation consistently shows max = 16
   - Depth parameter not documented

3. **Ternary Support Gap** (Medium Priority)
   - Independence checker returns False for non-binary targets
   - Cannot validate ternary results fully

4. **Symmetry Breaking Not Implemented** (Medium Priority)
   - Stub exists but unused
   - Could provide ~8× search space reduction

5. **XOR Detection Limitation** (Low Priority)
   - Test skipped for XOR independence edge case

### Enhancements from Report 005

**Approach 4: SAT-Based Hybrid**:
- Pure Boolean encoding for Z3's optimized SAT core
- Cardinality constraints for "exactly one function per node"
- Tree structure with choice variables
- Iterative deepening: depth 1, 2, 3...
- Witness extraction for debugging

**Performance Targets**:
- Binary/ternary: Maintain current ~10-100ms performance
- Quaternary+: Enable feasible search (~500ms vs ~10s enumeration)
- Completeness: Full coverage up to depth 5

---

## Success Criteria

- [ ] All missing composition patterns implemented (unary-outer, ternary, mixed-arity)
- [ ] Z3 SAT-based solver fully functional with witness extraction
- [ ] Adaptive strategy: enumeration for arity ≤3, Z3 for arity ≥4
- [ ] Symmetry breaking implemented and integrated
- [ ] XOR independence test passing
- [ ] Documentation discrepancy resolved (16 vs ≥42)
- [ ] Depth parameter explicitly logged in all search outputs
- [ ] All 159 tests passing (currently 158 passing, 1 skipped)
- [ ] Comprehensive validation: binary max=3, unary+binary max=7, ternary max verified
- [ ] Performance benchmarks: no regression for arity ≤3

---

## Technical Design

### Architecture: Hybrid Three-Tier Approach

```
Independence Checking Strategy:
┌─────────────────────────────────────────────────────────┐
│ is_definable(target, basis, depth, use_z3=False)        │
├─────────────────────────────────────────────────────────┤
│ Tier 1: Fast Path (Arity ≤3, Small Basis)              │
│   → Complete pattern enumeration (new patterns added)   │
│   → Performance: ~10-100ms                               │
│   → Completeness: Full up to depth 3                    │
├─────────────────────────────────────────────────────────┤
│ Tier 2: Z3 SAT Backend (Arity ≥4 or use_z3=True)       │
│   → SAT-based composition tree encoding                 │
│   → Iterative deepening with witness extraction         │
│   → Performance: ~100-500ms                              │
│   → Completeness: Full up to depth 5                    │
├─────────────────────────────────────────────────────────┤
│ Tier 3: Conservative Fallback                           │
│   → Return False (conservative) if Z3 times out         │
│   → Log warning about incomplete check                  │
└─────────────────────────────────────────────────────────┘
```

### New Module: src/independence_z3.py

**Core Components**:

1. **CompositionTree**: Witness data structure
   ```python
   class CompositionTree:
       function: Connective
       left_child: Optional[CompositionTree]
       right_child: Optional[CompositionTree]

       def to_formula(self) -> str:
           # "NOT(AND(x, y))" format

       def evaluate(self, inputs: Tuple[int, ...]) -> int:
           # Verify witness correctness
   ```

2. **SAT Encoder**: Build Z3 constraints
   ```python
   def encode_composition_tree_sat(
       target: Connective,
       basis: List[Connective],
       depth: int
   ) -> Tuple[Solver, Dict[str, Any]]:
       # Returns solver and variable mapping for witness extraction
   ```

3. **Iterative Deepening Solver**:
   ```python
   def is_definable_z3_sat(
       target: Connective,
       basis: List[Connective],
       max_depth: int = 3,
       timeout_ms: int = 5000
   ) -> Tuple[bool, Optional[CompositionTree]]:
       # Try depth 1, then 2, then 3...
       # Return first satisfying composition
   ```

### Enhanced Module: src/independence.py

**New Composition Patterns** (addresses Report 004, Section 2.3):

```python
# Depth 2 Patterns (Binary Target)
- [✓] f(g(x,y), h(x,y))          # Binary-outer, binary-inner (EXISTING)
- [✗] u(f(x,y))                  # Unary-outer, binary-inner (MISSING - HIGH PRIORITY)
- [✓] f(u(x), v(y))              # Binary-outer, unary-inner (EXISTING)
- [✗] f(c, g(x,y))               # Binary-outer, constant + binary (MISSING)
- [✗] f(x, c)                    # Binary-outer, variable + constant (MISSING)

# Depth 3 Patterns (Binary Target)
- [✓] u(f(g(x,y), h(x,y)))       # Unary-outer, binary-middle (EXISTING)
- [✗] f(u(g(x,y)), v(h(x,y)))    # Binary-outer, unary-middle (MISSING)
- [✗] u(v(f(x,y)))               # Unary-unary-binary chain (MISSING)

# Ternary Target Patterns
- [✗] f(g(x,y,z), h(x,y,z))      # Binary-outer, ternary-inner (MISSING - MEDIUM PRIORITY)
- [✗] u(f(x,y,z))                # Unary-outer, ternary-inner (MISSING)
- [✗] f(g(x,y), z)               # Binary-outer, binary+variable (MISSING)
- [✗] t(u(x), v(y), w(z))        # Ternary-outer, unary-inner (MISSING)
```

**Adaptive Strategy Selection**:
```python
def is_definable(target: Connective, basis: List[Connective],
                max_depth: int = 3, timeout_ms: int = 5000,
                use_z3: Optional[bool] = None) -> bool:
    """
    Args:
        use_z3: None (auto), True (force Z3), False (force enumeration)
    """
    # Auto-select strategy
    if use_z3 is None:
        use_z3 = (target.arity >= 4) or (len(basis) > 20)

    if not use_z3:
        # Tier 1: Complete pattern enumeration
        return _check_composition_enumeration_complete(target, basis, max_depth)
    else:
        # Tier 2: Z3 SAT-based solver
        from src.independence_z3 import is_definable_z3_sat
        is_def, witness = is_definable_z3_sat(target, basis, max_depth, timeout_ms)
        if witness:
            print(f"Z3 found composition: {witness.to_formula()}")
        return is_def
```

### Enhanced Module: src/post_classes.py

**Symmetry Breaking Implementation** (addresses Report 004, Section 5.2, Issue 5):

```python
def equivalence_class_representative(connective: Connective) -> int:
    """
    Compute canonical representative under:
    - Variable permutation
    - Variable negation
    - Output negation

    Returns smallest truth table value in equivalence class.
    """
    # Implement full symmetry reduction
    # For arity n: n! permutations × 2^(n+1) negations = (n!)×2^(n+1) variants
    # Return min(all_variants)
```

**Usage in Search**:
```python
# In search.py
def filter_by_equivalence(connectives: List[Connective]) -> List[Connective]:
    """Remove equivalent connectives, keep only representatives."""
    seen = set()
    filtered = []
    for c in connectives:
        rep = equivalence_class_representative(c)
        if rep not in seen:
            seen.add(rep)
            filtered.append(c)
    return filtered
```

### Enhanced Module: src/search.py

**Depth Parameter Logging** (addresses Report 004, Section 6.1):

```python
def find_maximum_nice_set(
    connectives: List[Connective],
    max_size: int = 10,
    max_depth: int = 3,  # ← Explicitly documented
    use_z3: bool = False,
    verbose: bool = False
) -> Tuple[int, List[List[Connective]], Dict[str, Any]]:
    """
    Returns: (max_size, nice_sets, metadata)

    metadata includes:
        - composition_depth: max_depth used
        - strategy: "enumeration" or "z3_sat"
        - search_time: seconds
        - basis_size: number of connectives searched
    """
```

---

## Implementation Phases

### Phase 1: Foundation - Complete Pattern Enumeration
**Objective**: Implement all missing composition patterns for complete independence checking
**Complexity**: Medium
**Estimated Time**: 1-2 days

**Tasks**:
- [ ] Add unary-outer, binary-inner pattern: `u(f(x,y))`
  - File: `src/independence.py`
  - Function: `_check_unary_binary(target, unary_basis, binary_basis)` (already stubbed)
  - Test case: Verify NAND = NOT(AND) is detected

- [ ] Add binary-outer, constant patterns: `f(c, g(x,y))`, `f(x, c)`
  - File: `src/independence.py`
  - Function: `_check_binary_constant_patterns(target, binary, nullary)`
  - Test case: Verify `OR(FALSE, x)` is detected as identity

- [ ] Add depth-3 unary-binary patterns: `f(u(g(x,y)), v(h(x,y)))`
  - File: `src/independence.py`
  - Function: `_check_binary_unary_binary_unary_binary(target, binary, unary)`
  - Test case: Complex De Morgan's law variants

- [ ] Add ternary patterns: `f(g(x,y,z), h(x,y,z))`, `u(f(x,y,z))`
  - File: `src/independence.py`
  - Functions: `_check_binary_ternary_ternary()`, `_check_unary_ternary()`
  - Test case: Ternary decompositions

- [ ] Update `_check_composition_enumeration()` to dispatch to all new patterns
  - File: `src/independence.py`, lines 160-236
  - Ensure all patterns tried systematically

**Testing**:
```bash
pytest tests/test_independence.py::test_unary_outer_binary_inner -v
pytest tests/test_independence.py::test_nand_detection -v
pytest tests/test_independence.py::test_ternary_compositions -v
```

**Expected Outcomes**:
- XOR independence test (currently skipped) should now pass
- All binary decompositions detected
- Ternary target independence checking enabled

**Validation**:
- Run binary-only search: should still find max=3
- Run unary+binary search: should still find max=7
- Run ternary search: may find different max if independence was too conservative

---

### Phase 2: Z3 SAT Backend - Core Encoding
**Objective**: Implement SAT-based composition tree encoding (Approach 4 from Report 005)
**Complexity**: High
**Estimated Time**: 2-3 days

**Tasks**:
- [ ] Create `src/independence_z3.py` module
  - Initialize file with imports and module docstring
  - Document Approach 4 encoding strategy from Report 005

- [ ] Implement `CompositionTree` witness class
  - Fields: `function`, `left_child`, `right_child`
  - Methods: `to_formula()`, `evaluate()`, `__repr__()`
  - Support unary (1 child), binary (2 children), and leaf nodes (0 children)
  - File: `src/independence_z3.py`, lines 1-80

- [ ] Implement `_build_tree_structure()` helper
  - Compute number of nodes for given depth and max arity
  - Return tree topology (parent-child relationships)
  - Support binary trees (arity 2) initially
  - File: `src/independence_z3.py`, lines 82-120

- [ ] Implement `_encode_tree_choices()` - choice variables
  - Create Bool variables: `choice[node][func]` = "node uses function func"
  - Add cardinality constraints: exactly one function per node
  - Use Z3's `PbEq` for efficient encoding
  - File: `src/independence_z3.py`, lines 122-160

- [ ] Implement `_encode_tree_outputs()` - output variables
  - Create Bool variables: `output[node][input]` = "node outputs 1 for input"
  - Link outputs to chosen functions via `Implies` constraints
  - File: `src/independence_z3.py`, lines 162-220

- [ ] Implement `_encode_tree_structure()` - parent-child constraints
  - Leaf nodes: outputs are input variables (no choice)
  - Internal nodes: inputs come from children's outputs
  - Support variable-arity trees (unary and binary nodes)
  - File: `src/independence_z3.py`, lines 222-280

- [ ] Implement `_encode_target_match()` - root matches target
  - Root node output must equal target's truth table
  - For all input assignments
  - File: `src/independence_z3.py`, lines 282-310

**Testing**:
```bash
pytest tests/test_independence_z3.py::test_composition_tree -v
pytest tests/test_independence_z3.py::test_sat_encoding_structure -v
```

**Expected Outcomes**:
- Z3 solver can be constructed with all constraints
- Solver accepts simple test cases (e.g., identity, constant)
- Encoding is quantifier-free (no `ForAll`/`Exists`)

**Validation**:
- Manual inspection: check that generated clauses are reasonable size
- For binary target, depth 2, 5 basis functions: ~50 variables, ~200 clauses expected

---

### Phase 3: Z3 SAT Backend - Witness Extraction
**Objective**: Extract composition tree witnesses from satisfying Z3 models
**Complexity**: Medium
**Estimated Time**: 1 day

**Tasks**:
- [ ] Implement `_extract_witness_from_model()`
  - Given Z3 model, identify which choice variables are True
  - Recursively build `CompositionTree` from root to leaves
  - File: `src/independence_z3.py`, lines 312-380

- [ ] Implement witness verification
  - Evaluate extracted `CompositionTree` on all inputs
  - Assert outputs match target's truth table (sanity check)
  - Raise exception if witness is invalid
  - File: `src/independence_z3.py`, lines 382-420

- [ ] Implement `is_definable_z3_sat()` main API
  - Iterative deepening: try depth 1, 2, 3, ..., max_depth
  - Return (True, witness) if SAT, (False, None) if UNSAT
  - Handle Z3 "unknown" result as conservative False
  - File: `src/independence_z3.py`, lines 422-480

- [ ] Add timeout and error handling
  - Set Z3 timeout via `s.set("timeout", timeout_ms)`
  - Catch Z3 exceptions and return conservative False
  - Log warnings for timeouts and errors
  - File: `src/independence_z3.py`, lines 450-460

**Testing**:
```bash
pytest tests/test_independence_z3.py::test_witness_extraction -v
pytest tests/test_independence_z3.py::test_nand_from_not_and -v
pytest tests/test_independence_z3.py::test_iterative_deepening -v
```

**Expected Outcomes**:
- Z3 finds NAND = NOT(AND) witness at depth 2
- Witnesses are verifiably correct (evaluation matches target)
- Iterative deepening finds shallow compositions first

**Validation**:
- Compare Z3 results with pattern enumeration on binary connectives
- Should agree 100% for depth ≤3

---

### Phase 4: Hybrid Integration - Adaptive Strategy
**Objective**: Integrate Z3 SAT backend with pattern enumeration via adaptive dispatch
**Complexity**: Low
**Estimated Time**: 0.5 days

**Tasks**:
- [ ] Update `is_definable()` signature in `src/independence.py`
  - Add `use_z3: Optional[bool] = None` parameter
  - Add docstring explaining auto-selection logic
  - File: `src/independence.py`, lines 16-34

- [ ] Implement adaptive strategy selection
  - If `use_z3 is None`: auto-select based on arity and basis size
  - Threshold: arity ≥4 or basis size > 20 → use Z3
  - Otherwise: use pattern enumeration
  - File: `src/independence.py`, lines 36-50

- [ ] Add dispatch to Z3 backend
  - Import `independence_z3.is_definable_z3_sat` conditionally
  - Call Z3 solver if `use_z3=True`
  - Print witness formula if found (for debugging)
  - File: `src/independence.py`, lines 52-65

- [ ] Update `is_independent()` to pass through `use_z3` parameter
  - File: `src/independence.py`, lines 410-440

- [ ] Update search functions to accept `use_z3` parameter
  - `find_nice_sets_of_size()`, `find_maximum_nice_set()`, etc.
  - File: `src/search.py`, lines 17-110

**Testing**:
```bash
pytest tests/test_independence.py::test_adaptive_strategy -v
pytest tests/test_search.py::test_binary_with_z3 -v
```

**Expected Outcomes**:
- Binary search with `use_z3=False`: uses pattern enumeration
- Binary search with `use_z3=True`: uses Z3 SAT backend
- Both produce identical results for arity ≤3

**Validation**:
- Run binary-only search with both strategies: should find max=3
- Performance: pattern enumeration should be ~2× faster for binary

---

### Phase 5: Symmetry Breaking Implementation
**Objective**: Implement equivalence class reduction to speed up search
**Complexity**: Medium
**Estimated Time**: 1 day

**Tasks**:
- [ ] Implement `_compute_under_permutation()` helper
  - Given connective and variable permutation, compute permuted truth table
  - Example: AND(x,y) with perm=(1,0) → AND(y,x) = same truth table
  - File: `src/post_classes.py`, lines 288-320

- [ ] Implement `_compute_under_negation()` helper
  - Given connective and negation mask, compute negated truth table
  - Example: AND(x,y) with mask=(1,0) → AND(~x,y) = different truth table
  - File: `src/post_classes.py`, lines 322-360

- [ ] Implement `equivalence_class_representative()`
  - Generate all permutations (n! variants)
  - Generate all negations (2^(n+1) variants)
  - Compute truth table for each variant
  - Return minimum truth table value (canonical representative)
  - File: `src/post_classes.py`, lines 264-400

- [ ] Implement `filter_by_equivalence()` in `src/search.py`
  - Takes list of connectives, returns list of representatives only
  - Track seen equivalence classes via `set()`
  - File: `src/search.py`, lines 280-310

- [ ] Integrate into search algorithms
  - Filter connective pool before searching: `connectives = filter_by_equivalence(connectives)`
  - Add timing metrics: log reduction ratio (original / filtered)
  - File: `src/search.py`, lines 92-96, 215-220

**Testing**:
```bash
pytest tests/test_post_classes.py::test_equivalence_class -v
pytest tests/test_post_classes.py::test_symmetry_breaking -v
pytest tests/test_search.py::test_filtered_search -v
```

**Expected Outcomes**:
- Binary connectives: 16 total → ~6-8 representatives (~2× reduction)
- Ternary connectives: 256 total → ~30-40 representatives (~8× reduction)
- Search time reduced proportionally

**Validation**:
- Binary search with symmetry breaking: should still find max=3
- But search time should decrease by ~50%
- Maximum nice set should be same size (just faster to find)

---

### Phase 6: Comprehensive Testing and Validation
**Objective**: Add missing tests, fix skipped tests, validate all results
**Complexity**: Low
**Estimated Time**: 1 day

**Tasks**:
- [ ] Fix skipped XOR independence test
  - File: `tests/test_independence.py`
  - Test name: `test_xor_independence` (currently skipped)
  - Should now pass with complete pattern enumeration
  - Assert: XOR is independent from {AND, OR, NOT}

- [ ] Add tests for all new composition patterns
  - Test: `test_unary_outer_detection` - NAND = NOT(AND)
  - Test: `test_constant_patterns` - OR(FALSE, x) = x
  - Test: `test_ternary_decompositions` - ternary functions
  - File: `tests/test_independence.py`, new tests

- [ ] Add Z3 SAT backend tests
  - Test: `test_z3_vs_enumeration_agreement` - both find same results
  - Test: `test_z3_witness_correctness` - all witnesses verify
  - Test: `test_z3_iterative_deepening` - depths tried in order
  - File: `tests/test_independence_z3.py` (new file)

- [ ] Add symmetry breaking tests
  - Test: `test_equivalence_class_binary` - AND ≅ AND(permuted)
  - Test: `test_filtered_search_correctness` - same max size
  - Test: `test_search_speedup` - faster with filtering
  - File: `tests/test_post_classes.py`, `tests/test_search.py`

- [ ] Run comprehensive validation suite
  - Binary-only search: max = 3? (with depth=3, depth=5)
  - Unary+Binary search: max = 7? (with depth=3, depth=5)
  - Ternary search: max = ? (document result with depth parameter)
  - File: `tests/test_validation.py` (new file)

**Testing**:
```bash
pytest tests/ -v --tb=short
pytest tests/ --cov=src --cov-report=term-missing
```

**Expected Outcomes**:
- All 159+ tests passing (no skipped)
- Code coverage: ≥90% for all modules
- Validation outputs: binary max=3, unary+binary max=7, ternary max documented

**Validation**:
- Compare new ternary results with old results
- If max changes from 16: analyze why (likely due to complete independence checking)
- Document composition depth used for all results

---

### Phase 7: Documentation Resolution and Parameter Logging [COMPLETED]
**Objective**: Resolve 16 vs ≥42 discrepancy, document depth parameter, update all docs
**Complexity**: Low
**Estimated Time**: 1 day
**Actual Time**: ~2 hours

**Tasks**:
- [x] Add depth parameter to all search output
  - Modified `find_maximum_nice_set()` to return metadata dict
  - Includes: `composition_depth`, `strategy`, `search_time`, `basis_size`
  - File: `src/search.py`, updated signature and all callers
  - Tests: Updated `tests/test_search.py` to handle new signature

- [x] Re-run ternary search with comprehensive logging
  - Created `scripts/validate_binary_search.py` - validates binary max=3
  - Created `scripts/validate_ternary_search.py` - comprehensive validation
  - Validated: depth=3 yields max=16 (consistent result)
  - Confirmed: Binary max=3 with metadata logging ✓

- [x] Update FINAL_ANSWER.md
  - Removed ≥42 claim (unvalidated)
  - Replaced with validated max = 16
  - Added depth/strategy columns to all tables
  - Documented composition depth semantics and impact
  - File: `FINAL_ANSWER.md`

- [x] Update RESULTS_SUMMARY.md
  - Added "Composition Depth" column to results table
  - Added "Strategy" column (enumeration vs Z3)
  - Added performance metrics (search time)
  - Added depth impact analysis section
  - File: `RESULTS_SUMMARY.md`

- [x] Update README.md
  - Added dedicated "Composition Depth Parameter" section
  - Documented depth semantics (depth 1, 2, 3, etc.)
  - Added depth impact table showing results at different depths
  - Documented metadata logging feature
  - File: `README.md`

- [x] Create comprehensive validation report
  - Documented all Phase 7 changes and validations
  - Explained 16 vs ≥42 resolution (42 was unvalidated, 16 is correct)
  - Included validation script output examples
  - File: `specs/reports/006_validation_and_resolution.md`

**Testing**:
```bash
python scripts/validate_ternary_search.py --depth 3 --verbose
python scripts/validate_ternary_search.py --depth 5 --verbose
python scripts/compare_results.py
```

**Expected Outcomes**:
- Clear documentation of all results with depth parameter
- Explanation of why depth=3 vs depth=5 yields different results
- Resolution of 16 vs ≥42 discrepancy (likely: 42 was error, 16 is correct)

**Validation**:
- All stakeholders can reproduce results with documented parameters
- No ambiguity about which depth was used

---

### Phase 8: Performance Benchmarking and Optimization
**Objective**: Benchmark hybrid approach, optimize if needed, document performance
**Complexity**: Low
**Estimated Time**: 0.5 days

**Tasks**:
- [ ] Create benchmark suite
  - Benchmark: Binary search (enumeration vs Z3)
  - Benchmark: Ternary search (enumeration vs Z3)
  - Benchmark: Quaternary search (Z3 only, if feasible)
  - Benchmark: Effect of symmetry breaking
  - Script: `scripts/benchmark.py` (new file)

- [ ] Run benchmarks and collect data
  - Measure: time per search size (1, 2, 3, ..., max)
  - Measure: Z3 solver calls (count and avg time)
  - Measure: symmetry breaking reduction ratio
  - Output: CSV/JSON for analysis

- [ ] Analyze benchmark results
  - Verify: enumeration ≤100ms for binary/ternary (no regression)
  - Verify: Z3 enables quaternary search (<5s total)
  - Verify: symmetry breaking provides ~2-5× speedup

- [ ] Optimize hot paths if needed
  - If enumeration regressed: optimize pattern matching
  - If Z3 is slow: tune timeout, tactics, or encoding
  - If symmetry breaking is slow: cache representatives

- [ ] Document performance characteristics
  - Add "Performance" section to README.md
  - Document: when to use enumeration vs Z3
  - Document: expected search times for different arities
  - File: `README.md`, `specs/reports/007_performance_analysis.md` (new file)

**Testing**:
```bash
python scripts/benchmark.py --runs 5 --output benchmarks.csv
python scripts/analyze_benchmarks.py benchmarks.csv
```

**Expected Outcomes**:
- Performance documented and validated
- No regressions for arity ≤3 (should be within 10% of original)
- Clear guidance on when to use Z3 vs enumeration

**Validation**:
- Binary search: <100ms total (as before)
- Ternary search: <2s total (as before or faster with symmetry breaking)
- Quaternary search: <10s total (new capability!)

---

## Testing Strategy

### Unit Tests
**Coverage Target**: ≥90% for all modules

**Key Test Files**:
- `tests/test_independence.py`: All composition patterns (20+ tests)
- `tests/test_independence_z3.py`: SAT encoding and witness extraction (15+ tests)
- `tests/test_post_classes.py`: Symmetry breaking and equivalence classes (10+ tests)
- `tests/test_search.py`: Adaptive strategy and hybrid integration (10+ tests)
- `tests/test_validation.py`: End-to-end search validation (5+ tests)

**Test Commands**:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Run specific module tests
pytest tests/test_independence_z3.py -v
```

### Integration Tests
**Validation Scenarios**:
1. Binary-only search (both strategies) → max = 3
2. Unary+Binary search (both strategies) → max = 7
3. Ternary search with depth=3 → max = X (documented)
4. Ternary search with depth=5 → max = Y (documented)
5. Quaternary search with Z3 → max = ? (exploratory)

**Validation Commands**:
```bash
python scripts/validate_ternary_search.py --depth 3
python scripts/validate_ternary_search.py --depth 5
python scripts/compare_strategies.py
```

### Performance Tests
**Benchmarks**:
- Search time vs arity (1, 2, 3, 4)
- Z3 vs enumeration comparison
- Symmetry breaking speedup
- Composition depth impact

**Commands**:
```bash
python scripts/benchmark.py --output results.csv
pytest tests/test_performance.py --benchmark-only
```

---

## Documentation Requirements

### Code Documentation
- [ ] All new functions have comprehensive docstrings
- [ ] Docstrings include Args, Returns, Raises, Examples
- [ ] Complex algorithms have inline comments explaining logic
- [ ] Z3 encoding strategies documented in module docstrings

### Project Documentation
- [ ] Update README.md with hybrid approach explanation
- [ ] Update FINAL_ANSWER.md with validated results
- [ ] Update RESULTS_SUMMARY.md with depth parameters
- [ ] Create specs/reports/006_validation_and_resolution.md
- [ ] Create specs/reports/007_performance_analysis.md

### API Documentation
- [ ] Document `is_definable()` parameters (especially `use_z3`)
- [ ] Document `CompositionTree` witness structure
- [ ] Document search metadata return values
- [ ] Document depth parameter semantics

---

## Dependencies

### Existing Dependencies
- `z3-solver` (already installed)
- `pytest` (already installed)
- Standard library: `itertools`, `typing`, `time`

### New Dependencies (Optional)
- `pytest-benchmark`: For performance testing
- `pytest-cov`: For coverage reporting (likely already installed)

**Install Commands**:
```bash
pip install pytest-benchmark pytest-cov
```

---

## Risk Assessment and Mitigation

### High-Risk Areas

**Risk 1: Z3 SAT Encoding Complexity**
- **Impact**: Incorrect encoding produces wrong results
- **Likelihood**: Medium
- **Mitigation**:
  - Extensive unit tests for encoding functions
  - Witness verification (always evaluate extracted tree)
  - Compare Z3 results with enumeration on binary/ternary cases

**Risk 2: Performance Regression**
- **Impact**: Search becomes slower than before
- **Likelihood**: Low
- **Mitigation**:
  - Adaptive strategy keeps enumeration as default for arity ≤3
  - Benchmark before/after to detect regressions
  - Symmetry breaking should offset any overhead

**Risk 3: Witness Extraction Bugs**
- **Impact**: Z3 returns SAT but witness is invalid
- **Likelihood**: Medium
- **Mitigation**:
  - Always verify witnesses by evaluation
  - Raise exception on verification failure
  - Extensive testing with known compositions

### Medium-Risk Areas

**Risk 4: Symmetry Breaking Errors**
- **Impact**: Equivalence classes computed incorrectly, missing connectives
- **Likelihood**: Low-Medium
- **Mitigation**:
  - Comprehensive tests for all permutation/negation variants
  - Verify filtered search finds same max size as unfiltered

**Risk 5: New Pattern Enumeration Bugs**
- **Impact**: Miss or falsely detect compositions
- **Likelihood**: Low
- **Mitigation**:
  - Test each pattern independently
  - Use known examples (NAND = NOT(AND), etc.)
  - Compare with Z3 results as oracle

---

## Success Metrics

### Functional Success
- [ ] All 159+ tests passing (currently 158 + skipped XOR test)
- [ ] Binary max = 3 (both strategies)
- [ ] Unary+Binary max = 7 (both strategies)
- [ ] Ternary max validated with documented depth
- [ ] Documentation discrepancy resolved

### Performance Success
- [ ] Binary search: ≤100ms (no regression)
- [ ] Ternary search: ≤2s (improved with symmetry breaking)
- [ ] Quaternary search: feasible with Z3 (<10s)
- [ ] Symmetry breaking: ~2-5× speedup

### Code Quality Success
- [ ] Code coverage: ≥90%
- [ ] All functions have docstrings
- [ ] No pylint errors (severity ≥warning)
- [ ] Type hints for all public APIs

---

## Post-Implementation Validation

### Validation Checklist
After all phases complete:

1. **Correctness Validation**
   ```bash
   pytest tests/ -v  # All pass?
   python scripts/validate_all.py  # Reproduce known results?
   ```

2. **Performance Validation**
   ```bash
   python scripts/benchmark.py --compare-baseline  # No regression?
   ```

3. **Documentation Validation**
   - [ ] README accurately describes hybrid approach
   - [ ] FINAL_ANSWER.md has validated results only
   - [ ] Depth parameter documented everywhere
   - [ ] 16 vs ≥42 discrepancy explained

4. **API Validation**
   - [ ] Can reproduce binary max=3 with simple script
   - [ ] Can enable Z3 mode with `use_z3=True`
   - [ ] Can extract and print composition witnesses

5. **Research Validation**
   - [ ] All claims in FINAL_ANSWER.md are code-validated
   - [ ] Composition depth explicitly stated for all results
   - [ ] Performance characteristics documented

---

## Notes

### Implementation Order Rationale

The phases are ordered to:
1. **Build foundation first** (Phase 1): Complete pattern enumeration establishes baseline
2. **Add Z3 incrementally** (Phases 2-3): Core encoding, then witness extraction
3. **Integrate carefully** (Phase 4): Hybrid approach with fallback to enumeration
4. **Optimize** (Phase 5): Symmetry breaking as independent enhancement
5. **Validate thoroughly** (Phases 6-7): Testing and documentation resolution
6. **Benchmark** (Phase 8): Performance analysis after all features stable

This ordering minimizes risk by:
- Keeping enumeration working throughout (no regression)
- Adding Z3 as optional enhancement (can disable if problems)
- Validating each component before integration

### Depth Parameter Semantics

**Depth = 1**: Direct application (identity, single function)
**Depth = 2**: One level of composition (e.g., `f(g(x), h(y))`)
**Depth = 3**: Two levels (e.g., `f(g(h(x)), i(y))`)

**Trade-off**:
- Lower depth: More conservative (larger independent sets possible)
- Higher depth: More restrictive (smaller independent sets, but more "truly" independent)

**Recommendation**: Document results for multiple depths (3, 5) to show sensitivity

### Z3 Tactics for Optimization

If Z3 SAT solving is slow, consider tactics:
```python
s = Solver()
s.set("timeout", 5000)
s.set("sat.cardinality.solver", True)  # Enable cardinality optimization
# Optional: Use tactics for SAT preprocessing
tactic = With('simplify', Then('propagate-values', 'solve-eqs', 'sat'))
```

See Z3 documentation for available tactics: `theory.stanford.edu/~nikolaj/programmingz3.html`

### Future Enhancements (Out of Scope)

Not included in this refactor, but possible future work:
- **Parallelization**: Search multiple sizes concurrently
- **Caching**: Store composition results across queries
- **Incremental Z3**: Reuse solver context across similar queries
- **Alternative backends**: Try other SMT solvers (CVC5, Yices)
- **Higher arities**: Extend to quinternary+ (arity 5+)

---

## Cross-References

**Source Reports**:
- `specs/reports/004_comprehensive_project_analysis.md`: Identifies all deficits to address
- `specs/reports/005_z3_smt_application_analysis.md`: Recommends Approach 4 (SAT-based)

**Related Plans**:
- `specs/plans/001_nice_connectives_solver.md`: Original implementation (complete)

**Project Standards**:
- `CLAUDE.md`: Python/Z3 coding standards, testing protocols

**Validation Scripts** (to be created):
- `scripts/validate_ternary_search.py`
- `scripts/compare_strategies.py`
- `scripts/benchmark.py`

---

**Plan prepared by**: Claude Code `/plan` command
**Based on**: Comprehensive analysis (Report 004) and Z3 approach evaluation (Report 005)
**Estimated Total Time**: 7-9 days
**Complexity**: High (8 phases, significant refactoring)
