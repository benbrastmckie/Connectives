# Scripts Directory

Utility scripts for validation, benchmarking, and performance analysis of the Nice Connectives Solver.

## Overview

This directory contains standalone scripts that supplement the main implementation:
- **Validation scripts** verify correctness against known results
- **Benchmark scripts** measure performance across different configurations
- **Analysis scripts** study performance characteristics and trade-offs

All scripts are executable Python modules that can be run directly from the command line.

---

## Validation Scripts

### validate_binary_search.py

Validates the binary-only search against the classical result (max = 3).

**Purpose:**
- Confirms implementation correctness for binary connectives
- Tests metadata logging and result tracking
- Provides regression testing for algorithm changes

**Usage:**
```bash
# Basic validation (depth 3)
./scripts/validate_binary_search.py

# Custom depth
./scripts/validate_binary_search.py --depth 5

# Disable symmetry breaking
./scripts/validate_binary_search.py --no-symmetry-breaking

# Verbose output
./scripts/validate_binary_search.py --verbose
```

**Arguments:**
- `--depth N` - Maximum composition depth (default: 3)
- `--use-z3` - Use Z3 SAT backend instead of pattern enumeration
- `--no-symmetry-breaking` - Disable equivalence class filtering
- `--verbose` - Print detailed progress information

**Expected Output:**
```
BINARY-ONLY SEARCH VALIDATION
Parameters:
  Composition depth: 3
  Strategy: enumeration
  Symmetry breaking: True

[search output...]

VALIDATION STATUS
✓ PASS: Found expected maximum size of 3
```

**Exit Codes:**
- 0: Validation passed (max = 3 found)
- Non-zero: Validation failed

---

### validate_ternary_search.py

Validates the full search including ternary connectives (max = 16).

**Purpose:**
- Verifies maximum nice set size with ternary connectives
- Compares results across different composition depths
- Analyzes arity distribution in maximal nice sets

**Usage:**
```bash
# Single depth validation
./scripts/validate_ternary_search.py --depth 3

# Compare multiple depths
./scripts/validate_ternary_search.py --compare

# Custom depth with verbose output
./scripts/validate_ternary_search.py --depth 5 --verbose

# Disable symmetry breaking
./scripts/validate_ternary_search.py --no-symmetry-breaking
```

**Arguments:**
- `--depth N` - Maximum composition depth (default: 3)
- `--compare` - Compare results across depths 3, 5, 7
- `--use-z3` - Use Z3 SAT backend
- `--no-symmetry-breaking` - Disable equivalence class filtering
- `--verbose` - Print detailed search progress

**Expected Output (single depth):**
```
TERNARY SEARCH VALIDATION - Depth 3
Parameters:
  Composition depth: 3
  Strategy: enumeration
  Symmetry breaking: True

Generating connectives...
  Arity 0: 2 connectives
  Arity 1: 4 connectives
  Arity 2: 16 connectives
  Arity 3: 256 connectives
Total connectives: 278

[search output...]

RESULTS SUMMARY
Maximum nice set size: 16
Number of maximal nice sets found: 5
Search time: 2.34s

Example maximal nice sets:
Set 1:
  - XOR (arity 2)
  - f3_23 (arity 3)
  [... more ternary functions]
```

**Comparison Mode:**
Compares results across depths 3, 5, 7 to verify consistency:
```
COMPARISON TABLE
Depth    Max Size     # Sets      Time (s)     Strategy
------------------------------------------------------------------------
3        16           5           2.34         enumeration
5        16           3           45.67        enumeration
7        16           2           892.14       enumeration

✓ All depths found the same maximum size: 16
```

---

## Benchmark Scripts

### benchmark.py

Comprehensive performance benchmarking suite.

**Purpose:**
- Measure performance across different search strategies
- Compare enumeration vs Z3 SAT approaches
- Quantify symmetry breaking impact
- Generate CSV/JSON reports for analysis

**Usage:**
```bash
# Run comprehensive benchmark (5 runs per test)
./scripts/benchmark.py

# Custom number of runs
./scripts/benchmark.py --runs 10

# Save results to specific files
./scripts/benchmark.py --output my_benchmark.csv --json my_benchmark.json
```

**Arguments:**
- `--runs N` - Number of runs per benchmark (default: 5)
- `--output FILE` - Output CSV file path (default: benchmarks.csv)
- `--json FILE` - Optional JSON output file path

**Benchmark Suite:**
1. Binary-only search (enumeration, no symmetry breaking)
2. Binary-only search (enumeration, with symmetry breaking)
3. Full search arity 0-3 (enumeration, no symmetry breaking)
4. Full search arity 0-3 (enumeration, with symmetry breaking)
5. Symmetry breaking impact analysis (binary)
6. Symmetry breaking impact analysis (ternary)

**Output:**
Creates CSV with columns:
- Search Type
- Strategy (enumeration/z3_sat)
- Symmetry Breaking (yes/no)
- Runs
- Avg Time (s)
- Min Time (s)
- Max Time (s)
- Std Dev (s)
- Max Size
- Connectives Count

**Example Output:**
```
BENCHMARK RESULTS SUMMARY

1. binary_only
------------------------------------------------------------------------
  Strategy: enumeration
  Symmetry breaking: no
  Average time: 1.2345s
  Min time: 1.2100s
  Max time: 1.2600s
  Std dev: 0.0156s
  Max nice set size: 3

2. binary_only
------------------------------------------------------------------------
  Strategy: enumeration
  Symmetry breaking: yes
  Average time: 0.8234s
  Min time: 0.8100s
  Max time: 0.8400s
  Std dev: 0.0098s
  Max nice set size: 3

[...]

5. symmetry_breaking_impact_arity_2
------------------------------------------------------------------------
  Without symmetry breaking: 1.2345s
  With symmetry breaking:    0.8234s
  Speedup:                   1.50×
  Space reduction:           2.67×
```

**Use Cases:**
- Performance regression testing
- Comparing algorithm improvements
- Hardware comparison
- Identifying performance bottlenecks

---

### quick_benchmark.py

Fast performance check for key metrics.

**Purpose:**
- Quick validation of search performance
- Smoke test for performance regressions
- Provides baseline timing for development

**Usage:**
```bash
./scripts/quick_benchmark.py
```

**No arguments required** - runs fixed benchmarks.

**Tests:**
1. Binary-only search without symmetry breaking
2. Binary-only search with symmetry breaking

**Output:**
```
QUICK PERFORMANCE BENCHMARK

1. Binary-only search (no symmetry breaking)...
   Result: max=3, time=1.234s

2. Binary-only search (with symmetry breaking)...
   Result: max=3, time=0.823s

RESULTS SUMMARY
Binary search (no SB):   1.234s
Binary search (with SB): 0.823s
Speedup from SB:         1.50×

Both strategies found max=3 ✓
Binary search completes in <1s ✓
```

**Typical Runtime:** < 3 seconds

---

### benchmark_depth.py

Systematic depth performance analysis for crossover studies.

**Purpose:**
- Measure performance vs composition depth
- Identify practical depth limits
- Quantify exponential growth in search time
- Support research on depth/performance trade-offs

**Usage:**
```bash
# Test depths 1-5 (default)
./scripts/benchmark_depth.py

# Custom depth range
./scripts/benchmark_depth.py --depths 1,2,3,4,5,6,7

# More runs for statistical significance
./scripts/benchmark_depth.py --runs 5

# Custom output file
./scripts/benchmark_depth.py --output depth_analysis.csv
```

**Arguments:**
- `--depths LIST` - Comma-separated depths to test (default: 1,2,3,4,5)
- `--runs N` - Number of runs per depth (default: 3)
- `--output FILE` - Output CSV file path (default: depth_results.csv)

**Output:**
```
DEPTH CROSSOVER BENCHMARK
Depths to test: [1, 2, 3, 4, 5]
Runs per depth: 3

  Depth 1: 0.234s 0.229s 0.237s (avg: 0.233s)
  Depth 2: 0.456s 0.451s 0.459s (avg: 0.455s)
  Depth 3: 0.823s 0.818s 0.828s (avg: 0.823s)
  Depth 4: 2.145s 2.138s 2.152s (avg: 2.145s)
  Depth 5: 8.734s 8.721s 8.748s (avg: 8.734s)

RESULTS SUMMARY
Depth    Avg Time     Min Time     Max Time     Max Size
------------------------------------------------------------------------
1        0.2333       0.2290       0.2370       3
2        0.4553       0.4510       0.4590       3
3        0.8230       0.8180       0.8280       3
4        2.1450       2.1380       2.1520       3
5        8.7343       8.7210       8.7480       3

Results saved to: depth_results.csv
```

**Analysis:**
- Shows exponential growth in search time with depth
- Identifies practical depth limits (typically depth ≤ 5)
- Useful for choosing optimal depth parameter

**CSV Output:**
Contains columns: Depth, Runs, Avg Time, Min Time, Max Time, Std Dev, Max Size, Avg Num Sets

**Example Output:**
See [examples/depth_results.csv](../examples/depth_results.csv) for sample benchmark data showing performance across depths 1-5.

---

## Common Patterns

### Import Path Setup

All scripts include:
```python
sys.path.insert(0, str(Path(__file__).parent.parent))
```
This allows importing from `src/` regardless of execution directory.

### Execution

Scripts are executable and can be run as:
```bash
# Method 1: Direct execution (requires shebang)
./scripts/benchmark.py

# Method 2: Via Python interpreter
python3 scripts/benchmark.py

# Method 3: As module (from project root)
python3 -m scripts.benchmark
```

### Output Formats

**Console Output:**
- Box drawing for section headers (═, ─)
- Unicode checkmark (✓) for validation success
- Unicode cross (✗) for validation failure
- Formatted tables for results

**CSV Output:**
- Standard comma-separated format
- Headers in first row
- Numeric values with 4 decimal precision
- Compatible with spreadsheet software

**JSON Output:**
- Structured data with full details
- Includes all timing runs (not just averages)
- Preserves metadata and configuration

---

## Performance Expectations

### Binary-Only Validation
- **Runtime:** < 1 second (with symmetry breaking)
- **Max Size:** 3 (consistent across all depths)

### Ternary Search Validation
- **Runtime (depth 3):** 2-5 seconds
- **Runtime (depth 5):** 30-60 seconds
- **Runtime (depth 7):** 10-15 minutes
- **Max Size:** 16 (consistent across all depths)

### Benchmark Suite
- **Quick benchmark:** < 5 seconds
- **Comprehensive benchmark:** 2-5 minutes
- **Depth benchmark (depths 1-5):** 1-2 minutes
- **Depth benchmark (depths 1-7):** 10-20 minutes

---

## Use Cases

### Development Workflow

**Before committing changes:**
```bash
# Quick validation
./scripts/quick_benchmark.py

# Full validation
./scripts/validate_binary_search.py
./scripts/validate_ternary_search.py
```

**Performance regression testing:**
```bash
# Run before changes
./scripts/benchmark.py --output before.csv

# Make changes...

# Run after changes
./scripts/benchmark.py --output after.csv

# Compare results
diff before.csv after.csv
```

**Research Analysis:**
```bash
# Study depth trade-offs
./scripts/benchmark_depth.py --depths 1,2,3,4,5,6,7 --runs 5

# Comprehensive performance study
./scripts/benchmark.py --runs 10 --json full_results.json
```

### CI/CD Integration

**Validation in CI pipeline:**
```bash
# Fast validation (< 5 seconds)
./scripts/quick_benchmark.py || exit 1

# Full validation (< 10 seconds)
./scripts/validate_binary_search.py || exit 1
```

**Performance monitoring:**
```bash
# Track performance over time
./scripts/benchmark.py --runs 3 --output "benchmark_$(date +%Y%m%d).csv"
```

---

## Dependencies

All scripts use only project dependencies:
- Python 3.6+
- pytest (for testing framework, not required by scripts)
- src/ modules (connectives, search, etc.)

**No additional dependencies required.**

---

## Navigation

- [← Project README](../README.md)
- [Examples](../examples/README.md)
- [Implementation Details](../src/README.md)
- [Usage Guide](../USAGE.md)
