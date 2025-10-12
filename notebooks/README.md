# Nice Connectives Jupyter Notebooks

Interactive notebooks for exploring logical connectives, completeness, independence, and searching for nice sets.

## Installation

```bash
# Install with Jupyter support
pip install -e ".[jupyter]"

# Or install from requirements.txt
pip install -r notebooks/requirements.txt
```

## Quick Start

```bash
# Launch Jupyter from the notebooks directory
cd notebooks/
jupyter notebook

# Open 00_setup_and_basics.ipynb to begin
```

## Notebook Overview

| # | Notebook | Level | Topics | Time |
|---|----------|-------|--------|------|
| 00 | Setup and Basics | Beginner | Installation, first connective, visualization | 10 min |
| 01 | Connectives Intro | Beginner | Nullary, unary, binary connectives | 20 min |
| 02 | Truth Tables | Intermediate | BitVec encoding, row indexing, ternary connectives | 20 min |
| 03 | Completeness | Intermediate | Post's theorem, 5 Post classes | 30 min |
| 04 | Independence | Intermediate | Pattern enumeration, nice sets | 30 min |
| 05 | Search: Binary | Advanced | Enumeration search, max=3 result | 30 min |
| 06 | Search: Ternary | Advanced | Z3 search, size-17+, arity distributions | 30 min |

**Total time**: ~3 hours

## Learning Paths

### Path 1: Beginner (Get Started)
Start here if you're new to the project:
1. 00_setup_and_basics.ipynb
2. 01_connectives_intro.ipynb
3. 02_truth_tables.ipynb

**Time**: ~50 minutes
**Goal**: Understand connectives and truth table encoding

### Path 2: Researcher (Complete Understanding)
For deep dive into nice set theory:
1. 00_setup_and_basics.ipynb
2. 01_connectives_intro.ipynb
3. 02_truth_tables.ipynb
4. 03_completeness.ipynb
5. 04_independence.ipynb
6. 05_search_binary.ipynb
7. 06_search_ternary.ipynb

**Time**: ~3 hours
**Goal**: Understand the complete research problem and approach

### Path 3: Quick Demo (Show Me Results)
Just want to see nice sets?
1. 00_setup_and_basics.ipynb (quick verification)
2. 05_search_binary.ipynb (classical result)
3. 06_search_ternary.ipynb (current research)

**Time**: ~1 hour
**Goal**: See search results and examples

## Features

### Interactive Exploration
- Run code cells to create and visualize connectives
- Modify examples to explore different scenarios
- Test your own connective sets

### Visualization Tools
- Truth table displays with pandas DataFrames
- Heatmap visualizations with matplotlib
- Side-by-side connective comparisons
- Arity distribution plots

### Real Research Code
- All notebooks use the actual library code
- Same algorithms as CLI and research scripts
- Results match published findings

## Utilities

The `utils.py` module provides helper functions:

```python
from notebooks.utils import (
    display_truth_table,          # Show truth table as DataFrame
    visualize_truth_table,         # Heatmap visualization
    compare_connectives,           # Side-by-side comparison
    plot_arity_distribution,       # Arity bar chart
    print_nice_set_summary,        # Summary statistics
    get_common_connectives,        # Quick access to AND, OR, XOR, etc.
)
```

## Tips

### Running Notebooks
- **Run cells in order** - later cells depend on earlier ones
- **Restart kernel** if you get unexpected results
- **Shift+Enter** runs current cell and moves to next
- **Kernel → Restart & Run All** to run entire notebook

### Performance Notes
- Size-17 searches take ~1-2 seconds
- Size-30 searches take ~4 minutes
- Larger searches (size 35+) take significantly longer
- Consider using the CLI for large-scale searches

### Troubleshooting
- **Import errors**: Make sure you ran `pip install -e ".[jupyter]"`
- **Kernel issues**: Try restarting the kernel (Kernel → Restart)
- **Visualization not showing**: Check that `%matplotlib inline` is run
- **Slow performance**: Reduce search sizes or use CLI instead
- **Compatibility issues**: See [JUPYTER.md Compatibility Fixes](../docs/JUPYTER.md#compatibility-fixes-applied) for detailed troubleshooting of all known notebook issues

## Additional Resources

### Documentation
- **[Usage Guide](../docs/USAGE.md)** - CLI commands and workflows
- **[JUPYTER.md](../docs/JUPYTER.md)** - Complete Jupyter usage guide
- **[Installation](../docs/INSTALLATION.md)** - Setup instructions

### Research
- **[Results](../docs/RESULTS.md)** - Research findings (size-35!)
- **[Glossary](../glossary/connectives.md)** - All 256 ternary connectives
- **[Examples](../examples/README.md)** - Real execution examples

### Project Info
- **[README](../README.md)** - Project overview
- **[CLAUDE_CODE.md](../docs/CLAUDE_CODE.md)** - AI assistance guide

## Contributing

Found a bug or have an improvement? See the main [README](../README.md) for contribution guidelines.

## License

MIT License - See main project README for details.
