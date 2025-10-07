# Test Suite Documentation

Comprehensive test suite for the Nice Connectives solver.

## Overview

The test suite validates all aspects of the implementation:
- Connective representation and evaluation
- Post's Completeness Theorem implementation
- Independence checking via bounded composition
- Search algorithms for finding nice sets

**Status**: 159 tests passing

## Running Tests

### All Tests

```bash
# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

### Specific Test Files

```bash
# Test connectives module
pytest tests/test_connectives.py -v

# Test Post class membership
pytest tests/test_post_classes.py -v

# Test independence checking
pytest tests/test_independence.py -v

# Test search algorithms
pytest tests/test_search.py -v
```

## Test Organization

### test_connectives.py
Tests for truth table representation and evaluation:
- BitVec encoding correctness
- evaluate() and evaluate_all() methods
- Connective equality and hashing
- generate_all_connectives() function

### test_post_classes.py
Tests for completeness checking:
- T0 (0-preserving) membership
- T1 (1-preserving) membership
- Monotonicity checking
- Self-dual checking
- Affine checking
- is_complete() function with known complete sets

### test_independence.py
Tests for independence checking:
- Depth-1 composition (permutations)
- Depth-2 composition patterns
- Depth-3 composition patterns (De Morgan's Law)
- is_independent() function with known independent/dependent sets
- Edge cases and boundary conditions

### test_search.py
Tests for search algorithms:
- find_nice_sets_of_size() with various sizes
- find_maximum_nice_set() on binary connectives
- Binary-only search (validates max=3 result)
- Incremental arity search
- analyze_nice_set() function

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

Current coverage by module:
- `connectives.py`: ~95% (core data structure)
- `post_classes.py`: ~90% (all 5 clones tested)
- `independence.py`: ~85% (main patterns covered)
- `search.py`: ~80% (integration tests)

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

## Continuous Integration

Tests are designed to be run in CI pipelines:
- Fast execution (< 5 minutes for full suite)
- Deterministic results (no random failures)
- Clear error messages for debugging

## Navigation

- [← Project README](../README.md)
- [Source Code](../src/README.md)
- [Examples](../examples/README.md)
- [CLAUDE.md](../CLAUDE.md) - Testing protocols
