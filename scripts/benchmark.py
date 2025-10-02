#!/usr/bin/env python3
"""
Performance benchmarking suite for nice connectives search.

Benchmarks different search strategies (enumeration vs Z3), symmetry breaking
impact, and performance across different arities.
"""

import sys
import time
import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connectives import generate_all_connectives
from src.search import (
    search_binary_only,
    find_maximum_nice_set,
    filter_by_equivalence
)


def benchmark_binary_search(
    use_z3: bool = False,
    use_symmetry_breaking: bool = False,
    runs: int = 5
) -> Dict[str, Any]:
    """
    Benchmark binary-only search.

    Args:
        use_z3: Use Z3 SAT backend
        use_symmetry_breaking: Apply equivalence class filtering
        runs: Number of runs to average

    Returns:
        Dictionary with benchmark results
    """
    times = []
    max_sizes = []

    for _ in range(runs):
        start = time.time()
        max_size, nice_sets = search_binary_only(
            max_depth=3,
            verbose=False,
            use_z3=use_z3,
            use_symmetry_breaking=use_symmetry_breaking
        )
        elapsed = time.time() - start

        times.append(elapsed)
        max_sizes.append(max_size)

    return {
        'search_type': 'binary_only',
        'use_z3': use_z3,
        'use_symmetry_breaking': use_symmetry_breaking,
        'runs': runs,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'std_dev': (sum((t - sum(times)/len(times))**2 for t in times) / len(times))**0.5,
        'max_size': max_sizes[0],  # Should be consistent
        'all_times': times
    }


def benchmark_full_search(
    max_arity: int = 3,
    use_z3: bool = False,
    use_symmetry_breaking: bool = True,
    runs: int = 3
) -> Dict[str, Any]:
    """
    Benchmark full search with multiple arities.

    Args:
        max_arity: Maximum arity to include
        use_z3: Use Z3 SAT backend
        use_symmetry_breaking: Apply equivalence class filtering
        runs: Number of runs to average

    Returns:
        Dictionary with benchmark results
    """
    times = []
    max_sizes = []

    # Generate connective pool
    connectives = []
    for arity in range(0, max_arity + 1):
        connectives.extend(generate_all_connectives(arity))

    # Apply symmetry breaking if requested
    if use_symmetry_breaking:
        connectives = filter_by_equivalence(connectives)

    for _ in range(runs):
        start = time.time()
        max_size, nice_sets, metadata = find_maximum_nice_set(
            connectives,
            max_size=20,
            max_depth=3,
            verbose=False,
            use_z3=use_z3
        )
        elapsed = time.time() - start

        times.append(elapsed)
        max_sizes.append(max_size)

    return {
        'search_type': f'arity_0_to_{max_arity}',
        'use_z3': use_z3,
        'use_symmetry_breaking': use_symmetry_breaking,
        'runs': runs,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'std_dev': (sum((t - sum(times)/len(times))**2 for t in times) / len(times))**0.5,
        'max_size': max_sizes[0],
        'connectives_count': len(connectives),
        'all_times': times
    }


def benchmark_symmetry_breaking_impact(
    max_arity: int = 3,
    runs: int = 3
) -> Dict[str, Any]:
    """
    Benchmark the impact of symmetry breaking.

    Args:
        max_arity: Maximum arity to test
        runs: Number of runs to average

    Returns:
        Dictionary comparing with/without symmetry breaking
    """
    print(f"Benchmarking symmetry breaking impact (arity 0-{max_arity})...")

    # Without symmetry breaking
    print("  Running without symmetry breaking...")
    without_sb = benchmark_full_search(
        max_arity=max_arity,
        use_z3=False,
        use_symmetry_breaking=False,
        runs=runs
    )

    # With symmetry breaking
    print("  Running with symmetry breaking...")
    with_sb = benchmark_full_search(
        max_arity=max_arity,
        use_z3=False,
        use_symmetry_breaking=True,
        runs=runs
    )

    speedup = without_sb['avg_time'] / with_sb['avg_time']

    return {
        'search_type': f'symmetry_breaking_impact_arity_{max_arity}',
        'without_sb': without_sb,
        'with_sb': with_sb,
        'speedup': speedup,
        'space_reduction': without_sb['connectives_count'] / with_sb['connectives_count']
    }


def run_comprehensive_benchmark(runs: int = 5) -> List[Dict[str, Any]]:
    """
    Run comprehensive benchmark suite.

    Args:
        runs: Number of runs per benchmark

    Returns:
        List of benchmark results
    """
    results = []

    print("=" * 80)
    print("COMPREHENSIVE PERFORMANCE BENCHMARK")
    print("=" * 80)
    print(f"Runs per benchmark: {runs}")
    print()

    # 1. Binary-only benchmarks
    print("1. Binary-only search (enumeration, no symmetry breaking)...")
    results.append(benchmark_binary_search(
        use_z3=False,
        use_symmetry_breaking=False,
        runs=runs
    ))

    print("2. Binary-only search (enumeration, with symmetry breaking)...")
    results.append(benchmark_binary_search(
        use_z3=False,
        use_symmetry_breaking=True,
        runs=runs
    ))

    # 3. Full search benchmarks (arity 0-3)
    print("3. Full search arity 0-3 (enumeration, no symmetry breaking)...")
    results.append(benchmark_full_search(
        max_arity=3,
        use_z3=False,
        use_symmetry_breaking=False,
        runs=max(1, runs // 3)  # Fewer runs for slower benchmarks
    ))

    print("4. Full search arity 0-3 (enumeration, with symmetry breaking)...")
    results.append(benchmark_full_search(
        max_arity=3,
        use_z3=False,
        use_symmetry_breaking=True,
        runs=runs
    ))

    # 4. Symmetry breaking impact analysis
    print("5. Analyzing symmetry breaking impact...")
    results.append(benchmark_symmetry_breaking_impact(
        max_arity=2,  # Binary only
        runs=runs
    ))

    results.append(benchmark_symmetry_breaking_impact(
        max_arity=3,  # Include ternary
        runs=max(1, runs // 3)
    ))

    return results


def print_results_summary(results: List[Dict[str, Any]]):
    """
    Print a formatted summary of benchmark results.

    Args:
        results: List of benchmark result dictionaries
    """
    print()
    print("=" * 80)
    print("BENCHMARK RESULTS SUMMARY")
    print("=" * 80)
    print()

    for i, result in enumerate(results, 1):
        search_type = result.get('search_type', 'unknown')
        print(f"{i}. {search_type}")
        print("-" * 80)

        if 'symmetry_breaking_impact' in search_type:
            # Special formatting for symmetry breaking comparison
            print(f"  Without symmetry breaking: {result['without_sb']['avg_time']:.4f}s")
            print(f"  With symmetry breaking:    {result['with_sb']['avg_time']:.4f}s")
            print(f"  Speedup:                   {result['speedup']:.2f}×")
            print(f"  Space reduction:           {result['space_reduction']:.2f}×")
        else:
            # Standard benchmark result
            use_z3 = result.get('use_z3', False)
            use_sb = result.get('use_symmetry_breaking', False)
            print(f"  Strategy: {'z3_sat' if use_z3 else 'enumeration'}")
            print(f"  Symmetry breaking: {'yes' if use_sb else 'no'}")
            print(f"  Average time: {result['avg_time']:.4f}s")
            print(f"  Min time: {result['min_time']:.4f}s")
            print(f"  Max time: {result['max_time']:.4f}s")
            print(f"  Std dev: {result['std_dev']:.4f}s")
            if 'max_size' in result:
                print(f"  Max nice set size: {result['max_size']}")
            if 'connectives_count' in result:
                print(f"  Connectives searched: {result['connectives_count']}")

        print()


def save_results_csv(results: List[Dict[str, Any]], output_path: str):
    """
    Save benchmark results to CSV file.

    Args:
        results: List of benchmark result dictionaries
        output_path: Path to output CSV file
    """
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Search Type',
            'Strategy',
            'Symmetry Breaking',
            'Runs',
            'Avg Time (s)',
            'Min Time (s)',
            'Max Time (s)',
            'Std Dev (s)',
            'Max Size',
            'Connectives Count'
        ])

        # Data rows
        for result in results:
            if 'symmetry_breaking_impact' not in result.get('search_type', ''):
                writer.writerow([
                    result.get('search_type', ''),
                    'z3_sat' if result.get('use_z3', False) else 'enumeration',
                    'yes' if result.get('use_symmetry_breaking', False) else 'no',
                    result.get('runs', ''),
                    f"{result.get('avg_time', 0):.4f}",
                    f"{result.get('min_time', 0):.4f}",
                    f"{result.get('max_time', 0):.4f}",
                    f"{result.get('std_dev', 0):.4f}",
                    result.get('max_size', ''),
                    result.get('connectives_count', '')
                ])

    print(f"Results saved to: {output_path}")


def save_results_json(results: List[Dict[str, Any]], output_path: str):
    """
    Save benchmark results to JSON file.

    Args:
        results: List of benchmark result dictionaries
        output_path: Path to output JSON file
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Detailed results saved to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Benchmark nice connectives search performance'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=5,
        help='Number of runs per benchmark (default: 5)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='benchmarks.csv',
        help='Output CSV file path (default: benchmarks.csv)'
    )
    parser.add_argument(
        '--json',
        type=str,
        help='Optional JSON output file path'
    )

    args = parser.parse_args()

    # Run benchmarks
    results = run_comprehensive_benchmark(runs=args.runs)

    # Print summary
    print_results_summary(results)

    # Save results
    save_results_csv(results, args.output)

    if args.json:
        save_results_json(results, args.json)

    print()
    print("=" * 80)
    print("BENCHMARK COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
