# Testing Guide

Comprehensive testing guide for the nice_connectives project.

## Table of Contents

- [Overview](#overview)
- [Test Organization](#test-organization)
- [Running Tests](#running-tests)
- [Test Markers](#test-markers)
- [Testing New Features](#testing-new-features)
- [Mock Patching Guidelines](#mock-patching-guidelines)
- [Pre-PR Checklist](#pre-pr-checklist)
- [Troubleshooting](#troubleshooting)
- [Test Infrastructure](#test-infrastructure)

## Overview

The nice_connectives project uses pytest as the testing framework with comprehensive coverage across all modules. The test suite includes 338+ tests covering:

- Core connective definitions and operations
- Completeness checking (Post's theorem)
- Independence verification (composition-based)
- Search algorithms (binary-only and incremental arity)
- CLI argument parsing
- Command implementations
- Proof systems (Z3 and enumeration)
- Jupyter notebook validation

**Current Status**: 338 passed, 0 failed, 0 skipped, 0 warnings

## Test Organization

### Test Files and Purpose

```
tests/
├── conftest.py                      # Shared fixtures and test configuration
├── test_cli.py                      # CLI argument parsing (23 tests)
├── test_constants.py                # Constants and helper functions (22 tests)
├── test_connectives.py              # Core connective definitions (48 tests)
├── test_post_classes.py             # Post's completeness theorem (36 tests)
├── test_independence.py             # Independence checking (28 tests)
├── test_search.py                   # Search algorithms (51 tests)
├── test_z3_proof.py                 # Z3 proof system (17 tests)
├── test_enumeration_proof.py        # Enumeration proof (3 tests)
├── test_commands_prove.py           # Prove command tests (12 tests)
├── test_commands_validate.py        # Validate command tests (12 tests)
├── test_commands_search.py          # Search command tests (24 tests)
├── test_commands_benchmark.py       # Benchmark command tests (15 tests)
└── test_notebooks.py                # Jupyter notebook validation (9 tests)
```

### Test Categories

#### Unit Tests
Test individual functions and methods in isolation:
- `test_connectives.py` - Connective creation, evaluation, truth tables
- `test_constants.py` - Helper functions, lookups, collections
- `test_post_classes.py` - Post class membership checks

#### Integration Tests
Test complete workflows with real execution:
- `test_search.py` - Full search execution with small datasets
- `test_z3_proof.py::TestZ3Integration` - Small Z3 pool searches
- `test_commands_*.py` - End-to-end command workflows

#### Command Tests
Test CLI command implementations with mocks:
- `test_commands_prove.py` - Z3 and enumeration proof commands
- `test_commands_validate.py` - Binary and ternary validation
- `test_commands_search.py` - Search command variants
- `test_commands_benchmark.py` - Benchmark command structure

#### Notebook Tests
Validate Jupyter notebooks execute without errors:
- `test_notebooks.py` - Uses jupyter nbconvert for execution testing

## Running Tests

### Quick Development Cycle (Recommended)

Run tests excluding slow ones (~60 seconds):

```bash
pytest tests/ -m "not slow"
```

**Output**: 324 passed, 18 deselected

### Full Test Suite (Required for PRs)

Run all tests including slow incremental searches (~8-10 minutes):

```bash
pytest tests/
```

**Output**: 338 passed, 0 skipped, 0 warnings

### Verbose Output

See detailed test names and results:

```bash
pytest tests/ -v
```

### Specific Test Files

```bash
# Run CLI tests only
pytest tests/test_cli.py -v

# Run all command tests
pytest tests/test_commands_*.py -v

# Run a specific test class
pytest tests/test_search.py::TestBinaryOnlySearch -v

# Run a specific test
pytest tests/test_search.py::TestBinaryOnlySearch::test_binary_only_max_size_is_3 -v
```

### Test by Marker

```bash
# Run only slow tests
pytest tests/ -m "slow" -v

# Run only notebook tests
pytest tests/ -m "notebook" -v

# Run only integration tests
pytest tests/ -m "integration" -v

# Exclude multiple markers
pytest tests/ -m "not slow and not notebook" -v
```

### Coverage Reports

Generate HTML coverage report:

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

Generate terminal coverage report:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Parallel Execution (Optional)

Speed up test execution with pytest-xdist:

```bash
pip install pytest-xdist
pytest tests/ -n auto  # Use all CPU cores
```

## Test Markers

Test markers are defined in `pyproject.toml` and used to categorize tests.

### Available Markers

#### `@pytest.mark.slow`
Tests that take more than 1 second to execute.

**Usage**:
```python
@pytest.mark.slow
def test_incremental_search_arity_2_fast(self):
    """Incremental search takes several minutes."""
    max_size, sets, stats = search_incremental_arity(max_arity=2, verbose=False)
    assert max_size == 5
```

**Run slow tests**: `pytest tests/ -m "slow"`
**Exclude slow tests**: `pytest tests/ -m "not slow"`

#### `@pytest.mark.notebook`
Tests that validate Jupyter notebook execution.

**Usage**:
```python
@pytest.mark.notebook
@pytest.mark.slow
def test_notebook_execution(notebook_path):
    """Test that each notebook executes without errors."""
    result = subprocess.run([...])
    assert result.returncode == 0
```

**Run notebook tests**: `pytest tests/ -m "notebook"`

#### `@pytest.mark.integration`
End-to-end tests with real execution (not mocked).

**Usage**:
```python
@pytest.mark.integration
def test_small_pool_search(self):
    """Integration test with real Z3 execution."""
    result = z3_proof_approach_1_symmetry_breaking(...)
    assert result is True
```

**Run integration tests**: `pytest tests/ -m "integration"`

## Testing New Features

### Step-by-Step Process

1. **Write Tests First (TDD Recommended)**
   ```bash
   # Create test file
   touch tests/test_my_feature.py

   # Write failing tests
   # Implement feature
   # Verify tests pass
   ```

2. **Follow Existing Patterns**
   - Use test classes: `class TestMyFeature:`
   - Descriptive test names: `test_my_feature_handles_edge_case`
   - Clear docstrings: Explain what's being tested
   - Use fixtures from `conftest.py`

3. **Use Appropriate Markers**
   ```python
   @pytest.mark.slow
   def test_expensive_operation(self):
       """Mark tests that take >1 second."""
       pass

   @pytest.mark.integration
   def test_real_execution(self):
       """Mark end-to-end tests."""
       pass
   ```

4. **Mock Expensive Operations**
   ```python
   from unittest.mock import Mock, patch

   @patch('src.commands.search.search_binary_only')
   def test_search_command(self, mock_search):
       """Mock expensive searches in command tests."""
       mock_search.return_value = (3, [])
       exit_code = search_binary(max_depth=3)
       assert exit_code == 0
   ```

5. **Run Tests Frequently**
   ```bash
   # Run your new tests
   pytest tests/test_my_feature.py -v

   # Run related tests
   pytest tests/test_search.py tests/test_my_feature.py -v

   # Run all tests
   pytest tests/
   ```

6. **Verify Coverage**
   ```bash
   pytest tests/test_my_feature.py --cov=src.my_feature --cov-report=term-missing
   ```

### Example Test Structure

```python
"""
Test suite for my new feature.

Tests core functionality, edge cases, and integration with existing code.
"""

import pytest
from unittest.mock import Mock, patch
from src.my_feature import my_function


class TestMyFunction:
    """Test my_function basic functionality."""

    def test_basic_case(self):
        """Test normal operation with valid input."""
        result = my_function(input_value=42)
        assert result == expected_value

    def test_edge_case(self):
        """Test boundary condition."""
        result = my_function(input_value=0)
        assert result is not None

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test systematic input variations."""
        assert my_function(input) == expected


class TestMyFunctionIntegration:
    """Test my_function integration with other modules."""

    @pytest.mark.integration
    def test_end_to_end(self):
        """Test complete workflow with real execution."""
        result = my_function(input_value=42)
        assert validate_result(result)
```

## Mock Patching Guidelines

### Critical Rules

**Rule 1: Patch Where Functions Are USED, Not Where They're DEFINED**

```python
# In src/commands/search.py:
from src.search import search_binary_only

def search_binary():
    result = search_binary_only()  # Used here
    return result

# CORRECT - Patch where it's used
@patch('src.commands.search.search_binary_only')
def test_search_binary(mock_search):
    mock_search.return_value = (3, [])
    search_binary()
    assert mock_search.called

# INCORRECT - Patching where it's defined won't work
@patch('src.search.search_binary_only')  # Won't be called!
def test_search_binary(mock_search):
    search_binary()
    assert mock_search.called  # Fails!
```

**Rule 2: For Local Imports, Patch at SOURCE**

```python
# In src/commands/search.py:
def search_validate():
    from src.post_classes import get_missing_classes  # Local import
    missing = get_missing_classes(nice_set)
    return missing

# CORRECT - Patch at source for local imports
@patch('src.post_classes.get_missing_classes')
def test_search_validate(mock_get_missing):
    mock_get_missing.return_value = []
    search_validate()
    assert mock_get_missing.called
```

### Common Patterns

#### Mock Return Values

```python
@patch('src.commands.search.search_binary_only')
def test_with_return_value(mock_search):
    """Mock function with specific return value."""
    mock_search.return_value = (3, [Mock(), Mock(), Mock()])

    result = search_binary()
    assert result == 0
```

#### Mock Multiple Functions

```python
@patch('src.commands.search.analyze_nice_set')
@patch('src.commands.search.search_binary_only')
def test_multiple_mocks(mock_search, mock_analyze):
    """Mock multiple dependencies (bottom-up in decorator order)."""
    mock_search.return_value = (3, [])
    mock_analyze.return_value = {'size': 3}

    result = search_binary()
    mock_search.assert_called_once()
    mock_analyze.assert_called_once()
```

#### Use Fixtures for File I/O

```python
def test_checkpoint_save(tmp_path):
    """Use pytest tmp_path fixture for file operations."""
    checkpoint_file = tmp_path / "checkpoint.json"
    save_checkpoint(checkpoint_file, data)

    assert checkpoint_file.exists()
    assert json.loads(checkpoint_file.read_text()) == data
```

## Pre-PR Checklist

Before submitting a pull request, ensure:

### Required Checks

- [ ] **All tests pass**: `pytest tests/` shows 338+ passed, 0 failed
- [ ] **No skipped tests**: Output shows 0 skipped
- [ ] **No warnings**: No warning messages in output
- [ ] **New features have tests**: Minimum 80% coverage for new code
- [ ] **Slow tests marked**: Use `@pytest.mark.slow` for tests >1s
- [ ] **Expensive operations mocked**: Don't run full searches in unit tests
- [ ] **Documentation updated**: Update README files and docstrings

### Verification Commands

```bash
# 1. Run full test suite
pytest tests/ -v

# Expected output line:
# ========== 338 passed in XXXs ==========

# 2. Check for skipped tests (should be empty)
pytest tests/ -v | grep SKIPPED
# (no output expected)

# 3. Check for warnings (should be empty or only external library warnings)
pytest tests/ -v 2>&1 | grep -i warning
# (no output expected, or only Z3 warnings which are filtered)

# 4. Verify coverage for new code
pytest tests/test_my_feature.py --cov=src.my_feature --cov-report=term-missing
# (should show 80%+ coverage)

# 5. Run slow tests to ensure they pass
pytest tests/ -m "slow" -v
# (may take 8-10 minutes)
```

### Common Issues to Avoid

- **Don't commit with failing tests**
- **Don't skip tests without good reason** (use markers instead)
- **Don't ignore warnings** (fix or filter appropriately)
- **Don't test implementation details** (test behavior, not internals)
- **Don't create brittle tests** (avoid hardcoded values, use fixtures)

## Troubleshooting

### Mock Not Being Called

**Symptom**: `AssertionError: Expected 'function' to be called once. Called 0 times.`

**Cause**: Incorrect patch path (patching where function is defined, not where it's used)

**Solution**:
```python
# Check where the function is imported in the module being tested
# In src/commands/search.py:
from src.search import search_binary_only

# Patch it where it's USED
@patch('src.commands.search.search_binary_only')  # Correct
# NOT where it's DEFINED
@patch('src.search.search_binary_only')  # Wrong
```

### Tests Skipped Unexpectedly

**Symptom**: Output shows "X skipped" but you expect all tests to run

**Cause**: `@pytest.mark.skip` decorator present

**Solution**: Remove skip decorator or replace with conditional skip:
```python
# Remove this:
@pytest.mark.skip(reason="Too slow")

# Use markers instead:
@pytest.mark.slow
```

### Warnings About Unknown Markers

**Symptom**: `PytestUnknownMarkWarning: Unknown pytest.mark.mymarker`

**Cause**: Marker not registered in `pyproject.toml`

**Solution**: Add marker to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "mymarker: description of my marker",
]
```

### Notebook Tests Failing

**Symptom**: `ModuleNotFoundError: No module named 'jupyter'`

**Cause**: Missing notebook dependencies

**Solution**: Install Jupyter dependencies:
```bash
pip install jupyter nbconvert ipykernel
```

### Z3 Deprecation Warnings

**Symptom**: Warnings about `pkg_resources is deprecated`

**Status**: Already filtered in `pyproject.toml`

**Verification**: These warnings from external Z3 library are automatically suppressed:
```toml
[tool.pytest.ini_options]
filterwarnings = [
    "ignore:pkg_resources is deprecated:DeprecationWarning:z3.*",
    "ignore:Deprecated call to.*pkg_resources.*:DeprecationWarning",
]
```

### Tests Too Slow

**Symptom**: Test suite takes too long during development

**Solution**: Exclude slow tests during development:
```bash
# Fast tests only (~60 seconds)
pytest tests/ -m "not slow"

# Run slow tests before committing
pytest tests/ -m "slow"
```

### Import Errors in Tests

**Symptom**: `ModuleNotFoundError: No module named 'src'`

**Cause**: Python path not set up correctly

**Solution**: Run pytest from project root:
```bash
cd /path/to/nice_connectives
pytest tests/
```

Or set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/nice_connectives:$PYTHONPATH
pytest tests/
```

## Test Infrastructure

### Shared Fixtures (conftest.py)

The `tests/conftest.py` file provides shared fixtures used across test files:

#### `sample_connective_pool()`
Returns a small pool of connectives for testing:
```python
def test_my_function(sample_connective_pool):
    """Use predefined connective pool."""
    result = find_nice_sets_of_size(sample_connective_pool, 2)
    assert len(result) > 0
```

#### `temp_checkpoint_file(tmp_path)`
Provides a temporary file path for checkpoint testing:
```python
def test_checkpoint_save(temp_checkpoint_file):
    """Test checkpoint file operations."""
    save_checkpoint(temp_checkpoint_file, data)
    assert temp_checkpoint_file.exists()
```

#### `mock_z3_solver()`
Provides a mocked Z3 solver for fast unit tests:
```python
def test_z3_proof(mock_z3_solver):
    """Test proof logic without real Z3 execution."""
    result = prove_with_z3(mock_z3_solver)
    assert result is not None
```

### Test Configuration (pyproject.toml)

Test behavior is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "notebook: marks notebook validation tests",
    "integration: marks integration tests (end-to-end with real execution)",
]
filterwarnings = [
    "ignore:pkg_resources is deprecated:DeprecationWarning:z3.*",
    "ignore:Deprecated call to.*pkg_resources.*:DeprecationWarning",
]
```

### Dependencies

Test dependencies are specified in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-timeout>=2.1.0",
    "nbval>=0.10.0",  # Optional, not required with nbconvert approach
]
jupyter = [
    "jupyter>=1.0.0",
    "ipykernel>=6.0.0",
]
```

Install test dependencies:
```bash
pip install -e ".[dev]"
pip install -e ".[jupyter]"  # For notebook tests
```

## Additional Resources

- **Project Standards**: See `CLAUDE.md` for code standards and testing strategy
- **Implementation Plans**: See `specs/plans/016_comprehensive_test_coverage.md` for test implementation details
- **pytest Documentation**: https://docs.pytest.org/
- **unittest.mock Guide**: https://docs.python.org/3/library/unittest.mock.html

## Quick Reference

```bash
# Fast development tests (60s)
pytest tests/ -m "not slow"

# Full test suite for PRs (8-10min)
pytest tests/

# Specific test file
pytest tests/test_search.py -v

# Specific test
pytest tests/test_search.py::TestBinaryOnlySearch::test_binary_only_max_size_is_3 -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Parallel execution
pytest tests/ -n auto

# Only slow tests
pytest tests/ -m "slow"

# Exclude slow tests
pytest tests/ -m "not slow"
```

**Expected Output**: `338 passed, 0 failed, 0 skipped, 0 warnings`
