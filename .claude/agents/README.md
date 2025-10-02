# Agents Directory

Specialized AI agent definitions for Claude Code. Each agent is a focused assistant with specific capabilities, tool access, and expertise designed to handle particular aspects of development workflows.

## Purpose

Agents enable modular, focused assistance by providing:

- **Specialized capabilities** for specific task types
- **Restricted tool access** for safety and predictability
- **Consistent behavior** across invocations
- **Reusable expertise** that can be invoked by commands

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Command (/implement, /plan, /test, etc.)                   │
│ Orchestrates workflow and task delegation                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Agent Invocation                                            │
│ Loads agent definition and context                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Specialized Agent                                           │
├─────────────────────────────────────────────────────────────┤
│ • Focused instruction set                                   │
│ • Limited tool access                                       │
│ • Domain-specific expertise                                 │
│ • Task completion and reporting                             │
└─────────────────────────────────────────────────────────────┘
```

## Available Agents

### code-reviewer.md
**Purpose**: Analyze code for quality, standards compliance, and potential issues

**Capabilities**:
- Code quality assessment
- Standards compliance checking
- Bug detection
- Performance analysis
- Security review

**Allowed Tools**: Read, Grep, Glob, Bash

**Typical Use Cases**:
- Pre-commit code review
- Refactoring analysis
- Quality assurance checks

---

### code-writer.md
**Purpose**: Write and modify code following project standards

**Capabilities**:
- Code generation
- Feature implementation
- Bug fixes
- Refactoring
- Standards-compliant formatting

**Allowed Tools**: Read, Write, Edit, Bash, TodoWrite

**Typical Use Cases**:
- Implementing features from specs
- Fixing identified bugs
- Refactoring code sections

---

### debug-specialist.md
**Purpose**: Investigate and diagnose issues without making changes

**Capabilities**:
- Error analysis
- Log inspection
- Environment investigation
- Root cause analysis
- Diagnostic report generation

**Allowed Tools**: Read, Grep, Glob, Bash

**Typical Use Cases**:
- Troubleshooting failures
- Understanding error messages
- Investigating performance issues

---

### doc-writer.md
**Purpose**: Create and update documentation

**Capabilities**:
- README generation
- API documentation
- Usage examples
- Architecture diagrams
- Standards compliance

**Allowed Tools**: Read, Write, Edit, Grep, Glob

**Typical Use Cases**:
- Creating missing READMEs
- Updating documentation after changes
- Generating API documentation

---

### metrics-specialist.md
**Purpose**: Analyze performance metrics and generate insights

**Capabilities**:
- Metrics analysis
- Performance trend identification
- Bottleneck detection
- Optimization recommendations
- Report generation

**Allowed Tools**: Read, Grep, Bash

**Typical Use Cases**:
- Monthly performance reviews
- Identifying slow commands
- Optimization planning

---

### plan-architect.md
**Purpose**: Design implementation plans from requirements

**Capabilities**:
- Requirements analysis
- Architecture design
- Phase breakdown
- Risk assessment
- Success criteria definition

**Allowed Tools**: Read, Write, Grep, Glob

**Typical Use Cases**:
- Creating implementation plans
- Designing feature architecture
- Breaking down complex tasks

---

### research-specialist.md
**Purpose**: Conduct research and generate comprehensive reports

**Capabilities**:
- Technology investigation
- Best practices research
- Feasibility analysis
- Alternative comparison
- Report writing

**Allowed Tools**: Read, Write, Grep, Glob, WebSearch

**Typical Use Cases**:
- Technology evaluation
- Problem investigation
- Pre-implementation research

---

### test-specialist.md
**Purpose**: Run tests, analyze results, and ensure quality

**Capabilities**:
- Test execution
- Result analysis
- Failure diagnosis
- Coverage assessment
- Test improvement suggestions

**Allowed Tools**: Read, Bash, Grep, Glob

**Typical Use Cases**:
- Running test suites
- Analyzing test failures
- Validating implementations

## Agent Definition Format

Each agent is defined in a markdown file with frontmatter metadata:

```markdown
---
allowed-tools: Read, Write, Edit, Bash
description: Brief description of agent purpose
---

# Agent Name

Detailed description of agent capabilities and role.

## Core Capabilities

### Capability 1
Description and details

### Capability 2
Description and details

## Standards Compliance

How this agent follows project standards

## Typical Workflows

Common usage patterns and examples
```

### Metadata Fields

- **allowed-tools**: Comma-separated list of tools the agent can use
- **description**: One-line summary of agent purpose

## Tool Access Patterns

### Read-Only Agents
Agents that analyze without modifying:
- **Tools**: Read, Grep, Glob, Bash (read-only commands)
- **Examples**: code-reviewer, debug-specialist, metrics-specialist

### Writing Agents
Agents that create or modify content:
- **Tools**: Read, Write, Edit, Bash
- **Examples**: code-writer, doc-writer, plan-architect

### Research Agents
Agents that gather external information:
- **Tools**: Read, Write, Grep, Glob, WebSearch
- **Examples**: research-specialist

### Testing Agents
Agents that execute and analyze tests:
- **Tools**: Read, Bash, Grep, Glob
- **Examples**: test-specialist

## Agent Invocation

Agents are typically invoked by commands, not directly by users.

### From Commands
```markdown
I'll invoke the code-writer agent to implement this feature.

[Invoke code-writer with context]
```

### Context Passing
When invoking an agent, provide:
- **Task description**: What needs to be done
- **Relevant files**: Files the agent should focus on
- **Standards**: CLAUDE.md sections to follow
- **Constraints**: Any limitations or requirements

## Best Practices

### Agent Design
- **Single responsibility**: Each agent has one clear purpose
- **Minimal tool access**: Only tools necessary for the agent's role
- **Clear instructions**: Detailed capability descriptions
- **Standards awareness**: Reference CLAUDE.md sections

### Tool Selection
- **Read-only when possible**: Prefer analysis over modification
- **Bash for verification**: Allow running tests or checks
- **TodoWrite for tracking**: Enable progress visibility in multi-step tasks

### Error Handling
- **Graceful degradation**: Handle missing tools or files
- **Clear reporting**: Explain what was done and what failed
- **Non-blocking**: Don't halt workflows on non-critical failures

## Creating Custom Agents

### Step 1: Define Purpose
Identify the specific task or domain the agent will handle.

### Step 2: Determine Tools
Choose minimal tools needed for the agent's responsibilities.

### Step 3: Write Definition
Create agent markdown file with metadata and instructions.

```bash
# Create new agent
nvim .claude/agents/your-agent.md
```

### Step 4: Document Capabilities
Clearly describe what the agent can and cannot do.

### Step 5: Test
Invoke the agent from a command and verify behavior.

## Agent Communication

### Input
Agents receive:
- **Task context**: Description of what to do
- **File paths**: Relevant files to work with
- **Standards**: CLAUDE.md sections to follow
- **State**: Current project state

### Output
Agents provide:
- **Completion status**: Success or failure
- **Results**: What was created or found
- **Next steps**: Recommendations for follow-up
- **Issues**: Problems encountered

## Integration with Commands

Commands orchestrate agents to accomplish complex workflows:

```
/implement
  ├── plan-architect → Design phases
  ├── code-writer → Implement each phase
  ├── test-specialist → Verify implementation
  └── doc-writer → Update documentation

/report
  ├── research-specialist → Gather information
  └── doc-writer → Format report

/debug
  ├── debug-specialist → Investigate issue
  └── code-writer → Apply fixes (if requested)
```

## Standards Compliance

All agents follow documentation standards:

- **NO emojis** in file content
- **Unicode box-drawing** for diagrams
- **Clear, concise** language
- **Code examples** with syntax highlighting
- **CommonMark** specification

See [/home/benjamin/.config/nvim/docs/GUIDELINES.md](../../nvim/docs/GUIDELINES.md) for complete standards.

## Navigation

### Agent Definitions
- [code-reviewer.md](code-reviewer.md) - Code quality analysis
- [code-writer.md](code-writer.md) - Code implementation
- [debug-specialist.md](debug-specialist.md) - Issue investigation
- [doc-writer.md](doc-writer.md) - Documentation creation
- [metrics-specialist.md](metrics-specialist.md) - Performance analysis
- [plan-architect.md](plan-architect.md) - Implementation planning
- [research-specialist.md](research-specialist.md) - Research and reports
- [test-specialist.md](test-specialist.md) - Testing and validation

### Related
- [← Parent Directory](../README.md)
- [commands/](../commands/README.md) - Commands that use agents
- [docs/agent-integration-guide.md](../docs/agent-integration-guide.md) - Integration guide
- [docs/agent-development-guide.md](../docs/agent-development-guide.md) - Development guide

## Examples

### Invoking Code Writer
```markdown
I'll use the code-writer agent to implement the new feature.

Task: Implement user authentication module
Files: src/auth.lua
Standards: Follow CLAUDE.md code standards (2 space indent, snake_case)
```

### Invoking Research Specialist
```markdown
I'll use the research-specialist agent to investigate options.

Topic: Evaluate TTS engines (espeak-ng vs festival vs pico-tts)
Output: Research report in specs/reports/
Focus: Performance, voice quality, installation complexity
```

### Invoking Test Specialist
```markdown
I'll use the test-specialist agent to validate the changes.

Target: Run full test suite
Analyze: Any failures or regressions
Report: Coverage and quality metrics
```
