# Test Suite

Comprehensive test suite for the nice_connectives project covering all core algorithms, CLI infrastructure, proof systems, and command implementations.

## Current Status

**Test Count**: 338+ passing tests
**Skipped Tests**: 0
**Warnings**: 0
**Framework**: pytest 7.0+
**Execution Time**: ~60 seconds (non-slow tests), ~8-10 minutes (full suite)
**Optimizations**: Session-scoped fixtures, tiny test pools, configurable depth tests

## Quick Start

```bash
# Fast tests for development (60 seconds)
pytest tests/ -m "not slow"

# Full test suite for PRs (8-10 minutes)
pytest tests/

# Specific test file
pytest tests/test_search.py -v

# With coverage report
pytest tests/ --cov=src --cov-report=html
```

## Test Organization

### Core Algorithm Tests

#### test_connectives.py (48 tests)
Tests for connective representation and evaluation:
- BitVec encoding and truth table operations
- Connective creation, equality, and hashing
- evaluate() and evaluate_all() methods
- Standard connective definitions (AND, OR, NOT, XOR, etc.)
- generate_all_connectives() for arbitrary arities
- Projection functions

**Coverage**: Core connective operations

#### test_post_classes.py (36 tests)
Tests for Post's completeness theorem implementation:
- T0 (0-preserving) membership detection
- T1 (1-preserving) membership detection
- Monotonicity checking
- Self-dual function detection
- Affine (linear) function detection
- is_complete() validation with known complete/incomplete sets
- get_missing_classes() utility functions

**Coverage**: All five Post classes

#### test_independence.py (28 tests)
Tests for composition-based independence checking:
- Depth-1 compositions (direct substitution)
- Depth-2 compositions (nested functions)
- Depth-3 compositions (De Morgan's Law detection)
- Binary-constant compositions
- Unary function chains
- is_definable() and is_independent() functions
- Known dependency detection (OR from {NOT, AND})

**Coverage**: Composition pattern enumeration

#### test_search.py (51 tests)
Tests for search algorithms:
- find_nice_sets_of_size() with various sizes
- find_maximum_nice_set() optimization
- search_binary_only() (validates max=3)
- search_incremental_arity() (includes slow tests)
- analyze_nice_set() result analysis
- validate_nice_set() validation logic
- Known results verification
- Performance benchmarks

**Coverage**: Search algorithms and validation

### Infrastructure Tests

#### test_cli.py (23 tests)
Tests for CLI argument parsing:
- Main parser structure
- Subcommand argument parsing (prove, validate, benchmark, search)
- Flag handling (definability-mode, verbose, checkpoint)
- Error handling for invalid commands
- Required vs optional arguments

**Coverage**: CLI infrastructure

#### test_constants.py (22 tests)
Tests for constants module:
- get_binary_by_value() lookup function
- get_connective_by_name() lookup function
- Case insensitivity handling
- ALL_BINARY collection completeness
- Edge cases and invalid inputs

**Coverage**: Helper functions and collections

### Command Implementation Tests

#### test_commands_prove.py (12 tests)
Tests for prove command implementations:
- prove_z3() function with various parameters
- prove_enumeration() function
- Checkpoint file handling
- Definability mode flag handling
- Mock Z3 execution for unit tests

**Coverage**: Prove command logic

#### test_commands_validate.py (12 tests)
Tests for validate command implementations:
- validate_binary() function
- validate_ternary() function
- Symmetry breaking flag handling
- Comparison mode for ternary validation
- Success/failure exit codes

**Coverage**: Validate command logic

#### test_commands_search.py (24 tests)
Tests for search command implementations:
- search_binary() function
- search_full() incremental arity search
- search_validate() size-16 validation
- Verbose/quiet flag behavior
- Result analysis and reporting
- Mock patching for search functions

**Coverage**: Search command logic

#### test_commands_benchmark.py (15 tests)
Tests for benchmark command implementations:
- benchmark_full() function structure
- benchmark_quick() function structure
- benchmark_depth() function structure
- Error handling for missing benchmark modules
- Parameter validation

**Coverage**: Benchmark command structure

### Proof System Tests

#### test_z3_proof.py (17 tests)
Tests for Z3 proof system:
- build_connective_pool() with various max_arity values
- save_checkpoint() creates valid JSON
- load_checkpoint() reads data correctly
- Checkpoint data structure validation
- Small pool search integration test
- Checkpoint timestamp and elapsed time tracking

**Coverage**: Z3 proof infrastructure

#### test_enumeration_proof.py (3 tests)
Tests for enumeration proof approach:
- Proof function existence
- Basic structure validation
- Function signatures

**Coverage**: Enumeration proof structure

### Validation Tests

#### test_notebooks.py (9 tests)
Tests for Jupyter notebook validation:
- Notebook execution tests (7 notebooks)
- Notebook existence verification
- Directory structure validation
- Uses jupyter nbconvert for execution testing

**Coverage**: All 7 Jupyter notebooks

### Test Infrastructure

#### conftest.py
Shared fixtures for all tests:
- `sample_connective_pool()` - Small pool for testing
- `temp_checkpoint_file()` - Temporary file fixture
- `mock_z3_solver()` - Mocked Z3 solver

## Test Markers

Test markers allow selective test execution:

```python
@pytest.mark.slow         # Tests taking >1 second
@pytest.mark.notebook     # Notebook validation tests
@pytest.mark.integration  # End-to-end with real execution
```

### Usage

```bash
# Run only slow tests
pytest tests/ -m "slow"

# Exclude slow tests (recommended for development)
pytest tests/ -m "not slow"

# Run only notebook tests
pytest tests/ -m "notebook"

# Run only integration tests
pytest tests/ -m "integration"

# Exclude multiple markers
pytest tests/ -m "not slow and not notebook"
```

## Testing Conventions

### Naming

- **Test files**: `test_*.py` or `*_test.py`
- **Test classes**: `class Test<Feature>:`
- **Test functions**: `def test_<specific_behavior>():`

### Structure

```python
class TestFeature:
    """Test suite for feature."""

    def test_basic_case(self):
        """Test normal operation."""
        # Arrange
        input_data = setup()

        # Act
        result = feature(input_data)

        # Assert
        assert result == expected
```

### Assertions

```python
# Clear assertion messages
assert result == expected, f"Expected {expected}, got {result}"

# Test both positive and negative cases
assert is_complete([NOT, AND])
assert not is_complete([AND, OR])
```

### Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiple_inputs(input, expected):
    assert function(input) == expected
```

## Mock Patching

### Critical Rule

**Patch where functions are USED, not where they're DEFINED**

```python
# In src/commands/search.py:
from src.search import search_binary_only

# CORRECT - Patch where it's used
@patch('src.commands.search.search_binary_only')
def test_command(mock_search):
    mock_search.return_value = (3, [])
    search_binary()

# INCORRECT - Patching where it's defined won't work
@patch('src.search.search_binary_only')  # Won't be called!
```

### Common Patterns

```python
# Mock return values
@patch('src.module.function')
def test_with_mock(mock_func):
    mock_func.return_value = expected_value

# Mock multiple functions (bottom-up in decorator order)
@patch('src.module.second_func')
@patch('src.module.first_func')
def test_multiple(mock_first, mock_second):
    pass

# Use fixtures for file I/O
def test_with_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")
```

## Running Tests

### Development Workflow

```bash
# 1. Run fast tests during development
pytest tests/ -m "not slow" -v

# 2. Run specific test file you're working on
pytest tests/test_my_module.py -v

# 3. Run related tests
pytest tests/test_connectives.py tests/test_search.py -v

# 4. Before committing, run full suite
pytest tests/
```

### Coverage Reports

```bash
# Terminal report
pytest tests/ --cov=src --cov-report=term-missing

# HTML report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# Coverage for specific module
pytest tests/test_search.py --cov=src.search
```

### Parallel Execution

For faster test execution on multi-core systems:

```bash
# Install pytest-xdist (if not already installed)
pip install pytest-xdist

# Run tests in parallel (auto-detect CPU cores)
pytest tests/ -n auto

# Run non-slow tests in parallel (recommended for development)
pytest tests/ -m "not slow" -n auto

# Full suite in parallel
pytest tests/ -n auto
```

**Performance Gains**:
- Expected: 2.5-3x speedup on 4-core systems
- Non-slow tests: ~60s → ~20s
- Full suite: ~10min → ~3-4min

### Performance Optimization Tips

The test suite has been optimized for speed:

1. **Session-scoped fixtures**: Connective pools generated once per session
   - `sample_connective_pool()`: 22 connectives (0-2 arity)
   - `tiny_connective_pool()`: 8 connectives (minimal for speed)
   - `minimal_complete_set()`: {NOT, AND}
   - `standard_complete_set()`: {NOT, AND, OR}

2. **Parallel execution**: Use `-n auto` to distribute tests across CPU cores

3. **Selective test execution**: Use markers to run specific test categories
   ```bash
   pytest -m "not slow"      # Skip slow tests
   pytest -m "integration"   # Only integration tests
   pytest -m "notebook"      # Only notebook tests
   ```

4. **Short traceback**: Configured with `--tb=short` for faster output

## Pre-PR Checklist

Before submitting a pull request:

- [ ] All tests pass: `pytest tests/` (338+ passed, 0 failed, 0 skipped)
- [ ] No warnings in output
- [ ] New features have tests (80%+ coverage)
- [ ] Slow tests marked with `@pytest.mark.slow`
- [ ] Mock expensive operations (Z3, large searches)
- [ ] Tests have clear docstrings

## Adding New Tests

### Process

1. **Identify what to test** (new feature, bug fix, edge case)
2. **Choose appropriate test file** (or create new one)
3. **Write test following conventions**
4. **Use fixtures from conftest.py**
5. **Add appropriate markers** (`@pytest.mark.slow` if >1s)
6. **Run tests**: `pytest tests/test_new.py -v`
7. **Verify coverage**: `pytest tests/test_new.py --cov=src.module`

### Example

```python
"""
Test suite for new feature.

Tests basic functionality, edge cases, and integration.
"""

import pytest
from unittest.mock import Mock, patch


class TestNewFeature:
    """Test new feature implementation."""

    def test_basic_functionality(self):
        """Test normal operation with valid input."""
        result = new_feature(input_value)
        assert result == expected

    @pytest.mark.parametrize("input,expected", [
        (0, result_for_zero),
        (1, result_for_one),
        (-1, result_for_negative),
    ])
    def test_edge_cases(self, input, expected):
        """Test boundary conditions."""
        assert new_feature(input) == expected

    @pytest.mark.slow
    def test_expensive_operation(self):
        """Test long-running operation."""
        result = expensive_new_feature()
        assert result is not None
```

## Troubleshooting

### Mock Not Called

**Problem**: `AssertionError: Expected 'function' to be called once. Called 0 times.`

**Solution**: Check mock patch path - patch where function is USED, not DEFINED

### Tests Skipped

**Problem**: Output shows "X skipped"

**Solution**: Remove `@pytest.mark.skip` decorators, use markers instead

### Unknown Marker Warning

**Problem**: `PytestUnknownMarkWarning: Unknown pytest.mark.mymarker`

**Solution**: Register marker in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
markers = [
    "mymarker: description",
]
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run pytest from project root:
```bash
cd /path/to/nice_connectives
pytest tests/
```

## Additional Resources

- **[docs/TESTING.md](../docs/TESTING.md)** - Comprehensive testing guide
- **[CLAUDE.md](../CLAUDE.md)** - Project testing protocols
- **[specs/plans/016_comprehensive_test_coverage.md](../specs/plans/016_comprehensive_test_coverage.md)** - Test implementation plan
- **pytest Documentation**: https://docs.pytest.org/
- **unittest.mock Guide**: https://docs.python.org/3/library/unittest.mock.html

## Quick Reference

```bash
# Fast development tests (60s)
pytest tests/ -m "not slow"

# Full suite for PRs (8-10min)
pytest tests/

# Specific test
pytest tests/test_search.py::TestBinaryOnlySearch::test_binary_only_max_size_is_3 -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Parallel execution
pytest tests/ -n auto
```

**Expected Result**: `338 passed, 0 failed, 0 skipped, 0 warnings`

## Navigation

- [← Project Root](../README.md)
- [Documentation](../docs/README.md)
- [Comprehensive Testing Guide](../docs/TESTING.md)
- [Source Code](../src/README.md)
