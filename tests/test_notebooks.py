"""
Test suite for Jupyter notebook validation.

This module tests that all Jupyter notebooks execute without errors,
ensuring imports work correctly and all cells run successfully.
"""

import pytest
from pathlib import Path
import subprocess
import sys


# Get project root and notebook directory
PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"


def get_all_notebooks():
    """Get list of all notebook files to test."""
    return sorted(NOTEBOOK_DIR.glob("*.ipynb"))


@pytest.mark.notebook
@pytest.mark.slow
@pytest.mark.parametrize("notebook_path", get_all_notebooks(),
                         ids=lambda p: p.name)
def test_notebook_execution(notebook_path):
    """
    Test that each notebook executes without errors.

    This test runs each notebook through nbval to validate:
    - All imports resolve correctly
    - All cells execute without errors
    - No runtime exceptions occur

    Note: This test is marked as 'slow' because notebooks can take
    several seconds to execute. Skip with: pytest -m "not slow"
    """
    # Use pytest's nbval plugin via command line
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--nbval", str(notebook_path), "-v"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    # Check if notebook executed successfully
    assert result.returncode == 0, (
        f"Notebook {notebook_path.name} failed to execute.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


@pytest.mark.notebook
def test_all_notebooks_exist():
    """
    Verify that all expected notebooks are present.

    This quick test ensures the notebook directory structure is intact.
    """
    notebooks = get_all_notebooks()

    # We expect at least 7 notebooks based on recent additions
    assert len(notebooks) >= 7, (
        f"Expected at least 7 notebooks, found {len(notebooks)}"
    )

    # Verify key notebooks exist
    expected_notebooks = [
        "00_setup_and_basics.ipynb",
        "01_connectives_intro.ipynb",
        "02_truth_tables.ipynb",
        "03_completeness.ipynb",
        "04_independence.ipynb",
        "05_search_binary.ipynb",
        "06_search_ternary.ipynb",
    ]

    notebook_names = [nb.name for nb in notebooks]

    for expected in expected_notebooks:
        assert expected in notebook_names, (
            f"Expected notebook '{expected}' not found in {NOTEBOOK_DIR}"
        )


@pytest.mark.notebook
def test_notebook_directory_structure():
    """
    Verify notebook directory has proper structure.

    Checks for:
    - notebooks/ directory exists
    - README.md exists
    - utils.py exists (if present)
    """
    assert NOTEBOOK_DIR.exists(), f"Notebook directory not found: {NOTEBOOK_DIR}"
    assert NOTEBOOK_DIR.is_dir(), f"Not a directory: {NOTEBOOK_DIR}"

    readme = NOTEBOOK_DIR / "README.md"
    assert readme.exists(), f"Missing notebooks/README.md"
