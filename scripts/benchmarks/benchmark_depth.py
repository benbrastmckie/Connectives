#!/usr/bin/env python3
"""
Systematic depth benchmarking for crossover analysis.

Measures performance across different composition depths to identify
the empirical crossover point where enumeration becomes impractical.
"""

import sys
import time
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add project root directory to path for imports (now 2 levels up from scripts/benchmarks/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.search import search_binary_only


def benchmark_depth(depth: int, runs: int = 3) -> Dict[str, Any]:
    """
    Benchmark binary search at a specific depth.

    Args:
        depth: Composition depth to test
        runs: Number of runs to average

    Returns:
        Dictionary with benchmark results
    """
    times = []
    max_sizes = []
    num_sets_list = []

    print(f"  Depth {depth}:", end=" ", flush=True)

    for run in range(runs):
        start = time.time()

        max_size, nice_sets = search_binary_only(
            max_depth=depth,
            verbose=False,
            use_z3=False,
            use_symmetry_breaking=True
        )

        elapsed = time.time() - start
        times.append(elapsed)
        max_sizes.append(max_size)
        num_sets_list.append(len(nice_sets))

        print(f"{elapsed:.3f}s", end=" " if run < runs - 1 else "", flush=True)

    print(f"(avg: {sum(times)/len(times):.3f}s)")

    return {
        'depth': depth,
        'runs': runs,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'std_dev': (sum((t - sum(times)/len(times))**2 for t in times) / len(times))**0.5,
        'max_size': max_sizes[0],  # Should be consistent
        'avg_num_sets': sum(num_sets_list) / len(num_sets_list),
        'all_times': times
    }


def run_benchmark_suite(depths: List[int], runs: int = 3, output: str = None):
    """
    Run comprehensive depth benchmark suite.

    Args:
        depths: List of depths to test
        runs: Number of runs per depth
        output: Output CSV file path (optional)
    """
    print("=" * 80)
    print("DEPTH CROSSOVER BENCHMARK")
    print("=" * 80)
    print(f"Depths to test: {depths}")
    print(f"Runs per depth: {runs}")
    print()

    results = []

    for depth in depths:
        try:
            result = benchmark_depth(depth, runs=runs)
            results.append(result)
        except Exception as e:
            print(f"  ERROR at depth {depth}: {e}")
            results.append({
                'depth': depth,
                'error': str(e)
            })

    # Print summary table
    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"{'Depth':<8} {'Avg Time':<12} {'Min Time':<12} {'Max Time':<12} {'Max Size':<10}")
    print("-" * 80)

    for result in results:
        if 'error' in result:
            print(f"{result['depth']:<8} ERROR: {result['error']}")
        else:
            print(f"{result['depth']:<8} "
                  f"{result['avg_time']:<12.4f} "
                  f"{result['min_time']:<12.4f} "
                  f"{result['max_time']:<12.4f} "
                  f"{result['max_size']:<10}")

    # Save to CSV if requested
    if output:
        save_to_csv(results, output)
        print(f"\nResults saved to: {output}")

    print()
    print("=" * 80)


def save_to_csv(results: List[Dict[str, Any]], output_path: str):
    """
    Save benchmark results to CSV.

    Args:
        results: List of result dictionaries
        output_path: Path to output CSV file
    """
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Depth',
            'Runs',
            'Avg Time (s)',
            'Min Time (s)',
            'Max Time (s)',
            'Std Dev (s)',
            'Max Size',
            'Avg Num Sets'
        ])

        # Data rows
        for result in results:
            if 'error' not in result:
                writer.writerow([
                    result['depth'],
                    result['runs'],
                    f"{result['avg_time']:.4f}",
                    f"{result['min_time']:.4f}",
                    f"{result['max_time']:.4f}",
                    f"{result['std_dev']:.4f}",
                    result['max_size'],
                    f"{result['avg_num_sets']:.1f}"
                ])


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Benchmark composition depth performance'
    )
    parser.add_argument(
        '--depths',
        type=str,
        default='1,2,3,4,5',
        help='Comma-separated list of depths to test (default: 1,2,3,4,5)'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Number of runs per depth (default: 3)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='depth_results.csv',
        help='Output CSV file path (default: depth_results.csv)'
    )

    args = parser.parse_args()

    # Parse depths
    depths = [int(d.strip()) for d in args.depths.split(',')]

    # Run benchmark
    run_benchmark_suite(depths, runs=args.runs, output=args.output)


if __name__ == '__main__':
    main()
