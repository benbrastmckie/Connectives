# Specs Directory

Research reports, implementation plans, and execution summaries for the Nice Connectives project.

## Directory Structure

```
specs/
├── reports/         # Research findings and analysis
├── plans/           # Implementation plans
└── summaries/       # Execution summaries
```

## Purpose

This directory contains the documentation for the research and development process:

- **reports/**: In-depth analysis, research findings, problem investigations
- **plans/**: Detailed implementation plans created with `/plan` command
- **summaries/**: Execution summaries generated after `/implement` runs

## File Naming Convention

All files use incremental numbering with descriptive names:

```
NNN_descriptive_name.md

Examples:
001_completeness_check_research.md
002_comprehensive_refactor_hybrid_z3.md
007_repository_reorganization_cli_consolidation.md
```

### Numbering Guidelines
- Start at 001 and increment sequentially
- Zero-pad to 3 digits (001, 002, ..., 999)
- Use underscores for spaces in names
- Keep names concise but descriptive

## Reports

Research reports document findings, analyze problems, and guide implementation decisions.

### Report Structure

```markdown
# Report Title

## Metadata
- Date: YYYY-MM-DD
- Type: Research | Analysis | Investigation
- Related: Links to related plans/reports

## Overview
Brief summary of the research question or problem

## Findings
Detailed analysis and results

## Recommendations
Suggested actions based on findings

## References
Links to code, documentation, external resources
```

### Example Reports
- Investigation of Z3 bugs in independence checking
- Analysis of pattern enumeration completeness
- Benchmark results for depth crossover analysis

## Plans

Implementation plans created with the `/plan` command provide detailed roadmaps for features and refactorings.

### Plan Structure

```markdown
# Implementation Plan Title

## Metadata
- Date: YYYY-MM-DD
- Feature: Brief description
- Scope: What will be changed
- Estimated Phases: N
- Standards File: Path to CLAUDE.md
- Research Reports: Links to supporting reports

## Overview
High-level description of the plan

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Design
Detailed design decisions

## Implementation Phases
### Phase 1: Title
- Tasks
- Testing
- Validation

### Phase 2: Title
...

## Dependencies
Required libraries, tools, or prior work

## Notes
Additional context and decisions
```

### Example Plans
- `002_comprehensive_refactor_hybrid_z3.md` - Pattern enumeration improvements
- `006_z3_proof_improvements_and_repo_organization.md` - Z3 integration
- `007_repository_reorganization_cli_consolidation.md` - CLI unification

## Summaries

Execution summaries document the actual implementation process and results.

### Summary Structure

```markdown
# Implementation Summary: Feature Name

## Metadata
- Plan: Link to implementation plan
- Date: YYYY-MM-DD
- Status: Complete | Partial
- Reports Used: Links to reports referenced

## Implementation Details
What was actually implemented

## Changes Made
List of files modified, created, deleted

## Test Results
Test outcomes and validation

## Deviations from Plan
Any differences from the original plan

## Lessons Learned
Insights gained during implementation
```

## Navigation Between Documents

Documents should cross-reference each other:

### In Reports
```markdown
**Related Plans**: [007_repository_reorganization](plans/007_repository_reorganization_cli_consolidation.md)
```

### In Plans
```markdown
**Research Reports**: [Z3 Bug Analysis](reports/003_z3_bug_investigation.md)
```

### In Summaries
```markdown
**Implementation Plan**: [007_repository_reorganization](plans/007_repository_reorganization_cli_consolidation.md)
**Reports Consulted**: [Pattern Coverage Report](reports/005_pattern_coverage_analysis.md)
```

## Creating New Documents

### Research Report
```bash
/report <topic or question>
```

### Implementation Plan
```bash
/plan <feature description> [report-path1] [report-path2]
```

### Update Existing Documents
```bash
/update-report <report-path> [specific-sections]
/update-plan <plan-path> [reason-for-update]
```

## Finding Documents

### List Plans
```bash
/list-plans [search-pattern]
```

### List Reports
```bash
/list-reports [search-pattern]
```

### List Summaries
```bash
/list-summaries [search-pattern]
```

## Best Practices

### Document Early
Create reports for significant research findings before starting implementation

### Plan Before Implementing
Use `/plan` for non-trivial features to ensure thorough design

### Link Documents
Always cross-reference related reports, plans, and summaries

### Update When Deviating
If implementation differs from plan, use `/update-plan` or note in summary

### Archive Obsolete Docs
Keep all historical documents; add "OBSOLETE" prefix if superseded

## Navigation

- [← Project README](../README.md)
- [Source Code](../src/README.md)
- [CLAUDE.md](../CLAUDE.md) - Project standards
