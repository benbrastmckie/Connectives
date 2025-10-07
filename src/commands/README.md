# CLI Command Implementations

This directory contains the implementation modules for the unified CLI command interface.

## Overview

Each module in this directory implements one or more CLI subcommands, providing a clean separation between command-line interface logic and core library functionality.

## Command Modules

### prove.py

Implements proof generation commands using different methodologies:

```python
def prove_z3(checkpoint=None, interval=100, target_size=17, max_depth=3):
    """Run Z3-based constraint solving proof for maximum nice set size."""

def prove_enumeration():
    """Run enumeration-based proof for maximum nice set size."""
```

**Usage:**
```bash
python -m src.cli prove z3 --target-size 17 --max-depth 3
python -m src.cli prove enum
```

**Implementation approach:**
- Dynamically imports from `scripts/proofs_z3/` and `scripts/proofs_enumeration/`
- Adds script directory to sys.path temporarily
- Executes main() function from original scripts
- Cleans up sys.path after execution

### validate.py

Implements validation commands for verifying search results:

```python
def validate_binary(depth=3, use_z3=False, use_symmetry_breaking=True):
    """Validate binary-only search results."""

def validate_ternary(depth=3, compare=False, use_z3=False,
                     use_symmetry_breaking=True, verbose=False):
    """Validate ternary search results with optional comparison."""
```

**Usage:**
```bash
python -m src.cli validate binary --depth 3 --use-z3
python -m src.cli validate ternary --compare --verbose
```

**Implementation approach:**
- Similar dynamic import pattern from `scripts/validation/`
- Supports multiple validation backends (pattern enumeration vs Z3)
- Configurable depth and symmetry breaking options

### benchmark.py

Implements performance measurement commands:

```python
def benchmark_full(runs=5, output='benchmarks.csv', json_output=None):
    """Run comprehensive benchmark suite."""

def benchmark_quick():
    """Run quick performance check."""

def benchmark_depth(depths='1,2,3,4,5', runs=3, output='depth_results.csv'):
    """Benchmark composition depth performance."""
```

**Usage:**
```bash
python -m src.cli benchmark full --runs 5 --output results.csv
python -m src.cli benchmark quick
python -m src.cli benchmark depth --depths 1,2,3,4,5
```

**Implementation approach:**
- Imports from `scripts/benchmarks/`
- Supports CSV and JSON output formats
- Configurable number of runs for statistical significance

### search.py

Implements interactive search commands:

```python
def search_binary(max_depth=3, verbose=True):
    """Search for nice sets using only binary connectives."""

def search_full(max_arity=3, max_depth=3, verbose=True):
    """Search for nice sets using multiple arities (incremental search)."""

def search_validate():
    """Validate that the maximum nice set size of 16 is achievable."""
```

**Usage:**
```bash
python -m src.cli search binary --max-depth 3
python -m src.cli search full --max-arity 3
python -m src.cli search validate
```

**Implementation approach:**
- Uses library functions from `src/search.py` directly
- No dynamic imports needed (clean library API)
- Provides formatted output and analysis

## Command Module Pattern

### Standard Structure

Each command module follows this pattern:

```python
"""
Module docstring explaining the command group.
"""

import sys
from pathlib import Path

def command_name(param1=default1, param2=default2):
    """
    Docstring explaining what this command does.

    Args:
        param1: Description
        param2: Description

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Implementation here
    return 0
```

### Dynamic Import Pattern

For commands that wrap scripts from `scripts/` directories:

```python
def command_using_script():
    """Execute functionality from script."""
    # Add script directory to path
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "category"
    sys.path.insert(0, str(script_dir))

    try:
        import script_module
        return script_module.main()

    except ImportError as e:
        print(f"Error importing module: {e}", file=sys.stderr)
        return 1

    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))
```

### Direct Library Usage Pattern

For commands using core library functions:

```python
def command_using_library(max_depth=3, verbose=True):
    """Use library functions directly."""
    from src.search import search_binary_only
    from src.connectives import analyze_nice_set

    max_size, sets = search_binary_only(
        max_depth=max_depth,
        verbose=verbose
    )

    if verbose and sets:
        analysis = analyze_nice_set(sets[0])
        print(f"Size: {analysis['size']}")

    return 0
```

## Adding New Subcommands

To add a new subcommand to the CLI:

### 1. Create Command Function

Add a new function to an existing module or create a new module:

```python
# In src/commands/analyze.py (new module)
def analyze_set(connective_list, depth=3):
    """Analyze a specific connective set."""
    from src.search import analyze_nice_set
    from src.post_classes import is_complete
    from src.independence import is_independent

    # Parse connective list
    # Run analysis
    # Print results

    return 0
```

### 2. Register in CLI

Update `src/cli.py` to add the subcommand:

```python
# Import the new command module
from src.commands import prove, validate, benchmark, search, analyze

# Add subparser for new command
analyze_parser = subparsers.add_parser(
    'analyze',
    help='Analyze specific connective sets'
)
analyze_parser.add_argument(
    'connectives',
    help='Comma-separated list of connectives'
)
analyze_parser.add_argument(
    '--depth',
    type=int,
    default=3,
    help='Composition depth for independence check'
)

# Add routing logic
elif args.command == 'analyze':
    return analyze.analyze_set(
        connective_list=args.connectives,
        depth=args.depth
    )
```

### 3. Test the New Command

```bash
python -m src.cli analyze --help
python -m src.cli analyze "XOR,AND,OR" --depth 3
```

## Design Principles

### Separation of Concerns
- **CLI layer** (`cli.py`): Argument parsing and routing
- **Command layer** (`commands/*.py`): Command-specific logic and formatting
- **Library layer** (`src/*.py`): Core algorithms and data structures

### Return Conventions
- Return `0` on success
- Return `1` on failure
- Use `sys.stderr` for error messages
- Use `sys.stdout` for normal output

### Error Handling
```python
def command_with_error_handling():
    """Example error handling pattern."""
    try:
        # Command logic
        result = do_something()

        if not result:
            print("Error: Operation failed", file=sys.stderr)
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
```

### Output Formatting
- Use clear section headers: `print("=" * 70)`
- Group related information together
- Provide progress updates for long operations
- Include timing information when relevant
- Use checkmarks (✓) and crosses (✗) for status indicators

## Testing Commands

Test each command individually:

```bash
# Test help text
python -m src.cli <command> --help

# Test basic execution
python -m src.cli <command> <subcommand>

# Test with various options
python -m src.cli <command> <subcommand> --option value

# Test error handling
python -m src.cli <command> <invalid-subcommand>
```

## Navigation

- [← src/README.md](../README.md) - Main source documentation
- [prove.py](prove.py) - Proof command implementations
- [validate.py](validate.py) - Validation command implementations
- [benchmark.py](benchmark.py) - Benchmark command implementations
- [search.py](search.py) - Search command implementations
- [../../README.md](../../README.md) - Project root
