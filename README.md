# Nice Connectives Solver

A solver for finding the maximum size of "nice" (complete and independent) sets of logical connectives in classical two-valued logic.

**Status**: Fully Implemented | **Tests**: 159 passing

---

## Quick Links

- **[Installation](docs/INSTALLATION.md)** - Platform-specific installation guide
- **[Usage Guide](docs/USAGE.md)** - Complete command reference and workflows
- **[Results](docs/RESULTS.md)** - **Research findings (size-30 sets found)**
- **[Examples](examples/README.md)** - Real execution examples and output
- **[Implementation](src/README.md)** - CLI and code documentation
- **[Testing](tests/README.md)** - Test suite documentation
- **[Specs](specs/README.md)** - Research reports and implementation plans

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Answer](#answer)
- [Quick Start](#quick-start)
- [Results Summary](#results-summary)
- [Technical Approach](#technical-approach)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [References](#references)

---

## Problem Statement

Given classical two-valued connectives of arbitrary arity, we define a set of connectives as **nice** if it is:

1. **Complete**: Every classical connective is definable from the set (via Post's Completeness Theorem)
2. **Independent**: No connective in the set is definable from the other connectives

### Research Question

**What is the largest size of a nice set?**

---

## Answer

### **Nice Sets of Size 30 Have Been Found**

Using Z3-based constraint solving with pattern enumeration (composition depth 3):

**Nice sets of size 30 have been discovered and verified.**

Current findings:
- **Binary-only**: Maximum size is 3 (classical result, proven and reproduced)
- **Unary + Binary**: Maximum size is 5 (proven via Z3 exhaustive search)
- **Unary + Binary + Ternary**: Nice sets of size 30 verified
- **Upper bound**: Unknown - maximum may be larger than 30

**The maximum size of nice sets with arbitrary arities remains an open question.**

**See [docs/RESULTS.md](docs/RESULTS.md) for complete research findings and verification details.**

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd nice_connectives

# Install dependencies
pip install -e .

# On NixOS, use directly without installation
# (pip install doesn't work with read-only /nix/store)
# nix-shell -p python3 python3Packages.pytest python3Packages.z3
# python3 -m src.cli --help
```

**See [docs/INSTALLATION.md](docs/INSTALLATION.md) for detailed installation instructions, including platform-specific guidance for Linux, macOS, Windows, and NixOS.**

### Basic Usage

```bash
# Validate a known size-16 nice set
python -m src.cli search validate

# Search for nice sets with binary connectives only (finds max = 3)
python -m src.cli search binary

# Search with full arity support (finds size ≥ 16)
python -m src.cli search full --max-arity 3

# Run Z3-based proof
python -m src.cli prove z3

# Run enumeration-based proof
python -m src.cli prove enum

# Validate search results
python -m src.cli validate binary
python -m src.cli validate ternary

# Run benchmarks
python -m src.cli benchmark quick
python -m src.cli benchmark full

# Run test suite
pytest tests/ -v

# Get help on any command
python -m src.cli --help
python -m src.cli search --help
python -m src.cli prove z3 --help
```

**See [docs/USAGE.md](docs/USAGE.md) for complete usage guide and [src/README.md](src/README.md) for CLI and implementation documentation.**

---

## Results Summary

| Arity Range | Known Nice Sets | Example |
|-------------|-----------------|---------|
| Binary only | Max size = 3 (proven) | {XOR, AND, TRUE} |
| Unary + Binary | Max size = 5 (proven) | {FALSE, TRUE, XOR, AND, IMP} |
| **Unary + Binary + Ternary** | **Size ≥ 30** | 1 constant + 2 binary + 27 ternary |

### Key Findings

1. **Size-30 nice sets exist** - found via Z3 constraint solving
2. **Ternary functions essential** - binary-only max is 3, with ternary reaches ≥30
3. **Pattern enumeration effective** - depth 3 composition checking verifies independence
4. **Validated implementation** - reproduces classical binary-only max=3 result
5. **Maximum unknown** - size 31+ remains unknown (search times out)

**See [docs/RESULTS.md](docs/RESULTS.md) for detailed findings and verification.**

---

## Technical Approach

### Core Techniques

**1. BitVec Encoding**
- Truth tables encoded as integers for compact storage and fast equality checks
- Example: AND (arity 2) = 0b1000 = 8

**2. Post's Completeness Theorem**
- Complete ↔ Escape all 5 maximal clones (T0, T1, M, D, A)
- O(n) completeness check vs exponential definability check

**3. Bounded Composition via Pattern Enumeration**
- Check definability up to depth d using explicit pattern matching
- Depth 3 balances thoroughness with performance

**4. Incremental Arity Search**
- Start with binary (16 functions) → max = 3 (proven)
- Add constants + unary (2 + 4 functions) → max = 5 (proven)
- Add ternary (256 functions) → size ≥ 30 (found via Z3)

**See [src/README.md](src/README.md) for complete implementation details.**

---

## Project Structure

```
nice_connectives/
├── src/                    # Source code
│   ├── cli.py              # Unified CLI entry point
│   ├── commands/           # CLI command implementations
│   │   ├── prove.py        # Proof commands (z3, enum)
│   │   ├── validate.py     # Validation commands (binary, ternary)
│   │   ├── benchmark.py    # Benchmark commands (full, quick, depth)
│   │   └── search.py       # Search commands (binary, full, validate)
│   ├── proofs/             # Formal proof scripts
│   │   ├── z3_proof.py     # Z3 constraint solver-based proof
│   │   ├── enumeration_proof.py  # Pattern enumeration-based proof
│   │   └── README.md       # Proof methodology documentation
│   ├── connectives.py      # BitVec truth table representation
│   ├── constants.py        # Predefined connectives
│   ├── post_classes.py     # Completeness checking
│   ├── independence.py     # Independence checking
│   ├── search.py           # Search algorithms
│   ├── main.py             # Library interface
│   └── README.md           # Implementation documentation
├── tests/                  # Test suite (159 passing)
│   └── README.md           # Testing documentation
├── examples/               # Real execution examples
│   └── README.md           # Examples documentation
├── docs/                   # Documentation
│   ├── INSTALLATION.md     # Complete installation guide
│   ├── USAGE.md            # Usage guide and command reference
│   └── RESULTS.md          # Research findings and conclusion
├── specs/                  # Research reports and plans
│   ├── reports/            # Research findings
│   ├── plans/              # Implementation plans
│   ├── summaries/          # Execution summaries
│   └── README.md           # Specs organization
├── pyproject.toml          # Package configuration
└── README.md               # This file
```

**All functionality is accessible through the unified CLI:**
- `python -m src.cli <subcommand>` (or `nice-connectives` if installed)
- See [src/README.md](src/README.md) for complete CLI documentation
- See [src/commands/README.md](src/commands/README.md) for command implementation details
- See [src/proofs/README.md](src/proofs/README.md) for proof script details

---

## References

**Post, E. L. (1941).** "The Two-Valued Iterative Systems of Mathematical Logic." *Annals of Mathematics Studies*, No. 5
- Proves completeness theorem for 5 maximal clones (T0, T1, M, D, A)
- Foundation for efficient completeness checking

---

## Documentation

### Getting Started
- **[Installation Guide](docs/INSTALLATION.md)** - Complete setup instructions for all platforms
  - Terminal basics for beginners
  - Python 3, pytest, and z3-solver installation
  - Platform-specific instructions (Linux, macOS, Windows, NixOS)
  - Troubleshooting common issues
  - Verification steps

- **[Usage Guide](docs/USAGE.md)** - Comprehensive command reference
  - All CLI commands with examples
  - Expected outputs and results
  - Common workflows
  - Performance tips
  - Advanced usage patterns

### Understanding the Research
- **[Research Results](docs/RESULTS.md)** - Key findings and conclusions
  - Binary-only: max = 3 (classical result)
  - Unary + Binary: max = 5 (proven)
  - With Ternary: size ≥ 30 (current verified maximum)
  - Systematic search results and analysis

- **[Examples](examples/README.md)** - Detailed example outputs
  - [Binary-only enumeration](examples/enum_binary_only_max3.md) - Exhaustive search finding all 76 nice sets
  - [Unary+Binary enumeration](examples/enum_unary_binary_max5.md) - Finding all 5 size-5 nice sets
  - [Classical binary analysis](examples/enum_classical_binary_max3.md) - Detailed walkthrough
  - [Z3 discoveries](examples/z3_nice_set_30.md) - Size-30 maximum (current record)
  - Enumeration vs Z3 comparison

### Implementation Details
- **[Source Code Documentation](src/README.md)** - Complete implementation guide
  - Module organization and architecture
  - CLI interface and commands
  - Core algorithms (BitVec encoding, Post classes, independence checking)
  - Performance characteristics
  - API reference

- **[Command Implementations](src/commands/README.md)** - CLI command modules
  - prove.py - Z3 and enumeration proofs
  - search.py - Enumeration search algorithms
  - validate.py - Result validation
  - benchmark.py - Performance testing

- **[Proof Scripts](src/proofs/README.md)** - Formal proof methodology
  - Z3 constraint solving approach
  - Enumeration proof strategy
  - Important code blocks with explanations

### Testing
- **[Test Suite](tests/README.md)** - 159 passing tests
  - Unit tests for core functionality
  - Integration tests for search algorithms
  - Proof validation tests
  - Coverage information

### Research Documentation
- **[Specs](specs/README.md)** - Research process documentation
  - [Reports](specs/reports/) - Research findings and analysis
  - [Plans](specs/plans/) - Implementation plans
  - [Summaries](specs/summaries/) - Execution summaries

---

**Project Status**: Implementation complete | 159 tests passing | Size-30 nice sets verified | Maximum unknown
