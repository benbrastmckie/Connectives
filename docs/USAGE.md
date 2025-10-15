# Usage Guide

Complete guide for using the Nice Connectives Solver.

**Prerequisites:** See [INSTALLATION.md](INSTALLATION.md) for installation instructions.

---

## Table of Contents

- [Quick Reference](#quick-reference)
- [Command Structure](#command-structure)
- [Search Commands](#search-commands)
- [Proof Commands](#proof-commands)
- [Validation Commands](#validation-commands)
- [Benchmark Commands](#benchmark-commands)
- [Understanding Output](#understanding-output)
- [Definability Modes](#definability-modes)
- [Common Workflows](#common-workflows)
- [Advanced Usage](#advanced-usage)
- [Performance Tips](#performance-tips)
- [Troubleshooting](#troubleshooting)

---

## Quick Reference

### Interactive Learning

**New to the project?** Try the interactive Jupyter notebooks:

```bash
# Install Jupyter dependencies
pip install -e ".[jupyter]"

# Launch notebooks
cd notebooks/
jupyter notebook

# Open 00_setup_and_basics.ipynb to begin
```

See **[JUPYTER.md](JUPYTER.md)** for complete Jupyter usage guide and **[notebooks/README.md](../notebooks/README.md)** for learning paths.

### Most Common Commands

```bash
# Validate implementation with known results
python -m src.cli search validate

# Reproduce classical binary-only result (max = 3)
python -m src.cli search binary

# Find unary+binary maximum (max = 5)
python -m src.cli prove z3 --target-size 5 --max-arity 2

# Search with ternary functions (finds size ≥ 30)
python -m src.cli search full --max-arity 3

# Find specific size using Z3
python -m src.cli prove z3 --target-size 17

# Run enumeration proof for binary-only
python -m src.cli prove enum --binary-only

# Run tests
pytest tests/ -v

# Get help
python -m src.cli --help
python -m src.cli search --help
python -m src.cli prove z3 --help
```

---

## Command Structure

### Unified CLI Interface

The project uses a hierarchical command structure:

```
python -m src.cli <command> <subcommand> [options]
```

### Available Commands

| Command | Purpose | Subcommands |
|---------|---------|-------------|
| `search` | Find nice sets via enumeration | `binary`, `full`, `validate` |
| `prove` | Find nice sets via formal methods | `z3`, `enum` |
| `validate` | Validate known results | `binary`, `ternary` |
| `benchmark` | Performance testing | `quick`, `full`, `depth` |

### Getting Help

```bash
# General help
python -m src.cli --help

# Command-specific help
python -m src.cli search --help
python -m src.cli prove --help
python -m src.cli validate --help
python -m src.cli benchmark --help

# Subcommand-specific help
python -m src.cli search binary --help
python -m src.cli prove z3 --help
```

---

## Search Commands

Search commands use brute-force pattern enumeration to find nice sets.

### `search binary` - Binary-Only Search

Find the maximum nice set using only binary connectives.

```bash
# Basic usage (uses depth 3)
python -m src.cli search binary

# With custom depth
python -m src.cli search binary --max-depth 3

# With custom timeout per size
python -m src.cli search binary --timeout 60
```

**Expected Results:**
- Maximum size: 3
- Example set: {XOR, AND, TRUE} or {FALSE, NAND, IFF}
- Time: ~5 seconds
- Nice sets found: 76 sets of size 3

**Output:**
```
Connectives: 16 (arity 2)

Size 1: 14 nice sets (0.00s, 16 combinations)
Size 2: 56 nice sets (0.00s, 120 combinations)
Size 3: 76 nice sets (0.22s, 560 combinations)
Size 4: 0 nice sets (1.27s, 1820 combinations)

Maximum nice set size: 3
```

### `search full` - Full Arity Search

Search with multiple arities (constants, unary, binary, ternary).

```bash
# Search up to ternary (arity 3)
python -m src.cli search full --max-arity 3

# Search up to binary (arity 2)
python -m src.cli search full --max-arity 2

# Custom depth
python -m src.cli search full --max-arity 3 --max-depth 3

# With timeout
python -m src.cli search full --max-arity 2 --timeout 120
```

**Expected Results (arity 2):**
- Maximum size: 5
- Pool: 22 connectives (2 constants + 4 unary + 16 binary)
- Time: ~60-70 seconds
- Nice sets found: 5 sets of size 5

**Expected Results (arity 3):**
- Pool: 278 connectives (2 + 4 + 16 + 256)
- Maximum: Unknown (enumeration becomes impractical)
- Recommendation: Use Z3 for ternary searches

**Output (arity 2):**
```
Connectives: 22 (arity 0-2)

Size 3: 203 nice sets (0.28s, 1540 combinations)
Size 4: 89 nice sets (2.68s, 7315 combinations)
Size 5: 5 nice sets (11.85s, 26334 combinations)
Size 6: 0 nice sets (31.49s, 38760 combinations)

Maximum nice set size: 5
```

### `search validate` - Quick Validation

Validates a known nice set to verify implementation correctness.

```bash
# Validate known size-16 set
python -m src.cli search validate

# With custom depth
python -m src.cli search validate --max-depth 5
```

**Expected Results:**
- Validates a known size-16 nice set
- Checks completeness and independence
- Time: <1 second

**Output:**
```
Validating known nice set (size 16)...

Completeness check:
  T0 (preserves false): Escaped ✓
  T1 (preserves true): Escaped ✓
  M (monotone): Escaped ✓
  D (self-dual): Escaped ✓
  A (affine): Escaped ✓
  COMPLETE ✓

Independence check (depth 3):
  Testing 16 connectives...
  All connectives independent ✓

VALIDATION SUCCESSFUL
```

---

## Proof Commands

Proof commands use formal methods (Z3 SMT solver or enumeration) to find nice sets.

### `prove z3` - Z3 Constraint Solving

Use Z3 SMT solver to find nice sets by encoding completeness and independence as constraints.

```bash
# Search for specific size
python -m src.cli prove z3 --target-size 17

# Binary-only maximum
python -m src.cli prove z3 --target-size 3 --max-arity 2

# Unary+Binary maximum
python -m src.cli prove z3 --target-size 5 --max-arity 2

# With ternary (size 30)
python -m src.cli prove z3 --target-size 30 --max-arity 3

# Custom depth
python -m src.cli prove z3 --target-size 17 --max-depth 3

# With timeout (seconds)
python -m src.cli prove z3 --target-size 31 --timeout 300
```

**Key Options:**
- `--target-size N`: Try to find nice set of size N
- `--max-arity N`: Maximum arity to include (default: 3)
- `--max-depth N`: Independence checking depth (default: 3)
- `--timeout N`: Search timeout in seconds (default: 180)

**Expected Results:**

| Target Size | Max Arity | Expected Time | Result |
|-------------|-----------|---------------|--------|
| 3 | 2 | <1s | Found (binary-only max) |
| 5 | 2 | 0.04s | Found (unary+binary max) |
| 17 | 3 | 0.69s | Found |
| 20 | 3 | 0.67s | Found |
| 25 | 3 | 3.44s | Found |
| 29 | 3 | 3.17s | Found |
| 30 | 3 | 245s (~4min) | Found |
| 31 | 3 | >300s | Timeout (unknown) |

**Output (successful):**
```
Z3 Proof: Finding nice set of size 17

Pool: 278 connectives (arity 0-3)
Target size: 17
Max depth: 3

Checking complete sets... (checked 22 candidates)
Found nice set! (0.69s)

Nice Set (size 17):
  FALSE (arity 0): 0b0
  NOT_Y (arity 2): 0b1100
  f3_18 (arity 3): 0b00010010
  f3_23 (arity 3): 0b00010111
  ... (13 more ternary functions)

Verification:
  Completeness: ✓ (escapes all 5 Post classes)
  Independence: ✓ (depth 3)

PROOF COMPLETE: Size-17 nice sets exist
```

**Output (timeout):**
```
Z3 Proof: Finding nice set of size 31

Pool: 278 connectives (arity 0-3)
Target size: 31
Max depth: 3

Checking complete sets... (checked 1247 candidates)
Timeout after 300.0 seconds

NO CONCLUSION: Size-31 unknown (search timed out)
```

### `prove enum` - Enumeration Proof

Exhaustive enumeration-based proof (slower but finds ALL nice sets).

```bash
# Binary-only proof
python -m src.cli prove enum --binary-only

# Full arity proof (warning: slow for arity 3+)
python -m src.cli prove enum --max-arity 2

# Custom depth
python -m src.cli prove enum --binary-only --max-depth 3
```

**Expected Results:**

| Configuration | Time | Sets Found | Maximum |
|---------------|------|------------|---------|
| Binary-only | ~5s | 76 (size 3) | 3 |
| Unary+Binary | ~70s | 5 (size 5) | 5 |
| With Ternary | Impractical (days/weeks) | - | - |

**Output:**
```
Enumeration Proof: Binary-only

Pool: 16 binary connectives
Max depth: 3

Size 1: 14 nice sets (0.00s)
Size 2: 56 nice sets (0.00s)
Size 3: 76 nice sets (0.22s)
Size 4: 0 nice sets (1.27s)

PROVEN: Maximum nice set size (binary-only) = 3
```

---

## Validation Commands

Validation commands verify known results against expected outcomes.

### `validate binary` - Binary-Only Validation

Validates the binary-only maximum result.

```bash
# Validate binary-only max = 3
python -m src.cli validate binary

# Custom depth
python -m src.cli validate binary --max-depth 5
```

**Expected Output:**
```
Binary-Only Validation

Pool: 16 binary connectives
Known maximum: 3

Testing size 3... ✓ (found 76 nice sets)
Testing size 4... ✓ (found 0 nice sets)

VALIDATION PASSED: Binary-only maximum confirmed as 3
```

### `validate ternary` - Ternary Validation

Validates known ternary nice sets.

```bash
# Validate ternary results
python -m src.cli validate ternary

# Custom depth
python -m src.cli validate ternary --max-depth 5
```

**Expected Output:**
```
Ternary Validation

Pool: 278 connectives (arity 0-3)

Testing known size-17 set... ✓
  Completeness: ✓
  Independence (depth 3): ✓

Testing known size-29 set... ✓
  Completeness: ✓
  Independence (depth 3): ✓

VALIDATION PASSED: All ternary results confirmed
```

---

## Benchmark Commands

Benchmark commands measure performance characteristics.

### `benchmark quick` - Quick Benchmark

Fast benchmark of core operations.

```bash
# Run quick benchmark
python -m src.cli benchmark quick
```

**Output:**
```
Quick Benchmark

Truth table operations:
  Connective creation: 0.12 μs/op
  Evaluation: 0.08 μs/op

Completeness checking:
  is_t0_preserving: 1.2 μs/op
  is_complete (5 checks): 6.5 μs/op

Independence checking (depth 3):
  Binary function: 145 μs/op
  Ternary function: 3.2 ms/op

Benchmark complete (5.2s)
```

### `benchmark full` - Full Benchmark

Comprehensive benchmark suite.

```bash
# Run full benchmark
python -m src.cli benchmark full
```

**Measures:**
- Core operations performance
- Completeness checking at different pool sizes
- Independence checking at different depths
- Search performance at different sizes

### `benchmark depth` - Depth Comparison

Compare independence checking performance across depths.

```bash
# Compare depths 1-5
python -m src.cli benchmark depth
```

**Output:**
```
Depth Comparison Benchmark

Binary connective independence checking:
  Depth 1: 0.05 ms/op (2 patterns)
  Depth 2: 0.42 ms/op (18 patterns)
  Depth 3: 2.1 ms/op (146 patterns)
  Depth 4: 12.7 ms/op (1,154 patterns)
  Depth 5: 89.3 ms/op (9,234 patterns)

Ternary connective independence checking:
  Depth 1: 0.08 ms/op (3 patterns)
  Depth 2: 1.2 ms/op (27 patterns)
  Depth 3: 18.5 ms/op (243 patterns)
  Depth 4: 156 ms/op (2,187 patterns)
  Depth 5: 1,402 ms/op (19,683 patterns)

Growth rate: ~8× per depth level
```

---

## Understanding Output

### Search Output Format

```
Connectives: 16 (arity 2)

Size 3: 76 nice sets (0.22s, 560 combinations)
        ^        ^       ^         ^
        |        |       |         └─ Total combinations tested
        |        |       └─ Time taken
        |        └─ Number of nice sets found
        └─ Set size being tested

Maximum nice set size: 3
```

### Completeness Verification

```
Completeness check:
  T0 (preserves false): Escaped ✓  ← At least one function not in T0
  T1 (preserves true): Escaped ✓   ← At least one function not in T1
  M (monotone): Escaped ✓          ← At least one non-monotone function
  D (self-dual): Escaped ✓         ← At least one non-self-dual function
  A (affine): Escaped ✓            ← At least one non-affine function
  COMPLETE ✓                       ← All 5 Post classes escaped
```

By **Post's Completeness Theorem**, escaping all 5 maximal clones means the set can express any Boolean function through composition.

### Independence Verification

```
Independence check (depth 3):
  Testing 16 connectives...
  Checked 16 × 2^20 patterns (16,777,216 total)
  No connective definable from others
  INDEPENDENT ✓
```

For each connective, tries all composition patterns up to depth 3 to see if it can be expressed from the other connectives. If none succeed, the set is independent.

### Z3 Search Progress

```
Z3 Proof: Finding nice set of size 17

Checking complete sets... (checked 22 candidates)
                                    ^
                                    └─ Number of complete sets examined
                                       Z3 prunes non-complete combinations

Found nice set! (0.69s)
```

Z3 uses constraint solving to efficiently explore the search space, checking only complete sets for independence.

---

## Definability Modes

### Overview

The `--definability-mode` flag allows choosing between two notions of function definability:

1. **`truth-functional`** (default): Clone-theoretic definability with universal projections and cross-arity constants
2. **`syntactic`**: Composition-based definability with depth bounds

**For detailed mathematical definitions and examples, see [DEFINABILITY.md](DEFINABILITY.md).**

### Truth-Functional Mode (Default)

**Clone-Theoretic Definability:**
- Universal projection rule: all projection functions are universally definable
- Cross-arity constant equivalence: TRUE_n ≡ TRUE_m, FALSE_n ≡ FALSE_m
- More permissive: typically finds smaller "nice" sets (more dependencies detected)

```bash
# Explicit truth-functional mode (same as default)
python -m src.cli search binary --definability-mode truth-functional

# Truth-functional is the default
python -m src.cli search binary

# Works with all commands
python -m src.cli prove z3 --target-size 17 --definability-mode truth-functional
python -m src.cli validate binary --definability-mode truth-functional
```

**Characteristics:**
- All projections (f(x,y,...) = xᵢ) are universally definable from any basis
- Constants of different arities but same truth value are equivalent
- More dependencies → typically smaller maximum nice set sizes

### Syntactic Mode

**Composition-Based Definability:**
- Functions definable only through explicit composition up to max-depth
- Arity-sensitive: functions of different arities are distinct
- More strict: typically finds larger "nice" sets

```bash
# Syntactic mode
python -m src.cli search binary --definability-mode syntactic

# Works with all commands
python -m src.cli prove z3 --target-size 3 --definability-mode syntactic
python -m src.cli validate binary --definability-mode syntactic
```

**Characteristics:**
- Cross-arity constants treated as independent (e.g., TRUE₀, TRUE₂, TRUE₃ are distinct)
- Projections require explicit composition (e.g., PROJECT_X from {AND, OR} at depth 2)
- Depth-bounded: only checks compositions up to specified depth

### Comparison

| Aspect | Syntactic | Truth-Functional |
|--------|-----------|------------------|
| **Projection definability** | Requires composition | Universal |
| **Cross-arity constants** | Independent | Equivalent if same value |
| **Typical max nice set size** | Larger | Smaller |
| **Use case** | Composition research | Clone theory research |
| **Default** | No | ✓ Yes |

### Example: Binary Search Comparison

```bash
# Truth-functional mode (default)
python -m src.cli search binary --definability-mode truth-functional
# Expected: Different results due to projection/constant rules

# Syntactic mode
python -m src.cli search binary --definability-mode syntactic
# Expected: max = 3, ~76 nice sets of size 3
```

### When to Use Each Mode

**Use Truth-Functional Mode When:**
- Studying clone theory or universal algebra (default choice)
- Want permissive, clone-theoretic definability
- Treating projection functions as "free"
- Analyzing cross-arity constant relationships

**Use Syntactic Mode When:**
- Studying composition-based definability
- Want strict, depth-bounded independence
- Reproducing classical results (binary-only max = 3)
- Conservative estimates of independence

### Technical Details

**Syntactic Mode:**
- Checks definability via pattern enumeration up to depth d
- `is_definable(target, basis, depth)` → explores all composition trees
- Arity-respecting: functions of arity n cannot directly use arity m ≠ n inputs

**Truth-Functional Mode:**
- Adds two special rules before composition checking:
  1. If target is a projection → return True (universal)
  2. If target and basis element are constants with same truth value → return True
- Then falls back to composition checking for other cases

**See Also:**
- **[DEFINABILITY.md](DEFINABILITY.md)** - Complete mathematical definitions and examples
- `tests/test_definability_modes.py` - Comprehensive test suite with 28 tests
- `src/independence.py:DefinabilityMode` - Implementation details

---

## Common Workflows

### Validate Implementation

Verify the implementation is working correctly:

```bash
# Quick validation (known size-16 set)
python -m src.cli search validate

# Reproduce classical result
python -m src.cli search binary

# Validate binary-only result
python -m src.cli validate binary

# Run test suite
pytest tests/ -v
```

### Reproduce Research Results

Reproduce key findings from the research:

```bash
# Binary-only maximum (classical result)
python -m src.cli search binary
# Expected: max = 3, ~5 seconds

# Unary+Binary maximum
python -m src.cli prove z3 --target-size 5 --max-arity 2
# Expected: found, ~0.04 seconds

# Size-17 discovery
python -m src.cli prove z3 --target-size 17
# Expected: found, ~0.69 seconds

# Size-29 discovery
python -m src.cli prove z3 --target-size 29
# Expected: found, ~3.17 seconds

# Size-30 discovery (current maximum)
python -m src.cli prove z3 --target-size 30
# Expected: found, ~245 seconds (~4 minutes)

# Size-31 attempt (unknown)
python -m src.cli prove z3 --target-size 31 --timeout 300
# Expected: timeout (no result)
```

### Explore Higher Sizes

Search for nice sets larger than 30:

```bash
# Try size 31 with longer timeout (10 minutes)
python -m src.cli prove z3 --target-size 31 --timeout 600

# Try size 32
python -m src.cli prove z3 --target-size 32 --timeout 600

# Try with depth 2 (faster, less thorough)
python -m src.cli prove z3 --target-size 35 --max-depth 2 --timeout 600
```

**Note:** Sizes above 30 have not been found. The actual maximum is unknown.

### Compare Z3 vs Enumeration

Compare the two search methods:

```bash
# Enumeration (exhaustive, finds all sets)
python -m src.cli search binary
# Result: 76 nice sets of size 3, ~5 seconds

# Z3 (finds one set via constraint solving)
python -m src.cli prove z3 --target-size 3 --max-arity 2
# Result: 1 nice set of size 3, <1 second

# For larger spaces, Z3 is essential:
python -m src.cli prove z3 --target-size 30
# Result: 1 nice set found, ~245 seconds

# Enumeration would take years for ternary functions
```

### Performance Analysis

Understand performance characteristics:

```bash
# Quick performance overview
python -m src.cli benchmark quick

# Compare independence checking depths
python -m src.cli benchmark depth

# Full comprehensive benchmark
python -m src.cli benchmark full
```

---

## Advanced Usage

### Custom Pool Construction

For programmatic use, construct custom connective pools:

```python
from src.connectives import generate_all_connectives
from src.search import find_nice_sets_of_size
from src.post_classes import is_complete
from src.independence import is_independent

# Build custom pool: binary + specific ternary functions
pool = generate_all_connectives(2)  # All 16 binary functions
pool += [Connective(3, tt, f'f3_{tt}') for tt in [18, 23, 48, 51]]  # Specific ternary

# Search for nice sets
nice_sets = find_nice_sets_of_size(pool, target_size=5, max_depth=3)

# Verify a specific set
my_set = [AND, OR, XOR, NOT, FALSE]
complete = is_complete(my_set)
independent = is_independent(my_set, max_depth=3)
print(f"Nice set: {complete and independent}")
```

### Depth Sensitivity Analysis

Test how independence results change with depth:

```bash
# Same set, different depths
python -m src.cli prove z3 --target-size 17 --max-depth 1
python -m src.cli prove z3 --target-size 17 --max-depth 2
python -m src.cli prove z3 --target-size 17 --max-depth 3
python -m src.cli prove z3 --target-size 17 --max-depth 4
python -m src.cli prove z3 --target-size 17 --max-depth 5
```

**Expected:** Higher depths may reduce maximum size (more patterns to check = harder to maintain independence).

### Arity Progression

Observe how maximum size grows with arity:

```bash
# Arity 2: Binary only
python -m src.cli prove z3 --target-size 3 --max-arity 2
# Pool: 16 connectives, max = 3

# Arity 2: Unary + Binary
python -m src.cli prove z3 --target-size 5 --max-arity 2
# Pool: 22 connectives, max = 5

# Arity 3: + Ternary
python -m src.cli prove z3 --target-size 30 --max-arity 3
# Pool: 278 connectives, max ≥ 30

# Arity 4: + Quaternary (warning: slow!)
python -m src.cli prove z3 --target-size 50 --max-arity 4 --timeout 3600
# Pool: 65,814 connectives, max = ???
```

---

## Performance Tips

### 1. Start Small, Scale Up

```bash
# Always start with validation
python -m src.cli search validate

# Then binary-only (fast)
python -m src.cli search binary

# Then small targets with Z3
python -m src.cli prove z3 --target-size 17

# Finally, larger searches
python -m src.cli prove z3 --target-size 30
```

### 2. Use Appropriate Tools

**Enumeration (`search`, `prove enum`):**
- Small pools (≤25 connectives)
- Small sizes (≤6)
- Want ALL nice sets (complete census)
- Educational/exploratory purposes

**Z3 (`prove z3`):**
- Large pools (100+ connectives)
- Large sizes (10+)
- Just need existence proof
- Production searches

### 3. Adjust Depth for Speed

Lower depth = faster but less thorough:

```bash
# Depth 2: Fast but may miss dependencies
python -m src.cli prove z3 --target-size 30 --max-depth 2

# Depth 3: Standard (recommended)
python -m src.cli prove z3 --target-size 30 --max-depth 3

# Depth 5: Thorough but slow
python -m src.cli prove z3 --target-size 17 --max-depth 5
```

### 4. Use Timeouts

Prevent searches from running too long:

```bash
# 5-minute timeout
python -m src.cli prove z3 --target-size 35 --timeout 300

# 1-hour timeout for exploratory search
python -m src.cli prove z3 --target-size 50 --max-arity 4 --timeout 3600
```

### 5. Leverage Known Results

Don't search blindly - use known results to guide:

```bash
# We know size 30 exists, so search nearby:
python -m src.cli prove z3 --target-size 31 --timeout 600

# We know binary-only max is 3, no need to search size 4+
# (but good for validation)
```

---

## Troubleshooting

### Command Not Found

**Error:** `python: command not found` or `python3: command not found`

**Solution:** Install Python 3 (see [INSTALLATION.md](INSTALLATION.md))

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:** Run from project root
```bash
cd /path/to/nice_connectives
python -m src.cli --help
```

### Search Too Slow

**Problem:** Enumeration search taking too long

**Solutions:**
1. Use Z3 instead: `python -m src.cli prove z3 --target-size <N>`
2. Reduce max-depth: `--max-depth 2`
3. Use smaller pool: `--max-arity 2`
4. Add timeout: `--timeout 60`

### Z3 Timeout

**Problem:** Z3 search times out without finding result

**Interpretation:** Size may not exist, or search space too large

**Solutions:**
1. Increase timeout: `--timeout 600`
2. Try smaller size: `--target-size <N-1>`
3. Reduce depth: `--max-depth 2`
4. Try different arity: `--max-arity 2`

### Tests Failing

**Problem:** pytest shows failures

**Solutions:**
```bash
# Re-run with verbose output
pytest tests/ -vv

# Run specific failing test
pytest tests/test_search.py::test_binary_only_max -vv

# Check imports work
python -c "from src import cli; print('OK')"

# Reinstall dependencies
pip install -e .
```

### Import Errors in Tests

**Problem:** pytest can't import src modules

**Solution:** Run pytest as module
```bash
python -m pytest tests/ -v
```

### Memory Issues

**Problem:** Out of memory during large searches

**Solutions:**
1. Reduce pool size: `--max-arity 2`
2. Reduce depth: `--max-depth 2`
3. Use Z3 (more memory efficient): `prove z3` instead of `search`
4. Close other applications

### Unexpected Results

**Problem:** Results don't match documented findings

**Steps:**
1. Verify you're using correct command
2. Check version: `git log -1 --oneline`
3. Run validation: `python -m src.cli search validate`
4. Run tests: `pytest tests/ -v`
5. Check for uncommitted changes: `git status`

---

## Next Steps

### Learn More

- **[JUPYTER.md](JUPYTER.md)** - Interactive Jupyter notebook tutorials
- **[INSTALLATION.md](INSTALLATION.md)** - Installation and setup
- **[RESULTS.md](RESULTS.md)** - Research findings and verified results
- **[../src/README.md](../src/README.md)** - Implementation documentation
- **[../examples/README.md](../examples/README.md)** - Example outputs and analysis
- **[../README.md](../README.md)** - Project overview and mathematical background

### Explore Examples

See [examples/](../examples/) for:
- Binary-only maximum (classical result)
- Unary+Binary maximum (Z3 proof)
- Size-17, 29, 30 discoveries (Z3 constraint solving)
- Enumeration vs Z3 comparison

### Run Tests

```bash
# Full test suite
pytest tests/ -v

# Specific test categories
pytest tests/test_connectives.py -v
pytest tests/test_post_classes.py -v
pytest tests/test_independence.py -v
pytest tests/test_search.py -v
```

### Programmatic Use

For Python integration:

```python
from src.search import search_binary_only, find_nice_sets_of_size
from src.connectives import generate_all_connectives
from src.post_classes import is_complete
from src.independence import is_independent

# Use library functions in your code
```

See [src/README.md](../src/README.md) for API documentation.

---

**Ready to explore nice connective sets!**
