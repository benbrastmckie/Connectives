# Usage Guide

Quick guide for running the Nice Connectives Solver.

## Installation

```bash
# Install dependencies
pip install pytest

# Navigate to project root
cd /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives
```

## Running Searches

### Basic Validation

Validate the implementation against known results:

```bash
python3 -m src.main --validate
```

This verifies a known size-16 nice set is complete and independent.

### Binary-Only Search

Reproduce the classical result that max nice set size for binary-only is 3:

```bash
python3 -m src.main --binary-only
```

**Expected output:**
```
RESULT: Maximum nice set size = 3
Example: {NOR, AND, IFF}
```

### Full Incremental Search

Search with ternary connectives (main research question):

```bash
python3 -m src.main --max-arity 3 --max-depth 3
```

**Expected output:**
```
Adding arity 2: max = 3
Adding arity 1: max = 7
Adding arity 3: max = 16
FINAL RESULT: Maximum nice set size = 16
```

### Advanced Options

**More conservative independence checking (depth 5):**
```bash
python3 -m src.main --max-arity 3 --max-depth 5
```

**Quiet mode (minimal output):**
```bash
python3 -m src.main --max-arity 3 --quiet
```

**Higher arities (slow):**
```bash
python3 -m src.main --max-arity 4 --max-depth 3
```
*Warning: Arity 4 adds 65,536 connectives, search may be very slow.*

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--binary-only` | flag | false | Search only binary connectives |
| `--max-arity` | int | 3 | Maximum arity to include in search |
| `--max-depth` | int | 3 | Maximum composition depth for independence |
| `--validate` | flag | false | Validate known maximum result |
| `--quiet` | flag | false | Suppress verbose output |

## Running Tests

### Full Test Suite

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run all tests (concise)
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term
```

### Specific Test Modules

```bash
# Test truth table operations
pytest tests/test_connectives.py -v

# Test Post's lattice completeness
pytest tests/test_post_classes.py -v

# Test independence checking
pytest tests/test_independence.py -v

# Test search algorithms
pytest tests/test_search.py -v
```

### Test Filtering

```bash
# Run tests matching pattern
pytest tests/ -k "binary" -v

# Run specific test
pytest tests/test_search.py::test_binary_only_max -v
```

## Expected Results

### Binary-Only (arity 2)
- **Maximum size:** 3
- **Example set:** {NOR, AND, IFF}
- **Search time:** ~1-2 seconds

### Unary + Binary (arity 0-2)
- **Maximum size:** 7
- **Example set:** {CONST_0, ID, CONST_1, INHIBIT, NOT_Y, IMPLIES, PROJ_X}
- **Search time:** ~60-80 seconds

### Full Search (arity 0-3)
- **Maximum size:** 16
- **Typical composition:** 1 binary + 15 ternary functions
- **Search time:** ~2-5 seconds
- **Note:** Matches theoretical upper bound

## Understanding Output

### Incremental Search Output

```
============================================================
Adding arity 2 connectives...
============================================================
Added 16 connectives of arity 2
Total pool size: 16

Searching for maximum nice set size...
Size 1: Found 12 nice sets (0.00s)
Size 2: Found 45 nice sets (0.01s)
Size 3: Found 20 nice sets (0.15s)
Size 4: No nice sets found (0.03s)

Arity 2 result: max size = 3
```

**Interpretation:**
- Added 16 binary connectives to the search pool
- Found nice sets of sizes 1, 2, and 3
- No nice sets of size 4 exist using only binary connectives
- Maximum for binary-only is 3

### Validation Output

```
VALIDATING MAXIMUM NICE SET SIZE = 16
Checking completeness... ✓
Checking independence (depth 5)... ✓
VALIDATION SUCCESSFUL

The size-16 set is:
  - Complete (escapes all 5 Post classes)
  - Independent (no function definable at depth ≤ 5)
```

## Troubleshooting

### Tests Failing

```bash
# Re-run failed tests only
pytest tests/ --lf -v

# Run with detailed output
pytest tests/ -vv
```

### Search Taking Too Long

For arity 4+, the search space becomes intractable. Solutions:
- Reduce `--max-depth` to 2
- Use `--quiet` to reduce overhead
- Consider random sampling instead of exhaustive search

### Import Errors

Ensure you're running from the project root:
```bash
cd /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives
python3 -m src.main --validate
```

## Performance Tips

1. **Start small:** Begin with `--binary-only` to validate setup
2. **Incremental depth:** Use `--max-depth 3` (standard) before trying depth 5
3. **Limit arity:** Arity 0-3 is the practical limit for exhaustive search
4. **Use validation:** Run `--validate` to quickly verify implementation

## Next Steps

- See [Examples](examples/README.md) for real execution examples and output
- See [Implementation Details](src/README.md) for code documentation
- See [Results](RESULTS.md) for research conclusions
- See [Project README](README.md) for mathematical background
- See [Scripts](scripts/README.md) for validation and benchmarking tools
