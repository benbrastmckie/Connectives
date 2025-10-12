# Jupyter Notebook Usage Guide

Complete guide for using Jupyter notebooks with the Nice Connectives project.

## Installation

### Install Jupyter Dependencies

```bash
# Option 1: Install with optional dependencies (recommended)
pip install -e ".[jupyter]"

# Option 2: Install from requirements file
cd notebooks/
pip install -r requirements.txt

# Verify installation
python -c "import jupyter, matplotlib, pandas; print('✓ Jupyter dependencies installed')"
```

### Dependencies Included
- `jupyter>=1.0.0` - Jupyter notebook server
- `ipykernel>=6.0.0` - IPython kernel
- `matplotlib>=3.5.0` - Plotting and visualization
- `pandas>=2.0.0` - DataFrames for tabular data

## Launching Jupyter

```bash
# Navigate to notebooks directory
cd notebooks/

# Launch Jupyter notebook
jupyter notebook

# Your browser will open to http://localhost:8888
```

## Getting Started

### First Time Users

1. **Start with 00_setup_and_basics.ipynb**
   - Verifies your installation
   - Introduces basic concepts
   - Shows first examples

2. **Follow the learning path**
   - See [notebooks/README.md](../notebooks/README.md) for learning paths
   - Beginner path: notebooks 00-02 (~50 min)
   - Complete path: notebooks 00-06 (~3 hours)

3. **Run cells in order**
   - Use Shift+Enter to run cells
   - Earlier cells set up variables for later cells

### Python Path Setup

**All notebooks include automatic path setup** - no manual configuration needed!

Each notebook starts with a path setup cell that automatically adds the project root to Python's path:

```python
# Setup Python path to find the src module
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"✓ Project root added to path: {project_root}")
```

Simply run this cell first, then imports from `src` will work correctly.

## Notebook Tips

### Running Code

**Basic Navigation**:
- `Shift + Enter` - Run current cell and move to next
- `Ctrl + Enter` - Run current cell and stay
- `Alt + Enter` - Run current cell and insert new cell below

**Kernel Operations**:
- `Kernel → Restart` - Restart Python kernel (clears all variables)
- `Kernel → Restart & Run All` - Fresh start, run all cells
- `Kernel → Interrupt` - Stop a long-running cell

### Visualization

Notebooks use matplotlib for visualizations:

```python
import matplotlib.pyplot as plt
%matplotlib inline  # Display plots inline

# Create visualization
from notebooks.utils import visualize_truth_table
from src.constants import AND

fig = visualize_truth_table(AND)
plt.show()
```

### Modifying Examples

Feel free to modify and experiment!

```python
# Original example
from src.constants import AND, OR, XOR
from notebooks.utils import compare_connectives

fig = compare_connectives([AND, OR, XOR])
plt.show()

# Your modification - try different connectives!
from src.constants import NAND, NOR, EQUIV
fig = compare_connectives([NAND, NOR, EQUIV])
plt.show()
```

## Notebook Structure

### 00: Setup and Basics
**Topics**: Installation check, first connective, visualization
**Time**: 10 minutes
**Prerequisites**: None

### 01: Connectives Introduction
**Topics**: Arity, truth tables, binary connectives
**Time**: 20 minutes
**Prerequisites**: Notebook 00

### 02: Truth Tables
**Topics**: BitVec encoding, row indexing, ternary connectives
**Time**: 20 minutes
**Prerequisites**: Notebook 01

### 03: Completeness
**Topics**: Post's theorem, completeness checking
**Time**: 30 minutes
**Prerequisites**: Notebooks 00-02

### 04: Independence
**Topics**: Pattern enumeration, nice sets
**Time**: 30 minutes
**Prerequisites**: Notebooks 00-03

### 05: Binary Search
**Topics**: Enumeration search, max=3 result
**Time**: 30 minutes
**Prerequisites**: Notebooks 00-04

### 06: Ternary Search
**Topics**: Z3 search, size-17+, current research
**Time**: 30 minutes
**Prerequisites**: Notebooks 00-05

## Common Tasks

### Check if a Set is Nice

```python
from src.constants import AND, XOR, TRUE
from src.post_classes import is_complete
from src.independence import is_independent

my_set = [AND, XOR, TRUE]

# Check completeness
complete = is_complete(my_set)
print(f\"Complete: {complete}\")

# Check independence
independent = is_independent(my_set, max_depth=3)
print(f\"Independent: {independent}\")

# Nice set?
if complete and independent:
    print(\"✓ This is a nice set!\")
```

### Visualize a Custom Connective

```python
from src.connectives import Connective
from notebooks.utils import visualize_truth_table
import matplotlib.pyplot as plt

# Create custom connective
# Truth table value 150 = ternary majority
my_conn = Connective(3, 150)

# Visualize
fig = visualize_truth_table(my_conn, title=\"My Custom Connective\")
plt.show()
```

### Search for Nice Sets

```python
# Binary-only search (fast)
from src.constants import ALL_BINARY
from src.search import search_nice_sets_enumeration

nice_sets = search_nice_sets_enumeration(
    ALL_BINARY,
    target_size=3,
    max_depth=3
)

print(f\"Found {len(nice_sets)} nice sets of size 3\")

# Show first result
if nice_sets:
    from notebooks.utils import print_nice_set_summary
    print_nice_set_summary(nice_sets[0], \"Example Nice Set\")
```

## Troubleshooting

### Import Errors

```
ModuleNotFoundError: No module named 'pandas'
```

**Solution**: Install Jupyter dependencies
```bash
pip install -e \".[jupyter]\"
```

**Problem 2: Cannot import from src**
```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Run the path setup cell (first code cell in each notebook)
- All notebooks include automatic path setup
- Simply run the first cell that starts with `# Setup Python path`
- This adds the project root to Python's path

### Kernel Issues

**Symptoms**: Cells won't run, \"Kernel busy\" forever

**Solution**: Restart kernel
- Click `Kernel → Restart` in menu
- Re-run cells from the top

### Visualizations Not Showing

**Symptoms**: Plots don't appear

**Solution**: Check matplotlib inline mode
```python
%matplotlib inline
import matplotlib.pyplot as plt
```

### Slow Performance

**Symptoms**: Searches take very long

**Solutions**:
- **Use smaller target sizes** for learning (size 17 instead of 30)
- **Use CLI for large searches** (`python -m src.cli prove z3`)
- **Increase max_candidates** only if needed

### Cell Output Cleared

**Symptoms**: Previous cell outputs disappeared

**Cause**: Notebooks are stored without output (nbstripout)

**Solution**: Normal! Just run cells again

## Performance Guide

### Expected Search Times

| Search Type | Size | Time | Notebook |
|-------------|------|------|----------|
| Binary enumeration | 3 | <1 second | 05 |
| Binary enumeration | 4 | ~10 seconds | 05 |
| Z3 ternary | 17 | ~1-2 seconds | 06 |
| Z3 ternary | 30 | ~4 minutes | 06 |
| Z3 ternary | 35 | ~46 minutes | CLI only |

### When to Use CLI

For large searches (size 30+), use the CLI instead:

```bash
# Exit Jupyter and use CLI
cd ..
python -m src.cli prove z3 --target-size 30 --max-depth 3

# See results
cat examples/z3_nice_set_30.md
```

## Advanced Usage

### Custom Connective Pools

```python
from src.connectives import Connective

# Create custom pool (only specific ternary connectives)
my_ternary = [Connective(3, i) for i in [19, 23, 150, 232, 247]]

# Add binary connectives
from src.constants import AND, OR, XOR
my_pool = [AND, OR, XOR] + my_ternary

# Search in custom pool
from src.independence import is_independent
from src.post_classes import is_complete

if is_complete(my_pool) and is_independent(my_pool, max_depth=3):
    print(\"Nice set!\")
```

### Exporting Results

```python
# Save truth table to CSV
import pandas as pd
from notebooks.utils import display_truth_table
from src.constants import AND

df = display_truth_table(AND)
df.to_csv(\"and_truth_table.csv\", index=False)

# Save visualization
from notebooks.utils import visualize_truth_table
import matplotlib.pyplot as plt

fig = visualize_truth_table(AND)
fig.savefig(\"and_visualization.png\", dpi=300, bbox_inches='tight')
plt.close()
```

## Compatibility Fixes Applied

This section documents all compatibility fixes that were applied to make Jupyter notebooks work seamlessly with the codebase. Understanding these fixes can help troubleshoot issues and understand the notebook architecture.

### Python Path Setup (Commit: df68dfd)

**Issue**: Notebooks couldn't import from `src` module because the project root wasn't in Python's path.

**Solution**: Added automatic path setup to all 7 notebooks:
```python
import sys
from pathlib import Path
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

**Impact**: All notebooks (00-06) now work regardless of how Jupyter is launched.

### Constant Aliases (Commit: 769bd05)

**Issue**: Notebooks imported constants with simple names (`TRUE`, `FALSE`) but source code used descriptive names (`CONST_TRUE`, `CONST_FALSE`).

**Solution**: Added convenience aliases in `src/constants.py`:
```python
# Aliases for convenience
FALSE = CONST_FALSE
TRUE = CONST_TRUE
IMP = IMPLIES
EQUIV = IFF
ID = IDENTITY
```

**Impact**: Notebooks can use intuitive constant names while maintaining descriptive names in source code.

### Flexible evaluate() Method (Commit: 8ae4bc3)

**Issue**: Notebooks called `evaluate(0, 1)` but method expected `evaluate((0, 1))` tuple argument.

**Solution**: Modified `Connective.evaluate()` in `src/connectives.py` to accept both styles:
```python
def evaluate(self, *args) -> int:
    # Handle both evaluate((0,1)) and evaluate(0,1) styles
    if len(args) == 1 and isinstance(args[0], (tuple, list)):
        inputs = tuple(args[0])
    else:
        inputs = args
```

**Impact**: More Pythonic API - notebooks can use natural unpacked argument style.

### truth_table_int Formatting (Commit: 936eee6)

**Issue**: Z3 BitVecNumRef objects don't support Python format strings, causing `TypeError` in format operations.

**Solution**: Replaced all `truth_table` with `truth_table_int` in format strings:
```python
# Before (failed with Z3 objects)
print(f"{conn.truth_table:2d} = 0b{conn.truth_table:04b}")

# After (works correctly)
print(f"{conn.truth_table_int:2d} = 0b{conn.truth_table_int:04b}")
```

**Impact**: Fixed formatting errors in notebooks 00, 01, 02, and 05. All truth table displays now work correctly.

### Function Name Aliases (Commits: 5fbc793, 0994bf0, fc91b6f)

**Issue**: Notebooks imported functions with different names than source code definitions.

**Solutions**:

1. **get_post_class_memberships** (Commit: 5fbc793)
   ```python
   # src/post_classes.py
   get_post_class_memberships = get_post_class_membership
   ```

2. **search_nice_sets_enumeration** (Commit: 0994bf0)
   ```python
   # src/search.py
   def search_nice_sets_enumeration(connectives, target_size, max_depth=3):
       return find_nice_sets_of_size(connectives, target_size, max_depth, verbose=False)
   ```

3. **search_z3_nice_set** (Commit: fc91b6f)
   ```python
   # src/proofs/z3_proof.py
   def search_z3_nice_set(pool, target_size, max_depth=3, max_candidates=100):
       result = z3_proof_approach_1_symmetry_breaking(
           pool=pool, target_size=target_size, max_depth=max_depth,
           checkpoint_path=None, checkpoint_interval=100,
           max_candidates=max_candidates
       )
       return None if result else pool[:target_size]
   ```

**Impact**: Notebooks can use intuitive function names while source code maintains descriptive, verbose names.

### Set Membership Checks (Commit: 6763e76)

**Issue**: Code tried to access sets with dictionary syntax `memberships['T0']` instead of set membership syntax.

**Solution**: Fixed all set membership checks in notebook 03_completeness.ipynb (5 cells):
```python
# Before (incorrect - sets don't support indexing)
t0 = "✓" if memberships['T0'] else "✗"

# After (correct - set membership check)
t0 = "✓" if 'T0' in memberships else "✗"
```

**Impact**: All Post class membership displays now work correctly.

### Summary of Fixes

| Fix | Commits | Files Affected | Type |
|-----|---------|----------------|------|
| Python path setup | df68dfd | All 7 notebooks | Path configuration |
| Constant aliases | 769bd05 | src/constants.py | API simplification |
| Flexible evaluate() | 8ae4bc3 | src/connectives.py | API enhancement |
| truth_table_int | 936eee6 | 4 notebooks (00,01,02,05) | Z3 compatibility |
| Function aliases | 5fbc793, 0994bf0, fc91b6f | 3 source files | API simplification |
| Set membership | 6763e76 | 03_completeness.ipynb | Bug fix |

**Total**: 11 compatibility fixes across 8 commits

### Troubleshooting with Compatibility Context

When encountering errors, reference these fixes:

- **Import errors** → Check Python path setup cell was run
- **Constant not found** → Use aliased names (TRUE vs CONST_TRUE)
- **evaluate() TypeError** → Both tuple and unpacked args supported
- **Format string errors** → Use truth_table_int for formatting
- **Function not found** → Use aliased function names
- **Set subscript errors** → Use `in` operator for set membership

These fixes maintain backward compatibility while providing a better notebook experience.

## Additional Resources

### Documentation
- **[Notebooks README](../notebooks/README.md)** - Notebook overview and learning paths
- **[Usage Guide](USAGE.md)** - CLI commands
- **[Installation Guide](INSTALLATION.md)** - Setup instructions

### Research
- **[Results](RESULTS.md)** - Research findings
- **[Glossary](../glossary/connectives.md)** - Ternary connectives reference
- **[Examples](../examples/README.md)** - CLI output examples

### Help
- **[Claude Code Guide](CLAUDE_CODE.md)** - AI assistance
- **[Project README](../README.md)** - Project overview

## Next Steps

1. **Launch Jupyter**: `cd notebooks/ && jupyter notebook`
2. **Start with notebook 00**: Setup and basics
3. **Follow a learning path**: See notebooks/README.md
4. **Experiment**: Modify examples and explore
5. **Share findings**: Contribute back to the project!

Happy exploring!
