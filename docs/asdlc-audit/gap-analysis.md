# Gap Analysis: Missing ASDLC Practices

**Document:** FB-36 Spike Deliverable (Part 2)
**Date:** 2026-01-17

---

## Overview

This document identifies ASDLC practices that are **missing** from our current command set, organized by severity and impact on ASDLC alignment.

---

## Critical Gaps (Blocking Full ASDLC Alignment)

### 1. Spec Pattern Not Implemented (Plans ≠ Specs)

**Impact**: CRITICAL - Core ASDLC artifact missing

**Current State**:
- Commands produce `.plans/` files (transient)
- Plans have "Implementation Steps" (execution-focused)
- Plans are created once, then referenced, not evolved

**ASDLC Requirement**:
- Commands should produce `specs/` files (permanent)
- Specs have "Blueprint + Contract" structure (design + verification)
- Specs are living documents that evolve with code

**Affected Commands**:
- `/create-plan` (primary producer)
- `/start-task` (consumes plans)
- `/complete-task` (references plans in PR)
- `/create-test` (should read Contract)

**Resolution**: **FB-24** (already exists) - "Restructure .plans/ to specs/ with Blueprint/Contract separation"

**Additional work needed**:
- Update `/create-plan` to output Spec format
- Update consumers to read from `specs/`
- Add Spec evolution workflow (update Spec when code changes)

---

### 2. No Review Gates (Missing 2nd Tier of Context Gates)

**Impact**: CRITICAL - Quality Control pillar incomplete

**Current State**:
- `/complete-task` implements **Quality Gates** only (lint, tests)
- Goes directly from Quality Gates → Acceptance Gate (human PR review)
- Missing probabilistic validation layer

**ASDLC Requirement**:
- Three-tier Context Gates:
  1. Quality Gates (deterministic) ✅ Implemented
  2. **Review Gates (probabilistic)** ❌ Missing
  3. Acceptance Gates (human) ✅ Implemented

**Missing Patterns**:
- **Constitutional Review**: Validate against AGENTS.md
- **Adversarial Code Review**: Critic Agent validates Spec compliance

**Resolution**: New stories needed:
- **FB-37**: "Add Constitutional Review to /complete-task"
- **FB-39**: "Implement Adversarial Code Review in /review-code"
- **FB-40**: "Add Constitutional Review to /review-code"

---

### 3. PBI Structure Not Enforced (Pointer Pattern Missing)

**Impact**: CRITICAL - Standardized Parts pillar incomplete

**Current State**:
- `/create-task` creates issues but doesn't enforce PBI structure
- Issues contain full descriptions (container model)
- No Context Pointers to Specs
- No Verification Pointers to Contract

**ASDLC Requirement**:
- PBIs should be **pointers**, not containers
- 4-part PBI anatomy:
  1. Directive (what to do)
  2. Context Pointer (link to Spec Blueprint)
  3. Verification Pointer (link to Spec Contract)
  4. Refinement Rule (handling divergence)

**Resolution**: New story needed:
- **FB-41**: "Enforce PBI structure in /create-task and /decompose-task"

---

### 4. Tests Are Code-Driven, Not Contract-Driven

**Impact**: CRITICAL - Verification not Spec-aligned

**Current State**:
- `/create-test` generates tests from code analysis
- Tests verify code behavior (implementation-focused)
- No BDD approach (no Gherkin scenarios)

**ASDLC Requirement**:
- Tests should verify **Spec Contract**, not code behavior
- Gherkin scenarios in Contract define test cases
- Tests are Contract-driven, not implementation-driven

**Resolution**: Story needed:
- **FB-38**: "Align /create-test with Spec Contract pattern"

**Dependencies**: Blocks on FB-24, FB-25 (Specs must exist with Gherkin)

---

## Major Gaps (Significant ASDLC Practices Missing)

### 5. No Ralph Loop Support (No Self-Correction)

**Impact**: HIGH - Prevents autonomous agent operation

**Current State**:
- Commands stop on first failure (lint fails, tests fail, MCP fails)
- No iteration or self-correction mechanism
- Human intervention required for every failure

**ASDLC Requirement**:
- Ralph Loop: Agent iterates until external verification passes
- Self-correction: Agent analyzes failures and retries
- Autonomous operation: Agent converges to solution without human intervention

**Missing Capabilities**:
- Iteration logic in commands
- Failure analysis and retry
- Progress tracking across iterations
- Context rotation for large tasks

**Resolution**: New epic needed:
- **"Implement Ralph Loop pattern across commands"**
- Affects: `/complete-task`, `/create-test`, potentially others

**Priority**: HIGH - Enables L3-L4 autonomy

---

### 6. No Constitutional Review Command

**Impact**: HIGH - Quality Control tier missing

**Current State**:
- Constitutional Review is manual (if done at all)
- No dedicated command for validating against AGENTS.md
- Review happens ad-hoc during human code review

**ASDLC Requirement**:
- Constitutional Review should be automated
- Validate code against AGENTS.md Operational Boundaries
- Report violations with remediation paths

**Resolution**: New command needed:
- **"Create /constitutional-review command"**
- Input: PR or branch
- Output: Constitutional violation report (PASS/FAIL)
- Integration: Called by `/complete-task` before PR creation

**Priority**: HIGH - Core ASDLC pattern

---

### 7. No Spec Evolution Workflow

**Impact**: HIGH - Living Documents not maintained

**Current State**:
- Plans are created once, not updated
- No workflow for updating Specs when code changes
- Specs (once migrated) may drift from code

**ASDLC Requirement**:
- Specs are **living documents** that evolve with code
- When implementation diverges from Spec, Spec is updated
- PBI Refinement Rule defines when to update Spec

**Resolution**: New command needed:
- **"Create /update-spec command"**
- Updates Spec when implementation changes
- Called during `/complete-task` if code changes contracts

**Priority**: MEDIUM (after FB-24 creates Specs)

---

## Minor Gaps (Nice-to-Have Improvements)

### 8. No Model Routing Guidance

**Impact**: MEDIUM - Suboptimal model selection

**Current State**:
- All commands use default Cursor model
- No guidance on when to use reasoning vs speed models
- No Builder/Critic model separation

**ASDLC Recommendation**:
- Builder tasks: Use speed models (Gemini Flash, Claude Haiku)
- Critic tasks: Use reasoning models (Gemini Deep Think, Claude Opus)
- Model routing optimizes cost vs quality

**Resolution**: Enhancement to AGENTS.md and command documentation

**Priority**: LOW

---

### 9. Limited Living Specs Practice

**Impact**: MEDIUM - Spec maintenance unclear

**Current State**:
- Plan files are created but not maintained
- No clear "when to update Spec" guidance
- No Spec versioning or evolution tracking

**ASDLC Requirement**:
- Specs evolve with every feature change
- Clear guidelines on when/how to update Specs
- Spec changes committed alongside code changes

**Resolution**: FB-26 already exists - "Create spec templates following ASDLC Living Specs pattern"

**Priority**: MEDIUM

---

### 10. No Parallel Execution Guidance (Swarm)

**Impact**: LOW - Single-agent workflows only

**Current State**:
- Commands assume single agent working sequentially
- No concurrency guidance
- No conflict resolution for parallel work

**ASDLC Potential**:
- Multiple agents working on different PBIs in parallel
- Atomic PBIs prevent merge conflicts
- Swarm execution for faster delivery

**Resolution**: Out of scope (requires orchestration layer beyond commands)

**Priority**: LOW (future enhancement)

---

## Gap Summary Table

| Gap | Severity | Current State | ASDLC Requirement | Resolution Story | Priority |
|-----|----------|---------------|-------------------|------------------|----------|
| **Plans ≠ Specs** | CRITICAL | Plans (transient) | Specs (permanent, Blueprint+Contract) | FB-24 (exists) | CRITICAL |
| **No Review Gates** | CRITICAL | Quality Gates only | 3-tier gates (Quality/Review/Acceptance) | FB-37, FB-39, FB-40 | CRITICAL |
| **PBI Structure** | CRITICAL | Issues as containers | PBIs as pointers (4-part anatomy) | FB-41 (new) | CRITICAL |
| **Code-Driven Tests** | CRITICAL | Tests from code | Tests from Contract | FB-38 (new) | HIGH |
| **No Ralph Loop** | HIGH | Stop on failure | Iterate until pass | New epic | HIGH |
| **No Constitutional Review Cmd** | HIGH | Manual/ad-hoc | Automated command | New command | HIGH |
| **No Spec Evolution** | HIGH | Plans not updated | Specs evolve | New command | MEDIUM |
| **No Model Routing** | MEDIUM | Default model | Builder/Critic models | AGENTS.md update | LOW |
| **Limited Living Specs** | MEDIUM | Create once | Evolve continuously | FB-26 (exists) | MEDIUM |
| **No Swarm Guidance** | LOW | Single agent | Parallel agents | Future work | LOW |

---

## Impact Assessment

### If We Proceed with FB-18 (Schemas) Without Addressing Gaps

**Risks**:
1. **Lock in wrong structure** - Schemas codify plan files, not Specs
2. **Incomplete Quality Control** - Schema validates command structure but not ASDLC patterns
3. **Rework needed** - After migrating to Specs, schemas need rewrite

**Benefits**:
1. **Incremental progress** - Schemas for current state better than no schemas
2. **Parallel work** - Schema work can proceed while gaps are addressed
3. **Early validation** - Schemas catch structural issues before pattern work

**Recommendation**: **GO with parallel execution**
- **FB-18**: Define schemas for **current** command structure
- **FB-24, FB-37-41**: Address critical gaps in parallel
- **Iterate schemas**: Update FB-18 schemas after pattern implementations

---

## Recommendations

See `recommendations.md` for detailed action plan and story creation.

---

**Next Document**: `recommendations.md` (actionable refinement stories)
