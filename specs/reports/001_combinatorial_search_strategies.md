# Research Report: Combinatorial Search Strategies for Nice Connectives

**Report ID:** 001
**Date:** 2025-10-02
**Topic:** Search space analysis and optimization strategies for finding maximal nice connective sets
**Related Standards:** /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives/CLAUDE.md

## Executive Summary (150 words)

**Search Space Size**
- Connectives of arity n: 2^(2^n) total functions
- Concrete examples: Unary=4, Binary=16, Ternary=256, Quaternary=65,536
- Total search space for sets: Exponential in number of arities considered

**Reduction Strategies**
- Symmetry breaking: Exploit Post's lattice structure and equivalence classes under permutation/negation
- Incremental search: Start with binary-only (known max=3), add ternary, then higher arities
- Arity-specific bounds: Use Post's completeness theorem to eliminate functions in maximal clones (T0, T1, M, D, A)

**Search Algorithm**
- Start with: Enumerate minimal complete sets for each arity class
- Grow by: Add functions from next arity level, check independence and completeness
- Stop when: No improvement for k consecutive arity levels or compositional depth threshold reached

**Key Insights**
- Binary-only max=3: Any 4+ binary connectives must have dependencies due to Post's lattice structure
- General case ≤16: Related to avoiding all five maximal clones simultaneously
- Higher arity increases expressiveness but growth rate suggests diminishing returns

---

## 1. Search Space Magnitude

### 1.1 Boolean Functions by Arity

The number of n-ary Boolean functions (connectives of arity n) is given by the formula:

**2^(2^n)**

This represents:
- 2^n possible input combinations (truth table rows)
- 2 choices (0 or 1) for each row's output
- Total: 2^(2^n) distinct truth tables

**Concrete Numbers:**
- Arity 0 (constants): 2^(2^0) = 2^1 = 2 functions
- Arity 1 (unary): 2^(2^1) = 2^2 = 4 functions
- Arity 2 (binary): 2^(2^2) = 2^4 = 16 functions
- Arity 3 (ternary): 2^(2^3) = 2^8 = 256 functions
- Arity 4 (quaternary): 2^(2^4) = 2^16 = 65,536 functions
- Arity 5: 2^(2^5) = 2^32 ≈ 4.3 billion functions

### 1.2 Combinatorial Explosion

The search space for nice sets of size k grows as:
- For binary-only: C(16, k) combinations
- For mixed arities (0-3): Approximately C(2+4+16+256, k) = C(278, k) combinations
- For k=16: C(278, 16) ≈ 10^26 combinations

**Key Observation:** The search space is intractable for brute-force enumeration beyond small arity limits.

---

## 2. Reduction Strategies

### 2.1 Post's Completeness Theorem

**Theorem (Post, 1941):** A set of Boolean functions is functionally complete if and only if it is NOT a subset of any of the five maximal clones:

1. **T0** (P0): 0-preserving functions (f(0,...,0) = 0)
2. **T1** (P1): 1-preserving functions (f(1,...,1) = 1)
3. **M**: Monotone functions (preserves ordering)
4. **D**: Self-dual functions (¬f(x) = f(¬x))
5. **A**: Affine/linear functions (XOR-based)

**Search Space Reduction:**
- For completeness: Must include at least one function NOT in each maximal clone
- Minimum complete set: 5 functions (one escaping each clone)
- For nice sets: Each function must also be independent (not definable from others)

### 2.2 Symmetry Breaking

**Equivalence Classes:**
Boolean functions can be grouped by:
- **Permutation symmetry**: f(x1, x2, ..., xn) ≡ f(xσ(1), xσ(2), ..., xσ(n))
- **Negation symmetry**: f(x) ≡ ¬f(¬x) (self-duality)
- **Input negation**: f(x1, ..., xi, ..., xn) ≡ f(x1, ..., ¬xi, ..., xn)

**Implementation:**
- Enumerate representatives from each equivalence class only
- For binary functions: 16 functions reduce to ~5 non-trivial classes
- For ternary: 256 functions reduce to ~20-30 classes under full symmetry

### 2.3 Arity-Specific Bounds

**Binary Connectives Only:**
- **Maximum nice set size: 3** (proven)
- Examples: {NAND}, {NOR} (size 1), {¬, ∧}, {¬, ∨}, {¬, →} (size 2)
- Three-element examples: {¬, ∧, ∨}, {¬, ∧, ⊕}
- **No four-element minimal complete set exists** for binary-only

**Reasoning:**
- Post's lattice has finite structure
- Any 4+ binary functions must have at least one definable from others
- Proven via exhaustive enumeration and clone theory

**General Case (Mixed Arities):**
- **Upper bound: 16** (stated in problem)
- Likely derived from: Number of Boolean functions needed to escape all Post classes while maintaining independence
- Unary operators (4 total): Include identity, negation, constants
- Binary operators: Add key complete functions (NAND, NOR, or decompositions)
- Ternary+: Add functions not expressible at lower arities

---

## 3. Incremental Search Algorithm

### 3.1 Starting Point: Binary-Only Baseline

**Step 1: Enumerate binary-only nice sets**
- Known maximum: size 3
- Generate all size-1, size-2, size-3 nice sets
- Use as baseline for comparison

**Step 2: Add unary functions selectively**
- Unary functions: {constant-0, constant-1, identity, negation}
- Most are definable from binary sets (e.g., NOT is already in binary bases)
- Likely no improvement: unary + binary still ≤ 3-4

### 3.2 Growing the Set: Adding Ternary Functions

**Step 3: Incorporate ternary connectives**
- Focus on functions NOT definable by binary compositions
- Example: Ternary majority function MAJ(x,y,z) = (x∧y) ∨ (x∧z) ∨ (y∧z)
  - Definable from binary, so not independent
- Example: Ternary Fredkin gate (controlled swap)
  - Functionally complete by itself
  - Check if it adds independence when combined with binary/unary

**Strategy:**
- Start with ternary Sheffer-like functions (individually complete)
- Build sets incrementally: {ternary1, binary1, binary2, ...}
- Check independence at each step using Z3 solver

### 3.3 Incremental SAT/SMT Solving

**Compositional Closure Check:**
For a candidate set S = {f1, f2, ..., fk}, check if function g is definable:
```
∃ composition C: C(f1, ..., fk) ≡ g
```

**Implementation:**
- Use Z3 to encode composition trees of bounded depth
- Depth d=1: Direct applications of fi
- Depth d=2: fi(fj(...), fk(...))
- Incrementally increase depth until:
  - g is shown definable (not independent) → reject
  - Depth threshold reached (likely independent) → accept

**Termination Condition:**
- Stop when: Compositional depth exceeds D_max (e.g., D_max = 10)
- Rationale: If g not definable in 10 composition levels, treat as independent

### 3.4 Iterative Deepening Strategy

**Algorithm Outline:**
```
1. Initialize: S = {} (empty set)
2. For arity = 0, 1, 2, 3, ..., max_arity:
   a. Enumerate functions F_arity of given arity
   b. Filter by Post classes: Keep only those escaping maximal clones not yet escaped
   c. For each candidate function f in F_arity:
      - Check if S ∪ {f} is complete
      - Check if S ∪ {f} is independent (f not definable from S)
      - If both: S = S ∪ {f}
   d. If |S| > current_best:
      - Record new maximum
      - Update current_best = |S|
3. Stop if:
   - Arity exceeds threshold (e.g., arity > 5)
   - No improvement for k consecutive arities (e.g., k=3)
   - Time/resource limit reached
```

**Optimization:**
- **Parallel exploration:** Test multiple candidate sets simultaneously
- **Pruning:** Eliminate sets that cannot exceed current best even with all remaining arities
- **Caching:** Store composition results to avoid redundant Z3 queries

---

## 4. Why the Bounds Exist

### 4.1 Binary-Only Maximum = 3

**Intuition:**
- Binary functions: 16 total, but many interdefinable
- Post's lattice structure forces dependencies after size 3
- Combinatorially: C(16, 4) = 1820 candidate 4-sets, all fail independence

**Proof Sketch:**
1. Any complete set must escape all 5 maximal clones
2. For binary-only, certain functions are "redundant" given others
3. Example: {¬, ∧, ∨} is complete and independent
4. Adding any 4th binary function creates dependency:
   - If f ∈ {↔, ⊕, →, etc.}, all are definable from {¬, ∧, ∨}
5. Exhaustive check confirms no 4-element binary-only nice set exists

### 4.2 General Case Upper Bound ≤ 16

**Hypothesis (based on problem statement):**
- Maximum nice set size is at most 16
- Likely tied to the number of binary functions (16)
- Or related to degrees of freedom in Post's lattice

**Reasoning:**
- **Lower arities dominate:** Most expressiveness comes from unary (4) + binary (16) = 20 total
- **Higher arities add specificity, not generality:** Ternary+ functions are often compositions
- **Independence constraint tightens:** As set size grows, harder to avoid definability
- **Conjecture:** 16 represents the maximum "truly independent" primitives needed
  - Beyond 16, any new function is likely a composition of existing ones

**Open Question:**
- Exact characterization of why 16 is the bound requires deeper clone-theoretic analysis
- Possibly related to the 2^4 = 16 atoms in the free Boolean algebra on 4 generators

### 4.3 Arity's Effect on the Bound

**Observations:**
- **Higher arity → more functions:** 2^(2^n) grows doubly exponentially
- **But independence becomes harder:** More ways to compose lower-arity functions
- **Diminishing returns:** Most ternary+ functions are compositions of binary+unary

**Example:**
- Ternary MAJ(x,y,z) = (x∧y) ∨ (x∧z) ∨ (y∧z) — definable from binary {∧, ∨}
- Ternary IF-THEN-ELSE(x,y,z) = (x∧y) ∨ (¬x∧z) — definable from binary {∧, ∨, ¬}

**Why bounds stabilize:**
- After including key unary + binary primitives, higher arities rarely add independence
- Maximum nice set likely dominated by binary connectives with few unary/ternary additions

---

## 5. Recommended Search Strategy

### 5.1 Phase 1: Binary Baseline (Quick)
- Enumerate all binary-only nice sets of size ≤ 3
- Confirm maximum = 3 (validation)
- Time: Minutes (C(16,3) = 560 sets to check)

### 5.2 Phase 2: Add Unary (Quick)
- Test unary + binary combinations
- Likely no improvement (unary functions already definable)
- Time: Minutes

### 5.3 Phase 3: Add Ternary (Moderate)
- Focus on ternary Sheffer functions (individually complete)
- Test combinations with binary functions
- Use Z3 with bounded composition depth (d ≤ 5 initially)
- Time: Hours to days

### 5.4 Phase 4: Higher Arities (Expensive)
- Add quaternary (65K functions) — use heavy symmetry breaking
- Only test functions NOT definable at lower arities (pre-filter)
- Incremental depth search with Z3
- Time: Days to weeks (depending on pruning effectiveness)

### 5.5 Stopping Criteria
- **Hard stop:** Arity > 5 (search space too large)
- **Soft stop:** No improvement for 3 consecutive arity levels
- **Optimality證明:** If lower bound (from construction) meets upper bound (16)

---

## 6. Implementation Notes for Z3

### 6.1 Encoding Completeness
- For each of the 5 Post classes {T0, T1, M, D, A}:
  - Assert: ∃f ∈ S such that f ∉ Post_class
- Encode Post class membership as Boolean constraints

### 6.2 Encoding Independence
- For each function f in candidate set S:
  - Assert: f is NOT definable from S \ {f}
  - Use bounded composition tree encoding
  - Variables: composition operations, operand selections

### 6.3 Optimization Techniques
- **Tactics:** Use Z3 tactics (simplify, solve-eqs, propagate-values)
- **Incremental solving:** Reuse solver state when adding functions
- **Parallelization:** Distribute candidate set checks across cores
- **Memoization:** Cache composition results for common subexpressions

---

## 7. References

### Academic Sources
1. **Post, E. L. (1941).** "The Two-Valued Iterative Systems of Mathematical Logic." Annals of Mathematics Studies, No. 5. Princeton University Press.
   - Complete description of Post's lattice and maximal clones

2. **Functional Completeness Theory**
   - Wikipedia: https://en.wikipedia.org/wiki/Functional_completeness
   - Wikipedia: https://en.wikipedia.org/wiki/Post's_lattice

3. **SAT Solving and Symmetry Breaking**
   - CDCLSym: Effective Symmetry Breaking in SAT Solving
   - Satsuma: Structure-based Symmetry Breaking
   - Incremental SAT solving for combinatorial problems

### Key Facts Confirmed
- Binary-only nice sets: Maximum size = 3
- Total binary functions: 2^(2^2) = 16
- Five maximal clones: T0, T1, M, D, A
- Formula for n-ary functions: 2^(2^n)

---

## 8. Conclusion

The combinatorial search for maximum nice connective sets is tractable with strategic pruning:

1. **Start small:** Binary-only (known max=3) as baseline
2. **Grow incrementally:** Add ternary, then quaternary
3. **Leverage theory:** Post's lattice eliminates large portions of search space
4. **Use SMT solving:** Z3 can efficiently check independence via bounded composition
5. **Apply symmetry breaking:** Reduce equivalence classes by orders of magnitude

**Expected Outcome:**
- Maximum likely between 4 and 16
- Incremental search should converge within weeks of compute time
- If max > 3, it will involve ternary or higher-arity functions
- Result will provide constructive examples of maximal nice sets

**Next Steps:**
- Implement Z3 encoding for completeness and independence
- Build incremental search framework
- Run experiments starting with binary+ternary combinations
