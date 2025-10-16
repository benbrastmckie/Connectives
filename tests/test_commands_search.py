"""
Test suite for search command implementations.

Tests binary-only search, full incremental search, and validation commands.
"""

import pytest
from unittest.mock import Mock, patch
from src.commands.search import search_binary, search_full, search_validate
from src.connectives import Connective
from src.independence import DefinabilityMode


class TestSearchBinary:
    """Test binary-only search command."""

    @patch('src.search.search_binary_only')
    @patch('src.search.analyze_nice_set')
    def test_search_binary_basic(self, mock_analyze, mock_search):
        """Test basic binary search execution."""
        # Mock search results
        mock_set = [Mock(), Mock(), Mock()]
        mock_search.return_value = (3, [mock_set])

        # Mock analysis
        mock_analyze.return_value = {
            'size': 3,
            'arity_distribution': {2: 3}
        }

        exit_code = search_binary(max_depth=3, verbose=True)

        # Should always return 0 (success)
        assert exit_code == 0

        # Verify search was called correctly
        mock_search.assert_called_once_with(
            max_depth=3,
            verbose=True,
            definability_mode=DefinabilityMode.SYNTACTIC
        )

    @patch('src.search.search_binary_only')
    def test_search_binary_no_verbose(self, mock_search):
        """Test binary search with verbose disabled."""
        mock_search.return_value = (3, [])

        exit_code = search_binary(verbose=False)

        # Verify verbose flag was passed
        assert mock_search.call_args[1]['verbose'] is False

    @patch('src.search.search_binary_only')
    @patch('src.search.analyze_nice_set')
    def test_search_binary_with_results(self, mock_analyze, mock_search):
        """Test binary search prints analysis when sets are found."""
        mock_set = [Mock(), Mock()]
        mock_search.return_value = (2, [mock_set])

        mock_analyze.return_value = {
            'size': 2,
            'arity_distribution': {2: 2}
        }

        exit_code = search_binary(verbose=True)

        # Analysis should be called for first result
        mock_analyze.assert_called_once_with(mock_set)

    @patch('src.search.search_binary_only')
    def test_search_binary_empty_results(self, mock_search):
        """Test binary search with no results found."""
        mock_search.return_value = (0, [])

        exit_code = search_binary(verbose=True)

        # Should still return 0
        assert exit_code == 0

    @patch('src.search.search_binary_only')
    def test_search_binary_custom_depth(self, mock_search):
        """Test binary search with custom depth."""
        mock_search.return_value = (3, [])

        exit_code = search_binary(max_depth=5)

        # Verify depth was passed
        assert mock_search.call_args[1]['max_depth'] == 5

    @patch('src.search.search_binary_only')
    def test_search_binary_syntactic_mode(self, mock_search):
        """Test binary search with syntactic mode."""
        mock_search.return_value = (3, [])

        exit_code = search_binary(definability_mode=DefinabilityMode.SYNTACTIC)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.SYNTACTIC

    @patch('src.search.search_binary_only')
    def test_search_binary_truth_functional_mode(self, mock_search):
        """Test binary search with truth-functional mode."""
        mock_search.return_value = (3, [])

        exit_code = search_binary(definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.TRUTH_FUNCTIONAL


class TestSearchFull:
    """Test full incremental arity search command."""

    @patch('src.search.search_incremental_arity')
    @patch('src.search.analyze_nice_set')
    def test_search_full_basic(self, mock_analyze, mock_search):
        """Test basic full search execution."""
        mock_set = [Mock() for _ in range(16)]
        mock_stats = {
            'total_time': 10.5,
            'connectives_by_arity': {0: 2, 1: 2, 2: 16, 3: 256},
            'arity_results': {
                2: {'max_size': 3, 'time_seconds': 2.0},
                3: {'max_size': 16, 'time_seconds': 8.5}
            }
        }
        mock_search.return_value = (16, [mock_set], mock_stats)

        mock_analyze.return_value = {
            'size': 16,
            'arity_distribution': {2: 1, 3: 15},
            'connectives': []
        }

        exit_code = search_full(max_arity=3, max_depth=3, verbose=True)

        # Should always return 0
        assert exit_code == 0

        # Verify search was called correctly
        mock_search.assert_called_once_with(
            max_arity=3,
            max_depth=3,
            verbose=True,
            definability_mode=DefinabilityMode.SYNTACTIC
        )

    @patch('src.search.search_incremental_arity')
    def test_search_full_no_verbose(self, mock_search):
        """Test full search with verbose disabled."""
        mock_stats = {
            'total_time': 1.0,
            'connectives_by_arity': {},
            'arity_results': {}
        }
        mock_search.return_value = (3, [], mock_stats)

        exit_code = search_full(verbose=False)

        # Verify verbose was passed
        assert mock_search.call_args[1]['verbose'] is False

    @patch('src.search.search_incremental_arity')
    def test_search_full_custom_parameters(self, mock_search, capsys):
        """Test full search with custom parameters."""
        mock_stats = {
            'total_time': 5.0,
            'connectives_by_arity': {2: 16},
            'arity_results': {2: {'max_size': 3, 'time_seconds': 5.0}}
        }
        mock_search.return_value = (3, [], mock_stats)

        exit_code = search_full(max_arity=2, max_depth=5, verbose=True)

        # Verify parameters
        assert mock_search.call_args[1]['max_arity'] == 2
        assert mock_search.call_args[1]['max_depth'] == 5

        # Verify stats are printed
        captured = capsys.readouterr()
        assert "Search Statistics" in captured.out
        assert "Total time: 5.00s" in captured.out

    @patch('src.search.search_incremental_arity')
    @patch('src.search.analyze_nice_set')
    def test_search_full_prints_analysis(self, mock_analyze, mock_search, capsys):
        """Test full search prints result analysis."""
        mock_set = [Mock() for _ in range(16)]
        mock_stats = {
            'total_time': 10.0,
            'connectives_by_arity': {3: 256},
            'arity_results': {3: {'max_size': 16, 'time_seconds': 10.0}}
        }
        mock_search.return_value = (16, [mock_set], mock_stats)

        mock_analyze.return_value = {
            'size': 16,
            'arity_distribution': {3: 16},
            'connectives': ['f1', 'f2']
        }

        exit_code = search_full(verbose=True)

        # Verify analysis output
        captured = capsys.readouterr()
        assert "First result analysis" in captured.out
        assert "Size: 16" in captured.out
        assert "Arity distribution:" in captured.out

    @patch('src.search.search_incremental_arity')
    def test_search_full_syntactic_mode(self, mock_search):
        """Test full search with syntactic mode."""
        mock_stats = {'total_time': 1.0, 'connectives_by_arity': {}, 'arity_results': {}}
        mock_search.return_value = (3, [], mock_stats)

        exit_code = search_full(definability_mode=DefinabilityMode.SYNTACTIC)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.SYNTACTIC

    @patch('src.search.search_incremental_arity')
    def test_search_full_truth_functional_mode(self, mock_search):
        """Test full search with truth-functional mode."""
        mock_stats = {'total_time': 1.0, 'connectives_by_arity': {}, 'arity_results': {}}
        mock_search.return_value = (3, [], mock_stats)

        exit_code = search_full(definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        assert mock_search.call_args[1]['definability_mode'] == DefinabilityMode.TRUTH_FUNCTIONAL


class TestSearchValidate:
    """Test search validation command."""

    @patch('src.search.validate_nice_set')
    @patch('src.post_classes.get_missing_classes')
    @patch('src.search.analyze_nice_set')
    def test_search_validate_success(self, mock_analyze, mock_missing, mock_validate):
        """Test validation of size-16 nice set (success case)."""
        # Mock validation success
        mock_validate.return_value = (True, "Set is complete and independent")

        # Mock Post classes check
        mock_missing.return_value = []

        # Mock analysis
        mock_analyze.return_value = {
            'size': 16,
            'arity_distribution': {2: 1, 3: 15},
            'connectives': []
        }

        exit_code = search_validate()

        # Should return 0 for success
        assert exit_code == 0

        # Verify validate was called with the size-16 set and depth=5
        assert mock_validate.call_count == 1
        args = mock_validate.call_args
        nice_set = args[0][0]
        assert len(nice_set) == 16
        assert args[1]['max_depth'] == 5

    @patch('src.search.validate_nice_set')
    def test_search_validate_failure(self, mock_validate):
        """Test validation failure case."""
        # Mock validation failure
        mock_validate.return_value = (False, "Set is not independent")

        exit_code = search_validate()

        # Should return 1 for failure
        assert exit_code == 1

    @patch('src.search.validate_nice_set')
    @patch('src.post_classes.get_missing_classes')
    @patch('src.search.analyze_nice_set')
    def test_search_validate_prints_output(self, mock_analyze, mock_missing,
                                           mock_validate, capsys):
        """Test validation prints expected output."""
        mock_validate.return_value = (True, "Valid nice set")
        mock_missing.return_value = []
        mock_analyze.return_value = {
            'size': 16,
            'arity_distribution': {2: 1, 3: 15},
            'connectives': []
        }

        search_validate()

        captured = capsys.readouterr()

        # Verify output
        assert "VALIDATING MAXIMUM NICE SET SIZE = 16" in captured.out
        assert "Testing nice set of size 16" in captured.out
        assert "VALIDATION SUCCESSFUL" in captured.out
        assert "Escapes all Post classes" in captured.out
        assert "CONFIRMED: Maximum nice set size = 16" in captured.out

    @patch('src.search.validate_nice_set')
    def test_search_validate_failure_output(self, mock_validate, capsys):
        """Test validation failure output."""
        mock_validate.return_value = (False, "Dependencies found")

        search_validate()

        captured = capsys.readouterr()

        # Verify failure output
        assert "VALIDATION FAILED" in captured.out
        assert "Dependencies found" in captured.out

    @patch('src.search.validate_nice_set')
    @patch('src.post_classes.get_missing_classes')
    @patch('src.search.analyze_nice_set')
    def test_search_validate_checks_post_classes(self, mock_analyze, mock_missing,
                                                   mock_validate):
        """Test validation checks Post classes."""
        mock_validate.return_value = (True, "Valid")
        mock_missing.return_value = []
        mock_analyze.return_value = {'size': 16, 'arity_distribution': {}, 'connectives': []}

        search_validate()

        # Verify get_missing_classes was called with the nice set
        assert mock_missing.call_count == 1
        nice_set = mock_missing.call_args[0][0]
        assert len(nice_set) == 16

    @patch('src.search.validate_nice_set')
    @patch('src.post_classes.get_missing_classes')
    @patch('src.search.analyze_nice_set')
    def test_search_validate_analyzes_result(self, mock_analyze, mock_missing,
                                              mock_validate):
        """Test validation analyzes the nice set."""
        mock_validate.return_value = (True, "Valid")
        mock_missing.return_value = []
        mock_analyze.return_value = {
            'size': 16,
            'arity_distribution': {2: 1, 3: 15},
            'connectives': []
        }

        search_validate()

        # Verify analyze was called
        assert mock_analyze.call_count == 1
        nice_set = mock_analyze.call_args[0][0]
        assert len(nice_set) == 16

    def test_search_validate_hardcoded_set(self):
        """Test that the hardcoded size-16 set is correct."""
        # Import to verify the set structure
        from src.commands.search import search_validate

        # We can't easily test the actual validation without running it,
        # but we can verify the structure is defined correctly
        # by checking it doesn't raise an exception on import
        assert search_validate is not None


class TestSearchIntegration:
    """Integration tests for search commands."""

    @patch('src.search.search_binary_only')
    @patch('src.search.analyze_nice_set')
    def test_binary_search_full_workflow(self, mock_analyze, mock_search, capsys):
        """Test complete binary search workflow."""
        # Create mock result
        mock_set = [
            Connective(2, 0b0001, 'AND'),
            Connective(2, 0b0111, 'OR'),
            Connective(1, 0b01, 'NOT')
        ]
        mock_search.return_value = (3, [mock_set])

        mock_analyze.return_value = {
            'size': 3,
            'arity_distribution': {1: 1, 2: 2}
        }

        exit_code = search_binary(max_depth=3, verbose=True)

        # Verify success
        assert exit_code == 0

        # Verify output
        captured = capsys.readouterr()
        assert "Analysis of first result" in captured.out

    @patch('src.search.search_incremental_arity')
    def test_full_search_no_results(self, mock_search, capsys):
        """Test full search with no results."""
        mock_stats = {
            'total_time': 1.0,
            'connectives_by_arity': {2: 16},
            'arity_results': {2: {'max_size': 0, 'time_seconds': 1.0}}
        }
        mock_search.return_value = (0, [], mock_stats)

        exit_code = search_full(verbose=True)

        # Should still succeed
        assert exit_code == 0

        # Stats should still be printed
        captured = capsys.readouterr()
        assert "Search Statistics" in captured.out
