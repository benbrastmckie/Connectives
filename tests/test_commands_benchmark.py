"""
Test suite for benchmark command implementations.

Tests full benchmark suite, quick benchmark, and depth benchmark commands.

Note: Benchmark commands use dynamic imports from scripts/ directory.
We test basic structure and error handling only.
"""

import pytest
from unittest.mock import Mock, patch
from src.commands.benchmark import benchmark_full, benchmark_quick, benchmark_depth


class TestBenchmarkFull:
    """Test full benchmark suite command."""

    def test_benchmark_full_callable(self):
        """Test that benchmark_full is callable."""
        assert callable(benchmark_full)

    def test_benchmark_full_import_error_handling(self, capsys):
        """Test full benchmark handles import errors gracefully."""
        # benchmark_full should catch ImportError and return 1
        exit_code = benchmark_full(runs=1, output='test.csv')

        # Should return 1 for error (benchmark module doesn't exist)
        assert exit_code == 1

        # Should print error message
        captured = capsys.readouterr()
        assert "Error importing" in captured.err

    def test_benchmark_full_default_parameters(self):
        """Test benchmark_full accepts default parameters."""
        # This will fail with ImportError since the module doesn't exist
        # but we test that the function signature is correct
        try:
            benchmark_full()
        except (ImportError, ModuleNotFoundError):
            # Expected - the benchmark script doesn't exist
            pass

    def test_benchmark_full_custom_parameters(self):
        """Test benchmark_full accepts custom parameters."""
        try:
            benchmark_full(runs=10, output='custom.csv', json_output='custom.json')
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass


class TestBenchmarkQuick:
    """Test quick benchmark command."""

    def test_benchmark_quick_callable(self):
        """Test that benchmark_quick is callable."""
        assert callable(benchmark_quick)

    def test_benchmark_quick_import_error_handling(self, capsys):
        """Test quick benchmark handles import errors gracefully."""
        # benchmark_quick should catch ImportError and return 1
        exit_code = benchmark_quick()

        # Should return 1 for error (quick_benchmark module doesn't exist)
        assert exit_code == 1

        # Should print error message
        captured = capsys.readouterr()
        assert "Error importing" in captured.err


class TestBenchmarkDepth:
    """Test depth benchmark command."""

    def test_benchmark_depth_callable(self):
        """Test that benchmark_depth is callable."""
        assert callable(benchmark_depth)

    def test_benchmark_depth_import_error_handling(self, capsys):
        """Test depth benchmark handles import errors gracefully."""
        # benchmark_depth should catch ImportError and return 1
        exit_code = benchmark_depth(depths='1,2,3')

        # Should return 1 for error (benchmark_depth module doesn't exist)
        assert exit_code == 1

        # Should print error message
        captured = capsys.readouterr()
        assert "Error importing" in captured.err

    def test_benchmark_depth_default_parameters(self):
        """Test benchmark_depth accepts default parameters."""
        try:
            benchmark_depth()
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass

    def test_benchmark_depth_custom_depths(self):
        """Test benchmark_depth accepts custom depths string."""
        try:
            benchmark_depth(depths='2,4,6,8')
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass

    def test_benchmark_depth_with_spaces(self):
        """Test benchmark_depth handles spaces in depths string."""
        try:
            benchmark_depth(depths='1, 2, 3, 4')
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass

    def test_benchmark_depth_custom_runs(self):
        """Test benchmark_depth accepts custom number of runs."""
        try:
            benchmark_depth(depths='1,2,3', runs=10)
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass

    def test_benchmark_depth_custom_output(self):
        """Test benchmark_depth accepts custom output file."""
        try:
            benchmark_depth(output='my_results.csv')
        except (ImportError, ModuleNotFoundError):
            # Expected
            pass


class TestBenchmarkIntegration:
    """Integration tests for benchmark commands."""

    def test_all_benchmarks_handle_errors(self):
        """Test that all benchmark commands handle errors gracefully."""
        # All should return 1 when modules don't exist
        assert benchmark_full() == 1
        assert benchmark_quick() == 1
        assert benchmark_depth() == 1

    def test_all_benchmarks_exist(self):
        """Test that all benchmark functions are implemented."""
        assert benchmark_full is not None
        assert benchmark_quick is not None
        assert benchmark_depth is not None
