# Contributing Guide

A complete guide to contributing to the Nice Connectives project, from creating a feature branch to submitting a pull request.

---

## Table of Contents

- [Quick Overview](#quick-overview)
- [Before You Start](#before-you-start)
- [Feature Branch Workflow](#feature-branch-workflow)
- [Development Process](#development-process)
- [Testing Your Changes](#testing-your-changes)
- [Updating Documentation](#updating-documentation)
- [Commit Guidelines](#commit-guidelines)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Review Process](#code-review-process)
- [After Your PR is Merged](#after-your-pr-is-merged)
- [Troubleshooting](#troubleshooting)
- [Getting Help](#getting-help)

---

## Quick Overview

The contribution process at a glance:

1. **Fork & Clone**: Create your own copy of the repository
2. **Create Branch**: Make a feature branch for your changes
3. **Develop**: Write code following project standards
4. **Test**: Ensure all tests pass (175+ tests)
5. **Document**: Update relevant documentation
6. **Commit**: Write clear commit messages
7. **Push**: Push your branch to your fork
8. **Pull Request**: Open a PR on GitHub
9. **Review**: Respond to feedback
10. **Merge**: Maintainers merge your contribution

**Estimated time**: 30 minutes to several hours depending on contribution size.

---

## Before You Start

### Prerequisites

Before contributing, ensure you have:

- [ ] **GitHub account** - [Create one](https://github.com/signup) if needed
- [ ] **Repository fork** - See [GitHub Setup Guide](GITHUB.md) for forking instructions
- [ ] **Development environment** - Follow [Installation Guide](INSTALLATION.md)
- [ ] **Tests passing** - Verify: `pytest tests/ -v` (should show 175+ passing tests)

### Recommended Setup

**Fork the Repository** (if you haven't already):
- Follow the complete guide: [GITHUB.md](GITHUB.md)
- Quick version: Click "Fork" on the [repository page](https://github.com/benbrastmckie/Connectives)

**Clone Your Fork Locally**:
```bash
# Clone your fork (replace YOUR-USERNAME)
git clone git@github.com:YOUR-USERNAME/nice_connectives.git
cd nice_connectives

# Add upstream remote (to get updates from original)
git remote add upstream https://github.com/benbrastmckie/Connectives.git

# Verify remotes
git remote -v
# Should show:
#   origin    git@github.com:YOUR-USERNAME/nice_connectives.git (your fork)
#   upstream  https://github.com/benbrastmckie/Connectives.git (original)
```

**Install Dependencies**:
```bash
# Install Python dependencies
pip install -e .

# Or install manually if pip install -e . doesn't work
pip install pytest z3-solver

# Verify installation
pytest tests/ -v
```

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md).

### Sync Your Fork (If You've Forked Before)

Before starting new work, update your fork with latest changes:

```bash
# Fetch latest changes from original repository
git fetch upstream

# Switch to master branch
git checkout master

# Merge upstream changes
git merge upstream/master

# Push updates to your fork
git push origin master
```

---

## Feature Branch Workflow

Always create a new branch for your changes. Never commit directly to `master`.

### Creating a Branch

```bash
# Make sure you're on master and it's up to date
git checkout master
git pull upstream master

# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Verify you're on the new branch
git branch
# * feature/your-feature-name  (asterisk shows current branch)
#   master
```

### Branch Naming Conventions

Use descriptive branch names with prefixes:

**Feature additions:**
```bash
git checkout -b feature/arity-4-support
git checkout -b feature/visualization-tool
git checkout -b feature/parallel-search
```

**Bug fixes:**
```bash
git checkout -b fix/independence-check-bug
git checkout -b fix/cli-argument-parsing
git checkout -b fix/z3-timeout-handling
```

**Documentation:**
```bash
git checkout -b docs/improve-readme
git checkout -b docs/add-tutorial
git checkout -b docs/fix-installation-steps
```

**Tests:**
```bash
git checkout -b test/add-ternary-tests
git checkout -b test/improve-coverage
```

**Refactoring:**
```bash
git checkout -b refactor/simplify-search
git checkout -b refactor/extract-patterns
```

### Keeping Branches Focused

**Good practice:**
- One feature or fix per branch
- Small, focused changes (easier to review)
- Clear purpose and scope

**Example - Good branches:**
- `feature/add-quaternary-support` - Adds arity-4 connectives
- `fix/post-class-bug` - Fixes specific bug in Post's classes
- `docs/update-results` - Updates RESULTS.md with new findings

**Example - Avoid:**
- `feature/multiple-things` - Too vague, likely too large
- `fix-and-add-features` - Mixing concerns
- `updates` - Unclear purpose

---

## Development Process

Follow project coding standards and best practices.

### Project Coding Standards

The project follows standards defined in [CLAUDE.md](../CLAUDE.md):

**Python Style:**
- **Language**: Python 3.8+
- **Indentation**: 4 spaces (no tabs)
- **Line length**: ~100 characters
- **Naming conventions**:
  - Variables and functions: `snake_case`
  - Constants: `UPPER_CASE`
  - Classes: `PascalCase` (if applicable)
- **Error handling**: Use try-except blocks appropriately
- **Type hints**: Encouraged but not required

**Example:**
```python
def check_independence(connectives, max_depth=3):
    """
    Check if connectives are independent using pattern enumeration.

    Args:
        connectives: List of connective truth tables (BitVec format)
        max_depth: Maximum composition depth (default: 3)

    Returns:
        bool: True if independent, False otherwise
    """
    try:
        patterns = enumerate_patterns(connectives, depth=max_depth)
        return not has_definable_connective(patterns)
    except Exception as e:
        logger.error(f"Independence check failed: {e}")
        raise
```

### Making Changes

**Step-by-step:**

1. **Write code** following project style
2. **Add tests** for new functionality (see `tests/` directory)
3. **Run tests frequently** during development:
   ```bash
   # Run all tests
   pytest tests/ -v

   # Run specific test file
   pytest tests/test_independence.py -v

   # Run tests matching pattern
   pytest tests/ -v -k "independence"
   ```

4. **Check for issues** before committing:
   ```bash
   # Verify imports work
   python3 -c "from src import cli; print('OK')"

   # Run quick validation
   python3 -m src.cli search validate
   ```

### Code Quality Tips

**Write clear, readable code:**
- Use descriptive variable and function names
- Add comments explaining complex logic
- Include docstrings for public functions
- Break complex functions into smaller pieces

**Example:**
```python
# Good: Clear variable names and comments
def find_nice_sets(max_arity, target_size):
    """Find nice connective sets up to target size."""
    # Start with all connectives up to max arity
    all_connectives = generate_connectives(max_arity)

    # Filter to complete sets using Post's theorem
    complete_sets = filter_complete_sets(all_connectives)

    # Check independence using pattern enumeration
    for candidate in generate_candidates(complete_sets, target_size):
        if is_independent(candidate):
            return candidate

    return None

# Avoid: Unclear names and no comments
def find(a, t):
    c = gen(a)
    cs = filt(c)
    for x in gen2(cs, t):
        if check(x):
            return x
    return None
```

**Test your changes thoroughly:**
- Add tests for new features
- Ensure existing tests still pass
- Test edge cases and error conditions
- Verify performance is reasonable

---

## Testing Your Changes

Testing is crucial. All pull requests must have passing tests.

### Running the Full Test Suite

```bash
# Run all tests with verbose output
pytest tests/ -v

# Expected output (end of test run):
# ======================== 175 passed in XX.XXs =========================
```

**All 175+ tests must pass before submitting a pull request.**

### Running Specific Tests

```bash
# Test specific file
pytest tests/test_independence.py -v

# Test specific function
pytest tests/test_independence.py::test_pattern_enumeration -v

# Test using keyword match
pytest tests/ -v -k "independence"

# Test with output capture disabled (see print statements)
pytest tests/ -v -s
```

### Adding Tests for New Features

If you add new functionality, add corresponding tests:

**Test file location:**
```
tests/
├── test_connectives.py      # Truth table operations
├── test_post_classes.py     # Completeness checking
├── test_independence.py     # Independence checking
├── test_search.py           # Search algorithms
└── test_cli.py              # CLI commands
```

**Example test:**
```python
# In tests/test_independence.py

def test_new_feature():
    """Test description of what this tests."""
    # Arrange: Set up test data
    connectives = [CONSTANT_FALSE, CONSTANT_TRUE, XOR]

    # Act: Call the function being tested
    result = your_new_function(connectives)

    # Assert: Verify expected behavior
    assert result == expected_value
    assert len(result) == 3
```

### Test Commands to Know

```bash
# Quick validation (runs fast, sanity check)
python3 -m src.cli search validate

# Full test suite (comprehensive, ~30 seconds)
pytest tests/ -v

# Test with coverage report
pytest tests/ --cov=src --cov-report=html

# Stop on first failure (useful for debugging)
pytest tests/ -x

# Show test output even when passing
pytest tests/ -v -s
```

### What If Tests Fail?

**Before committing:**
1. Read the test failure message carefully
2. Run the specific failing test: `pytest tests/test_file.py::test_name -v`
3. Debug the issue in your code
4. Re-run tests until all pass

**Common test failure causes:**
- Import errors (missing dependencies)
- Logic errors in new code
- Breaking changes to existing functions
- Edge cases not handled

**Need help debugging?** See [Getting Help](#getting-help) section.

---

## Updating Documentation

Keep documentation in sync with code changes.

### What Documentation to Update

**For new features:**
- [ ] **Docstrings**: Add/update function and class docstrings
- [ ] **README.md**: Add to feature list if major feature
- [ ] **USAGE.md**: Document new CLI commands or options
- [ ] **src/README.md**: Update implementation documentation
- [ ] **Examples**: Add example outputs to `examples/` if applicable

**For bug fixes:**
- [ ] **Code comments**: Explain the fix if non-obvious
- [ ] **RESULTS.md**: Update if fix affects results
- [ ] **src/README.md**: Update if changing implementation details

**For documentation improvements:**
- [ ] Update the relevant `.md` files
- [ ] Verify all cross-references still work
- [ ] Check markdown formatting

### Documentation Standards

Follow the project documentation policy from [CLAUDE.md](../CLAUDE.md):

**Markdown files:**
- Use **CommonMark** markdown specification
- Include table of contents for long documents
- Use code blocks with language specification:
  ````markdown
  ```python
  def example():
      pass
  ```
  ````
- Cross-reference related documents
- Keep language clear and accessible

**Docstrings:**
```python
def function_name(param1, param2):
    """
    Brief description of function.

    Longer description if needed, including mathematical
    notation or algorithm details.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Example:
        >>> function_name(x, y)
        result
    """
    pass
```

### Verifying Documentation Changes

```bash
# Check markdown files parse correctly
python3 -c "import markdown; markdown.markdown(open('docs/USAGE.md').read())"

# Verify links in documentation
grep -o '\[.*\](.*\.md)' docs/*.md

# Check for broken links
for link in $(grep -oh '\[.*\](.*\.md)' docs/*.md | cut -d'(' -f2 | cut -d')' -f1); do
    [ -f "$link" ] || echo "Broken link: $link"
done
```

---

## Commit Guidelines

Write clear, descriptive commit messages.

### Commit Message Format

Use this format:

```
<type>: <brief description>

[optional longer description]

[optional reference to issue]
```

### Commit Types

**feat**: New feature
```bash
git commit -m "feat: add arity-4 connective support"
git commit -m "feat: implement parallel search algorithm"
```

**fix**: Bug fix
```bash
git commit -m "fix: correct independence check for depth 4"
git commit -m "fix: handle empty connective sets in search"
```

**docs**: Documentation changes
```bash
git commit -m "docs: update RESULTS.md with size-36 findings"
git commit -m "docs: add examples for quaternary connectives"
```

**test**: Adding or updating tests
```bash
git commit -m "test: add edge cases for Post class checking"
git commit -m "test: improve coverage for search algorithms"
```

**refactor**: Code restructuring without behavior changes
```bash
git commit -m "refactor: simplify pattern enumeration logic"
git commit -m "refactor: extract completeness checking to separate module"
```

**perf**: Performance improvements
```bash
git commit -m "perf: optimize Z3 constraint generation"
git commit -m "perf: add caching for repeated pattern checks"
```

### Commit Examples

**Good commits:**
```bash
git commit -m "feat: add quaternary connective generation

Implements generate_quaternary_connectives() function that creates
all 65536 quaternary (4-input) connectives using BitVec encoding.

Includes unit tests and documentation."

git commit -m "fix: correct Post's M class check

The monotone class check was incorrectly handling constant functions.
Updated logic to properly exclude constants from monotone detection.

Fixes #42"
```

**Avoid:**
```bash
git commit -m "updates"  # Too vague
git commit -m "fix stuff"  # Not descriptive
git commit -m "WIP"  # Don't commit work-in-progress to shared branches
```

### Committing Changes

```bash
# See what files changed
git status

# View changes in detail
git diff

# Stage specific files
git add src/connectives.py
git add tests/test_connectives.py

# Or stage all changes
git add .

# Commit with message
git commit -m "feat: add helper function for truth table display"

# Verify commit
git log -1
```

---

## Submitting a Pull Request

Once your changes are ready, submit a pull request (PR) to propose merging them.

### Step 1: Push Your Branch to Your Fork

```bash
# Push your feature branch to your fork on GitHub
git push origin feature/your-feature-name

# If this is the first push of this branch:
git push -u origin feature/your-feature-name
```

**Note**: This pushes to `origin` (your fork), not `upstream` (the original repository).

### Step 2: Create Pull Request on GitHub

1. **Go to your fork** on GitHub:
   ```
   https://github.com/YOUR-USERNAME/nice_connectives
   ```

2. **You'll see a yellow banner** saying "your-feature-name had recent pushes"
   - Click **"Compare & pull request"** button

3. **If no banner appears:**
   - Click "Pull requests" tab
   - Click green "New pull request" button
   - Click "compare across forks"
   - Set:
     - **base repository**: `benbrastmckie/Connectives` base: `master`
     - **head repository**: `YOUR-USERNAME/nice_connectives` compare: `feature/your-feature-name`
   - Click "Create pull request"

### Step 3: Write a Clear PR Description

**Title**: Brief, descriptive summary
```
Add quaternary connective support
Fix Post's M class check for constants
Update RESULTS.md with size-36 findings
```

**Description**: Explain what and why

Use this template:

```markdown
## Summary
Brief description of what this PR does.

## Changes
- List key changes made
- Bullet points for each major change
- Include affected files/components

## Testing
- Describe how you tested the changes
- List any new tests added
- Confirm all tests pass: pytest tests/ -v

## Documentation
- List documentation files updated
- Note any new examples added

## Related Issues
Fixes #42
Related to #38

## Checklist
- [ ] All tests pass (175+ tests)
- [ ] Code follows project style (CLAUDE.md)
- [ ] Documentation updated
- [ ] Commit messages are clear
```

**Example PR description:**

```markdown
## Summary
Adds support for quaternary (4-input) connectives to enable searching
for larger nice sets beyond the current maximum of 35.

## Changes
- Added `generate_quaternary_connectives()` to src/connectives.py
- Extended `search_nice_sets()` to handle arity 4
- Updated CLI to accept `--max-arity 4` option
- Added 12 new unit tests for quaternary operations

## Testing
- All 187 tests pass (175 existing + 12 new)
- Manually tested: `python -m src.cli search full --max-arity 4`
- Performance: Quaternary generation takes ~2 seconds

## Documentation
- Updated docs/USAGE.md with --max-arity 4 examples
- Added quaternary examples to examples/README.md
- Updated src/README.md implementation section

## Related Issues
Relates to #55 (exploring higher arities)

## Checklist
- [x] All tests pass
- [x] Code follows project style
- [x] Documentation updated
- [x] Commit messages are clear
```

### Step 4: Submit the PR

1. Review your PR description
2. Click **"Create pull request"**
3. Your PR is now submitted for review!

---

## Code Review Process

After submitting a PR, maintainers will review your changes.

### What to Expect

**Timeline:**
- Initial response: Usually within a few days
- Review and feedback: Depends on PR complexity
- Merge: After approval and passing checks

**Review feedback may include:**
- Suggestions for code improvements
- Questions about design decisions
- Requests for additional tests
- Documentation clarifications
- Style consistency fixes

### Responding to Feedback

**Stay positive and collaborative:**
- Reviews help improve code quality
- Questions are opportunities to explain your approach
- Suggestions often come from project experience

**How to address feedback:**

1. **Read all feedback carefully**
2. **Ask questions if unclear:**
   ```markdown
   Thanks for the review! Could you clarify what you mean by
   "simplify the pattern matching"? Should I extract it to a
   separate function or use a different algorithm?
   ```

3. **Make requested changes:**
   ```bash
   # Make the changes in your local branch
   git checkout feature/your-feature-name

   # Edit files as needed
   # ...

   # Commit changes
   git add .
   git commit -m "refactor: simplify pattern matching per review feedback"

   # Push updates to your PR
   git push origin feature/your-feature-name
   ```

4. **Respond to comments:**
   ```markdown
   Done! I've simplified the pattern matching logic and added
   a helper function as you suggested. Let me know if this looks better.
   ```

### Common Review Requests

**"Add tests for X":**
- Write tests covering the requested scenario
- Push updated tests to your branch

**"Update documentation":**
- Add or improve relevant documentation
- Push documentation updates

**"Fix style issues":**
- Adjust code to match project style
- Run tests to ensure no breakage

**"Simplify this logic":**
- Refactor the code as suggested
- Ensure tests still pass

### If Changes Are Requested

1. Make the changes locally
2. Commit with clear message (e.g., "refactor: address review feedback")
3. Push to your feature branch
4. GitHub automatically updates the PR
5. Comment on the PR when ready for re-review

---

## After Your PR is Merged

Congratulations! Your contribution is now part of the project.

### Clean Up Your Local Repository

```bash
# Switch back to master
git checkout master

# Pull the merged changes
git pull upstream master

# Delete your feature branch (local)
git branch -d feature/your-feature-name

# Delete your feature branch (remote fork)
git push origin --delete feature/your-feature-name

# Update your fork's master
git push origin master
```

### Start Your Next Contribution

```bash
# Sync with upstream
git pull upstream master

# Create new branch for next feature
git checkout -b feature/next-feature-name
```

---

## Troubleshooting

### Tests Fail Locally

**Problem**: Tests that passed before now fail.

**Solutions**:

1. **Pull latest changes:**
   ```bash
   git checkout master
   git pull upstream master
   git checkout feature/your-feature-name
   git merge master
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -e .
   ```

3. **Check specific failure:**
   ```bash
   pytest tests/test_failing_test.py -v -s
   ```

4. **Run only failing test:**
   ```bash
   pytest tests/ -x  # Stop on first failure
   ```

### Merge Conflicts

**Problem**: Git can't automatically merge your changes.

**Solution**:

```bash
# Update master
git checkout master
git pull upstream master

# Attempt merge
git checkout feature/your-feature-name
git merge master

# Git will mark conflicts in files
# Edit conflicted files, looking for:
# <<<<<<< HEAD
# your changes
# =======
# upstream changes
# >>>>>>> master

# After fixing conflicts:
git add .
git commit -m "fix: resolve merge conflicts with master"
git push origin feature/your-feature-name
```

**Tip**: Use a merge tool if available:
```bash
git mergetool
```

### Push Rejected

**Problem**: `git push` fails with "rejected" error.

**Solutions**:

1. **Pull first, then push:**
   ```bash
   git pull origin feature/your-feature-name
   git push origin feature/your-feature-name
   ```

2. **If you rewrote history (force push needed):**
   ```bash
   git push -f origin feature/your-feature-name
   ```
   **Warning**: Only force push to your own branches, never to master!

### Can't Find Your Fork

**Problem**: Don't remember if you forked the repository.

**Solution**:

Check your GitHub repositories:
```
https://github.com/YOUR-USERNAME?tab=repositories
```

Or check remotes:
```bash
git remote -v
# If origin points to benbrastmckie, you don't have a fork yet
# If origin points to YOUR-USERNAME, you have a fork
```

### PR Accidentally Created from Wrong Branch

**Problem**: Opened PR from master instead of feature branch.

**Solution**:

1. Close the incorrect PR
2. Create correct feature branch:
   ```bash
   git checkout -b feature/correct-branch-name
   git push origin feature/correct-branch-name
   ```
3. Open new PR from feature branch

---

## Getting Help

### Documentation Resources

- **[Installation Guide](INSTALLATION.md)** - Setup and dependency issues
- **[GitHub Setup](GITHUB.md)** - Fork, clone, SSH configuration
- **[Usage Guide](USAGE.md)** - CLI commands and workflows
- **[Source Code Docs](../src/README.md)** - Implementation details
- **[Main README](../README.md)** - Project overview

### AI-Powered Assistance

**[Claude Code](CLAUDE_CODE.md)** provides interactive help:

```bash
# Start Claude Code in the repository
cd nice_connectives
claude

# Example questions:
"How do I create a feature branch?"
"My tests are failing with import errors, can you help debug?"
"Can you review my changes before I submit a PR?"
"How do I resolve these merge conflicts?"
```

Claude Code can:
- Answer questions about the codebase
- Help debug errors and test failures
- Review your changes before submission
- Suggest improvements to code or documentation
- Guide you through Git workflows

### Community Support

**Open an issue** if you:
- Find a bug
- Have a question
- Want to discuss a feature idea
- Need help with contribution process

**Before opening an issue:**
1. Search existing issues (might already be reported)
2. Check documentation (might be answered)
3. Try Claude Code for quick questions

**When opening an issue, include:**
- Clear description of problem/question
- Steps to reproduce (if bug)
- Your environment (OS, Python version)
- Relevant error messages
- What you've already tried

### Quick Reference Commands

```bash
# Sync your fork with upstream
git fetch upstream && git merge upstream/master

# Create feature branch
git checkout -b feature/your-feature-name

# Check what changed
git status
git diff

# Run tests
pytest tests/ -v

# Commit changes
git add .
git commit -m "feat: description"

# Push to your fork
git push origin feature/your-feature-name

# Update PR after feedback
git add .
git commit -m "refactor: address review feedback"
git push origin feature/your-feature-name
```

---

## Areas for Contribution

Looking for ideas? Consider contributing to:

### Code Improvements
- **Performance optimizations** - Improve search algorithms
- **Higher arities** - Explore quaternary (arity 4) connectives
- **Parallel search** - Implement multi-threaded search
- **Caching** - Add memoization for repeated calculations

### Testing
- **Edge cases** - Add tests for boundary conditions
- **Coverage** - Improve test coverage percentage
- **Performance tests** - Add benchmarks for regressions

### Documentation
- **Tutorials** - Write beginner-friendly guides
- **Examples** - Add more real-world examples
- **Clarifications** - Improve unclear sections
- **Translations** - Translate documentation (if multilingual)

### Visualization
- **Result visualization** - Tools to visualize nice sets
- **Truth table display** - Better truth table formatting
- **Search progress** - Visual progress indicators

### Jupyter Notebooks
- **Interactive tutorials** - Educational content
- **Research notebooks** - Analysis and exploration
- **Visualization demos** - Visual explanations

### Infrastructure
- **CI/CD improvements** - Better automated testing
- **Build tools** - Improved development workflow
- **Performance monitoring** - Track speed improvements

**Questions about where to start?** Open an issue or ask in Claude Code!

---

**Ready to make your first contribution? Follow the [Feature Branch Workflow](#feature-branch-workflow) to get started!**
