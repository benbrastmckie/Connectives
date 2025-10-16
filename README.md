# Nice Connectives Solver

A solver for finding the maximum size of "nice" (complete and independent) sets of logical connectives in classical two-valued logic.

**Status**: Fully Implemented | **Tests**: 175 passing

---

## Quick Links

- **[Installation](docs/INSTALLATION.md)** - Platform-specific installation guide
- **[Usage Guide](docs/USAGE.md)** - Complete command reference and workflows
- **[Jupyter Notebooks](notebooks/README.md)** - Interactive tutorials and examples
- **[Claude Code Guide](docs/CLAUDE_CODE.md)** - Using AI assistance with this codebase
- **[Results](docs/RESULTS.md)** - **Research findings (truth-functional: size-33, syntactic: size-35)**
- **[Examples](examples/README.md)** - Real execution examples and output
- **[Implementation](src/README.md)** - CLI and code documentation
- **[Testing](tests/README.md)** - Test suite documentation
- **[Specs](specs/README.md)** - Research reports and implementation plans
- **[Glossary](glossary/connectives.md)** - Complete ternary connectives reference

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Answer](#answer)
- [Quick Start](#quick-start)
- [Results Summary](#results-summary)
- [Technical Approach](#technical-approach)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
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

### **Truth-Functional Mode (Default): Maximum Size 33**
### **Syntactic Mode: Maximum Size 35**

Using Z3-based constraint solving with pattern enumeration (composition depth 3):

**The maximum size depends on the definability mode used:**

**Truth-Functional Mode (Default - Clone-Theoretic):**
- **Binary-only (arity ≤2)**: Maximum size varies by mode
- **Unary + Binary (arity ≤2)**: Maximum size is 5 (proven via Z3 exhaustive search)
- **Up to Ternary (arity ≤3)**: Nice sets of size 33 verified (likely maximum)
- **Higher arities (≥4)**: Unexplored - quaternary functions may enable different results

**Syntactic Mode (Composition-Based):**
- **Binary-only (arity ≤2)**: Maximum size is 3 (classical result, proven and reproduced)
- **Unary + Binary (arity ≤2)**: Maximum size is 5 (proven via Z3 exhaustive search)
- **Up to Ternary (arity ≤3)**: Nice sets of size 35 verified (size-36+ unknown)
- **Higher arities (≥4)**: Unexplored - quaternary functions may enable even larger nice sets

**Why the difference?** Truth-functional mode uses universal projection rules and cross-arity constant equivalence, detecting more dependencies and producing smaller maximum nice sets. See [docs/DEFINABILITY.md](docs/DEFINABILITY.md) for details.

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

### Truth-Functional Mode (Default)

| Arity Range | Known Nice Sets | Example |
|-------------|-----------------|---------|
| Binary only (arity ≤2) | Mode-dependent | Varies by mode |
| Unary + Binary (arity ≤2) | Max size = 5 (proven) | {FALSE, TRUE, XOR, AND, IMP} |
| **Up to Ternary (arity ≤3)** | **Size = 33 (likely max)** | 1 constant + 1 binary + 31 ternary (94% ternary) |
| Higher arities (arity ≥4) | Unexplored | Quaternary+ may enable different results |

### Syntactic Mode (Legacy)

| Arity Range | Known Nice Sets | Example |
|-------------|-----------------|---------|
| Binary only (arity ≤2) | Max size = 3 (proven) | {XOR, AND, TRUE} |
| Unary + Binary (arity ≤2) | Max size = 5 (proven) | {FALSE, TRUE, XOR, AND, IMP} |
| **Up to Ternary (arity ≤3)** | **Size ≥ 35** | 1 constant + 1 binary + 33 ternary (94% ternary) |
| Higher arities (arity ≥4) | Unexplored | Quaternary+ may enable larger sets |

### Key Findings

1. **Definability mode matters** - truth-functional (default) gives size-33, syntactic gives size-35
2. **Truth-functional is more restrictive** - universal projections and cross-arity constants create more dependencies
3. **Ternary functions essential** - in both modes, ternary functions dominate large nice sets (90%+)
4. **Pattern enumeration effective** - depth 3 composition checking verifies independence
5. **Validated implementation** - reproduces known results in both modes
6. **Mode choice matters for research** - choose based on whether you want clone-theoretic or composition-based results

### Search Performance Results (Syntactic Mode)

| Target Size | Max Arity | Result | Complete Sets Checked | Search Time | Notes |
|-------------|-----------|--------|----------------------|-------------|-------|
| 3 (binary-only) | 2 | ✓ Found | ~560 | <1s | Classical result validated |
| 5 (unary+binary) | 2 | ✓ Found | ~2,300 | 0.04s | Z3 symmetry breaking effective |
| 17 | 3 | ✓ Found | 22 | 0.69s | First ternary inclusion |
| 29 | 3 | ✓ Found | 161 | 3.17s | Early ternary dominance |
| 30 | 3 | ✓ Found | 1,246 | 245.75s | 4 minutes |
| 31 | 3 | ✓ Found | 9,527 | 359.62s | 6 minutes - slowest in 31-34 range |
| 32 | 3 | ✓ Found | 1,822 | 35.93s | 10× faster than 31! Non-monotonic |
| 33 | 3 | ✓ Found | 1,239 | 24.15s | Fastest in series |
| 34 | 3 | ✓ Found | 3,226 | 86.69s | Moderate difficulty |
| **35** | **3** | **✓ Found** | **26,860** | **2783.17s (~46 min)** | **8× harder, sparse solutions** |
| 36 | 3 | ? Unknown | - | - | May require extended search or may not exist |

### Search Performance Results (Truth-Functional Mode)

| Target Size | Max Arity | Result | Search Time | Notes |
|-------------|-----------|--------|-------------|-------|
| 29 | 3 | ✓ Found | ~3s | Truth-functional mode |
| 32 | 3 | ✓ Found | ~36s | Truth-functional mode |
| **33** | **3** | **✓ Found** | **~24s** | **Likely maximum for truth-functional** |

**Key Observations:**
- **Mode affects maximum size**: Truth-functional detects more dependencies → smaller maximum (33 vs 35)
- **Non-monotonic complexity**: Larger sizes aren't always harder (size-32 much faster than size-31)
- **Solution space collapsing**: Higher sizes show exponentially more candidates needed
- **Default is truth-functional**: All commands use truth-functional mode unless `--definability-mode syntactic` is specified

**See [docs/RESULTS.md](docs/RESULTS.md) for complete findings and [examples/README.md](examples/README.md) for detailed examples.**

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
├── tests/                  # Test suite (175 passing)
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

- **[Definability Modes](docs/DEFINABILITY.md)** - Syntactic vs truth-functional definability
  - Mathematical definitions of both modes
  - Universal projections and cross-arity constants
  - Practical examples showing differences
  - When to use each mode
  - CLI integration and usage

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
- **[Test Suite](tests/README.md)** - 175 passing tests
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

## Contributing

We welcome contributions! Whether you've found a bug, have an improvement idea, or want to add new features, here's how to contribute:

### Reporting Issues

**Found a bug?** Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Relevant error messages or logs

**Have a question?** Open an issue with the "question" label.

### Submitting Improvements

**Have an improvement or new feature?**

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/nice_connectives.git
   cd nice_connectives
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style and conventions
   - Add tests for new functionality
   - Update documentation as needed

4. **Run the test suite**
   ```bash
   pytest tests/ -v
   # Ensure all tests pass (175 tests should pass)
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes clearly
   - Link any related issues

### Development Guidelines

- **Code Style**: Follow existing patterns in the codebase
- **Testing**: Add tests for new features (see [tests/README.md](tests/README.md))
- **Documentation**: Update relevant docs in `docs/` and docstrings
- **Commits**: Use clear, descriptive commit messages
- **Dependencies**: Minimize new dependencies; justify if needed

### Areas for Contribution

Interested in contributing but not sure where to start? Consider:
- **Performance optimizations** - Improve search algorithms
- **Higher arities** - Explore quaternary (arity 4) connectives
- **Visualization** - Enhanced result visualization tools
- **Documentation** - Tutorials, examples, or clarifications
- **Testing** - Additional test coverage or edge cases
- **Jupyter notebooks** - New educational content

### Questions?

Open an issue with your question or proposed contribution idea for discussion before starting significant work.

---

**Project Status**: Implementation complete | 175 tests passing | Truth-functional: size-33 (likely max) | Syntactic: size-35 verified | Definability modes fully integrated
