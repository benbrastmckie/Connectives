# Using Claude Code with the Nice Connectives Project

This guide explains how to install and use Claude Code to work with this codebase.

## What is Claude Code?

Claude Code is Anthropic's official command-line interface that allows you to interact with Claude AI directly in your terminal. It's particularly useful for:
- Asking questions about the codebase
- Making code changes with AI assistance
- Running analyses and generating documentation
- Understanding complex algorithms and mathematical proofs

## Installation

### macOS

```bash
# Using Homebrew (recommended)
brew install anthropics/claude/claude-code

# Or using curl
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh
```

### Windows

**Option 1: Using winget (Windows 11)**
```powershell
winget install Anthropic.ClaudeCode
```

**Option 2: Using PowerShell**
```powershell
# Run in PowerShell (as Administrator)
irm https://raw.githubusercontent.com/anthropics/claude-code/main/install.ps1 | iex
```

**Option 3: Using WSL (Windows Subsystem for Linux)**
```bash
# Follow the Linux installation instructions below
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh
```

### Linux

**Debian/Ubuntu:**
```bash
# Download and install
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh

# Or using apt (if available)
sudo apt update
sudo apt install claude-code
```

**Arch Linux:**
```bash
# Using yay (AUR helper)
yay -S claude-code

# Or using paru
paru -S claude-code

# Or manual installation
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh
```

**Fedora/RHEL:**
```bash
# Using dnf
sudo dnf install claude-code

# Or using the install script
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh
```

### Verify Installation

After installation, verify Claude Code is installed correctly:

```bash
claude --version
```

You should see the version number displayed.

## Authentication

Before using Claude Code, you need to authenticate:

```bash
# Start the authentication process
claude auth login

# Follow the prompts to:
# 1. Open the provided URL in your browser
# 2. Log in with your Anthropic account
# 3. Authorize Claude Code
# 4. Return to the terminal
```

Once authenticated, you're ready to use Claude Code!

## Using Claude Code with This Repository

### First Time Setup: Cloning and Installing

If you haven't cloned this repository yet, Claude Code can help you follow the installation instructions. Once you have Claude Code installed and authenticated, start it in the directory that you want to clone this repository into (this will be the directory you will then work out of):

```bash
claude
```

Then ask Claude Code to follow the installation instructions:

```
Please follow the installation instructions at
https://github.com/benbrastmckie/Connectives/blob/master/docs/INSTALLATION.md
to clone the repository into this directory and install all dependencies.
```

Claude Code will:
1. Fetch and read the installation instructions from the URL
2. Clone the repository to your current directory
3. Install Z3 and all required Python packages
4. Verify the installation works correctly

**Prerequisites:** Make sure you have Python 3 and git installed before running the installation.

### Basic Workflow

**1. Navigate to the repository:**

```bash
# Change to the nice_connectives directory
cd ~/Documents/Philosophy/Projects/Z3/nice_connectives

# Or use your full path
cd /home/benjamin/Documents/Philosophy/Projects/Z3/nice_connectives
```

**2. Start Claude Code:**

```bash
# Start an interactive session
claude
```

**3. Ask questions or request changes:**

Once Claude Code starts, you'll see a prompt where you can interact with Claude. The AI has full context of your codebase.

### Example Usage Scenarios

#### Example 1: Understanding the Codebase

```bash
cd ~/Documents/Philosophy/Projects/Z3/nice_connectives
claude
```

Then in Claude Code:
```
How does the Z3-based independence checking work in this codebase?
```

Claude will analyze the relevant files and explain the implementation.

#### Example 2: Explaining a Specific Connective

```
What is the truth table for connective f3_150? Can you show me
how it's used in the nice set examples?
```

Claude will look up the connective in the glossary and show you where it appears.

#### Example 3: Developing a Feature on a New Branch

This example shows the complete workflow for developing a feature using Claude Code, following the [Contributing Guide](CONTRIBUTING.md).

```
I want to add a feature that displays truth tables in a more readable
format. Can you help me follow the contribution workflow from
docs/CONTRIBUTING.md to:
1. Create a feature branch
2. Implement the feature
3. Add tests
4. Update documentation
```

**Claude will guide you through each step:**

**Step 1: Create Feature Branch**
```
Let me help you create a feature branch following the project's
contribution guidelines.

First, let's make sure your master branch is up to date:
```

Claude will run:
```bash
git checkout master
git pull upstream master
```

Then create your feature branch:
```bash
git checkout -b feature/readable-truth-tables
```

**Step 2: Implement the Feature**
```
Now I'll add a function to src/connectives.py that formats truth
tables in a readable way.
```

Claude will:
1. Read the existing code in src/connectives.py
2. Write a new `format_truth_table()` function
3. Show you the implementation
4. Explain the design decisions

```python
def format_truth_table(connective, arity):
    """
    Format a connective's truth table in human-readable form.

    Args:
        connective: BitVec representation of truth table
        arity: Number of inputs (0, 1, 2, or 3)

    Returns:
        str: Formatted truth table with headers and rows
    """
    # Implementation here...
```

**Step 3: Add Tests**
```
Following the testing guidelines in docs/CONTRIBUTING.md, I'll add
tests to tests/test_connectives.py
```

Claude will create test cases like:
```python
def test_format_truth_table_binary():
    """Test formatting for binary connectives."""
    # Test AND connective
    formatted = format_truth_table(AND, 2)
    assert "A B | Output" in formatted
    assert "T T | T" in formatted
    # ... more assertions
```

**Step 4: Run Tests**
```
Let me run the test suite to make sure everything passes:
```

Claude will execute:
```bash
pytest tests/ -v
```

And show you the results (should be 175+ passing tests).

**Step 5: Update Documentation**
```
According to docs/CONTRIBUTING.md, we should update relevant
documentation. I'll add this feature to:
- src/README.md (API documentation)
- Docstrings in the code
```

**Step 6: Commit Changes**
```
Following the commit guidelines in docs/CONTRIBUTING.md#commit-guidelines,
I'll create a clear commit message:
```

Claude will help you commit:
```bash
git add src/connectives.py tests/test_connectives.py src/README.md
git commit -m "feat: add readable truth table formatting

Implements format_truth_table() function that displays truth tables
with proper headers and formatting. Includes comprehensive tests and
documentation updates."
```

Your feature is now ready for a pull request! See [Example 4](#example-4-submitting-a-pull-request) for the next steps.

#### Example 4: Submitting a Pull Request

After developing your feature (as shown in [Example 3](#example-3-developing-a-feature-on-a-new-branch)), Claude Code can guide you through submitting a pull request following the [Contributing Guide](CONTRIBUTING.md).

```
My feature is complete with passing tests. Can you help me submit
a pull request following the guidelines in docs/CONTRIBUTING.md?
```

**Claude will guide you through the PR process:**

**Step 1: Push Your Branch**
```
First, let's push your feature branch to your fork on GitHub:
```

Claude will run:
```bash
git push origin feature/readable-truth-tables
```

If this is your first push of this branch, Claude will use:
```bash
git push -u origin feature/readable-truth-tables
```

**Step 2: Create the Pull Request**
```
Now I'll help you create a pull request. According to
docs/CONTRIBUTING.md#submitting-a-pull-request, you need to:

1. Go to your fork on GitHub
2. You'll see a yellow banner with "Compare & pull request"
3. Click that button

Alternatively, you can use the GitHub CLI if you have it installed.
Would you like me to create the PR using the gh command?
```

If you have `gh` CLI installed, Claude can run:
```bash
gh pr create --title "Add readable truth table formatting" --body "$(cat <<'EOF'
## Summary
Adds a new `format_truth_table()` function that displays connective
truth tables in a human-readable format with proper headers and
formatting.

## Changes
- Added `format_truth_table()` function to src/connectives.py
- Added comprehensive test coverage in tests/test_connectives.py
- Updated API documentation in src/README.md

## Testing
- All 177 tests pass (175 existing + 2 new)
- Tested with binary, ternary, and edge cases
- Run: `pytest tests/test_connectives.py::test_format_truth_table* -v`

## Documentation
- Updated src/README.md with new function documentation
- Added docstrings following project standards
- Included usage examples

## Checklist
- [x] All tests pass
- [x] Code follows project style (CLAUDE.md)
- [x] Documentation updated
- [x] Commit messages are clear

Follows guidelines from docs/CONTRIBUTING.md
EOF
)"
```

**Step 3: Address Review Feedback**

Once your PR is submitted, reviewers may provide feedback. Claude Code can help:

```
I received review feedback on my PR. The reviewer suggests
simplifying the formatting logic. Can you help me address this?
```

Claude will:
1. Read the PR comments and understand the feedback
2. Make the requested changes
3. Run tests to ensure they still pass
4. Help you commit and push the updates

```bash
# Claude makes the changes, then:
git add src/connectives.py
git commit -m "refactor: simplify truth table formatting logic per review feedback"
git push origin feature/readable-truth-tables
```

The PR will automatically update with your new commits.

**Step 4: After PR is Merged**

Once your PR is merged, Claude can help clean up:

```
My PR was merged! Can you help me clean up my local repository
following the post-merge steps in docs/CONTRIBUTING.md?
```

Claude will run:
```bash
# Switch back to master
git checkout master

# Pull the merged changes
git pull upstream master

# Delete your feature branch locally
git branch -d feature/readable-truth-tables

# Delete the feature branch from your fork
git push origin --delete feature/readable-truth-tables

# Update your fork's master
git push origin master
```

```
Great! Your contribution is now part of the project. Ready to start
your next feature?
```

**Learn More:**
- Complete workflow: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
- GitHub setup: [docs/GITHUB.md](GITHUB.md)
- Commit guidelines: [docs/CONTRIBUTING.md#commit-guidelines](CONTRIBUTING.md#commit-guidelines)
- PR process: [docs/CONTRIBUTING.md#submitting-a-pull-request](CONTRIBUTING.md#submitting-a-pull-request)

#### Example 5: Running Searches

```
I want to search for a size-36 nice set. Can you help me set up
the command with appropriate parameters based on the size-35
search?
```

Claude will suggest the command with optimized parameters.

#### Example 6: Understanding Research Results

```
Can you explain the pattern in search times for sizes 31-35?
Why did size-32 search faster than size-31?
```

Claude will analyze the data in the example files and provide insights.

#### Example 7: Documentation Updates

```
The RESULTS.md file says the maximum is size 30, but we've now
found size 35. Can you update all the documentation to reflect
this?
```

Claude will:
1. Find all references to the old maximum
2. Update them consistently
3. Show you what changed

### Advanced Features

#### Using Slash Commands

Claude Code supports custom slash commands defined in `.claude/commands/`:

```bash
# List available commands
/help

# Use project-specific commands (if defined)
/test              # Run tests
/search            # Start a search
/validate          # Validate a nice set
```

#### Multi-file Operations

Claude can work with multiple files at once:

```
Can you compare the structure of z3_nice_set_30.md and
z3_nice_set_35.md? What are the key differences in the
ternary functions used?
```

#### Code Generation

```
Create a script that generates a visualization of the truth
table distribution for all ternary connectives in the size-35
nice set
```

#### Refactoring

```
The independence checking code in src/independence.py is getting
long. Can you refactor it to separate pattern enumeration from
Z3 constraint generation?
```

## Tips for Effective Use

### 1. Be Specific

**Less effective:**
```
How does this work?
```

**More effective:**
```
How does the pattern enumeration algorithm in src/independence.py
handle depth-3 compositions of ternary functions?
```

### 2. Reference Files Directly

```
In examples/z3_nice_set_35.md, can you explain why f3_2 and f3_247
appear together in the nice set?
```

### 3. Ask for Explanations Before Changes

```
Before I run a size-36 search, can you explain what the
--max-candidates parameter does and what value I should use
based on the size-35 results?
```

### 4. Request Validation

```
I added a new pattern to the independence checker. Can you
review it for correctness and test it against the known
nice sets?
```

### 5. Use Context from Previous Exchanges

Claude Code maintains conversation history, so you can build on previous questions:

```
You: What is the largest nice set found?
Claude: The largest is size 35, found in z3_nice_set_35.md...

You: Can you show me the ternary functions in that set?
Claude: Here are the 33 ternary functions from the size-35 set...

You: Which of these have truth table values over 200?
Claude: The ternary functions with values over 200 are...
```

## Project-Specific Use Cases

### Understanding Nice Sets

```
Explain what makes a connective set "nice" using examples from
the size-17 set in examples/z3_nice_set_17.md
```

### Truth Table Lookups

```
Show me the truth tables for f3_19, f3_23, and f3_26 from the
glossary and explain what they have in common
```

### Search Optimization

```
Based on the search evolution data in z3_nice_set_35.md, what
parameters should I use to search for size-36?
```

### Code Understanding

```
Walk me through how Post's completeness theorem is implemented
in src/post_classes.py
```

### Reproducibility

```
I want to reproduce the size-33 result. What exact command
should I run and how long will it take?
```

### Documentation

```
Generate a summary of all the size records from 17 to 35 in
a table format showing size, search time, and percentage
of ternary functions
```

## Working with the Glossary

The project includes a comprehensive ternary connectives glossary at `glossary/connectives.md`:

```
Look up f3_150 in the glossary and show me its truth table
```

```
Which connectives in the glossary represent three-way XOR, OR,
and AND?
```

```
Are there any special patterns in the truth tables of the
connectives used in the size-35 nice set?
```

## Troubleshooting

### Claude Code won't start

```bash
# Check if Claude Code is in your PATH
which claude

# Try reinstalling
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh

# Check authentication
claude auth status
```

### Authentication issues

```bash
# Log out and log back in
claude auth logout
claude auth login
```

### Performance issues

```bash
# Clear cache
claude cache clear

# Check for updates
claude update
```

### Python environment issues

If Claude Code has trouble running Python commands:

```bash
# Ensure Python is in PATH
which python3

# Activate virtual environment if needed
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

# Then start Claude Code
claude
```

## Additional Resources

### Interactive Learning
- **[Jupyter Notebooks](JUPYTER.md)** - Interactive tutorials and examples
- **[Notebooks Overview](../notebooks/README.md)** - Notebook learning paths

### Documentation
- **Claude Code Documentation**: https://docs.claude.com/claude-code
- **Project README**: [../README.md](../README.md)
- **Research Results**: [RESULTS.md](RESULTS.md)
- **Examples Directory**: [../examples/README.md](../examples/README.md)
- **Ternary Connectives Glossary**: [../glossary/connectives.md](../glossary/connectives.md)

## Getting Help

### Within Claude Code

```
Can you help me understand how to use Claude Code more
effectively with this codebase?
```

### Common Questions

**Q: Can Claude Code run the search commands?**
A: Yes! Claude can execute commands like `python -m src.cli prove z3 --target-size 35`

**Q: Will Claude modify files without asking?**
A: No. Claude will show you proposed changes and ask for confirmation before modifying files.

**Q: Can Claude Code work offline?**
A: No, Claude Code requires an internet connection to communicate with Claude AI.

**Q: How much does it cost?**
A: Pricing depends on your Anthropic account plan. Check https://anthropic.com/pricing for details.

## Example Session

Here's a complete example session:

```bash
# Navigate to the repository
cd ~/Documents/Philosophy/Projects/Z3/nice_connectives

# Start Claude Code
claude

# Example conversation:
```

**You:**
```
Hi! I'm new to this codebase. Can you give me an overview of what
this project does?
```

**Claude:**
```
This is the Nice Connectives project, which searches for the maximum
size of "nice" connective sets in classical logic...
[detailed explanation]
```

**You:**
```
What's the current record for the largest nice set?
```

**Claude:**
```
The current record is size 35, discovered on 2025-10-07. You can see
the details in examples/z3_nice_set_35.md...
```

**You:**
```
Can you show me one of the ternary connectives from that set with
its complete truth table?
```

**Claude:**
```
Sure! Let me show you f3_19 from that set:

[truth table displayed]

This connective is interesting because...
```

**You:**
```
Great! Now I want to run a search for size 36. What command should
I use?
```

**Claude:**
```
Based on the size-35 search, I recommend:

python -m src.cli prove z3 --target-size 36 --max-depth 3 --max-candidates 100000

Here's why: [explanation]

Would you like me to run this command?
```

---

**Happy coding with Claude Code!**
