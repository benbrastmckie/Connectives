# Test Suite Documentation

Comprehensive test suite for the Nice Connectives solver.

## Overview

The test suite validates all aspects of the implementation:
- Connective representation and evaluation
- Post's Completeness Theorem implementation
- Independence checking via bounded composition
- Search algorithms for finding nice sets
- Performance benchmarks and depth crossover analysis

**Status**: 175 tests passing (138 core + 9 depth crossover + 9 notebooks + 19 other tests)

## Running Tests

### All Tests

```bash
# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

### Custom Pytest Marks

The test suite uses custom markers for test categorization:

- **`@pytest.mark.slow`**: Long-running tests (benchmarks, extended searches)
  ```bash
  # Run only slow tests
  pytest -m slow tests/

  # Skip slow tests (useful for quick validation)
  pytest -m "not slow" tests/
  ```

- **`@pytest.mark.notebook`**: Notebook validation tests
  ```bash
  # Run only notebook tests
  pytest -m notebook tests/

  # Skip notebook tests
  pytest -m "not notebook" tests/
  ```

View all registered marks:
```bash
pytest --markers | grep -E "(slow|notebook)"
```

### Specific Test Files

```bash
# Test connectives module (38 tests)
pytest tests/test_connectives.py -v

# Test Post class membership (57 tests)
pytest tests/test_post_classes.py -v

# Test independence checking (28 tests)
pytest tests/test_independence.py -v

# Test depth/performance crossover (9 tests)
pytest tests/test_depth_crossover.py -v

# Test search algorithms (6 tests, 4 skipped)
pytest tests/test_search.py -v

# Test notebook validation (9 tests - 7 notebooks + 2 structure tests)
pytest tests/test_notebooks.py -v

# Run all notebooks with nbval (direct validation)
pytest --nbval notebooks/*.ipynb
```

### Running with Coverage

```bash
# Core modules with coverage report
pytest tests/test_connectives.py tests/test_post_classes.py \
       tests/test_independence.py tests/test_depth_crossover.py \
       --cov=src --cov-report=term-missing

# Expected: 138 core tests passing in ~2 seconds, 41% overall coverage
```

## Test Organization

### test_connectives.py (38 tests)
Tests for truth table representation and evaluation:
- BitVec encoding correctness
- evaluate() and evaluate_all() methods
- Connective equality and hashing
- generate_all_connectives() function
- Standard connective definitions (AND, OR, NOT, XOR, etc.)
- Projection functions

**Coverage**: 96% of connectives.py

### test_post_classes.py (57 tests)
Tests for completeness checking:
- T0 (0-preserving) membership
- T1 (1-preserving) membership
- Monotonicity checking
- Self-dual checking
- Affine checking
- is_complete() function with known complete sets
- Symmetry breaking and equivalence classes

**Coverage**: 96% of post_classes.py

### test_independence.py (28 tests)
Tests for independence checking:
- Depth-1 composition (permutations)
- Depth-2 composition patterns (f(g(x,y), h(x,y)))
- Depth-3 composition patterns (De Morgan's Law)
- Binary-constant compositions (f(c, g(x,y)))
- Unary chains (u(v(f(x,y))))
- is_independent() function with known independent/dependent sets
- Edge cases and boundary conditions

**Coverage**: 61% of independence.py

### test_search.py (6 tests + 4 skipped)
Tests for search algorithms:
- find_nice_sets_of_size() with various sizes
- find_maximum_nice_set() on binary connectives
- Binary-only search (validates max=3 result)
- analyze_nice_set() and validate_nice_set() functions
- *Incremental arity search (skipped - too slow for CI)*

**Coverage**: 38% of search.py

### test_depth_crossover.py (9 tests)
Performance tests for depth parameter tuning:
- Fast depths (1-5) complete quickly
- Slow depths (7-10) take measurably longer
- Depth consistency across multiple runs
- Performance trend validation

**Coverage**: Focused on independence.py performance characteristics

### test_notebooks.py (9 tests)
Tests for Jupyter notebook validation:
- Notebook execution tests (7 parametrized tests, one per notebook)
- Notebook existence and structure validation
- Import compatibility verification
- Runtime error detection

**Marks**: All tests marked as `@pytest.mark.notebook`, execution tests also marked `@pytest.mark.slow`

**Usage**:
```bash
# Run notebook tests (requires nbval)
pytest tests/test_notebooks.py -v

# Skip slow notebook execution tests
pytest tests/test_notebooks.py -m "not slow" -v

# Run notebooks directly with nbval
pytest --nbval notebooks/*.ipynb
```

**Coverage**: Validates all 7 Jupyter notebooks execute without errors

## Testing Strategy

### Unit Tests
- Each module tested independently
- Focus on individual function correctness
- Edge cases: arity 0, arity 1, empty sets

### Integration Tests
- End-to-end search workflows
- Composition detection across multiple depths
- Complete + independent validation

### Regression Tests
- Validates known results (binary max=3)
- Ensures size-16 nice set is valid
- Prevents regressions during refactoring

## Test Conventions

### Naming
- Test files: `test_*.py`
- Test functions: `def test_feature_name():`
- Descriptive names explain what is being tested

### Assertions
```python
# Use clear assertions
assert result == expected, f"Expected {expected}, got {result}"

# Test both positive and negative cases
assert is_complete(complete_set)
assert not is_complete(incomplete_set)
```

### Test Data
```python
# Define test connectives clearly
AND = Connective(2, 0b1000, "AND")
OR = Connective(2, 0b1110, "OR")
NOT = Connective(1, 0b01, "NOT")
```

## Key Test Cases

### Binary-Only Maximum = 3
```python
def test_binary_maximum():
    """Validates that binary-only nice sets have maximum size 3."""
    max_size, sets = search_binary_only(max_depth=3)
    assert max_size == 3
    assert len(sets) > 0
```

### Size-16 Nice Set Validation
```python
def test_size_16_validation():
    """Validates known size-16 nice set."""
    nice_16 = [...]  # 1 binary + 15 ternary
    is_valid, _ = validate_nice_set(nice_16, max_depth=5)
    assert is_valid
```

### De Morgan's Law Detection
```python
def test_de_morgan():
    """Ensures OR is detected as definable from {NOT, AND}."""
    OR = Connective(2, 0b1110, "OR")
    NOT = Connective(1, 0b01, "NOT")
    AND = Connective(2, 0b1000, "AND")

    assert is_definable(OR, [NOT, AND], max_depth=3)
```

## Test Coverage

Current coverage by module (as of latest test run):
- `connectives.py`: 96% (core data structure fully tested)
- `post_classes.py`: 96% (all 5 Post classes tested)
- `independence.py`: 61% (main patterns covered, some edge cases untested)
- `search.py`: 38% (core functions tested, CLI integration untested)
- `constants.py`: 88% (standard connectives validated)
- `cli.py`: 6% (minimal CLI testing, integration tests needed)
- `commands/`: 9-18% (command implementations largely untested)
- `proofs/`: 9% (proof scripts not covered by unit tests)

**Overall**: 41% coverage across 1454 statements

### Coverage Goals

**High Priority** (Core functionality):
- ✅ `connectives.py` - 96% (excellent)
- ✅ `post_classes.py` - 96% (excellent)
- 🟡 `independence.py` - 61% (good, could improve edge cases)
- 🟡 `search.py` - 38% (adequate for core, missing utility functions)

**Lower Priority** (CLI/Integration):
- 🔴 `cli.py` - 6% (CLI integration testing)
- 🔴 `commands/*` - 9-18% (command-line tools)
- 🔴 `proofs/*` - 9% (proof generation scripts)

The test suite focuses on correctness of core algorithms (connectives, Post classes, independence checking). CLI and integration tests are minimal since these are primarily used for research workflows rather than production code.

## Adding New Tests

### 1. Identify Functionality
Determine what needs testing (new feature, edge case, bug fix)

### 2. Create Test Function
```python
def test_new_feature():
    """Test description."""
    # Arrange
    input_data = setup_test_data()

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_value
```

### 3. Run Tests
```bash
pytest tests/test_new_file.py::test_new_feature -v
```

### 4. Verify Coverage
```bash
pytest tests/test_new_file.py --cov=src.module_name
```

## Performance Notes

Test execution characteristics:
- **Fast tests** (connectives, post_classes, independence): ~2 seconds for 138 core tests
- **Slow tests** (search with large state spaces): Some tests skipped to avoid timeouts
- **Incremental search tests**: Skipped in regular runs (can take minutes)
- **Total execution time**: ~2-3 seconds for standard test suite

### Skipped Tests

Some tests are marked with `@pytest.mark.skip` because they:
- Take too long for regular testing (incremental arity search)
- Require extensive computation (full state space exploration)
- Are primarily for benchmarking rather than correctness validation

Run skipped tests manually when needed:
```bash
pytest -v --runxfail tests/test_search.py
```

## Continuous Integration

Tests are designed to be CI-friendly:
- Fast execution (< 5 seconds for core suite)
- Deterministic results (no random failures)
- Clear error messages for debugging
- Timeouts prevent runaway tests (10s default)

## Test Development Guidelines

### Adding New Tests

When adding new functionality:

1. **Write tests first** (TDD approach recommended for core algorithms)
2. **Group related tests** in classes (e.g., `TestBinaryConnectives`)
3. **Use descriptive names** - test name should explain what is being tested
4. **Test edge cases** - empty sets, boundary values, invalid inputs
5. **Include docstrings** - explain the purpose of each test

Example structure:
```python
class TestNewFeature:
    """Test suite for new feature."""

    def test_basic_functionality(self):
        """Basic feature should work with standard inputs."""
        # Arrange
        input_data = create_test_data()

        # Act
        result = new_feature(input_data)

        # Assert
        assert result == expected_output

    def test_edge_case(self):
        """Feature should handle edge case correctly."""
        # Test edge case
```

### Test Quality Standards

- **Coverage target**: Core modules should have >90% coverage
- **Performance**: Tests should complete in <10 seconds each
- **Independence**: Tests should not depend on each other
- **Clarity**: Assertions should have clear failure messages
- **Maintainability**: Avoid hardcoded values, use constants

### When to Skip Tests

Mark tests with `@pytest.mark.skip` when:
- Execution time > 30 seconds
- Testing exploratory/experimental features
- Requiring external resources not in CI environment
- Primarily for benchmarking, not correctness

Always include a reason:
```python
@pytest.mark.skip(reason="Takes >5 minutes for full search space")
def test_exhaustive_search():
    ...
```

## Test Summary

**Total**: 175 passing tests (138 core + 37 additional tests)
**Execution**: ~2 seconds for core suite, longer for slow tests
**Coverage**: 41% overall, 96% for core modules
**Framework**: pytest with coverage, timeout plugins

## Navigation

- [← Project README](../README.md)
- [Source Code](../src/README.md)
- [Examples](../examples/README.md)
- [Documentation](../docs/README.md)
- [CLAUDE.md](../CLAUDE.md) - Testing protocols
