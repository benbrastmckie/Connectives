"""
Tests for CLI argument parsing and command routing.

This module tests the command-line interface defined in src/cli.py,
including subcommand structure, argument parsing, and flag handling.
"""

import pytest
import sys
from unittest.mock import patch, Mock
from src.cli import main


class TestCLIStructure:
    """Test CLI parser structure and subcommand organization."""

    def test_no_arguments_shows_help(self):
        """Test that running with no arguments shows help."""
        with patch('sys.argv', ['nice-connectives']):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_command(self):
        """Test that invalid commands cause SystemExit."""
        with patch('sys.argv', ['nice-connectives', 'invalid']):
            with pytest.raises(SystemExit):
                main()


class TestProveZ3Arguments:
    """Test 'prove z3' subcommand argument parsing."""

    @patch('src.commands.prove.prove_z3')
    def test_prove_z3_defaults(self, mock_prove_z3):
        """Test prove z3 with default arguments."""
        mock_prove_z3.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3']):
            result = main()

        assert result == 0
        mock_prove_z3.assert_called_once()
        call_args = mock_prove_z3.call_args
        assert call_args.kwargs['checkpoint'] is None
        assert call_args.kwargs['interval'] == 100
        assert call_args.kwargs['target_size'] == 17
        assert call_args.kwargs['max_depth'] == 3

    @patch('src.commands.prove.prove_z3')
    def test_prove_z3_with_checkpoint(self, mock_prove_z3):
        """Test prove z3 with checkpoint argument."""
        mock_prove_z3.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3', '--checkpoint', 'test.json']):
            result = main()

        assert result == 0
        call_args = mock_prove_z3.call_args
        assert call_args.kwargs['checkpoint'] == 'test.json'

    @patch('src.commands.prove.prove_z3')
    def test_prove_z3_with_custom_interval(self, mock_prove_z3):
        """Test prove z3 with custom checkpoint interval."""
        mock_prove_z3.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3', '--interval', '50']):
            result = main()

        assert result == 0
        call_args = mock_prove_z3.call_args
        assert call_args.kwargs['interval'] == 50

    @patch('src.commands.prove.prove_z3')
    def test_prove_z3_with_target_size(self, mock_prove_z3):
        """Test prove z3 with custom target size."""
        mock_prove_z3.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3', '--target-size', '20']):
            result = main()

        assert result == 0
        call_args = mock_prove_z3.call_args
        assert call_args.kwargs['target_size'] == 20

    @patch('src.commands.prove.prove_z3')
    def test_prove_z3_definability_mode(self, mock_prove_z3):
        """Test prove z3 with definability mode flag."""
        mock_prove_z3.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3', '--definability-mode', 'syntactic']):
            result = main()

        assert result == 0
        call_args = mock_prove_z3.call_args
        # Should convert 'syntactic' to DefinabilityMode.SYNTACTIC
        assert str(call_args.kwargs['definability_mode']) == 'DefinabilityMode.SYNTACTIC'


class TestProveEnumArguments:
    """Test 'prove enum' subcommand argument parsing."""

    @patch('src.commands.prove.prove_enumeration')
    def test_prove_enum_defaults(self, mock_prove_enum):
        """Test prove enum with default arguments."""
        mock_prove_enum.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'prove', 'enum']):
            result = main()

        assert result == 0
        mock_prove_enum.assert_called_once()


class TestValidateBinaryArguments:
    """Test 'validate binary' subcommand argument parsing."""

    @patch('src.commands.validate.validate_binary')
    def test_validate_binary_defaults(self, mock_validate):
        """Test validate binary with default arguments."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'binary']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['depth'] == 3
        assert call_args.kwargs['use_z3'] is False
        assert call_args.kwargs['use_symmetry_breaking'] is True

    @patch('src.commands.validate.validate_binary')
    def test_validate_binary_with_z3(self, mock_validate):
        """Test validate binary with --use-z3 flag."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'binary', '--use-z3']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['use_z3'] is True

    @patch('src.commands.validate.validate_binary')
    def test_validate_binary_no_symmetry_breaking(self, mock_validate):
        """Test validate binary with --no-symmetry-breaking flag."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'binary', '--no-symmetry-breaking']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['use_symmetry_breaking'] is False


class TestValidateTernaryArguments:
    """Test 'validate ternary' subcommand argument parsing."""

    @patch('src.commands.validate.validate_ternary')
    def test_validate_ternary_defaults(self, mock_validate):
        """Test validate ternary with default arguments."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'ternary']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['depth'] == 3
        assert call_args.kwargs['compare'] is False
        assert call_args.kwargs['verbose'] is False

    @patch('src.commands.validate.validate_ternary')
    def test_validate_ternary_with_compare(self, mock_validate):
        """Test validate ternary with --compare flag."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'ternary', '--compare']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['compare'] is True

    @patch('src.commands.validate.validate_ternary')
    def test_validate_ternary_with_verbose(self, mock_validate):
        """Test validate ternary with --verbose flag."""
        mock_validate.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'validate', 'ternary', '--verbose']):
            result = main()

        assert result == 0
        call_args = mock_validate.call_args
        assert call_args.kwargs['verbose'] is True


class TestBenchmarkArguments:
    """Test 'benchmark' subcommand argument parsing."""

    @patch('src.commands.benchmark.benchmark_full')
    def test_benchmark_full_defaults(self, mock_benchmark):
        """Test benchmark full with default arguments."""
        mock_benchmark.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'benchmark', 'full']):
            result = main()

        assert result == 0
        call_args = mock_benchmark.call_args
        assert call_args.kwargs['runs'] == 5
        assert call_args.kwargs['output'] == 'benchmarks.csv'

    @patch('src.commands.benchmark.benchmark_full')
    def test_benchmark_full_custom_runs(self, mock_benchmark):
        """Test benchmark full with custom runs."""
        mock_benchmark.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'benchmark', 'full', '--runs', '10']):
            result = main()

        assert result == 0
        call_args = mock_benchmark.call_args
        assert call_args.kwargs['runs'] == 10

    @patch('src.commands.benchmark.benchmark_quick')
    def test_benchmark_quick(self, mock_benchmark):
        """Test benchmark quick command."""
        mock_benchmark.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'benchmark', 'quick']):
            result = main()

        assert result == 0
        mock_benchmark.assert_called_once()

    @patch('src.commands.benchmark.benchmark_depth')
    def test_benchmark_depth_defaults(self, mock_benchmark):
        """Test benchmark depth with default arguments."""
        mock_benchmark.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'benchmark', 'depth']):
            result = main()

        assert result == 0
        call_args = mock_benchmark.call_args
        assert call_args.kwargs['depths'] == '1,2,3,4,5'
        assert call_args.kwargs['runs'] == 3


class TestSearchArguments:
    """Test 'search' subcommand argument parsing."""

    @patch('src.commands.search.search_binary')
    def test_search_binary_defaults(self, mock_search):
        """Test search binary with default arguments."""
        mock_search.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'search', 'binary']):
            result = main()

        assert result == 0
        call_args = mock_search.call_args
        assert call_args.kwargs['max_depth'] == 3
        assert call_args.kwargs['verbose'] is True

    @patch('src.commands.search.search_binary')
    def test_search_binary_quiet(self, mock_search):
        """Test search binary with --quiet flag."""
        mock_search.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'search', 'binary', '--quiet']):
            result = main()

        assert result == 0
        call_args = mock_search.call_args
        assert call_args.kwargs['verbose'] is False

    @patch('src.commands.search.search_full')
    def test_search_full_defaults(self, mock_search):
        """Test search full with default arguments."""
        mock_search.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'search', 'full']):
            result = main()

        assert result == 0
        call_args = mock_search.call_args
        assert call_args.kwargs['max_arity'] == 3
        assert call_args.kwargs['max_depth'] == 3

    @patch('src.commands.search.search_validate')
    def test_search_validate(self, mock_search):
        """Test search validate command."""
        mock_search.return_value = 0

        with patch('sys.argv', ['nice-connectives', 'search', 'validate']):
            result = main()

        assert result == 0
        mock_search.assert_called_once()


class TestErrorHandling:
    """Test CLI error handling."""

    @patch('src.commands.prove.prove_z3')
    def test_exception_handling(self, mock_prove_z3):
        """Test that exceptions are caught and return error code."""
        mock_prove_z3.side_effect = Exception("Test error")

        with patch('sys.argv', ['nice-connectives', 'prove', 'z3']):
            with patch('sys.stderr'):
                result = main()

        assert result == 1
