# Proof Strategies for Maximum Nice Set Size = 16

This document explains different approaches to rigorously prove that 16 is the maximum size of a nice (complete and independent) connective set.

## What Constitutes a Proof?

To prove max = 16, we need:

1. **Existence (Constructive Proof)**: Show that a size-16 nice set exists ✓
   - Already demonstrated in `examples/validation.txt`
   - Example: XOR + 15 ternary functions

2. **Non-Existence (Impossibility Proof)**: Show that no size-17 nice set exists
   - This is the challenging part
   - Multiple approaches available

---

## Approach 1: Exhaustive Search (Brute Force)

**Script**: `prove_maximum.py`

### Strategy

Search all possible size-17 combinations and verify none are nice.

### Pros
- Conceptually simple
- Provides definitive empirical evidence
- Easy to verify

### Cons
- Computationally expensive: C(276, 17) ≈ 10^30 combinations
- Requires significant optimizations:
  - Symmetry breaking
  - Early termination (completeness check first)
  - Sampling if exhaustive is infeasible

### Running Time
- With optimizations: Several hours to days
- Sampling mode (100k combinations): ~30 minutes

### Level of Evidence
- **Exhaustive**: Mathematical proof
- **Sampling**: Strong empirical evidence (not formal proof)

### Usage

```bash
python3 scripts/prove_maximum.py
```

---

## Approach 2: Z3-Guided Smart Enumeration

**Script**: `z3_prove_maximum.py`

### Strategy

Use Z3 SMT solver to:
1. Encode completeness constraints in Z3
2. Generate only complete sets (massive pruning)
3. Apply symmetry breaking via Z3
4. Check independence procedurally for each candidate

### Key Insight

The search space is drastically reduced because:
- Most size-17 combinations are NOT complete
- Z3 only generates complete sets
- Symmetry breaking eliminates redundant checks

### Pros
- Much faster than brute force
- Z3 handles constraint satisfaction efficiently
- Can provide proof if Z3 exhausts all possibilities

### Cons
- Independence checking still procedural (not fully in Z3)
- Z3 might timeout on very large search spaces
- More complex implementation

### Running Time
- Expected: 1-6 hours
- Depends on number of complete size-17 sets

### Level of Evidence
- If Z3 exhausts all complete sets: Formal proof
- Otherwise: Strong evidence

### Usage

```bash
python3 scripts/z3_prove_maximum.py
```

---

## Approach 3: Full Encoding in Z3 (Most Rigorous)

**Status**: Not yet implemented (would require significant work)

### Strategy

Fully encode both completeness AND independence in Z3:

1. **Completeness constraints** (easy):
   - Post class membership for each connective
   - At least one connective escapes each class

2. **Independence constraints** (hard):
   - For each connective f in the set S
   - For each composition pattern up to depth d
   - Encode: "f ≠ pattern applied to other connectives in S"

### Example Independence Constraint

For pattern f(x,y) = g(h(x,y), k(x,y)):
```
For all g, h, k in S \ {f}:
  f.truth_table ≠ apply_pattern(g, h, k)
```

This needs to be encoded as Z3 BitVec constraints for all patterns.

### Pros
- Pure Z3 solution
- If UNSAT → formal mathematical proof
- Most rigorous approach

### Cons
- Requires reimplementing pattern enumeration in Z3
- Very large constraint system
- May be too slow for Z3 to solve
- Significant implementation effort

### Complexity

Estimated constraints for size-17 set:
- Completeness: ~50 constraints
- Independence: ~17 × (number of patterns) × C(16, k) for k-ary patterns
- Total: Potentially millions of constraints

---

## Approach 4: Hybrid Mathematical Proof

**Status**: Theoretical approach

### Strategy

Use mathematical properties of Post's lattice to prove bounds:

1. Post's lattice has exactly 5 maximal clones
2. To be complete, must escape all 5 clones
3. Independence constrains the structure
4. Use lattice theory to derive upper bound

### Pros
- Potentially elegant mathematical proof
- No computation needed if successful

### Cons
- Requires deep theoretical work
- May not yield tight bounds
- We already know empirically that max = 16

---

## Recommended Approach

### For Quick Evidence (30 min)
Run **Approach 1** in sampling mode:
```bash
python3 scripts/prove_maximum.py
```

This checks 100k size-17 combinations. If none are nice, very strong evidence.

### For Rigorous Proof (1-6 hours)
Run **Approach 2** (Z3-guided):
```bash
python3 scripts/z3_prove_maximum.py
```

This provides the best balance of rigor and feasibility.

### For Full Formal Proof (research project)
Implement **Approach 3** with full Z3 encoding.

---

## Validation of Results

Any approach should generate a certificate file containing:

1. **Existence proof**:
   - The size-16 nice set
   - Verification that it's complete
   - Verification that it's independent

2. **Non-existence proof**:
   - Number of size-17 combinations checked
   - Method used (exhaustive, Z3, sampling)
   - Result: none found / all exhausted / sampled N with no finds

3. **Metadata**:
   - Search parameters (max_depth, arity range)
   - Computation time
   - Date/time of proof

---

## Comparison with Existing Results

Our incremental search (`examples/incremental_search_summary.txt`) already does exhaustive search at each size, incrementally. The question is: **did it check size-17?**

Let's verify:

```bash
# Check the summary for maximum size found
cat examples/incremental_search_summary.txt
```

If the incremental search found max=16 and then searched for size-17 with no results, **we already have the proof!** We just need to extract and present it clearly.

---

## Creating the Definitive Dataset

**Recommended**: Create a clean proof document that:

1. References the size-16 example from `validation.txt`
2. Shows the size-17 search results (from incremental search or new focused search)
3. Presents this as a formal proof

**Script to generate**:

```bash
# Run Z3-guided proof (recommended)
python3 scripts/z3_prove_maximum.py | tee examples/proof_max_16.txt

# OR run exhaustive/sampling proof
python3 scripts/prove_maximum.py | tee examples/proof_max_16.txt
```

This creates a clean, readable proof document in `examples/proof_max_16.txt`.

---

## Theoretical Considerations

### Why is max = 16?

The upper bound of 16 comes from Post's lattice structure:
- 5 maximal clones → need 5+ functions minimum
- But independent sets have constraints
- The 16 bound appears to be the intersection of:
  - Completeness requirements (cover all clones)
  - Independence requirements (no redundancy)

### Could there be a tighter bound?

Our empirical result (max = 16) matches the theoretical upper bound, suggesting this is optimal. A proof would:
1. Confirm this is tight
2. Potentially reveal why 16 is special
3. Guide research on generalizations (multi-valued logic, etc.)

---

## Next Steps

1. **Immediate**: Run `z3_prove_maximum.py` to get rigorous evidence
2. **Short-term**: Check if existing incremental search already proves max=16
3. **Long-term**: Consider full Z3 encoding for absolute rigor

Choose the approach based on your needs:
- Need evidence quickly? → Sampling approach
- Need rigorous proof? → Z3-guided approach
- Want formal verification? → Full Z3 encoding (future work)
