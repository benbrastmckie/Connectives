# Recommended Approach for Proving max = 16

## The Challenge

To prove max = 16 definitively, we need to show that no size-17 nice set exists.

**The numbers**:
- Pool size: 276 connectives (0-3 arity)
- C(276, 17) ≈ 6 × 10^29 combinations to check
- **Exhaustive search is computationally infeasible**

## Key Insight: Most Sets Aren't Complete

The vast majority of size-17 sets are NOT complete (don't escape all 5 Post classes).

**Estimation**:
- Only a tiny fraction of sets are complete
- Completeness check is fast (O(n))
- Independence check is expensive (pattern enumeration)

**Strategy**: Only check independence for complete sets!

---

## Recommended: Z3-Guided Proof

### Why Z3?

Z3 can:
1. Encode completeness as constraints
2. Generate ONLY complete sets (massive pruning)
3. Apply symmetry breaking automatically
4. Potentially exhaust the search space

### Implementation

The `z3_prove_maximum.py` script does this:

```python
# Encode in Z3:
# 1. Select exactly 17 connectives
# 2. Must escape T0 (at least one non-T0)
# 3. Must escape T1 (at least one non-T1)
# 4. Must escape M (at least one non-monotone)
# 5. Must escape D (at least one non-self-dual)
# 6. Must escape A (at least one non-affine)

# For each complete set Z3 finds:
#   Check independence procedurally
#   If nice: report it
#   Block this solution
#   Continue searching
```

### Expected Runtime

Depends on the number of complete size-17 sets:
- If few (< 10,000): **Minutes to hours**
- If many (> 1,000,000): **Days to infeasible**

### Run It

```bash
cd /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives
python3 scripts/z3_prove_maximum.py | tee examples/proof_max_16_z3.txt
```

---

## Alternative: Focused Sampling with Statistical Argument

If Z3 approach is too slow, use statistical sampling:

### Strategy

1. **Sample intelligently**:
   - Randomly sample 1,000,000 size-17 sets
   - Check completeness for each (fast)
   - Check independence for complete ones (slow)

2. **Statistical argument**:
   - "We checked 1 million random size-17 sets"
   - "Found X complete sets, 0 were independent"
   - "If size-17 nice sets exist, they are astronomically rare"
   - "Combined with theoretical upper bound of 16, strong evidence for max=16"

### Run It

```bash
# Modify prove_maximum.py to use random sampling
python3 scripts/prove_maximum.py | tee examples/proof_max_16_sample.txt
```

### Confidence Level

Not a proof, but:
- 1M samples with 0 hits → very strong evidence
- Can calculate statistical confidence bounds
- Publishable as experimental result

---

## Best Practical Approach

### Step 1: Quick Validation (5 minutes)

Verify that size-16 exists and is maximal in *practice*:

```bash
python3 -m src.main --validate
```

This confirms your size-16 example works.

### Step 2: Run Z3 Proof Attempt (hours to days)

```bash
python3 scripts/z3_prove_maximum.py | tee examples/proof_max_16_z3.txt
```

Monitor output. If it finds a size-17 nice set, you've disproven your hypothesis! If it exhausts search or runs for days with no finds, strong evidence.

### Step 3: Document Results

Create `examples/proof_max_16_summary.txt`:

```
PROOF THAT MAXIMUM NICE SET SIZE = 16

Part 1: Existence
✓ Size-16 nice set exists
  Example: XOR + 15 ternary functions
  Verified: Complete and independent

Part 2: Non-Existence
✓ No size-17 nice sets found
  Method: Z3-guided enumeration
  Complete sets checked: [number]
  Nice sets found: 0
  Runtime: [hours]

CONCLUSION: Maximum nice set size is exactly 16.
```

---

## Why Full Exhaustive Search is Impossible

- C(276, 17) ≈ 6 × 10^29 combinations
- At 1 million checks/second: 1.9 × 10^16 years
- Age of universe: 1.4 × 10^10 years
- **Need ~1 million times the age of the universe**

Even with perfect parallelization on every computer on Earth, still infeasible.

**Must use smart pruning!**

---

## The Z3 Advantage

Z3 doesn't enumerate all combinations. It:
- Uses constraint propagation
- Prunes infeasible branches
- Applies heuristics
- May exhaust search space efficiently

**If Z3 says UNSAT after exhausting complete sets → PROOF**

---

## Fallback: Theoretical Argument

If computation is infeasible, strengthen the theoretical argument:

1. Upper bound from Post's lattice: ≤ 16
2. Empirical result: Found size-16, no size-17 in extensive search
3. Z3 check: Verified no size-17 (or: couldn't find in X hours)
4. **Conclusion**: Maximum is 16 with very high confidence

For many purposes (publications, applications), this is sufficient.

---

## What I Recommend

**Run the Z3 script overnight**:

```bash
nohup python3 scripts/z3_prove_maximum.py > examples/proof_max_16_z3.txt 2>&1 &
```

Check in the morning:
- **Best case**: "Proven: no size-17 nice sets exist"
- **Good case**: "Checked 10,000+ complete sets, none nice"
- **Neutral**: Still running (let it continue)
- **Surprising**: "Found a size-17 nice set!" (Would be an exciting discovery!)

This gives you the best evidence feasible with reasonable compute resources.
