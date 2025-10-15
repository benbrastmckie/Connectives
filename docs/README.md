# Documentation Directory

Complete documentation for the Nice Connectives project.

## Documentation Files

### Getting Started

#### [INSTALLATION.md](INSTALLATION.md)
**Complete installation guide for all platforms**

Platform-specific instructions for:
- Linux (Debian/Ubuntu, Arch, Fedora/RHEL)
- macOS (Homebrew, Official Installer)
- Windows (Official Installer, Microsoft Store, WSL)
- NixOS (nix-shell configuration)

Includes:
- Terminal basics for beginners
- Python 3, pytest, z3-solver installation
- Optional Jupyter dependencies
- Virtual environment setup
- Troubleshooting common issues
- Verification steps

**Start here** if you're setting up the project for the first time.

---

#### [USAGE.md](USAGE.md)
**Complete command reference and usage guide**

Comprehensive CLI documentation:
- All command categories (search, prove, validate, benchmark)
- Expected outputs and results
- Common workflows and patterns
- Performance tips and optimization
- Advanced usage examples
- Command options and parameters

**Read this** after installation to learn how to use the CLI.

---

#### [DEFINABILITY.md](DEFINABILITY.md)
**Definability modes: syntactic vs truth-functional**

Complete guide to definability notions:
- Mathematical definitions of both modes
- Universal projections in truth-functional mode
- Cross-arity constant equivalence
- Practical examples showing differences
- When to use each mode
- CLI integration and usage
- Implementation details and tests

**Read this** to understand definability mode choices.

---

### Interactive Learning

#### [JUPYTER.md](JUPYTER.md)
**Jupyter notebook usage guide**

Interactive tutorial system:
- Installation of Jupyter dependencies (`pip install -e ".[jupyter]"`)
- Launching and using Jupyter notebooks
- Notebook structure and learning paths
- Common tasks with code examples
- Performance expectations for searches
- Comprehensive troubleshooting guide
- Advanced usage patterns

**Includes**:
- 7 interactive notebooks (00-06)
- 3 learning paths (Beginner, Researcher, Quick Demo)
- Visualization tools and utilities
- Real search demonstrations

See also: [notebooks/README.md](../notebooks/README.md) for notebook overview and learning paths.

---

### AI Assistance

#### [CLAUDE_CODE.md](CLAUDE_CODE.md)
**Using Claude Code AI assistant with this codebase**

AI-powered help for:
- Understanding the codebase
- Installation assistance
- Troubleshooting errors
- Making code changes
- Running searches
- Understanding results

Installation instructions for:
- macOS (Homebrew)
- Windows (winget, PowerShell, WSL)
- Linux (curl install script, platform packages)

**Use this** for interactive AI help with the project.

---

### Research and Results

#### [RESULTS.md](RESULTS.md)
**Research findings and conclusions**

Complete research summary:
- **Binary-only maximum**: 3 (classical result, proven)
- **Unary + Binary maximum**: 5 (proven via Z3)
- **With Ternary (arity ≤3)**: Size 35 verified (current maximum)
- Systematic search results from size 17 through 35
- Performance analysis and non-monotonic complexity
- Arity distributions (90%+ ternary for large sets)
- Open questions and future work

**Read this** to understand the research findings.

---

## Quick Navigation

### By Task

**I want to install the project:**
→ Start with [INSTALLATION.md](INSTALLATION.md)

**I want to learn how to use the CLI:**
→ Read [USAGE.md](USAGE.md)

**I want to learn interactively with Jupyter:**
→ Follow [JUPYTER.md](JUPYTER.md) and [notebooks/README.md](../notebooks/README.md)

**I want AI help:**
→ Use [CLAUDE_CODE.md](CLAUDE_CODE.md)

**I want to see the research results:**
→ Read [RESULTS.md](RESULTS.md)

**I want to run examples:**
→ See [examples/README.md](../examples/README.md)

**I want to understand the code:**
→ Read [src/README.md](../src/README.md)

---

## Documentation Structure

```
docs/
├── README.md            # This file - documentation overview
├── INSTALLATION.md      # Platform-specific installation guide
├── USAGE.md             # Complete CLI command reference
├── DEFINABILITY.md      # Definability modes (syntactic vs truth-functional)
├── JUPYTER.md           # Jupyter notebook usage guide
├── CLAUDE_CODE.md       # AI assistance with Claude Code
└── RESULTS.md           # Research findings and conclusions
```

---

## Related Documentation

### Project Documentation
- **[Main README](../README.md)** - Project overview and problem statement
- **[CLAUDE.md](../CLAUDE.md)** - Project standards and conventions

### Implementation Documentation
- **[src/README.md](../src/README.md)** - CLI and code documentation
- **[src/commands/README.md](../src/commands/README.md)** - Command implementations
- **[src/proofs/README.md](../src/proofs/README.md)** - Proof methodologies

### Examples and Tutorials
- **[examples/README.md](../examples/README.md)** - Real execution examples
- **[notebooks/README.md](../notebooks/README.md)** - Interactive Jupyter notebooks
- **[glossary/connectives.md](../glossary/connectives.md)** - Ternary connectives reference

### Testing
- **[tests/README.md](../tests/README.md)** - Test suite documentation (175 passing tests)

### Research Documentation
- **[specs/README.md](../specs/README.md)** - Research reports and implementation plans

---

## Documentation Standards

All documentation follows the project standards defined in [CLAUDE.md](../CLAUDE.md):

- **UTF-8 encoding** - All documentation files
- **Markdown format** - CommonMark specification
- **Clear language** - Accessible to beginners
- **Code examples** - With syntax highlighting
- **Cross-references** - Proper linking between documents
- **Platform coverage** - Instructions for all major platforms

---

## Contributing to Documentation

When contributing documentation:

1. Follow the standards in [CLAUDE.md](../CLAUDE.md)
2. Maintain consistent formatting and style
3. Include code examples with syntax highlighting
4. Test all commands and examples
5. Update cross-references when adding new docs
6. Use clear, concise language

For AI-assisted documentation work, see [CLAUDE_CODE.md](CLAUDE_CODE.md).

---

## Getting Help

### Quick Help
- **Installation issues**: See [INSTALLATION.md](INSTALLATION.md) Troubleshooting section
- **Usage questions**: See [USAGE.md](USAGE.md) or run `python -m src.cli --help`
- **Jupyter problems**: See [JUPYTER.md](JUPYTER.md) Troubleshooting section
- **AI assistance**: Use [Claude Code](CLAUDE_CODE.md)

### Additional Resources
- **Project README**: [../README.md](../README.md)
- **Examples Directory**: [../examples/README.md](../examples/README.md)
- **Interactive Notebooks**: [../notebooks/README.md](../notebooks/README.md)
- **Glossary**: [../glossary/connectives.md](../glossary/connectives.md)

---

**Complete documentation for understanding, installing, using, and contributing to the Nice Connectives project.**
