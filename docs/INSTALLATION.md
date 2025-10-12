# Installation Guide

An accessible installation guide for the Nice Connectives Solver.

---

## Table of Contents

- [Quick Installation Summary](#quick-installation-summary)
- [Prerequisites](#prerequisites)
- [Installing Python 3](#installing-python-3)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Dependencies](#installing-dependencies)
- [Verifying Installation](#verifying-installation) (links to USAGE.md)
- [Platform-Specific Notes](#platform-specific-notes)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Terminal

This project is a **Command-Line Interface (CLI)** application, which means it runs in a terminal (also called command prompt or shell) rather than as a graphical application with windows and buttons.

### Opening the Terminal

**macOS:**
1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal" and press Enter
3. Or navigate to Applications → Utilities → Terminal

**Windows:**
1. Press `Win + R` to open Run dialog
2. Type `cmd` and press Enter (Command Prompt)
3. Or type `powershell` for PowerShell
4. Or search "Command Prompt" or "PowerShell" in the Start menu

Once the terminal is open, you can type commands and press Enter to execute them. All installation and usage commands in this guide should be entered in the terminal.

### Basic Terminal Navigation

**`cd` (Change Directory)** - Move between folders:
```bash
cd Documents              # Enter the Documents folder
cd nice_connectives       # Enter the nice_connectives folder
cd ..                     # Go up one level (to parent folder)
cd ~                      # Go to your home directory
```

**`ls` (List)** - See what's in the current folder:
```bash
ls                        # List files and folders
ls -la                    # List with details (Linux/macOS)
dir                       # List files (Windows Command Prompt)
```

**Example workflow:**
```bash
cd Documents              # Go to Documents
ls                        # See what's here
cd nice_connectives       # Enter the project folder
ls                        # Verify you see: src/, tests/, README.md
```

---

## Prerequisites

### Required Software

1. **Python 3.8 or later**
   - Check version: `python3 --version`
   - Required for all project functionality

2. **Git** (for cloning the repository)
   - Check version: `git --version`
   - Alternative: Download repository as ZIP from GitHub

3. **pip** (Python package manager)
   - Usually included with Python 3
   - Check version: `pip3 --version` or `pip --version`

**Tip**: For interactive help with installation on your specific platform, see the [Claude Code Guide](CLAUDE_CODE.md).

### Required Dependencies

- **pytest** - Testing framework for running the test suite
- **z3-solver** - SMT solver for Z3-based constraint solving proofs

These will be installed automatically with `pip install -e .`, but platform-specific installation methods are detailed below.

### Optional Dependencies (Jupyter Notebooks)

For interactive Jupyter notebook tutorials:
- **jupyter** - Jupyter notebook server
- **ipykernel** - IPython kernel for Jupyter
- **matplotlib** - Visualization library
- **pandas** - Data analysis and DataFrame support

Install with: `pip install -e ".[jupyter]"`

See **[Jupyter Notebooks Guide](JUPYTER.md)** for complete setup and usage instructions.

---

## Installing Python 3

### Linux (Debian/Ubuntu)

```bash
# Update package list
sudo apt update

# Install Python 3, pip, and dependencies
sudo apt install python3 python3-pip python3-pytest python3-z3

# Verify installation
python3 --version
pip3 --version
pytest --version
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
```

**Note:** Installing via apt provides system packages. Alternatively, use pip (see [Installing Dependencies](#installing-dependencies)).

### Linux (Arch)

```bash
# Install Python 3, pip, and dependencies
sudo pacman -S python python-pip python-pytest python-z3

# Verify installation
python3 --version
pip3 --version
pytest --version
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
```

**Note:** Arch provides z3 via `python-z3` package. Alternatively, use pip.

### macOS

**Option 1: Using Homebrew (Recommended)**

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3 and z3
brew install python3 z3

# Install pytest via pip (after Python is installed)
pip3 install pytest

# Verify installation
python3 --version
pip3 --version
pytest --version
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
```

**Option 2: Official Installer**

1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer package
3. Verify: `python3 --version`
4. Install dependencies: `pip3 install pytest z3-solver`

### Windows

**Option 1: Official Installer (Recommended)**

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **Important:** Check "Add Python to PATH" during installation
4. Verify in Command Prompt: `python --version`
5. Install dependencies:
   ```cmd
   pip install pytest z3-solver

   # Verify
   pytest --version
   python -c "import z3; print('z3 version:', z3.get_version_string())"
   ```

**Option 2: Microsoft Store**

1. Open Microsoft Store
2. Search "Python 3.11" (or latest version)
3. Click "Get" to install
4. Verify: `python --version`
5. Install dependencies:
   ```cmd
   pip install pytest z3-solver

   # Verify
   pytest --version
   python -c "import z3; print('z3 version:', z3.get_version_string())"
   ```

**Option 3: Windows Subsystem for Linux (WSL)**

```bash
# Enable WSL (PowerShell as Administrator)
wsl --install

# Restart computer, then install Python in WSL Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-pytest python3-z3

# Verify installation
python3 --version
pip3 --version
pytest --version
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
```

### NixOS

```bash
# Add to configuration.nix or use nix-shell
nix-shell -p python3 python3Packages.pip python3Packages.pytest python3Packages.z3

# Or add to environment.systemPackages in configuration.nix:
# environment.systemPackages = with pkgs; [
#   python3
#   python3Packages.pip
#   python3Packages.pytest
#   python3Packages.z3
# ];
```

---

## Cloning the Repository

### Using Git (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/nice_connectives.git

# Navigate into the directory
cd nice_connectives

# Verify you're in the right directory
ls -la
# Should see: src/, tests/, examples/, docs/, README.md, etc.
```

### Using SSH (if you have SSH keys configured)

```bash
git clone git@github.com:yourusername/nice_connectives.git
cd nice_connectives
```

### Download as ZIP (Alternative)

1. Visit the GitHub repository page
2. Click green "Code" button
3. Select "Download ZIP"
4. Extract the archive
5. Navigate into the extracted directory

```bash
# Linux/macOS
cd ~/Downloads/nice_connectives-main

# Windows (Command Prompt)
cd C:\Users\YourName\Downloads\nice_connectives-main
```

---

## Installing Dependencies

This project requires two critical Python packages:

1. **z3-solver** - Microsoft's Z3 SMT solver for constraint-based proof search
2. **pytest** - Testing framework for running the 175-test suite

These dependencies can be installed via:
- **Automatic**: `pip install -e .` (run from project root directory, installs from pyproject.toml)
- **Manual**: `pip install pytest z3-solver` (explicit installation, can run from anywhere)
- **System packages**: Platform-specific (apt, dnf, pacman, brew, nix)

### Standard Installation (Most Systems)

The project uses `pyproject.toml` for dependency management.

```bash
# Navigate to project root
cd nice_connectives

# Install in editable mode with all dependencies
pip install -e .

# This installs:
# - pytest (testing framework)
# - z3-solver (SMT solver for proofs)
# - The nice-connectives package itself
```

**Verify installation:**

```bash
# Check that the package is installed
pip list | grep nice-connectives

# Try importing the module
python3 -c "from src import cli; print('Import successful!')"
```

### Alternative: Manual Dependency Installation

If `pip install -e .` doesn't work on your system, or if you prefer explicit control:

```bash
# Install dependencies individually
pip3 install pytest z3-solver

# Verify pytest installation
pytest --version
# Expected output: pytest 7.x.x or later

# Verify z3-solver installation
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
# Expected output: z3 version: 4.x.x.x

# No package installation needed - can run directly
python3 -m src.cli --help
```

**When to use manual installation:**
- System package managers (apt, dnf, pacman, brew) don't have pytest or z3
- You want specific versions of dependencies
- pip install -e . fails due to permissions
- You prefer explicit dependency management

### NixOS Special Case

NixOS uses a read-only `/nix/store`, so `pip install -e .` won't work.

**Solution: Use directly without installation**

```bash
# Start nix-shell with dependencies
nix-shell -p python3 python3Packages.pytest python3Packages.z3

# Run commands directly
python3 -m src.cli --help
python3 -m src.cli search binary

# Or create a shell.nix file:
cat > shell.nix <<'EOF'
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pytest
    python3Packages.z3
  ];
}
EOF

# Then use:
nix-shell
python3 -m src.cli --help
```

### Virtual Environment (Optional)

Using a virtual environment isolates project dependencies.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install dependencies in virtual environment
pip install -e .

# When done working:
deactivate
```

---

## Verifying Installation

After installation, verify everything works correctly.

**Important:** Run these commands from the project root directory (where you cloned the repository).

```bash
# Navigate to project directory (if not already there)
cd nice_connectives

# Quick verification commands
python3 -m src.cli --help
python3 -m src.cli search validate
pytest tests/ -v
```

**For detailed verification steps, expected outputs, and usage examples, see [USAGE.md](USAGE.md).**

---

## Platform-Specific Notes

### Windows

**Command differences:**
- Use `python` instead of `python3` (if Python 3 is your default)
- Use backslashes `\` for paths or forward slashes `/`
- Use Command Prompt or PowerShell (not Git Bash for some commands)

**Path separators:**
```bash
# Windows Command Prompt or PowerShell
python -m src.cli search binary

# Works the same way (Python handles module paths)
```

**Long paths issue:**
If you encounter "path too long" errors:
1. Enable long paths in Windows
2. Or move repository closer to root: `C:\projects\nice_connectives`

### macOS

**Python 2 vs Python 3:**
- macOS may have Python 2 as `python`
- Always use `python3` explicitly
- Or create alias: `alias python=python3`

**Permissions:**
If you get permission errors with pip:
```bash
# Use user installation
pip3 install --user -e .

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Linux

**Multiple Python versions:**
```bash
# Check available Python versions
ls /usr/bin/python*

# Use specific version if needed
python3.11 -m src.cli --help

# Or create alias in ~/.bashrc
alias python3=/usr/bin/python3.11
```

**System vs user installation:**
```bash
# User installation (no sudo needed)
pip3 install --user -e .

# System-wide (requires sudo, not recommended)
sudo pip3 install -e .
```

### NixOS

**Do not use pip install:**
- NixOS filesystem is read-only
- Dependencies managed through nix packages
- Run project directly without installation

**Recommended workflow:**
```bash
# Create shell.nix (one-time setup)
cat > shell.nix <<'EOF'
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pytest
    python3Packages.z3
  ];
}
EOF

# Enter development shell
nix-shell

# Run commands
python3 -m src.cli search binary
pytest tests/
```

---

## Troubleshooting

### "python3: command not found"

**Solution:** Install Python 3 (see [Installing Python 3](#installing-python-3))

Or on some systems, Python 3 is installed as `python`:
```bash
python --version
# If shows Python 3.x.x, use 'python' instead of 'python3'
```

### "No module named 'src'"

**Cause:** Running from wrong directory

**Solution:** Navigate to project root
```bash
cd /path/to/nice_connectives
ls  # Should see src/, tests/, README.md
python3 -m src.cli --help
```

### "ModuleNotFoundError: No module named 'pytest'"

**Cause:** pytest not installed

**Solution:**
```bash
pip3 install pytest
# Or install all dependencies:
pip3 install -e .
```

### "ModuleNotFoundError: No module named 'z3'"

**Cause:** z3-solver not installed

**Solution:**
```bash
# Option 1: Install via pip
pip3 install z3-solver

# Option 2: Install via system package manager
# Debian/Ubuntu:
sudo apt install python3-z3
# Fedora/RHEL:
sudo dnf install python3-z3
# Arch:
sudo pacman -S python-z3
# macOS:
brew install z3

# Option 3: Install all dependencies:
pip3 install -e .

# Verify z3 is installed:
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
```

### "Permission denied" (Linux/macOS)

**Solution 1: User installation**
```bash
pip3 install --user -e .
```

**Solution 2: Virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Tests fail with import errors

**Cause:** pytest finding wrong Python version or modules

**Solution:** Run pytest as a module
```bash
python3 -m pytest tests/ -v
```

### "pip: command not found"

**Cause:** pip not installed

**Solution:**
```bash
# Linux (Debian/Ubuntu)
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade

# Windows
# Reinstall Python with "pip" option checked
```

### Virtual environment activation fails (Windows PowerShell)

**Error:** "cannot be loaded because running scripts is disabled"

**Solution:** Enable script execution
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\Activate.ps1
```

### Import works but CLI commands fail

**Cause:** Package installed but not in editable mode

**Solution:**
```bash
# Reinstall in editable mode
pip uninstall nice-connectives
pip install -e .
```

---

## Next Steps

After successful installation:

1. **Try interactive notebooks (optional):** [Jupyter Notebooks](JUPYTER.md) - Interactive tutorials and examples
2. **Read the usage guide:** [USAGE.md](USAGE.md)
3. **Use Claude Code for AI assistance:** [CLAUDE_CODE.md](CLAUDE_CODE.md) - Get help understanding and working with the codebase
4. **Explore examples:** [examples/README.md](../examples/README.md)
5. **View research results:** [RESULTS.md](RESULTS.md)
6. **Understand implementation:** [src/README.md](../src/README.md)
7. **Browse ternary connectives:** [Glossary](../glossary/connectives.md) - Complete reference for all f3_N connectives

### Verify Dependencies Installed

Before running the project, verify all dependencies are correctly installed:

```bash
# Check Python version (should be 3.8+)
python3 --version

# Check pytest is installed
pytest --version
# Expected: pytest 7.x.x or later

# Check z3-solver is installed
python3 -c "import z3; print('z3 version:', z3.get_version_string())"
# Expected: z3 version: 4.x.x.x

# Check src module can be imported
python3 -c "from src import cli; print('✓ Source code accessible')"
# Expected: ✓ Source code accessible
```

If any of these fail, review the [Troubleshooting](#troubleshooting) section.

### Quick Start Commands

```bash
# Validate installation
python3 -m src.cli search validate

# Reproduce classical result (binary-only max = 3)
python3 -m src.cli search binary

# Find size-5 nice set (unary + binary)
python3 -m src.cli prove z3 --target-size 5 --max-arity 2

# Run full test suite (requires pytest and z3-solver)
pytest tests/ -v

# Get help
python3 -m src.cli --help
```

---

## Getting Help

### AI-Powered Assistance

- **[Claude Code Guide](CLAUDE_CODE.md)** - Use Claude AI to help with installation, understanding code, and troubleshooting
  - Ask questions about the codebase
  - Get installation help interactively
  - Troubleshoot errors with AI assistance

### Documentation Resources

- **[README.md](../README.md)** - Project overview and mathematical background
- **[USAGE.md](USAGE.md)** - Complete usage guide for all commands
- **[src/README.md](../src/README.md)** - Implementation documentation
- **[examples/README.md](../examples/README.md)** - Example outputs and findings
- **[Glossary](../glossary/connectives.md)** - Ternary connectives reference

### Common Issues

If you encounter issues not covered here:

1. Check you're in the project root directory
2. Verify Python version is 3.8 or later: `python3 --version`
3. Verify dependencies are installed: `pip list | grep -E "pytest|z3"`
4. Try running in a fresh virtual environment
5. Check pytest can find the modules: `python3 -m pytest --collect-only`

### Reporting Issues

When reporting installation problems, include:
- Operating system and version
- Python version: `python3 --version`
- pip version: `pip3 --version`
- Exact error message (full traceback)
- Command that caused the error

---

**Installation complete! You're ready to explore nice connective sets.**
