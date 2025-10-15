#!/usr/bin/env python3
"""
Unified command-line interface for nice-connectives.

This provides a single entry point for all nice connectives tools:
- prove: Formal proofs of maximum nice set size
- validate: Validation and verification tools
- benchmark: Performance measurement tools
- search: Interactive search tools
"""

import sys
import argparse
from src.commands import prove, validate, benchmark, search
from src.independence import DefinabilityMode


def main():
    """Main CLI entry point with subcommand routing."""
    parser = argparse.ArgumentParser(
        prog='nice-connectives',
        description='Tools for finding and analyzing nice (complete and independent) connective sets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run Z3-based proof
  nice-connectives prove z3

  # Run enumeration-based proof
  nice-connectives prove enum

  # Validate binary search
  nice-connectives validate binary

  # Run quick benchmark
  nice-connectives benchmark quick

  # Search binary connectives
  nice-connectives search binary

For more information on each subcommand:
  nice-connectives <subcommand> --help
        """
    )

    # Create subparsers for main command groups
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='Available command groups',
        dest='command',
        required=True
    )

    # ===== PROVE subcommand =====
    prove_parser = subparsers.add_parser(
        'prove',
        help='Formal proofs of maximum nice set size',
        description='Run formal proofs using different methodologies'
    )
    prove_subparsers = prove_parser.add_subparsers(
        title='proof methods',
        description='Available proof methodologies',
        dest='method',
        required=True
    )

    # prove z3
    prove_z3_parser = prove_subparsers.add_parser(
        'z3',
        help='Z3-based constraint solving proof'
    )
    prove_z3_parser.add_argument(
        '--checkpoint',
        type=str,
        help='Path to checkpoint file for saving/loading progress'
    )
    prove_z3_parser.add_argument(
        '--interval',
        type=int,
        default=100,
        help='Save checkpoint every N candidates (default: 100)'
    )
    prove_z3_parser.add_argument(
        '--target-size',
        type=int,
        default=17,
        help='Target nice set size to search for (default: 17)'
    )
    prove_z3_parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum composition depth for independence checking (default: 3)'
    )
    prove_z3_parser.add_argument(
        '--max-arity',
        type=int,
        default=3,
        help='Maximum arity to include in connective pool (default: 3)'
    )
    prove_z3_parser.add_argument(
        '--max-candidates',
        type=int,
        default=10000,
        help='Maximum number of complete sets to check before stopping (default: 10000)'
    )
    prove_z3_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # prove enum
    prove_enum_parser = prove_subparsers.add_parser(
        'enum',
        help='Pattern enumeration proof'
    )
    prove_enum_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # ===== VALIDATE subcommand =====
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validation and verification tools',
        description='Validate search results with different configurations'
    )
    validate_subparsers = validate_parser.add_subparsers(
        title='validation types',
        description='Available validation tools',
        dest='type',
        required=True
    )

    # validate binary
    validate_binary_parser = validate_subparsers.add_parser(
        'binary',
        help='Validate binary-only search'
    )
    validate_binary_parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
    )
    validate_binary_parser.add_argument(
        '--use-z3',
        action='store_true',
        help='Use Z3 SAT backend instead of pattern enumeration'
    )
    validate_binary_parser.add_argument(
        '--no-symmetry-breaking',
        action='store_true',
        help='Disable symmetry breaking (slower)'
    )
    validate_binary_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # validate ternary
    validate_ternary_parser = validate_subparsers.add_parser(
        'ternary',
        help='Validate ternary search'
    )
    validate_ternary_parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
    )
    validate_ternary_parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare multiple depths (3, 5, 7)'
    )
    validate_ternary_parser.add_argument(
        '--use-z3',
        action='store_true',
        help='Use Z3 SAT backend instead of pattern enumeration'
    )
    validate_ternary_parser.add_argument(
        '--no-symmetry-breaking',
        action='store_true',
        help='Disable symmetry breaking (slower)'
    )
    validate_ternary_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed progress information'
    )
    validate_ternary_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # ===== BENCHMARK subcommand =====
    benchmark_parser = subparsers.add_parser(
        'benchmark',
        help='Performance measurement tools',
        description='Benchmark search performance with different configurations'
    )
    benchmark_subparsers = benchmark_parser.add_subparsers(
        title='benchmark types',
        description='Available benchmark tools',
        dest='type',
        required=True
    )

    # benchmark full
    benchmark_full_parser = benchmark_subparsers.add_parser(
        'full',
        help='Comprehensive benchmark suite'
    )
    benchmark_full_parser.add_argument(
        '--runs',
        type=int,
        default=5,
        help='Number of runs per benchmark (default: 5)'
    )
    benchmark_full_parser.add_argument(
        '--output',
        type=str,
        default='benchmarks.csv',
        help='Output CSV file path (default: benchmarks.csv)'
    )
    benchmark_full_parser.add_argument(
        '--json',
        type=str,
        help='Optional JSON output file path'
    )

    # benchmark quick
    benchmark_quick_parser = benchmark_subparsers.add_parser(
        'quick',
        help='Quick performance check'
    )

    # benchmark depth
    benchmark_depth_parser = benchmark_subparsers.add_parser(
        'depth',
        help='Depth crossover analysis'
    )
    benchmark_depth_parser.add_argument(
        '--depths',
        type=str,
        default='1,2,3,4,5',
        help='Comma-separated list of depths to test (default: 1,2,3,4,5)'
    )
    benchmark_depth_parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Number of runs per depth (default: 3)'
    )
    benchmark_depth_parser.add_argument(
        '--output',
        type=str,
        default='depth_results.csv',
        help='Output CSV file path (default: depth_results.csv)'
    )

    # ===== SEARCH subcommand =====
    search_parser = subparsers.add_parser(
        'search',
        help='Interactive search tools',
        description='Search for nice connective sets'
    )
    search_subparsers = search_parser.add_subparsers(
        title='search types',
        description='Available search tools',
        dest='type',
        required=True
    )

    # search binary
    search_binary_parser = search_subparsers.add_parser(
        'binary',
        help='Binary-only nice set search'
    )
    search_binary_parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
    )
    search_binary_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )
    search_binary_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # search full
    search_full_parser = search_subparsers.add_parser(
        'full',
        help='Full arity search'
    )
    search_full_parser.add_argument(
        '--max-arity',
        type=int,
        default=3,
        help='Maximum arity to consider (default: 3)'
    )
    search_full_parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
    )
    search_full_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )
    search_full_parser.add_argument(
        '--definability-mode',
        type=str,
        choices=['syntactic', 'truth-functional'],
        default='truth-functional',
        help='Definability notion: truth-functional (clone-theoretic, default) or syntactic (composition-based)'
    )

    # search validate
    search_validate_parser = search_subparsers.add_parser(
        'validate',
        help='Validate maximum size=16'
    )

    # Parse arguments
    args = parser.parse_args()

    # Route to appropriate command handler
    try:
        if args.command == 'prove':
            if args.method == 'z3':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return prove.prove_z3(
                    checkpoint=args.checkpoint,
                    interval=args.interval,
                    target_size=args.target_size,
                    max_depth=args.max_depth,
                    max_arity=args.max_arity,
                    max_candidates=args.max_candidates,
                    definability_mode=mode
                )
            elif args.method == 'enum':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return prove.prove_enumeration(definability_mode=mode)

        elif args.command == 'validate':
            if args.type == 'binary':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return validate.validate_binary(
                    depth=args.depth,
                    use_z3=args.use_z3,
                    use_symmetry_breaking=not args.no_symmetry_breaking,
                    definability_mode=mode
                )
            elif args.type == 'ternary':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return validate.validate_ternary(
                    depth=args.depth,
                    compare=args.compare,
                    use_z3=args.use_z3,
                    use_symmetry_breaking=not args.no_symmetry_breaking,
                    verbose=args.verbose,
                    definability_mode=mode
                )

        elif args.command == 'benchmark':
            if args.type == 'full':
                return benchmark.benchmark_full(
                    runs=args.runs,
                    output=args.output,
                    json_output=args.json
                )
            elif args.type == 'quick':
                return benchmark.benchmark_quick()
            elif args.type == 'depth':
                return benchmark.benchmark_depth(
                    depths=args.depths,
                    runs=args.runs,
                    output=args.output
                )

        elif args.command == 'search':
            if args.type == 'binary':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return search.search_binary(
                    max_depth=args.max_depth,
                    verbose=not args.quiet,
                    definability_mode=mode
                )
            elif args.type == 'full':
                mode = DefinabilityMode[args.definability_mode.replace('-', '_').upper()]
                return search.search_full(
                    max_arity=args.max_arity,
                    max_depth=args.max_depth,
                    verbose=not args.quiet,
                    definability_mode=mode
                )
            elif args.type == 'validate':
                return search.search_validate()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
