"""
Benchmark commands for performance measurement.

This module provides command implementations for benchmarking search
performance across different configurations.
"""

import sys
from pathlib import Path


def benchmark_full(runs=5, output='benchmarks.csv', json_output=None):
    """
    Run comprehensive benchmark suite.

    Args:
        runs: Number of runs per benchmark
        output: Output CSV file path
        json_output: Optional JSON output file path

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/benchmarks to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "benchmarks"
    sys.path.insert(0, str(script_dir))

    try:
        import benchmark

        # Run benchmarks
        results = benchmark.run_comprehensive_benchmark(runs=runs)

        # Print summary
        benchmark.print_results_summary(results)

        # Save results
        benchmark.save_results_csv(results, output)

        if json_output:
            benchmark.save_results_json(results, json_output)

        print()
        print("=" * 80)
        print("BENCHMARK COMPLETE")
        print("=" * 80)

        return 0

    except ImportError as e:
        print(f"Error importing benchmark module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))


def benchmark_quick():
    """
    Run quick performance benchmark.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/benchmarks to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "benchmarks"
    sys.path.insert(0, str(script_dir))

    try:
        import quick_benchmark
        return quick_benchmark.main()

    except ImportError as e:
        print(f"Error importing benchmark module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))


def benchmark_depth(depths='1,2,3,4,5', runs=3, output='depth_results.csv'):
    """
    Benchmark composition depth performance.

    Args:
        depths: Comma-separated list of depths to test
        runs: Number of runs per depth
        output: Output CSV file path

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/benchmarks to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "benchmarks"
    sys.path.insert(0, str(script_dir))

    try:
        import benchmark_depth

        # Parse depths
        depth_list = [int(d.strip()) for d in depths.split(',')]

        # Run benchmark
        benchmark_depth.run_benchmark_suite(depth_list, runs=runs, output=output)

        return 0

    except ImportError as e:
        print(f"Error importing benchmark module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))
