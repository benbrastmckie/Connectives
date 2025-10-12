---
allowed-tools: Task, TodoWrite, Read, Write, Bash, Grep, Glob
argument-hint: <workflow-description> [--parallel] [--sequential] [--create-pr]
description: Coordinate subagents through end-to-end development workflows
command-type: primary
dependent-commands: report, plan, implement, debug, test, document, github-specialist
---

# Multi-Agent Workflow Orchestration

I'll coordinate multiple specialized subagents through a complete development workflow, from research to documentation, while preserving context and enabling intelligent parallelization.

## Workflow Analysis

Let me first analyze your workflow description to identify the natural phases and requirements.

## Shared Utilities Integration

This command uses shared utility libraries for consistent workflow management:
- **Checkpoint Management**: Uses `.claude/lib/checkpoint-utils.sh` for saving/restoring workflow state
- **Artifact Registry**: Uses `.claude/lib/artifact-utils.sh` for tracking generated artifacts (reports, plans, summaries)
- **Error Handling**: Uses `.claude/lib/error-utils.sh` for agent error recovery and fallback strategies

These utilities ensure workflow state is preserved across interruptions and agent failures are handled gracefully.

### Step 1: Parse Workflow Description

I'll extract:
- **Core Feature/Task**: What needs to be accomplished
- **Workflow Type**: Feature development, refactoring, debugging, or investigation
- **Complexity Indicators**: Keywords suggesting scope and approach
- **Parallelization Hints**: Tasks that can run concurrently

### Step 2: Identify Workflow Phases

Based on the description, I'll determine which phases are needed:

**Standard Development Workflow**:
1. **Research Phase** (Parallel): Investigate patterns, best practices, alternatives
2. **Planning Phase** (Sequential): Synthesize findings into structured plan
3. **Implementation Phase** (Adaptive): Execute plan with testing
4. **Debugging Loop** (Conditional): Fix failures if tests don't pass
5. **Documentation Phase** (Sequential): Update docs and generate summary

**Simplified Workflows** (for straightforward tasks):
- Skip research if task is well-understood
- Direct to implementation for simple fixes
- Minimal documentation for internal changes

### Step 3: Initialize Workflow State

I'll create minimal orchestrator state:

```yaml
workflow_state:
  workflow_description: "[User's request]"
  workflow_type: "feature|refactor|debug|investigation"
  current_phase: "research|planning|implementation|debugging|documentation"
  completed_phases: []
  project_name: ""  # Auto-generated from workflow description

checkpoints:
  research_complete: null
  plan_ready: null
  implementation_complete: null
  tests_passing: null
  workflow_complete: null

context_preservation:
  research_summary: ""  # Max 200 words (deprecated in favor of artifact_registry)
  plan_path: ""
  implementation_status:
    tests_passing: false
    files_modified: []
  documentation_paths: []

artifact_registry:
  # Maps artifact IDs to file paths
  # Example:
  # research_001: "specs/artifacts/auth_system/existing_patterns.md"
  # research_002: "specs/artifacts/auth_system/best_practices.md"
  # research_003: "specs/artifacts/auth_system/alternatives.md"

error_history: []
performance_metrics:
  phase_times: {}
  parallel_effectiveness: 0
```

## Phase Coordination

### Research Phase (Parallel Execution)

#### Step 1: Identify Research Topics

I'll analyze the workflow description to extract 2-4 focused research topics:

**Topic Extraction Logic**:
- **Existing Patterns**: "How is [feature/component] currently implemented?"
- **Best Practices**: "What are industry standards for [technology/approach]?"
- **Alternatives**: "What alternative approaches exist for [problem]?"
- **Technical Constraints**: "What limitations or requirements should we consider?"

**Complexity-Based Research Strategy**:
```yaml
Simple Workflows (skip research):
  - Keywords: "fix", "update", "small change"
  - Action: Skip directly to planning phase
  - Thinking Mode: None (standard processing)

Medium Workflows (focused research):
  - Keywords: "add", "improve", "refactor"
  - Topics: 2-3 focused areas
  - Example: existing patterns + best practices
  - Thinking Mode: "think" (moderate complexity)

Complex Workflows (comprehensive research):
  - Keywords: "implement", "redesign", "architecture"
  - Topics: 3-4 comprehensive areas
  - Example: patterns + practices + alternatives + constraints
  - Thinking Mode: "think hard" (high complexity)

Critical Workflows (system-wide impact):
  - Keywords: "security", "breaking change", "core refactor"
  - Topics: 4+ comprehensive areas
  - Thinking Mode: "think harder" (critical decisions)
```

#### Step 1.5: Determine Thinking Mode

Analyze workflow complexity to set appropriate thinking mode for agents:

**Complexity Indicators**:
- **Simple** (score 0-3): Direct implementation, well-known patterns, single file changes
- **Medium** (score 4-6): Multiple components, some design decisions, moderate scope
- **Complex** (score 7-9): Architecture changes, novel solutions, large scope
- **Critical** (score 10+): System-wide impact, security concerns, breaking changes

**Scoring Algorithm**:
```
score = 0
score += count_keywords(["implement", "architecture", "redesign"]) * 3
score += count_keywords(["add", "improve", "refactor"]) * 2
score += count_keywords(["security", "breaking", "core"]) * 4
score += estimated_file_count / 5
score += (research_topics_needed - 1) * 2
```

**Thinking Mode Assignment**:
- score 0-3: No special thinking mode
- score 4-6: "think"
- score 7-9: "think hard"
- score 10+: "think harder"

This thinking mode will be applied to all agent prompts in this workflow.

#### Step 2: Launch Parallel Research Agents

For each identified research topic, I'll create a focused research task and invoke agents in parallel.

See [Parallel Agent Invocation](../docs/command-patterns.md#pattern-parallel-agent-invocation) for detailed parallel execution patterns.

**Orchestrate-specific invocation**:
- Launch 2-4 research agents simultaneously (single message, multiple Task blocks)
- Each agent receives ONLY its specific research focus
- NO orchestration routing logic in prompts
- Complete task description with success criteria per agent

#### Step 3: Research Agent Prompt Template

For agent prompt structure, see [Single Agent with Behavioral Injection](../docs/command-patterns.md#pattern-single-agent-with-behavioral-injection).

**Orchestrate-specific research template**:

```markdown
**Thinking Mode**: [think|think hard|think harder] (based on workflow complexity from Step 1.5)

# Research Task: [Specific Topic]

## Context
- **Workflow**: [User's original request - 1 line summary]
- **Research Focus**: [This agent's specific investigation area]
- **Project Standards**: /home/benjamin/.config/CLAUDE.md
- **Complexity Level**: [Simple|Medium|Complex|Critical]

## Objective
Investigate [specific topic] to inform planning and implementation.

## Requirements
[Specific requirements for this research topic]

### Specs Directory Management
Check `.claude/SPECS.md` for registered specs directories, auto-detect if needed.
Include "Specs Directory" in report metadata.

## Expected Output
Concise summary (max 150 words) with:
- Existing patterns found
- Recommended approaches
- Potential challenges
- Key planning insights
```

#### Step 3.5: Generate Project Name for Artifacts

Before launching research agents, generate a project name for artifact organization:

**Project Name Generation**:
```
1. Extract key terms from workflow description
2. Remove common words (the, a, implement, add, etc.)
3. Join remaining words with underscores
4. Convert to lowercase
5. Limit to 3-4 words max

Examples:
- "Implement user authentication system" → "user_authentication"
- "Add payment processing flow" → "payment_processing"
- "Refactor session management" → "session_management"
```

Store in workflow_state.project_name for artifact path generation.

**Research Agent Monitoring**:
- **Progress Streaming**: See [Progress Marker Detection](../docs/command-patterns.md#pattern-progress-marker-detection)
- Monitor parallel agent execution
- Collect artifact IDs as agents complete

#### Step 4: Store Research as Artifacts and Create References

After each research agent completes, store outputs as artifacts.

See [Artifact Storage and Registry](../docs/command-patterns.md#pattern-artifact-storage-and-registry) for detailed artifact management patterns.

**Orchestrate-specific artifact handling**:
- Generate artifact path: `specs/artifacts/{project_name}/{artifact_name}.md`
- Register in artifact_registry with descriptive ID
- Return references (not full content) to minimize context

#### Step 5: Aggregate Artifact References (Lightweight Context)

After all parallel research agents complete, aggregate artifact references.

See [Artifact Reference List](../docs/command-patterns.md#pattern-artifact-reference-list) for reference format.

**Context Reduction Achieved**:
- **Before**: 200+ words of full research summaries passed to plan-architect
- **After**: ~50 words of artifact references + selective reading by agent
- **Reduction**: 60-80% context savings

#### Step 5: Save Research Checkpoint

See [Save Checkpoint After Phase](../docs/command-patterns.md#pattern-save-checkpoint-after-phase) for checkpoint management.

**Orchestrate-specific checkpoint data**:
```yaml
checkpoint_research_complete:
  phase_name: "research"
  outputs:
    topics_investigated: ["topic1", "topic2", "topic3"]
    parallel_agents_used: 3
    status: "success"
  next_phase: "planning"
```

#### Step 6: Artifact Registry Validation

Before proceeding to planning, validate:
- [ ] All research artifacts saved to `specs/artifacts/{project_name}/`
- [ ] Artifact registry contains all artifact IDs and paths
- [ ] Artifact reference list ≤60 words (not full content)
- [ ] Checkpoint saved successfully

**If validation fails**: Retry artifact save or escalate to user

#### Research Phase Execution Example

```markdown
User Request: "Add user authentication with email and password"

Identified Research Topics:
1. Existing auth patterns in codebase
2. Security best practices for auth (2025)
3. Framework-specific auth implementations

Parallel Agent Invocations:
[Agent 1 - Codebase] → Finds: "No existing auth, uses session management in user.lua"
[Agent 2 - Security] → Finds: "Bcrypt for passwords, JWT for sessions, 2FA recommended"
[Agent 3 - Framework] → Finds: "Lua has lua-resty-jwt, examples in nginx configs"

Synthesized Summary (180 words):
"Codebase currently has session management in nvim/lua/neotex/user.lua but no
authentication system. Industry best practices (2025) recommend bcrypt for password
hashing, JWT tokens for session management, and optional 2FA for enhanced security.

Lua ecosystem provides lua-resty-jwt for token handling. Recommended approach:
Implement authentication module following existing session management patterns,
use bcrypt for password storage, JWT for auth tokens.

Key constraints: Neovim environment may limit some libraries; focus on pure Lua
solutions. Alternative: Delegate auth to external service if complexity warrants.

Actionable insights: Build on user.lua patterns, create auth/ subdirectory, implement
login/logout/verify functions, integrate with existing session system, add migration
for user credentials table, implement password reset flow, consider rate limiting."

Checkpoint Saved: research_complete
Next Phase: planning
```

### Planning Phase (Sequential Execution)

#### Step 1: Prepare Planning Context

Extract necessary context from previous phases:

**From Research Phase** (if completed):
```yaml
research_context:
  artifacts:
    research_001: "specs/artifacts/{project_name}/existing_patterns.md"
    research_002: "specs/artifacts/{project_name}/best_practices.md"
    research_003: "specs/artifacts/{project_name}/alternatives.md"
  artifact_summary: "[50-word reference list with key findings]"
```

**From User Request**:
```yaml
user_context:
  workflow_description: "[Original request]"
  feature_name: "[Extracted feature/task name]"
  workflow_type: "feature|refactor|debug|investigation"
```

**Context Injection Strategy**:
- Provide artifact reference list (not full summaries)
- Include user's original request for context
- Reference CLAUDE.md for project standards
- Agent uses Read tool to selectively access artifacts
- NO orchestration details or phase routing logic

#### Step 2: Generate Planning Agent Prompt

```markdown
# Planning Task: Create Implementation Plan for [Feature Name]

## Context

### User Request
[Original workflow description]

### Research Artifacts
[If research phase completed, provide artifact references:]

Available Research Artifacts:
1. **research_001** - Existing Patterns
   - Path: specs/artifacts/{project_name}/existing_patterns.md
   - Focus: Current implementation analysis
   - Use Read tool to access full findings

2. **research_002** - Best Practices
   - Path: specs/artifacts/{project_name}/best_practices.md
   - Focus: Industry standards (2025)
   - Use Read tool to access recommendations

3. **research_003** - Alternative Approaches
   - Path: specs/artifacts/{project_name}/alternatives.md
   - Focus: Implementation options and trade-offs
   - Use Read tool to access detailed comparisons

**Instructions**: Read relevant artifacts selectively based on planning needs. Not all artifacts may be needed for the plan.

[If no research: "Direct implementation - no prior research artifacts"]

### Project Standards
Reference standards at: /home/benjamin/.config/CLAUDE.md

## Objective
Create a comprehensive, phased implementation plan for [feature/task] that:
- Synthesizes research findings into actionable steps
- Defines clear implementation phases with tasks
- Establishes testing strategy for each phase
- Follows project coding standards and conventions

## Requirements

### Plan Structure
Use the /plan command to generate a structured implementation plan:

```bash
/plan [feature description] [research-report-path-if-exists]
```

The plan should include:
- Metadata (date, feature, scope, standards file, research reports)
- Overview and success criteria
- Technical design decisions
- Implementation phases with specific tasks
- Testing strategy
- Documentation requirements
- Risk assessment

### Task Specificity
Each task should:
- Reference specific files to create/modify
- Include line number ranges where applicable
- Specify testing requirements
- Define validation criteria

### Context from Research
[If research completed]
Incorporate these key findings:
- [Insight 1]
- [Insight 2]
- [Insight 3]

Recommended approach: [From research synthesis]

## Expected Output

**Primary Output**: Path to generated implementation plan
- Format: `specs/plans/NNN_feature_name.md`
- Location: Most appropriate directory in project structure
- **Note**: The /plan command will automatically:
  - Read specs directory from research reports (if provided)
  - Check/register in `.claude/SPECS.md`
  - Include "Specs Directory" in plan metadata

**Secondary Output**: Brief summary of plan
- Number of phases
- Estimated complexity
- Key technical decisions

## Success Criteria
- Plan follows project standards (CLAUDE.md)
- Phases are well-defined and testable
- Tasks are specific and actionable
- Testing strategy is comprehensive
- Plan integrates research recommendations

## Error Handling
- If /plan command fails: Report error and provide manual planning guidance
- If standards unclear: Make reasonable assumptions following best practices
- If research conflicts: Document trade-offs and chosen approach
```

#### Step 3: Invoke Planning Agent

**Task Tool Invocation**:
```yaml
subagent_type: general-purpose
description: "Create implementation plan for [feature] using plan-architect protocol"
prompt: "Read and follow the behavioral guidelines from:
         /home/benjamin/.config/.claude/agents/plan-architect.md

         You are acting as a Plan Architect with the tools and constraints
         defined in that file.

         [Generated planning prompt from Step 2]"
```

**Execution Details**:
- Single agent (sequential execution)
- Full access to project files for analysis
- Can invoke /plan slash command
- Returns plan file path and summary

**Monitoring**:
- **Progress Streaming**: Watch for `PROGRESS: <message>` markers in agent output
  - Examples: `PROGRESS: Analyzing requirements...`, `PROGRESS: Designing 4 phases...`
  - Display progress updates to user in real-time
- Track planning progress
- Watch for plan file creation

#### Step 4: Extract Plan Path and Validation

**Path Extraction**:
```markdown
From planning agent output, extract:
- Plan file path: specs/plans/NNN_*.md
- Plan number: NNN
- Phase count: N phases
- Complexity estimate: Low|Medium|High
```

**Validation Checks**:
- [ ] Plan file exists and is readable
- [ ] Plan follows standard format (metadata, phases, tasks)
- [ ] Plan references research reports (if applicable)
- [ ] Plan includes testing strategy
- [ ] Tasks are specific with file references

**If validation fails**:
- Retry planning with clarifications
- If retry fails: Escalate to user with error details

#### Step 5: Save Planning Checkpoint

**Checkpoint Data**:
```yaml
checkpoint_plan_ready:
  phase_name: "planning"
  completion_time: [timestamp]
  outputs:
    plan_path: "specs/plans/NNN_feature_name.md"
    plan_number: NNN
    phase_count: N
    complexity: "Low|Medium|High"
    status: "success"
  next_phase: "implementation"
  performance:
    planning_time: "[duration in seconds]"
```

**Context Update**:
- Store ONLY plan path, not plan content
- Mark planning phase as completed
- Prepare for implementation phase

#### Step 6: Planning Phase Completion

**Output to User** (brief status):
```markdown
✓ Planning Phase Complete

Plan created: specs/plans/NNN_feature_name.md
Phases: N
Complexity: Medium
Incorporating research from: [report paths if any]

Next: Implementation Phase
```

### Implementation Phase (Adaptive Execution)

#### Step 1: Prepare Implementation Context

**From Planning Phase**:
```yaml
implementation_context:
  plan_path: "specs/plans/NNN_feature_name.md"
  plan_number: NNN
  phase_count: N
  complexity: "Low|Medium|High"
```

**Execution Strategy**:
```yaml
strategy_selection:
  if complexity == "Low":
    approach: "direct_implementation"
    parallelization: false
  elif complexity == "Medium":
    approach: "phased_implementation"
    parallelization: "within_phases"
  else:  # High complexity
    approach: "incremental_phased"
    parallelization: "aggressive"
```

#### Step 2: Generate Implementation Agent Prompt

```markdown
# Implementation Task: Execute Implementation Plan

## Context

### Implementation Plan
Plan file: [plan_path]

Read the complete plan to understand:
- All implementation phases
- Specific tasks for each phase
- Testing requirements
- Success criteria

### Project Standards
Reference standards at: /home/benjamin/.config/CLAUDE.md

## Objective
Execute the implementation plan phase by phase, ensuring:
- All tasks completed as specified
- Tests pass after each phase
- Code follows project standards
- Git commits created per phase

## Requirements

### Execution Approach
Use the /implement command to execute the plan:

```bash
/implement [plan-file-path]
```

The implementation will:
- Parse plan and identify all phases
- Execute Phase 1 tasks
- Run tests specified in Phase 1
- Create git commit for Phase 1
- Repeat for all subsequent phases
- Handle errors with automatic retry

### Phase-by-Phase Execution
For each phase:
1. Display phase name and tasks
2. Implement all tasks in phase
3. Run phase-specific tests
4. Validate all tests pass
5. Create structured git commit
6. Save checkpoint before next phase

### Testing Requirements
- Run tests after EACH phase (not just at end)
- Tests must pass before proceeding to next phase
- If tests fail: Stop and report for debugging
- Test commands specified in plan or project standards

### Error Handling
- Automatic retry for transient errors (max 3 attempts)
- If tests fail: Do not proceed to next phase
- Report test failures with detailed error messages
- Preserve all completed work even if later phase fails

## Expected Output

**Primary Output**: Implementation results
- Tests passing: true|false
- Phases completed: N/M
- Files modified: [list of changed files]
- Git commits: [list of commit hashes]

**If Tests Fail**:
- Phase where failure occurred
- Test failure details
- Error messages
- Modified files up to failure point

## Success Criteria
- All plan phases executed successfully
- All tests passing
- Code follows project standards
- Git commits created for each phase
- No merge conflicts or build errors

## Error Handling
- Timeout errors: Retry with extended timeout
- Test failures: Stop and report (do not skip)
- Tool access errors: Retry with available tools
- If persistent errors: Escalate to debugging loop
```

#### Step 3: Invoke Implementation Agent

**Task Tool Invocation**:
```yaml
subagent_type: general-purpose
description: "Execute implementation plan [plan_number] using code-writer protocol"
prompt: "Read and follow the behavioral guidelines from:
         /home/benjamin/.config/.claude/agents/code-writer.md

         You are acting as a Code Writer with the tools and constraints
         defined in that file.

         [Generated implementation prompt from Step 2]"
timeout: 600000  # 10 minutes for complex implementations
```

**Monitoring**:
- **Progress Streaming**: Watch for `PROGRESS: <message>` markers in agent output
  - Display progress updates to user in real-time
  - Examples: `PROGRESS: Implementing login function...`, `PROGRESS: Running tests...`
- Track implementation progress via agent updates
- Watch for test failure signals
- Monitor for error patterns

#### Step 4: Extract Implementation Status

**Status Extraction**:
```markdown
From implementation agent output, extract:

Success Case:
- tests_passing: true
- phases_completed: "N/N"
- files_modified: [file1.ext, file2.ext, ...]
- git_commits: [hash1, hash2, ...]
- implementation_status: "success"

Failure Case:
- tests_passing: false
- phases_completed: "M/N" (M < N)
- failed_phase: N
- error_message: "[Test failure details]"
- files_modified: [files changed before failure]
- implementation_status: "failed"
```

**Validation**:
- [ ] Implementation completed all phases OR reported specific failure
- [ ] Test status clearly indicated
- [ ] Modified files list available
- [ ] Error details provided if failed

#### Step 5: Conditional Branch - Test Status Check

```yaml
if tests_passing == true:
  next_phase: "documentation"
  save_checkpoint: "implementation_complete"
else:
  next_phase: "debugging"
  save_checkpoint: "implementation_incomplete"
  prepare_debug_context:
    - failed_phase: N
    - error_message: "[details]"
    - modified_files: [list]
    - plan_path: "[path]"
```

#### Step 6: Save Implementation Checkpoint

**Success Checkpoint**:
```yaml
checkpoint_implementation_complete:
  phase_name: "implementation"
  completion_time: [timestamp]
  outputs:
    tests_passing: true
    phases_completed: "N/N"
    files_modified: [list]
    git_commits: [list]
    status: "success"
  next_phase: "documentation"
  performance:
    implementation_time: "[duration]"
```

**Failure Checkpoint** (for debugging):
```yaml
checkpoint_implementation_incomplete:
  phase_name: "implementation"
  completion_time: [timestamp]
  outputs:
    tests_passing: false
    phases_completed: "M/N"
    failed_phase: N
    error_message: "[details]"
    files_modified: [list]
    status: "failed"
  next_phase: "debugging"
  debug_context:
    failure_details: "[error messages]"
    affected_files: [list]
    plan_reference: "[plan_path]"
```

#### Step 7: Implementation Phase Completion

**Success Output**:
```markdown
✓ Implementation Phase Complete

All phases executed: N/N
Tests passing: ✓
Files modified: M files
Git commits: N commits

Next: Documentation Phase
```

**Failure Output** (triggers debugging):
```markdown
⚠ Implementation Phase Incomplete

Phases completed: M/N
Failed at: Phase N
Tests passing: ✗

Error: [Test failure details]

Next: Debugging Loop
```

### Debugging Loop (Conditional - Only if Tests Fail)

For test failure handling patterns, see [Test Failure Handling](../docs/command-patterns.md#pattern-test-failure-handling).

This phase engages ONLY when implementation reports test failures. Maximum 3 debugging iterations before escalating to user.

#### Step 1-2: Debug Investigation

**Orchestrate-specific debugging workflow**:
- Track debug iterations (max 3)
- Each iteration invokes debug-specialist agent via `/debug` command
- Agent creates diagnostic report with fix proposals
- Store previous attempts to refine analysis

**Debug context includes**:
- Failed phase number and error messages
- Modified files from implementation
- Plan path for intended behavior
- Previous debug attempts (iterations 2-3)

#### Step 3-8: Debug Investigation, Fix Application, and Checkpoint Management

For detailed debugging workflow patterns, see [Test Failure Handling](../docs/command-patterns.md#pattern-test-failure-handling).

**Orchestrate-specific debugging execution**:

**Agent Invocation** (Step 3-5):
- Invoke debug-specialist with behavioral injection
- Extract diagnostic report path and fix proposals
- Apply fixes via code-writer agent
- Validate test results

**Decision Logic** (Step 6-7):
```yaml
if tests_passing:
  → Proceed to Documentation Phase
  → Save success checkpoint
  → Update error_history with resolution

elif iteration < 3:
  → Increment iteration counter
  → Add attempt to previous_attempts history
  → Return to Step 1 with enriched context

else:  # iteration == 3
  → Escalate to user (see User Escalation Format pattern)
  → Save escalation checkpoint
  → Pause workflow for manual intervention
```

**Checkpoint Management** (Step 8):
- Success: Save `checkpoint_tests_passing` with debug metrics
- Escalation: Save `checkpoint_escalation` with all debug report paths and attempt summaries

#### Debugging Loop Example

```markdown
Iteration 1:
- Debug: Found "undefined variable 'config' in auth.lua:42"
- Fix: Added config parameter to function signature
- Test: Still failing - "config.secret is nil"

Iteration 2:
- Debug: config.secret not initialized in test environment
- Fix: Added config initialization in test setup
- Test: Still failing - "JWT decode error"

Iteration 3:
- Debug: JWT library not available in test context
- Fix: Added jwt library mock for tests
- Test: ✓ All tests passing

Checkpoint Saved: tests_passing
Next Phase: documentation
```

### Documentation Phase (Sequential Execution)

This phase updates all relevant documentation and generates a comprehensive workflow summary.

#### Step 1: Prepare Documentation Context

**Gather All Workflow Artifacts**:
```yaml
documentation_context:
  files_modified: [list from implementation]
  plan_path: "specs/plans/NNN_*.md"
  research_reports: [list if research phase completed]
  debug_reports: [list if debugging occurred]
  test_results: "passing|fixed_after_debugging"
  workflow_description: "[Original user request]"
```

**Calculate Performance Metrics**:
```yaml
performance_summary:
  total_workflow_time: "[duration in minutes]"
  phase_breakdown:
    research: "[duration or 'skipped']"
    planning: "[duration]"
    implementation: "[duration]"
    debugging: "[duration or 'not_needed']"
    documentation: "[current phase]"

  parallelization_metrics:
    parallel_research_agents: N
    time_saved_estimate: "[% saved vs sequential]"

  error_recovery:
    total_errors: N
    auto_recovered: N
    manual_interventions: N
    recovery_success_rate: "N%"
```

#### Step 2-4: Documentation Agent Invocation and Validation

**Orchestrate-specific documentation workflow**:

**Agent Prompt Structure**:
- Workflow context: Original request, workflow type, artifacts generated
- Implementation plan path with specs directory extraction
- Files modified list and test results
- Cross-referencing requirements for bidirectional linking
- Invoke `/document` command for documentation updates

**Cross-Referencing Strategy** (orchestrate-specific):
- Add "Implementation Summary" section to plan file
- Add "Implementation Status" section to research reports
- Verify bidirectional links using Read tool
- Handle edge cases (duplicate sections, multiple summaries)

**Validation Requirements**:
- At least one documentation file updated
- Cross-references include all workflow artifacts
- No broken links
- Follows project documentation standards

#### Step 3: Invoke Documentation Agent

**Task Tool Invocation**:
```yaml
subagent_type: general-purpose
description: "Update documentation for workflow using doc-writer protocol"
prompt: "Read and follow the behavioral guidelines from:
         /home/benjamin/.config/.claude/agents/doc-writer.md

         You are acting as a Doc Writer with the tools and constraints
         defined in that file.

         [Generated documentation prompt from Step 2]"
```

**Monitoring**:
- **Progress Streaming**: Watch for `PROGRESS: <message>` markers in agent output
  - Display progress updates to user in real-time
  - Examples: `PROGRESS: Updating README.md...`, `PROGRESS: Adding cross-references...`
- Track documentation updates
- Verify cross-referencing
- Watch for completion signal

#### Step 4: Extract Documentation Results

**Results Extraction**:
```markdown
From documentation agent output, extract:
- updated_files: [list of documentation files modified]
- readme_updates: [list of README files updated]
- spec_updates: [list of spec files updated]
- cross_references_added: N
- documentation_complete: true|false
```

**Validation**:
- [ ] At least one documentation file updated
- [ ] Cross-references include all workflow artifacts
- [ ] Documentation follows project standards
- [ ] No broken links or invalid references

#### Step 5: Generate Workflow Summary

**Summary File Creation**:

**Location Determination**:
```yaml
summary_location:
  directory: "same as plan (specs/summaries/)"
  filename: "NNN_workflow_summary.md"
  number: "matches plan number"
```

**Summary Template**:
```markdown
# Workflow Summary: [Feature/Task Name]

## Metadata
- **Date Completed**: [YYYY-MM-DD]
- **Specs Directory**: [path/to/specs/] (from plan metadata)
- **Summary Number**: [NNN] (matches plan number)
- **Workflow Type**: [feature|refactor|debug|investigation]
- **Original Request**: [User's workflow description]
- **Total Duration**: [HH:MM:SS]

## Workflow Execution

### Phases Completed
- [x] Research (parallel) - [duration or "Skipped"]
- [x] Planning (sequential) - [duration]
- [x] Implementation (adaptive) - [duration]
- [x] Debugging (conditional) - [duration or "Not needed"]
- [x] Documentation (sequential) - [duration]

### Artifacts Generated

**Research Reports**:
[If research phase completed]
- [Report 1: path - brief description]
- [Report 2: path - brief description]

**Implementation Plan**:
- Path: [plan_path]
- Phases: N
- Complexity: [Low|Medium|High]
- Link: [relative link to plan file]

**Debug Reports**:
[If debugging occurred]
- [Debug report 1: path - issue addressed]

## Implementation Overview

### Key Changes
**Files Created**:
- [new_file_1.ext] - [brief purpose]
- [new_file_2.ext] - [brief purpose]

**Files Modified**:
- [modified_file_1.ext] - [changes made]
- [modified_file_2.ext] - [changes made]

**Files Deleted**:
- [deleted_file.ext] - [reason for deletion]

### Technical Decisions
[Key architectural or technical decisions made during workflow]
- Decision 1: [what and why]
- Decision 2: [what and why]

## Test Results

**Final Status**: ✓ All tests passing

[If debugging occurred]
**Debugging Summary**:
- Iterations required: N
- Issues resolved:
  1. [Issue 1 and fix]
  2. [Issue 2 and fix]

## Performance Metrics

### Workflow Efficiency
- Total workflow time: [HH:MM:SS]
- Estimated manual time: [HH:MM:SS]
- Time saved: [N%]

### Phase Breakdown
| Phase | Duration | Status |
|-------|----------|--------|
| Research | [time] | [Completed/Skipped] |
| Planning | [time] | Completed |
| Implementation | [time] | Completed |
| Debugging | [time] | [Completed/Not needed] |
| Documentation | [time] | Completed |

### Parallelization Effectiveness
- Research agents used: N
- Parallel vs sequential time: [N% faster]

### Error Recovery
- Total errors encountered: N
- Automatically recovered: N
- Manual interventions: N
- Recovery success rate: [N%]

## Cross-References

### Research Phase
[If applicable]
This workflow incorporated findings from:
- [Report 1 path and title]
- [Report 2 path and title]

### Planning Phase
Implementation followed the plan at:
- [Plan path and title]

### Related Documentation
Documentation updated includes:
- [Doc 1 path]
- [Doc 2 path]

## Lessons Learned

### What Worked Well
- [Success 1]
- [Success 2]

### Challenges Encountered
- [Challenge 1 and how it was resolved]
- [Challenge 2 and how it was resolved]

### Recommendations for Future
- [Recommendation 1]
- [Recommendation 2]

## Notes

[Any additional context, caveats, or important information about this workflow]

---

*Workflow orchestrated using /orchestrate command*
*For questions or issues, refer to the implementation plan and research reports linked above.*
```

#### Step 6: Create Summary File

**File Creation**:
```yaml
action: create_summary_file
location: "[plan_directory]/specs/summaries/NNN_workflow_summary.md"
content: "[Generated from template above]"
cross_references:
  - update_plan: add_summary_reference
  - update_reports: add_summary_reference
```

**Cross-Reference Updates**:
```markdown
Update related files to link back to summary:

In Implementation Plan (specs/plans/NNN_*.md):
Add at bottom:
## Implementation Summary
This plan was executed on [date]. See workflow summary:
- [Summary path and link]

In Research Reports (if any):
Add in relevant section:
### Implementation Reference
Findings from this report were incorporated into:
- [Plan path] - Implementation plan
- [Summary path] - Workflow execution summary
```

#### Step 7: Save Final Checkpoint

**Workflow Complete Checkpoint**:
```yaml
checkpoint_workflow_complete:
  phase_name: "documentation"
  completion_time: [timestamp]
  outputs:
    documentation_updated: [list of files]
    summary_created: "specs/summaries/NNN_*.md"
    cross_references: [count]
    status: "success"
  next_phase: "complete"

  final_metrics:
    total_workflow_time: "[duration]"
    phases_completed: [list]
    artifacts_generated: [count]
    files_modified: [count]
    error_recovery_success: "[%]"

  workflow_summary:
    research_reports: [list]
    implementation_plan: "[path]"
    workflow_summary: "[path]"
    tests_passing: true
```

#### Step 8: Create Pull Request (Optional)

**When to Create PR:**
- If `--create-pr` flag is provided, OR
- If project CLAUDE.md has GitHub Integration configured with auto-PR for branch pattern

**Prerequisites Check:**
Before invoking github-specialist agent:
```bash
# Check if gh CLI is available and authenticated
if ! command -v gh &>/dev/null; then
  echo "Note: gh CLI not installed. Skipping PR creation."
  echo "Install: brew install gh (or equivalent)"
  exit 0
fi

if ! gh auth status &>/dev/null; then
  echo "Note: gh CLI not authenticated. Skipping PR creation."
  echo "Run: gh auth login"
  exit 0
fi
```

**Invoke github-specialist Agent:**

Use Task tool with behavioral injection:

```yaml
Task {
  subagent_type: "general-purpose"
  description: "Create PR for completed workflow using github-specialist protocol"
  prompt: |
    Read and follow the behavioral guidelines from:
    /home/benjamin/.config/.claude/agents/github-specialist.md

    You are acting as a GitHub Specialist Agent with the tools and constraints
    defined in that file.

    Create Pull Request for Workflow:
    - Plan: [absolute path to implementation plan]
    - Branch: [current branch name from git]
    - Base: main (or master, detect from repo)
    - Summary: [absolute path to workflow summary]

    PR Description Should Include:
    - Workflow overview from summary file
    - Research phase: N reports generated with key findings
    - Implementation: All N phases completed successfully
    - Test results: All passing (or fixed after M debug iterations)
    - Documentation: N files updated
    - Performance metrics: Time saved via parallelization
    - File changes summary from git diff --stat

    Follow comprehensive PR template structure from github-specialist agent.
    This is a workflow PR, so include cross-references to all artifacts:
    - Research reports (if any)
    - Implementation plan
    - Workflow summary
    - Debug reports (if debugging occurred)

    Output: PR URL and number for user
}
```

**Capture PR URL:**
After agent completes:
- Extract PR URL from agent output
- Update workflow summary with PR link
- Update plan file Implementation Summary section with PR link

**Example Update to Summary:**
```markdown
## Pull Request
- **PR**: https://github.com/user/repo/pull/123
- **Created**: [YYYY-MM-DD]
- **Status**: Open
```

**Graceful Degradation:**
If PR creation fails:
- Log the error from agent
- Provide manual gh pr create command
- Continue without blocking (workflow is complete)
- Summary file still valid without PR link

**Example Manual Command:**
```bash
gh pr create \
  --title "feat: [feature name from workflow]" \
  --body "$(cat pr_description.txt)" \
  --base main
```

#### Step 9: Workflow Completion Message

**Final Output to User**:
```markdown
✅ Workflow Complete

**Duration**: [HH:MM:SS]

**Artifacts Generated**:
[If research]
- Research reports: N ([paths])
- Implementation plan: [path]
- Workflow summary: [path]
- Documentation updates: N files
[If PR created]
- Pull Request: [PR URL]

**Implementation Results**:
- Files modified: N
- Tests: ✓ All passing
[If debugging occurred]
- Issues resolved: N (after M debug iterations)

**Performance**:
- Time saved via parallelization: [N%]
- Error recovery: [N/M errors auto-recovered]

**Summary**: [summary_path]

Review the workflow summary for complete details, cross-references, and lessons learned.
```

#### Documentation Phase Example

```markdown
User Request: "Add user authentication with email and password"

Workflow Phases Completed:
✓ Research (3 parallel agents, 5min)
✓ Planning (created specs/plans/013_auth_implementation.md, 3min)
✓ Implementation (4 phases, all tests passing, 25min)
✓ Documentation (updated 3 files, created summary, 4min)

Total Duration: 37 minutes

Documentation Updated:
- nvim/README.md (added auth section)
- nvim/docs/ARCHITECTURE.md (added auth module diagram)
- nvim/lua/neotex/auth/README.md (created)

Workflow Summary Created:
- specs/summaries/013_auth_workflow_summary.md
- Cross-referenced: 2 research reports, 1 plan, 3 updated docs

Performance Metrics:
- Parallel research saved ~8 minutes (estimated)
- Zero errors, no debugging needed
- All cross-references verified

Checkpoint Saved: workflow_complete
Status: ✅ Success
```

## Context Management Strategy

### Orchestrator Context (Minimal - <30% usage)

I maintain only:
- Current workflow state (phase, completion status)
- Checkpoint data (success/failure per phase)
- High-level summaries (research: 200 words max)
- File paths (not content): plan path, modified files, doc paths
- Error history: what failed, what recovery action taken
- Performance metrics: phase times, parallel effectiveness

### Subagent Context (Comprehensive)

Each subagent receives:
- Complete task description with clear objective
- Necessary context from prior phases (summaries only)
- Project standards reference (CLAUDE.md)
- Explicit success criteria
- Expected output format
- Error handling guidance

**No routing logic or orchestration details passed to subagents.**

### Context Passing Protocol

```markdown
For each subagent invocation:
1. Extract minimal necessary context from prior phases
2. Structure as focused task description
3. Remove all orchestration routing logic
4. Include explicit success criteria
5. Specify exact output format
```

## Error Recovery Mechanism

### Error Classification

**Error Types**:
1. **Timeout Errors**: Agent execution exceeds time limits
2. **Tool Access Errors**: Permission or availability issues
3. **Validation Failures**: Output doesn't meet criteria
4. **Test Failures**: Code tests fail (handled by Debugging Loop)
5. **Integration Errors**: Command invocation failures
6. **Context Overflow**: Orchestrator context approaches limits

### Automatic Recovery Strategies

See [Error Recovery Patterns](../docs/command-patterns.md#error-recovery-patterns) for detailed recovery strategies including:
- Automatic Retry with Backoff
- Error Classification and Routing (timeout, tool access, validation, integration)
- User Escalation Format

**Orchestrate-specific recovery**:
- Context Overflow Prevention: Compress context, summarize aggressively, reduce workflow scope
- Checkpoint-based recovery: Rollback to last successful phase
- Error history tracking: Learn from failures to improve future workflows

### Checkpoint Recovery System

See [Checkpoint Management Patterns](../docs/command-patterns.md#checkpoint-management-patterns) for checkpoint creation and restoration.

**Orchestrate-specific checkpoints**:
- Stored in orchestrator memory (minimal, ephemeral)
- Used for in-session recovery only
- Enable rollback to previous successful phase
- Preserve partial work on failures

### Manual Intervention Points

#### When to Escalate

**Automatic Escalation Triggers**:
1. **Max retries exceeded** (3 attempts for most error types)
2. **Critical failures** (data loss, security issues)
3. **Debugging loop limit** (3 debugging iterations)
4. **Context overflow** (cannot compress further)
5. **Architectural decisions** (user input required)

#### Escalation Format

See [User Escalation Format](../docs/command-patterns.md#pattern-user-escalation-format) for standard escalation message structure.

**User Options**:
- `continue`: Resume with manual fixes
- `retry [phase]`: Retry specific phase
- `rollback [phase]`: Return to checkpoint
- `terminate`: End workflow gracefully
- `debug`: Enter manual debugging mode

## Performance Monitoring

### Metrics Collection

Track throughout workflow:
- **Phase Execution Times**: Time per phase
- **Parallelization Effectiveness**: Actual vs potential time savings
- **Error Rates**: Failures per phase
- **Context Window Utilization**: Orchestrator context usage
- **Recovery Success**: Automatic vs manual interventions

### Optimization Recommendations

After workflow completion, suggest:
- Which phases could benefit from parallelization
- Bottleneck phases for optimization
- Checkpoint placement improvements
- Context management refinements

## Execution Flow

### Initial Workflow Processing

When invoked with `<workflow-description>`:

1. **Parse and Classify**:
   - Extract feature/task description
   - Determine workflow type
   - Identify complexity level
   - Check for parallel/sequential flags

2. **Initialize TodoWrite**:
   ```markdown
   Create todo list with identified phases:
   - [ ] Research phase (if needed)
   - [ ] Planning phase
   - [ ] Implementation phase
   - [ ] Debugging loop (conditional)
   - [ ] Documentation phase
   ```

3. **Execute Phases Sequentially**:
   - Research (parallel subagents) → synthesize
   - Planning (single subagent) → extract plan path
   - Implementation (single subagent) → check tests
   - Debugging (conditional loop) → ensure tests pass
   - Documentation (single subagent) → generate summary

4. **Update TodoWrite** after each phase completion

5. **Generate Final Summary**:
   - Workflow completion report
   - Performance metrics
   - Cross-references to all generated documents

## Usage Examples

### Example 1: Feature Development
```
/orchestrate Add user authentication with email and password
```
Expected flow:
- Research: auth patterns, security best practices
- Planning: structured multi-phase plan
- Implementation: backend + frontend + tests
- Documentation: API docs, user guide

### Example 2: Bug Investigation and Fix
```
/orchestrate Fix the command picker synchronization issue
```
Expected flow:
- Research: analyze current implementation, find issue
- Planning: fix strategy with validation
- Implementation: apply fix
- Debugging: ensure tests pass
- Documentation: issue report and fix notes

### Example 3: Refactoring
```
/orchestrate Refactor the specs directory structure for better organization
```
Expected flow:
- Research: current structure, best practices
- Planning: incremental refactoring approach
- Implementation: gradual restructuring with tests
- Documentation: architectural updates

## Notes

### Architecture Principles

**Supervisor Pattern** (LangChain 2025):
- Centralized coordination with minimal state
- Specialized subagents with focused tasks
- Context isolation prevents cross-contamination
- Forward message pattern avoids paraphrasing errors

**Context Preservation**:
- Orchestrator: <30% context usage (state, checkpoints, summaries only)
- Subagents: Comprehensive context for their specific task
- No routing logic passed to workers
- Structured handoffs with explicit success criteria

**Error Recovery**:
- Multi-level detection (timeout, tool access, validation)
- Automatic retry with adjusted parameters
- Checkpoint-based rollback and resume
- Graceful degradation to sequential execution

### When to Use /orchestrate

**Use /orchestrate for**:
- Complex multi-phase workflows (≥3 phases)
- Features requiring research + planning + implementation
- Tasks benefiting from parallel execution
- Workflows needing systematic error recovery

**Use individual commands for**:
- Simple single-phase tasks
- Direct implementation without planning
- Quick documentation updates
- Straightforward bug fixes

### Implementation Status

**Full implementation complete!** All phases have been implemented:

- [x] Phase 1: Foundation and Command Structure
- [x] Phase 2: Research Phase Coordination
- [x] Phase 3: Planning and Implementation Phase Integration
- [x] Phase 4: Error Recovery and Debugging Loop
- [x] Phase 5: Documentation Phase and Workflow Completion

The /orchestrate command provides comprehensive multi-agent workflow coordination with:
- Parallel research execution with context minimization
- Seamless integration with /plan, /implement, /debug, /document commands
- Robust error recovery with automatic retry strategies
- Intelligent debugging loop with 3-iteration limit
- Complete documentation generation with cross-referencing
- Checkpoint-based recovery system
- Performance metrics tracking

Ready to orchestrate end-to-end development workflows!

## Agent Usage

This command uses specialized agents for each workflow phase:

### Research Phase
- **Agent**: `research-specialist` (multiple instances in parallel)
- **Purpose**: Codebase analysis, best practices research, alternative approaches
- **Tools**: Read, Grep, Glob, WebSearch, WebFetch
- **Invocation**: 2-4 parallel agents depending on workflow complexity

### Planning Phase
- **Agent**: `plan-architect`
- **Purpose**: Generate structured implementation plans from research findings
- **Tools**: Read, Write, Grep, Glob, WebSearch
- **Invocation**: Single agent, sequential execution

### Implementation Phase
- **Agent**: `code-writer`
- **Purpose**: Execute implementation plans phase by phase with testing
- **Tools**: Read, Write, Edit, Bash, TodoWrite
- **Invocation**: Single agent with extended timeout for complex implementations

### Debugging Loop (Conditional)
- **Investigation**: `debug-specialist`
  - Purpose: Root cause analysis and diagnostic reporting
  - Tools: Read, Bash, Grep, Glob, WebSearch
- **Fix Application**: `code-writer`
  - Purpose: Apply proposed fixes from debug reports
  - Tools: Read, Write, Edit, Bash, TodoWrite
- **Invocation**: Up to 3 debugging iterations before escalation

### Documentation Phase
- **Agent**: `doc-writer`
- **Purpose**: Update documentation and generate workflow summaries
- **Tools**: Read, Write, Edit, Grep, Glob
- **Invocation**: Single agent, sequential execution

### Agent Integration Benefits
- **Specialized Expertise**: Each agent optimized for its specific task
- **Tool Restrictions**: Security through limited tool access per agent
- **Parallel Execution**: Research-specialist agents run concurrently
- **Context Isolation**: Agents receive only relevant context for their phase
- **Clear Responsibilities**: No ambiguity about which agent handles what

## Checkpoint Detection and Resume

Before starting the workflow, I'll check for existing checkpoints that might indicate an interrupted workflow.

### Step 1: Check for Existing Checkpoint

```bash
# Load most recent orchestrate checkpoint
CHECKPOINT=$(.claude/lib/load-checkpoint.sh orchestrate 2>/dev/null || echo "")
```

### Step 2: Interactive Resume Prompt (if checkpoint found)

If a checkpoint exists, I'll present interactive options:

```
Found existing checkpoint for orchestrate workflow
Project: [project_name]
Created: [created_at] ([age] ago)
Progress: Phase [current_phase] of [total_phases] completed
Status: [status]

Options:
  (r)esume - Continue from Phase [current_phase + 1]
  (s)tart fresh - Delete checkpoint and restart workflow
  (v)iew details - Show checkpoint contents
  (d)elete - Remove checkpoint without starting

Choice [r/s/v/d]:
```

### Step 3: Resume Workflow State (if user chooses resume)

If user selects resume:
1. Load `workflow_state` from checkpoint
2. Restore `project_name`, `artifact_registry`, `completed_phases`
3. Skip to next incomplete phase
4. Continue workflow from that point

### Step 4: Save Checkpoints at Key Milestones

Throughout workflow execution, save checkpoints after each major phase:

```bash
# After research phase
.claude/lib/save-checkpoint.sh orchestrate "$PROJECT_NAME" "$WORKFLOW_STATE_JSON"

# After planning phase
.claude/lib/save-checkpoint.sh orchestrate "$PROJECT_NAME" "$UPDATED_STATE_JSON"

# After implementation phase
.claude/lib/save-checkpoint.sh orchestrate "$PROJECT_NAME" "$UPDATED_STATE_JSON"

# After debugging (if needed)
.claude/lib/save-checkpoint.sh orchestrate "$PROJECT_NAME" "$UPDATED_STATE_JSON"
```

### Step 5: Cleanup on Completion

On successful workflow completion:
```bash
# Delete checkpoint file
rm .claude/data/checkpoints/orchestrate_${PROJECT_NAME}_*.json
```

On workflow failure:
```bash
# Archive checkpoint to failed/ directory
mv .claude/data/checkpoints/orchestrate_${PROJECT_NAME}_*.json .claude/data/checkpoints/failed/
```

Let me begin orchestrating your workflow based on the description provided.
