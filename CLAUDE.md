# Nice Connectives - Z3 Project

Research project exploring the maximum size of nice (complete and independent) connective sets using Z3 SMT solver.

## Code Standards
[Used by: /implement, /refactor, /plan]

### Z3/SMT Development
- **Language**: Python with Z3-solver library (primary), SMT-LIB2 format (secondary)
- **Indentation**: 4 spaces (Python standard)
- **Line Length**: ~100 characters
- **Naming**: snake_case for variables/functions, UPPER_CASE for constants
- **Error Handling**: Try-except blocks for solver operations, check sat/unsat results

### Z3-Specific Conventions
- **Solver Management**: Create fresh solver instances per query when appropriate
- **Formula Construction**: Use Z3 Python API for programmatic generation
- **Performance**: Profile solver time, use tactics for optimization when needed

## Testing Protocols
[Used by: /test, /test-all, /implement]

### Test Discovery
- **Test Pattern**: `test_*.py`, `*_test.py`
- **Test Framework**: pytest (Python standard)
- **Test Commands**: `pytest`, `pytest -v`, `pytest tests/`

### Testing Strategy
- **Unit Tests**: Test individual connective definitions and properties
- **Solver Tests**: Verify completeness and independence checks
- **Edge Cases**: Small arities (0,1,2), boundary conditions

## Documentation Policy
[Used by: /document, /plan]

### README Requirements
- **Problem Statement**: Clear description of "nice" connective sets
- **Mathematical Background**: Definitions of completeness and independence
- **Usage Examples**: How to run Z3 queries and interpret results
- **Results**: Document findings (maximum sizes, examples of nice sets)

### Code Documentation
- **Docstrings**: For all public functions, include mathematical notation where helpful
- **Comments**: Explain Z3 constraints, especially complex formulas
- **Character Encoding**: UTF-8 (for logical symbols if needed)

## Standards Discovery
[Used by: all commands]

### Discovery Method
Commands search for CLAUDE.md starting in the current directory and walking up the directory tree. The first CLAUDE.md found is used.

### Fallback Behavior
If no CLAUDE.md is found, commands use built-in defaults appropriate for the detected project type.

## Specs Directory Protocol

All research reports, implementation plans, and summaries are stored in `specs/`:

```
specs/
├── reports/         # Research findings and analysis
├── plans/           # Implementation plans
└── summaries/       # Execution summaries
```

### Report Numbering
Files use incremental numbering: `NNN_descriptive_name.md` (e.g., `001_completeness_check.md`)

## Project Context

### Research Goal
Determine the maximum size of a nice (complete and independent) connective set for classical two-valued logic with arbitrary arity connectives.

### Known Bounds
- Upper bound: 16 (general case)
- Binary connectives only: maximum size is 3
- Unknown: sizes for ternary, quaternary, and higher arity cases

### Computational Approach
- Model connectives as truth tables
- Encode completeness and independence as Z3 constraints
- Search for maximal nice sets using SMT solving
