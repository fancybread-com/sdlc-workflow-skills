# Command Audit Report: ASDLC Pattern Alignment

**Document:** FB-36 Spike Deliverable
**Date:** 2026-01-17
**Version:** 1.0
**Author:** ASDLC Alignment Initiative

---

## Executive Summary

### Overall Assessment

Our 9 homegrown Cursor commands represent a **well-structured workflow automation layer** that partially aligns with ASDLC principles. The commands successfully implement:

- **Factory Architecture**: Specialized stations for each SDLC phase
- **Phase Boundaries**: Clear Product → Planning → Development → Quality flow
- **Context Gates**: Input validation (MCP status checks) before operations

However, critical gaps exist in **artifact production** and **pattern implementation**:

| ASDLC Pillar | Current State | Gap |
|--------------|---------------|-----|
| **Factory Architecture** | ✅ 9 specialized commands | ⚠️ Missing Constitutional Review, Ralph Loop |
| **Standardized Parts** | ⚠️ Plan files (not Specs) | ❌ No schema validation, plan != Spec |
| **Quality Control** | ⚠️ Partial (Quality Gates) | ❌ Missing Review Gates, Constitutional Review |

### Key Findings

✅ **Strengths:**
1. Commands have **excellent structure** (Definitions, Prerequisites, Steps, Tools, Guidance)
2. **Intelligent validation** (information density scoring in `/create-task`, `/decompose-task`)
3. **MCP integration** is robust with comprehensive error handling
4. **Type-specific workflows** adapt behavior appropriately

❌ **Critical Gaps:**
1. **Plan files are not Specs** - `.plans/` directory produces planning documents, not ASDLC Specs (Blueprint+Contract)
2. **No Review Gates** - Missing Constitutional Review and Adversarial Code Review automation
3. **PBI pattern not fully implemented** - Commands create/consume issues but don't enforce PBI structure (Directive, Context Pointer, Verification Pointer)
4. **No Ralph Loop support** - No self-correction or iteration mechanisms

⚠️ **Moderate Gaps:**
1. `/review-code` doesn't implement Adversarial Code Review pattern (no Builder/Critic separation)
2. `/complete-task` has Quality Gates but no Review Gates before PR creation
3. Commands lack explicit Spec vs PBI distinction in documentation

### Go/No-Go Recommendation for FB-18

**Decision: GO (with modifications)**

Proceed with FB-18 (schema definition) BUT:
1. **First**: Create refinement stories for critical gaps (identified in Recommendations section)
2. **Parallel**: Begin schema work for current command structure
3. **Iterate**: Update schemas after command refinements complete

**Rationale**: Current command structure is solid enough to codify. Schemas will evolve as commands are refined. Don't block schema work completely—parallel execution accelerates alignment.

---

## Command-by-Command Analysis

### 1. `/mcp-status` - Infrastructure Validation

**Purpose & Phase**: Pre-flight validation (Context Gate: Input validation)

**SDLC Phase**: Infrastructure (supports all phases)

#### Artifact Analysis
- **Inputs**: MCP server configurations
- **Outputs**: Connection status report (transient, not persisted)
- **ASDLC Artifacts**: None (validation only)

#### Pattern Implementation
✅ **Context Gates** (Input Gate): Validates MCP connections before downstream operations
❌ **Other patterns**: Not applicable (utility command)

#### Field Manual Alignment
✅ **Aligned**: Implements pre-flight validation as recommended
✅ **Quality Control**: Prevents operations with broken integrations

#### Gaps Identified
- None significant (command fulfills its purpose well)
- Optional enhancement: Could cache connection status to reduce repeated MCP calls

#### Recommendation
**✅ KEEP AS-IS** - Well-designed validation command. No changes needed.

---

### 2. `/create-task` - Create Work Items (PBIs)

**Purpose & Phase**: Product backlog creation

**SDLC Phase**: Product (backlog management)

#### Artifact Analysis
- **Inputs**: User description, task type, optional plan file
- **Outputs**: Jira/GitHub issues (PBIs)
- **ASDLC Artifacts**: Produces **PBIs** (partially implemented)

#### Pattern Implementation
⚠️ **The PBI Pattern** (partially implemented):
- ✅ Creates transient work items (correct)
- ✅ Validates information density before creation (excellent)
- ❌ **Missing**: PBI structure enforcement (Directive, Context Pointer, Verification Pointer, Refinement Rule)
- ❌ **Missing**: PBI doesn't explicitly point to Spec as source of truth

✅ **Context Gates** (Input Gate): Intelligent information validation with 5-element scoring

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized station for PBI creation
⚠️ **Standardized Parts**: Creates issues but doesn't enforce PBI schema
✅ **Quality Control**: Information density validation prevents vague work items

#### Gaps Identified
1. **PBI Structure**: Issues created don't follow 4-part PBI anatomy:
   - Directive (what to do) ✅
   - Context Pointer (link to Spec) ❌
   - Verification Pointer (link to Contract criteria) ❌
   - Refinement Rule (what to do if reality diverges) ❌

2. **Spec References**: Created tasks don't reference Specs (because Specs don't exist yet - see `/create-plan` analysis)

3. **Epic Plan Files**: When creating epics from plan files, plans aren't structured as Specs

#### Recommendation
**⚠️ REFINE** - Add after FB-24 (Spec migration):
1. Update epic creation to produce Specs (not plans)
2. Add PBI template enforcement for story/task creation
3. Include Spec reference pointers in created issues
4. Add Verification Pointer linking to Spec's Contract section

**Priority**: Medium (after Spec infrastructure exists)

---

### 3. `/decompose-task` - Break Down Epics

**Purpose & Phase**: Product backlog decomposition

**SDLC Phase**: Product (backlog refinement)

#### Artifact Analysis
- **Inputs**: Epic/large story (PBI)
- **Outputs**: Child stories (PBIs)
- **ASDLC Artifacts**: Consumes/produces **PBIs**

#### Pattern Implementation
✅ **The PBI Pattern** (partially):
- ✅ Creates atomic, self-testable subtasks (excellent)
- ✅ Validates information density (5-element scoring)
- ✅ Ensures subtasks are appropriately sized (1-2 sprint points)
- ❌ **Missing**: Generated subtasks don't reference parent Spec

✅ **Context Gates** (Input Gate): Information density validation before decomposition

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized decomposition station
⚠️ **Standardized Parts**: Generates PBIs but doesn't enforce PBI schema
✅ **Quality Control**: Validation prevents decomposing insufficient information

#### Gaps Identified
1. **Spec Pointers**: Decomposed stories don't include Context Pointers to parent Spec
2. **Verification Pointers**: No automatic linking to Spec's Contract section
3. **Dependency Declaration**: Identifies dependencies but doesn't enforce explicit PBI dependency structure

#### Recommendation
**⚠️ REFINE** - After FB-24 (Spec migration):
1. Add Spec reference to generated child stories
2. Link Verification Pointers to parent Spec's Contract
3. Enforce explicit dependency declaration in PBI format

**Priority**: Medium

---

### 4. `/refine-task` - Backlog Refinement

**Purpose & Phase**: Product backlog refinement (Definition of Ready)

**SDLC Phase**: Product (pre-planning)

#### Artifact Analysis
- **Inputs**: Story/task (PBI)
- **Outputs**: Updated PBI with story points, refined description
- **ASDLC Artifacts**: Refines **PBIs**

#### Pattern Implementation
⚠️ **The PBI Pattern** (partially):
- ✅ Validates Definition of Ready criteria
- ✅ Uses historical data for estimation (data-driven)
- ⚠️ **Conservative refinement**: Only adds missing critical details (good instinct, but may not enforce PBI structure)
- ❌ **Missing**: Doesn't add Context Pointer to Spec

✅ **Context Gates** (Input Gate): Validates task is refinable (not Done)

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized refinement station
⚠️ **Standardized Parts**: Refines issues but doesn't enforce PBI template
✅ **Quality Control**: DoR validation ensures readiness

#### Gaps Identified
1. **User Feedback**: "Should provide intent and output required to inform the plan" - Currently focuses on estimation over planning context
2. **Spec Pointers**: Doesn't add Spec references during refinement
3. **PBI Enforcement**: Doesn't validate/enforce 4-part PBI structure

#### Recommendation
**⚠️ REFINE** - Two changes needed:
1. **Immediate** (FB-37): Adjust focus from "estimation report" to "planning readiness context"
   - Shift emphasis from story points to "What does the plan need to know?"
   - Provide intent, constraints, and context for `/create-plan`
   - Keep estimation but make it secondary

2. **Post-Spec Migration** (after FB-24): Add PBI structure enforcement
   - Validate Context Pointer exists
   - Ensure Verification Pointer links to Spec Contract
   - Add Refinement Rule for handling divergence

**Priority**: High (user feedback indicates immediate need)

---

### 5. `/create-plan` - Technical Planning

**Purpose & Phase**: Technical implementation planning

**SDLC Phase**: Planning

#### Artifact Analysis
- **Inputs**: Story/task (PBI)
- **Outputs**: Plan file (`.plans/{TASK_KEY}-*.plan.md`)
- **ASDLC Artifacts**: Should produce **Specs**, currently produces **plan files**

#### Pattern Implementation
❌ **The Spec Pattern** (NOT implemented):
- ❌ Plan files are not Specs (Blueprint+Contract structure)
- ❌ Missing Contract section with Gherkin scenarios
- ❌ Plans are transient (`.plans/`), not permanent (`specs/`)
- ❌ No separation of Blueprint (design) vs Contract (verification)

⚠️ **Partial alignment**:
- ✅ Contains "Acceptance Criteria" (similar to Contract)
- ✅ Contains "Technical Design" (similar to Blueprint)
- ✅ Contains "Implementation Steps" (execution guide)
- ❌ Structure doesn't match ASDLC Spec anatomy

✅ **Context Gates** (Input Gate): Validates story has sufficient detail

#### Field Manual Alignment
⚠️ **Factory Architecture**: Specialized planning station (correct)
❌ **Standardized Parts**: Produces plans, not Specs (misalignment)
⚠️ **Quality Control**: Plans are not verified artifacts (no Quality Gates)

#### Gaps Identified
1. **CRITICAL**: Plans are not Specs
   - Specs should be **permanent** (live with code)
   - Plans are **transient** (used then discarded)
   - Specs have **Blueprint + Contract** structure
   - Plans have "Implementation Steps" (execution-focused)

2. **No Gherkin scenarios**: Plans don't include BDD-style Contract scenarios

3. **No Living Document approach**: Plans are created once, not evolved with code

4. **File location**: `.plans/` vs `specs/` indicates different lifecycle

#### Recommendation
**🔴 REQUIRES REFACTOR** - This is the most critical misalignment:

**FB-24 already exists** for this: "Restructure .plans/ to specs/ with Blueprint/Contract separation"

**Required changes:**
1. Rename command to `/create-spec` (or keep name but change behavior)
2. Output to `specs/` directory, not `.plans/`
3. Restructure output to Blueprint + Contract format:
   - **Blueprint**: Architecture, Schemas, Anti-Patterns (design constraints)
   - **Contract**: Definition of Done, Gherkin scenarios, Regression Guardrails (verification)
4. Treat Specs as **permanent** (evolve with feature, not deleted after implementation)
5. Link PBIs to Specs via Context Pointers

**Priority**: CRITICAL - Blocks full ASDLC alignment

---

### 6. `/start-task` - Begin Development

**Purpose & Phase**: Development initiation

**SDLC Phase**: Development

#### Artifact Analysis
- **Inputs**: Plan file, PBI (story/task)
- **Outputs**: Git branch, Jira transition, work checklist
- **ASDLC Artifacts**: Consumes **plan** (should consume **Spec**)

#### Pattern Implementation
⚠️ **The Spec Pattern** (missing):
- ❌ Reads plan file, should read Spec (Blueprint for design constraints)
- ❌ Doesn't reference Spec's Contract for verification criteria

✅ **Context Gates** (Input Gate):
- ✅ Validates MCP status
- ✅ Validates plan file exists
- ✅ Validates story is in correct state

✅ **Git workflow**: Creates proper branch naming (`{type}/{TASK_KEY}`)

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized development initiation station
⚠️ **Standardized Parts**: Uses plans, not Specs
✅ **Quality Control**: Pre-flight checks prevent starting with broken state

#### Gaps Identified
1. **Spec vs Plan**: Should reference Spec (Blueprint) for architectural constraints, not plan
2. **Contract Reference**: Should reference Spec's Contract for verification criteria
3. **No Constitutional Reference**: Doesn't explicitly remind agent to follow AGENTS.md Constitution

#### Recommendation
**⚠️ REFINE** - After FB-24 (Spec migration):
1. Update to read from `specs/` directory instead of `.plans/`
2. Explicitly reference Spec's Blueprint for design constraints
3. Explicitly reference Spec's Contract for verification criteria
4. Add Constitution reminder in work checklist

**Priority**: Medium (after Spec infrastructure)

---

### 7. `/complete-task` - Finalize Development

**Purpose & Phase**: Development completion and PR creation

**SDLC Phase**: Development → Quality transition

#### Artifact Analysis
- **Inputs**: Code changes, plan file
- **Outputs**: Commit, PR, Jira transition
- **ASDLC Artifacts**: Reads **plan** (should read **Spec**)

#### Pattern Implementation
✅ **Context Gates** (Output Gate - partial):
- ✅ **Quality Gates**: Linting, tests (deterministic checks)
- ❌ **Review Gates**: NO Constitutional Review, NO Adversarial Code Review
- ⚠️ **Acceptance Gate**: Creates PR for human review (correct)

❌ **Constitutional Review**: Not implemented (critical gap)
❌ **Adversarial Code Review**: Not implemented (critical gap)

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized completion station
⚠️ **Standardized Parts**: Uses plans, not Specs
❌ **Quality Control**: Only implements 1 of 3 gate tiers (Quality Gates only)

#### Gaps Identified
1. **CRITICAL**: Missing Review Gates between Quality Gates and Acceptance Gates
   - No Constitutional Review (validate against AGENTS.md)
   - No Adversarial Code Review (Critic Agent validation against Spec)

2. **Spec vs Plan**: Reads plan for PR body, should read Spec (Contract for verification)

3. **No self-correction**: If Quality Gates fail (lint/test), command stops - no Ralph Loop iteration

#### Recommendation
**🔴 REQUIRES ENHANCEMENT** - Add Review Gates:

**New story needed: FB-37 "Add Constitutional Review to /complete-task"**
- Before PR creation, run Constitutional Review
- Validate code against AGENTS.md Operational Boundaries (3-tier system)
- If violations found, report and STOP (or iterate if Ralph Loop implemented)

**After FB-24**: Update to reference Spec Contract in PR body

**Priority**: HIGH - Critical for ASDLC Quality Control pillar

---

### 8. `/create-test` - Test Generation

**Purpose & Phase**: Quality assurance (test creation)

**SDLC Phase**: Quality

#### Artifact Analysis
- **Inputs**: Component/file to test
- **Outputs**: Test files
- **ASDLC Artifacts**: Should reference **Spec Contract**, currently standalone

#### Pattern Implementation
❌ **The Spec Pattern** (not implemented):
- ❌ Doesn't read Spec's Contract section for test scenarios
- ❌ Generates tests from code analysis, not Spec's Gherkin scenarios
- ❌ No BDD alignment (should implement Contract scenarios)

✅ **Good practices**:
- ✅ Detects test framework automatically
- ✅ Follows project conventions
- ✅ Uses AAA (Arrange-Act-Assert) pattern

#### Field Manual Alignment
✅ **Factory Architecture**: Specialized test generation station
❌ **Standardized Parts**: Generates tests without Spec Contract guidance
⚠️ **Quality Control**: Tests validate code but don't verify Spec Contract

#### Gaps Identified
1. **CRITICAL**: Tests are code-driven, not Contract-driven
   - Should read Spec's Contract section for scenarios
   - Should implement Gherkin scenarios as test cases
   - Tests verify code behavior, not Spec contracts

2. **No BDD alignment**: Doesn't follow Behavior-Driven Development pattern

3. **No Spec reference**: Generated tests don't reference which Spec Contract they verify

#### Recommendation
**🔴 REQUIRES REFACTOR** - After FB-24, FB-25:

**New story needed: FB-38 "Align /create-test with Spec Contract pattern"**
- Read Spec's Contract section for Gherkin scenarios
- Generate tests that verify Contract scenarios (BDD approach)
- Link tests to specific Contract criteria
- Support "Given-When-Then" test structure

**Priority**: HIGH - Critical for Spec-driven development

---

### 9. `/review-code` - AI Code Review

**Purpose & Phase**: Quality assurance (code review)

**SDLC Phase**: Quality (Review Gate - but not implemented correctly)

#### Artifact Analysis
- **Inputs**: PR or branch, code diff
- **Outputs**: Review report with findings
- **ASDLC Artifacts**: Should implement **Review Gate**, currently does analysis only

#### Pattern Implementation
❌ **Adversarial Code Review** (NOT implemented):
- ❌ No Builder/Critic separation (same agent does both)
- ❌ No fresh context session (no "context swap")
- ❌ No Spec compliance validation (doesn't read Spec)
- ❌ Doesn't act as Review Gate (reports findings but doesn't block)

❌ **Constitutional Review** (NOT implemented):
- ❌ Doesn't validate against AGENTS.md Constitution
- ❌ Doesn't check Operational Boundaries compliance

✅ **Good practices**:
- ✅ Categorizes findings (Critical, Major, Minor, Suggestions)
- ✅ Provides detailed analysis
- ✅ Checks security, performance, design

#### Field Manual Alignment
⚠️ **Factory Architecture**: Specialized review station (correct)
❌ **Standardized Parts**: No Spec/Constitution validation
❌ **Quality Control**: Should be Review Gate, currently just advisory analysis

#### Gaps Identified
1. **CRITICAL**: Not a true Review Gate
   - Doesn't enforce gate semantics (PASS/FAIL with blocking)
   - Provides suggestions but doesn't prevent PR merge on violations

2. **Missing Adversarial Code Review**:
   - No Builder/Critic separation
   - No fresh context session
   - No Spec compliance check

3. **Missing Constitutional Review**:
   - Doesn't validate against AGENTS.md
   - Doesn't check Operational Boundaries (3-tier system)

4. **No Spec integration**: Doesn't read Spec to validate contracts

#### Recommendation
**🔴 REQUIRES MAJOR REFACTOR** - Two new stories needed:

**FB-39: "Implement Adversarial Code Review in /review-code"**
- Add Builder/Critic role separation
- Implement fresh context session for Critic
- Read Spec and validate compliance
- Output structured violation reports (not just suggestions)
- Act as blocking Review Gate (PASS/FAIL)

**FB-40: "Add Constitutional Review to /review-code"**
- Read AGENTS.md Constitution
- Validate code against Operational Boundaries (3-tier system)
- Check for hardcoded values, missing error handling, etc.
- Report constitutional violations separately

**Priority**: CRITICAL - Core ASDLC Quality Control pattern

---

## Summary: Commands 1-9

### Commands Analyzed So Far
1. ✅ `/mcp-status` - Infrastructure validation (KEEP)
2. ⚠️ `/create-task` - Create PBIs (REFINE)
3. ⚠️ `/decompose-task` - Decompose epics (REFINE)
4. ⚠️ `/refine-task` - Refine backlog (REFINE)
5. 🔴 `/create-plan` - Create plans (REFACTOR to Spec)
6. ⚠️ `/start-task` - Begin development (REFINE)
7. 🔴 `/complete-task` - Complete work (ADD Review Gates)
8. 🔴 `/create-test` - Generate tests (REFACTOR to Contract-driven)
9. 🔴 `/review-code` - Code review (REFACTOR to Review Gate)

### Next Section
Continue to Gap Analysis...

---

*Note: This is a partial audit report. Full analysis continues in next sections.*
