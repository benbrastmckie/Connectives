"""
Test suite for validate command implementations.

Tests both binary and ternary validation commands.
"""

import pytest
from unittest.mock import Mock, patch
from src.commands.validate import validate_binary, validate_ternary
from src.independence import DefinabilityMode


class TestValidateBinary:
    """Test binary-only validation command."""

    @patch('src.search.search_binary_only')
    def test_validate_binary_success(self, mock_search):
        """Test binary validation when max size is 3 (expected)."""
        # Mock search returning max_size=3
        mock_search.return_value = (3, [])

        exit_code = validate_binary(depth=3)

        # Should return 0 for success
        assert exit_code == 0

        # Verify search was called with correct parameters
        mock_search.assert_called_once_with(
            max_depth=3,
            verbose=True,
            use_symmetry_breaking=True,
            definability_mode=DefinabilityMode.SYNTACTIC
        )

    @patch('src.search.search_binary_only')
    def test_validate_binary_failure(self, mock_search):
        """Test binary validation when max size is not 3 (unexpected)."""
        # Mock search returning max_size=4 (wrong!)
        mock_search.return_value = (4, [])

        exit_code = validate_binary(depth=3)

        # Should return 1 for failure
        assert exit_code == 1

    @patch('src.search.search_binary_only')
    def test_validate_binary_custom_depth(self, mock_search):
        """Test binary validation with custom depth parameter."""
        mock_search.return_value = (3, [])

        exit_code = validate_binary(depth=5)

        # Verify custom depth was passed
        assert mock_search.call_args[1]['max_depth'] == 5

    @patch('src.search.search_binary_only')
    def test_validate_binary_without_symmetry_breaking(self, mock_search):
        """Test binary validation with symmetry breaking disabled."""
        mock_search.return_value = (3, [])

        exit_code = validate_binary(depth=3, use_symmetry_breaking=False)

        # Verify symmetry breaking was disabled
        assert mock_search.call_args[1]['use_symmetry_breaking'] is False

    @patch('src.search.search_binary_only')
    def test_validate_binary_syntactic_mode(self, mock_search):
        """Test binary validation with syntactic mode."""
        mock_search.return_value = (3, [])

        exit_code = validate_binary(definability_mode=DefinabilityMode.SYNTACTIC)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.SYNTACTIC

    @patch('src.search.search_binary_only')
    def test_validate_binary_truth_functional_mode(self, mock_search):
        """Test binary validation with truth-functional mode."""
        mock_search.return_value = (3, [])

        exit_code = validate_binary(definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.TRUTH_FUNCTIONAL

    @patch('src.search.search_binary_only')
    def test_validate_binary_prints_output(self, mock_search, capsys):
        """Test binary validation prints expected output."""
        mock_search.return_value = (3, [])

        validate_binary(depth=3, use_symmetry_breaking=True)

        captured = capsys.readouterr()

        # Verify output contains key information
        assert "BINARY-ONLY SEARCH VALIDATION" in captured.out
        assert "Composition depth: 3" in captured.out
        assert "Symmetry breaking: True" in captured.out
        assert "VALIDATION STATUS" in captured.out
        assert "PASS" in captured.out


class TestValidateTernary:
    """Test ternary validation command.

    Note: Ternary validation uses dynamic imports which are difficult to test.
    We test basic structure and error handling only.
    """

    def test_validate_ternary_callable(self):
        """Test that validate_ternary is callable."""
        assert callable(validate_ternary)

    def test_validate_ternary_default_parameters(self):
        """Test validate_ternary accepts default parameters."""
        # This will fail with ImportError since the module doesn't exist
        # but we test that the function signature is correct
        try:
            validate_ternary(depth=3, compare=False, use_z3=False)
        except (ImportError, ModuleNotFoundError):
            # Expected - the validation script doesn't exist
            pass

    def test_validate_ternary_import_error_handling(self, capsys):
        """Test ternary validation handles import errors gracefully."""
        # validate_ternary should catch ImportError and return 1
        exit_code = validate_ternary(depth=3)

        # Should return 1 for error (validation script doesn't exist)
        assert exit_code == 1

        # Should print error message
        captured = capsys.readouterr()
        assert "Error importing" in captured.err


class TestValidateIntegration:
    """Integration tests for validate commands."""

    @patch('src.search.search_binary_only')
    def test_validate_binary_full_workflow(self, mock_search, capsys):
        """Test complete binary validation workflow."""
        # Mock successful validation
        mock_search.return_value = (3, [Mock(), Mock(), Mock()])

        exit_code = validate_binary(depth=3, use_symmetry_breaking=True)

        # Verify success
        assert exit_code == 0

        # Verify output
        captured = capsys.readouterr()
        assert "PASS" in captured.out
        assert "maximum size of 3" in captured.out

    @patch('src.search.search_binary_only')
    def test_validate_binary_failure_workflow(self, mock_search, capsys):
        """Test binary validation failure workflow."""
        # Mock unexpected result
        mock_search.return_value = (2, [])  # Too small!

        exit_code = validate_binary()

        # Verify failure
        assert exit_code == 1

        # Verify output
        captured = capsys.readouterr()
        assert "FAIL" in captured.out
        assert "Expected max=3, got max=2" in captured.out
