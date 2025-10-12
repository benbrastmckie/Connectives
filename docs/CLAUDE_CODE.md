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

#### Example 3: Making Code Changes

```
Can you add a function to src/connectives.py that converts a
ternary connective's truth table to a human-readable formula?
```

Claude will:
1. Read the existing code
2. Write the new function
3. Explain the implementation
4. Ask if you want to apply the changes

#### Example 4: Running Searches

```
I want to search for a size-36 nice set. Can you help me set up
the command with appropriate parameters based on the size-35
search?
```

Claude will suggest the command with optimized parameters.

#### Example 5: Understanding Research Results

```
Can you explain the pattern in search times for sizes 31-35?
Why did size-32 search faster than size-31?
```

Claude will analyze the data in the example files and provide insights.

#### Example 6: Documentation Updates

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
