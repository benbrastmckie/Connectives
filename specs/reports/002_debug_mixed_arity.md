# Debug Report: Mixed-Arity Composition Failures

## Metadata
- **Date**: 2025-10-02
- **Issue**: Independence checker fails to detect compositions involving mixed arities
- **Severity**: High
- **Type**: Debugging investigation
- **Related Reports**: None
- **Related Plan**: specs/plans/001_nice_connectives_solver.md (Phase 3)

## Problem Statement

The independence checker in `/home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/src/independence.py` fails to detect when a target connective is definable through compositions that involve mixed arities. Specifically:

- **Test Failures**: 10 out of 29 tests failing in `test_independence.py`
- **Primary Issue**: Cannot detect NAND(x,y) = NOT(AND(x,y)) - applying unary NOT to binary AND
- **Secondary Issue**: Cannot detect OR(x,y) = NOT(AND(NOT(x), NOT(y))) - De Morgan's Law requiring nested mixed-arity applications

### Impact
This bug blocks the core functionality of Phase 3, preventing the solver from correctly identifying independent sets of connectives. Without accurate independence checking, the nice connectives search will produce incorrect results.

## Investigation Process

### 1. Test Execution and Failure Analysis
Ran the test suite to identify failure patterns:
```bash
pytest tests/test_independence.py -v
```

**Results**: 19/29 passing, 10/29 failing

**Failed Tests**:
1. `test_or_from_not_and` - OR definable from {NOT, AND} via De Morgan
2. `test_nand_from_not_and` - NAND = NOT(AND(x,y))
3. `test_xor_from_and_or_not` - XOR requires mixed-arity compositions
4. `test_projection_independent_from_and_or` - False negative
5. `test_not_and_or_redundant` - Fails to detect OR redundancy
6. `test_or_redundant_in_complete_set` - Same root cause
7. `test_subset_removes_redundant` - Fails to remove OR from {NOT, AND, OR}
8. `test_de_morgan_or` - Duplicate of test 1
9. `test_de_morgan_and` - AND from {NOT, OR}
10. `test_depth_limit_affects_result` - Depth 3 should find OR

### 2. Code Flow Analysis

Traced the execution path for `is_definable(NAND, [NOT, AND], max_depth=2)`:

**Expected Behavior**: Should return `True` because NAND(x,y) = NOT(AND(x,y))

**Actual Behavior**: Returns `False`

**Execution Flow**:
1. `is_definable()` iterates through depths 1 to 2
2. **Depth 1**: `_check_depth_one()`
   - Checks only same-arity matches (lines 94-103)
   - NOT (arity=1) ≠ NAND (arity=2), skipped
   - AND (arity=2) = NAND (arity=2), checks permutations, no match
   - Returns `False`
3. **Depth 2**: `_check_composition_enumeration()`
   - Target arity is 2, calls `_check_binary_compositions()`
   - In `_check_binary_compositions()` (lines 187-213):
     - Extracts `binary_basis = [AND]` and `unary_basis = [NOT]`
     - Line 207: `for f in binary_basis:` - **ONLY iterates over binary functions**
     - Never considers unary outer functions
   - Returns `False`

### 3. Root Cause Identification

**Primary Root Cause**: Incomplete composition enumeration in `_check_binary_compositions()`

The function at lines 200-213 only enumerates composition patterns where the outer function `f` is binary:

```python
# Line 207-211 (independence.py)
for f in binary_basis:  # <-- ONLY BINARY outer functions!
    for g in binary_basis + unary_basis + [None]:
        for h in binary_basis + unary_basis + [None]:
            if _try_composition_f_g_h(target, f, g, h):
                return True
```

**Missing Patterns**:
1. **Unary outer, binary inner**: `NOT(AND(x,y))` - depth 2
2. **Unary outer, binary middle, unary inner**: `NOT(AND(NOT(x), NOT(y)))` - depth 3
3. **Binary outer, unary applied to each input**: `AND(NOT(x), NOT(y))` - depth 2

The code assumes compositions for binary targets must have binary outer functions, but this is mathematically incorrect. A binary target can absolutely be expressed as a unary function applied to a binary intermediate result.

### 4. Secondary Issues

**Issue in `_try_composition_f_g_h()`** (lines 216-262):
- Hardcoded to expect binary outer function `f` (line 256: `f.evaluate((g_result, h_result))`)
- Cannot handle unary outer functions
- The structure `f(g(...), h(...))` assumes arity-2 for `f`

**Issue in `_check_depth_one()`** (lines 77-103):
- Lines 91-103: Only checks same-arity matches
- Comment on line 99-101 acknowledges mixed-arity cases are "deferred to composition enumeration"
- But composition enumeration doesn't handle them either!

## Findings

### Root Cause Analysis

The independence checker uses a **simplified composition enumeration approach** that only handles same-arity outer functions. The code was designed with a "binary-to-binary" assumption, never enumerating compositions where:
- A unary function is applied to a binary result
- A binary function is applied to two unary results
- Higher-order nesting of mixed arities

This is evident from:
1. The loop structure at line 207 restricting `f` to `binary_basis`
2. The `_try_composition_f_g_h` signature assuming binary `f`
3. The comment at line 177: "This is a simplified version that checks common cases"

### Contributing Factors

1. **Conservative Approximation**: Line 184 returns `False` for non-binary targets, suggesting the implementation is incomplete
2. **Lack of General Tree Enumeration**: The code doesn't build full expression trees; it only checks specific patterns
3. **Insufficient Test Coverage During Development**: These fundamental cases should have been caught earlier

### Evidence

**Code Evidence** (independence.py):
- Line 72-74: Comment admits "enumerate all possible expression trees" but doesn't actually do this
- Line 177-178: Explicitly states "simplified version that checks common cases"
- Line 183-184: Non-binary arities return `False` conservatively
- Line 207: `for f in binary_basis:` is the smoking gun

**Test Evidence**:
- 10/29 tests failing, all involving mixed-arity compositions
- Zero false positives (no tests incorrectly detecting non-existent compositions)
- All failures are false negatives (missing valid compositions)

## Proposed Solutions

### Option 1: Extend Pattern Enumeration (Recommended)

**Description**: Augment `_check_binary_compositions()` to enumerate additional mixed-arity patterns.

**Implementation Approach**:
1. Add enumeration for unary outer functions:
   ```python
   # Check unary(binary(x,y)) patterns
   for f in unary_basis:
       for g in binary_basis:
           if _try_unary_binary_composition(target, f, g):
               return True
   ```

2. Add enumeration for binary outer with unary inners:
   ```python
   # Check binary(unary(x), unary(y)) patterns
   for f in binary_basis:
       for g in unary_basis + [None]:
           for h in unary_basis + [None]:
               if _try_binary_unary_unary_composition(target, f, g, h):
                   return True
   ```

3. Create helper functions:
   - `_try_unary_binary_composition(target, f_unary, g_binary)` - for NAND case
   - `_try_binary_unary_unary_composition(target, f_binary, g_unary, h_unary)` - for depth 2 with unary inners

4. For depth 3+, enumerate nested patterns:
   - `unary(binary(unary(x), unary(y)))` - for De Morgan's Law

**Pros**:
- Targeted fix for known failing patterns
- Preserves existing code structure
- Can be implemented incrementally (start with depth 2, then depth 3)
- Relatively low risk of introducing new bugs

**Cons**:
- Still not a general solution (will miss other exotic patterns)
- Code becomes more complex with many special cases
- May need additional patterns for ternary+ connectives

**Estimated Effort**: 2-4 hours
**Risk Level**: Low
**Confidence**: High

### Option 2: General Expression Tree Enumeration

**Description**: Replace pattern-based checking with full expression tree generation and evaluation.

**Implementation Approach**:
1. Define expression tree data structure:
   ```python
   class ExprNode:
       connective: Connective
       children: List[Union[ExprNode, Variable]]
   ```

2. Implement recursive tree generator:
   ```python
   def generate_trees(basis, depth, target_arity):
       """Generate all valid expression trees up to depth."""
       if depth == 0:
           return [Variable(i) for i in range(target_arity)]

       trees = []
       for conn in basis:
           for child_combo in combinations_with_replacement(
               generate_trees(basis, depth-1, target_arity),
               conn.arity
           ):
               trees.append(ExprNode(conn, child_combo))
       return trees
   ```

3. Evaluate each tree against target truth table

4. Handle variable substitution and projection

**Pros**:
- Complete solution handling all arities and depths
- Mathematically correct and principled
- Future-proof for ternary+ connectives
- Eliminates need for special-case patterns

**Cons**:
- Significantly more complex to implement correctly
- Explosion of tree count at higher depths (exponential growth)
- Performance concerns (may need aggressive caching/memoization)
- Higher risk of bugs in tree generation logic
- Requires refactoring substantial portions of independence.py

**Estimated Effort**: 8-16 hours
**Risk Level**: Medium-High
**Confidence**: Medium (correct but may have performance issues)

### Option 3: Z3-Based Symbolic Composition Search

**Description**: Use Z3 to symbolically encode composition operations and search for valid compositions.

**Implementation Approach**:
1. Encode each basis function as Z3 constraints
2. Create symbolic "composition tree" variables in Z3
3. Add constraints: tree structure, arity matching, depth bounds
4. Assert: composed function equals target function on all inputs
5. Check satisfiability with Z3 solver

**Pros**:
- Leverages Z3's powerful constraint solving
- Automatically handles all patterns without enumeration
- Can optimize search with Z3 tactics
- Conceptually elegant

**Cons**:
- Complex Z3 encoding for variable-arity functions
- Z3 performance may be poor for this problem domain
- Difficult to debug when solver returns "unknown"
- Requires deep Z3 expertise
- Original plan (line 68-69) intended bounded composition, not full Z3

**Estimated Effort**: 16-24 hours
**Risk Level**: High
**Confidence**: Low (may hit Z3 performance limits)

## Recommendations

**Primary Recommendation**: Implement **Option 1 (Extend Pattern Enumeration)** immediately to unblock Phase 3.

**Rationale**:
1. **Urgency**: Phase 3 is blocked; need a quick fix
2. **Risk**: Low risk of breaking existing functionality
3. **Scope**: Addresses all current test failures
4. **Incremental**: Can start with depth 2 patterns (NAND case), then add depth 3 (De Morgan)

**Implementation Priority**:
1. **High Priority**: Add `unary(binary(x,y))` pattern (fixes 6/10 failing tests)
2. **High Priority**: Add `binary(unary(x), unary(y))` pattern (fixes 2/10 additional tests)
3. **Medium Priority**: Add `unary(binary(unary(x), unary(y)))` pattern (fixes remaining 2/10 tests)
4. **Low Priority (Future)**: Consider Option 2 when extending to ternary+ connectives

**Secondary Recommendation**: Document the limitation and plan for Option 2 in Phase 5.

Add a comment in the code acknowledging the pattern-based approach is incomplete:
```python
# NOTE: This implementation uses pattern enumeration rather than full tree
# generation. It handles common mixed-arity patterns but may miss exotic cases.
# For ternary+ connectives, consider implementing general tree enumeration.
```

Add to Phase 5 tasks in the implementation plan:
- Evaluate need for general tree enumeration based on ternary connective results
- If pattern enumeration becomes unwieldy, refactor to Option 2

## Next Steps

### Immediate Actions (Option 1 Implementation)
1. Create `_try_unary_binary_composition()` helper function
2. Create `_try_binary_unary_unary_composition()` helper function
3. Add enumeration loops in `_check_binary_compositions()` for:
   - Unary outer, binary inner (depth 2)
   - Binary outer, unary inners (depth 2)
4. Extend to depth 3 with `_try_unary_binary_unary_unary_composition()`
5. Run full test suite to verify all 29/29 tests pass

### Testing
- Verify all 10 currently failing tests now pass
- Add edge case tests:
  - Multiple unary applications: NOT(NOT(AND(x,y)))
  - Chained mixed-arity: AND(NOT(OR(x,y)), z) (for ternary)
- Performance test: Ensure depth 3-4 searches complete in <1 second

### Documentation
- Update docstrings in independence.py to note mixed-arity support
- Add examples to docstrings showing NAND and De Morgan cases
- Update Phase 3 completion status in implementation plan

### Future Considerations
- Monitor pattern enumeration complexity in Phase 5 (ternary connectives)
- If pattern count exceeds ~10 special cases, prioritize Option 2 refactoring
- Consider hybrid approach: patterns for common cases, tree enumeration for rare cases

## References

### Affected Files
- `/home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/src/independence.py` (lines 187-213 primary issue)
- `/home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/tests/test_independence.py` (10 failing tests)

### Related Documentation
- Implementation Plan: `/home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/specs/plans/001_nice_connectives_solver.md`
- Phase 3 Objective: "Implement Z3-based definability checking with bounded depth"

### Key Functions to Modify
- `_check_binary_compositions()` - Add new enumeration loops
- Create new: `_try_unary_binary_composition()`
- Create new: `_try_binary_unary_unary_composition()`
- Create new: `_try_unary_binary_unary_unary_composition()` (depth 3)

### Mathematical Background
- **De Morgan's Laws**: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q and ¬(P ∨ Q) ≡ ¬P ∧ ¬Q
- **Function Composition**: Applying f:B→B to g:B²→B yields h:B²→B where h(x,y) = f(g(x,y))
- **Arity Mismatch**: Composition requires inner function output arity to match outer function input arity
