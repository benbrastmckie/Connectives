# Nice Connectives Solver

A solver for finding the maximum size of "nice" (complete and independent) sets of logical connectives in classical two-valued logic.

**Status**: Fully Implemented | **Date**: 2025-10-02 | **Tests**: 159 passing

---

## Quick Links

- **[CLI Documentation](src/README.md)** - Complete command-line interface guide
- **[Command Implementations](src/commands/README.md)** - CLI command details
- **[Examples](examples/README.md)** - Real execution examples and output
- **[Results](RESULTS.md)** - Research findings (size-17 sets found)
- **[Scripts](scripts/README.md)** - Proof methodology documentation
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

---

## Problem Statement

Given classical two-valued connectives of arbitrary arity, we define a set of connectives as **nice** if it is:

1. **Complete**: Every classical connective is definable from the set (via Post's Completeness Theorem)
2. **Independent**: No connective in the set is definable from the other connectives

### Research Question

**What is the largest size of a nice set?**

---

## Answer

### **Nice Sets of Size 17 Have Been Found**

Using Z3-based constraint solving with pattern enumeration (composition depth 3-5):

**Nice sets of size 17 have been discovered and verified.**

Current findings:
- **Binary-only**: Maximum size is 3 (classical result, proven)
- **Unary + Binary**: Maximum size is at least 7
- **Unary + Binary + Ternary**: Nice sets of size 17 exist (verified at depth 5)
- **Upper bound**: Unknown - maximum may be larger than 17

**The maximum size of nice sets with arbitrary arities remains an open question.**

**See [RESULTS.md](RESULTS.md) for complete research findings and verification details.**

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd nice_connectives

# On most systems, install with pip
pip install -e .

# On NixOS, use directly without installation
# (pip install doesn't work with read-only /nix/store)
```

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

**See [src/README.md](src/README.md) for complete CLI documentation.**

---

## Results Summary

| Arity Range | Known Nice Sets | Example |
|-------------|-----------------|---------|
| Binary only | Max size = 3 (proven) | {NOR, AND, IFF} |
| Unary + Binary | Size ≥ 7 | {CONST_0, ID, CONST_1, INHIBIT, NOT_Y, IMPLIES, PROJ_X} |
| **Unary + Binary + Ternary** | **Size ≥ 17** | 1 constant + 1 binary + 15 ternary |

### Key Findings

1. **Size-17 nice sets exist** - found via Z3 constraint solving
2. **Ternary functions essential** - binary-only max is 3, with ternary reaches ≥17
3. **Pattern enumeration effective** - depth 3-5 composition checking verifies independence
4. **Validated implementation** - reproduces classical binary-only max=3 result
5. **Maximum unknown** - upper bound remains an open research question

**See [RESULTS.md](RESULTS.md) for detailed findings and verification.**

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
- Add unary (4 functions) → size ≥ 7
- Add ternary (256 functions) → size ≥ 17 (found via Z3)

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
├── scripts/                # Proof methodology documentation
│   ├── proofs_z3/          # Z3-based proof approach
│   ├── proofs_enumeration/ # Enumeration-based proof approach
│   └── README.md           # Scripts documentation
├── specs/                  # Research reports and plans
│   ├── reports/            # Research findings
│   ├── plans/              # Implementation plans
│   ├── summaries/          # Execution summaries
│   └── README.md           # Specs organization
├── pyproject.toml          # Package configuration
├── README.md               # This file
├── USAGE.md                # Usage guide
└── RESULTS.md              # Research conclusion
```

**All functionality is accessible through the unified CLI:**
- `python -m src.cli <subcommand>` (or `nice-connectives` if installed)
- See [src/README.md](src/README.md) for complete CLI documentation
- See [src/commands/README.md](src/commands/README.md) for command implementation details

---

## References

**Post, E. L. (1941).** "The Two-Valued Iterative Systems of Mathematical Logic." *Annals of Mathematics Studies*, No. 5
- Proves completeness theorem for 5 maximal clones (T0, T1, M, D, A)
- Foundation for efficient completeness checking

---

**Project Status**: Implementation complete | 159 tests passing | Nice sets of size ≥17 found | Maximum unknown
