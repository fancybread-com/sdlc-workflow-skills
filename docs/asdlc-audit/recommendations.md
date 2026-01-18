# Recommendations: ASDLC Alignment Action Plan

**Document:** FB-36 Spike Deliverable (Part 3)
**Date:** 2026-01-17

---

## Go/No-Go Decision for FB-18

**DECISION: ✅ GO (with parallel execution strategy)**

### Rationale

**Proceed with FB-18 (schema definition)** BUT execute in **parallel** with critical gap resolution:

**Why GO**:
1. Current command structure is well-designed enough to codify
2. Schemas can evolve iteratively as commands are refined
3. Schema work validates current structure and catches structural issues
4. Blocking schema work completely delays ASDLC alignment unnecessarily

**Why PARALLEL**:
1. Critical gaps (Specs, Review Gates) require immediate attention
2. Some gaps block others (FB-24 blocks FB-38, FB-41)
3. Parallel execution accelerates alignment timeline
4. Schemas and pattern work inform each other (positive feedback)

### Execution Strategy

**Track 1: Schema Work** (FB-18-20)
- FB-18: Define command structure schemas ← Proceed
- FB-19: Add schema validation script ← Proceed
- FB-20: Implement CI/CD validation ← Proceed
- Note: Schemas will be updated after command refinements

**Track 2: Critical Gaps** (FB-24, FB-37-41)
- FB-24: Restructure to Specs ← HIGHEST PRIORITY
- FB-37: Add Constitutional Review to /complete-task ← HIGH
- FB-38: Align /create-test with Contract ← HIGH
- FB-39: Implement Adversarial Code Review ← HIGH
- FB-40: Add Constitutional Review to /review-code ← HIGH
- FB-41: Enforce PBI structure ← MEDIUM

**Track 3: Moderate Gaps** (FB-25-29)
- Continue as planned after critical gaps resolved

---

## Required Refinement Stories

### Immediate Priority (Phase 1, Before Schema Lock)

#### FB-37: Refactor /refine-task to Focus on Planning Context

**User Story**:
> As a developer, I want `/refine-task` to provide planning-ready context, so that `/create-plan` has the information it needs to design a solution.

**Context**:
- User feedback: "Should provide intent and output required to inform the plan"
- Current implementation focuses on story point estimation
- `/create-plan` needs intent, constraints, and context (not just points)

**Acceptance Criteria**:
1. `/refine-task` output emphasizes planning context over estimation
2. Output includes: intent, constraints, dependencies, technical context
3. Story points estimation becomes secondary (still present, not primary)
4. Refinement report structured for `/create-plan` consumption
5. Updated command documentation reflects new focus

**Recommendation**: **START IMMEDIATELY** - User has already flagged this

**Dependencies**: None

**Effort**: 2 points

---

#### FB-24: Restructure .plans/ to specs/ with Blueprint/Contract Separation

**Status**: Already exists in backlog

**Enhancement**: Based on audit findings:
1. Add explicit Blueprint + Contract section structure
2. Add Gherkin scenario templates for Contract section
3. Update all command documentation (create-plan, start-task, complete-task)
4. Migrate existing `.plans/` files to `specs/` (or create migration guide)
5. Add AGENTS.md reference to Spec location and structure

**Recommendation**: **HIGHEST PRIORITY** - Blocks multiple other stories

**Dependencies**: None

**Effort**: 5-8 points (major refactor)

---

### High Priority (Phase 1, Quality Control)

#### FB-37-NEW: Add Constitutional Review to /complete-task

**User Story**:
> As a developer, I want automatic Constitutional Review before PR creation, so that code violations are caught before human review.

**Context**:
- `/complete-task` currently runs Quality Gates only (lint, tests)
- Missing Review Gate between Quality and Acceptance
- ASDLC requires Constitutional Review as Review Gate

**Acceptance Criteria**:
1. Before PR creation, `/complete-task` runs Constitutional Review
2. Reads AGENTS.md Operational Boundaries (3-tier system)
3. Validates code against Constitution using Critic Agent approach
4. Reports violations with remediation paths
5. Blocks PR creation if CRITICAL violations found (Tier 3: NEVER)
6. Warns for violations in Tier 2 (ASK) and Tier 1 (ALWAYS)
7. Adds Constitutional Review report to PR description

**Technical Notes**:
- Implement as fresh context session (Critic Agent)
- Feed AGENTS.md + code diff to Critic
- Use structured violation report format (per Constitutional Review pattern)

**Dependencies**: AGENTS.md (FB-17) ✅ Complete

**Effort**: 5 points

---

#### FB-38: Align /create-test with Spec Contract Pattern

**User Story**:
> As a developer, I want tests generated from Spec Contract scenarios, so that tests verify spec compliance (not just code behavior).

**Context**:
- Currently tests are generated from code analysis
- ASDLC requires tests to verify Spec's Contract section
- BDD approach: Gherkin scenarios → test cases

**Acceptance Criteria**:
1. `/create-test` reads Spec's Contract section first
2. Extracts Gherkin scenarios (Given-When-Then)
3. Generates test cases that verify Contract scenarios
4. Falls back to code analysis if no Spec exists
5. Links generated tests to specific Contract criteria
6. Test names reference Contract scenario IDs

**Dependencies**:
- **Blocks on**: FB-24 (Specs must exist)
- **Blocks on**: FB-25 (Gherkin scenarios must be in Specs)

**Effort**: 5 points

---

#### FB-39: Implement Adversarial Code Review in /review-code

**User Story**:
> As a reviewer, I want `/review-code` to implement Builder/Critic separation, so that reviews are truly adversarial and catch Spec violations.

**Context**:
- Current `/review-code` does single-pass analysis
- ASDLC requires fresh context session (Critic Agent)
- Adversarial Code Review pattern ensures independent validation

**Acceptance Criteria**:
1. `/review-code` uses fresh context session for critique
2. Reads Spec and validates code against Spec contracts
3. Acts as Review Gate (PASS/FAIL, not just suggestions)
4. Outputs structured violation reports with remediation
5. Blocks on PASS/FAIL (not just advisory)
6. Uses reasoning-optimized model for Critic (if available)

**Dependencies**:
- **Blocks on**: FB-24 (Specs must exist for validation)

**Effort**: 8 points (major refactor)

---

#### FB-40: Add Constitutional Review to /review-code

**User Story**:
> As a reviewer, I want `/review-code` to validate against AGENTS.md Constitution, so that architectural principles are enforced.

**Context**:
- Extends FB-39 (Adversarial Code Review)
- Constitutional Review adds 2nd contract validation (Constitution + Spec)
- Catches architectural violations (like "LoadAll().Filter()" anti-pattern)

**Acceptance Criteria**:
1. Reads AGENTS.md Constitution (Operational Boundaries)
2. Validates code against 3-tier system (ALWAYS/ASK/NEVER)
3. Validates code against Command Structure Standards
4. Reports constitutional violations separately from spec violations
5. Provides remediation paths for violations
6. Blocks if Tier 3 (NEVER) violated

**Dependencies**:
- **Blocks on**: FB-39 (Adversarial Code Review infrastructure)
- **Requires**: AGENTS.md (FB-17) ✅ Complete

**Effort**: 3 points (extends FB-39)

---

### Medium Priority (Phase 1-2, After Critical Gaps)

#### FB-41: Enforce PBI Structure in /create-task and /decompose-task

**User Story**:
> As a product manager, I want created issues to follow PBI structure, so that they act as pointers (not containers) to permanent Specs.

**Context**:
- Current issues contain full descriptions (container model)
- ASDLC requires PBI 4-part anatomy (pointer model)
- Enables better traceability and Spec-driven development

**Acceptance Criteria**:
1. `/create-task` enforces 4-part PBI structure:
   - Directive (what to do)
   - Context Pointer (link to Spec)
   - Verification Pointer (link to Contract)
   - Refinement Rule (handling divergence)
2. `/decompose-task` generates child PBIs with proper structure
3. Template created for PBI format
4. Validation ensures all 4 parts present
5. Jira custom fields or description format enforces structure

**Dependencies**:
- **Blocks on**: FB-24 (Specs must exist to reference)

**Effort**: 5 points

---

#### FB-25: Add Gherkin Scenarios to Command Specs

**Status**: Already exists in backlog

**Enhancement**: Based on audit findings:
1. Focus on Contract section of Specs
2. Gherkin scenarios define test cases for `/create-test`
3. Scenarios are machine-verifiable (Given-When-Then)
4. Examples for each command type

**Dependencies**: FB-24 (Specs must exist)

**Effort**: 3 points (per existing estimate)

---

### Low Priority (Phase 2-3, Post-Foundation)

#### Enhancement: Add Model Routing Guidance to AGENTS.md

**Context**: Optimize model selection for Builder vs Critic tasks

**Changes**:
1. Add Model Routing section to AGENTS.md
2. Recommend speed models for generation (`/create-task`, `/start-task`)
3. Recommend reasoning models for review (`/review-code`, Constitutional Review)
4. Document model switching for Adversarial Code Review

**Effort**: 1 point (documentation only)

---

#### Enhancement: Add Ralph Loop to High-Iteration Commands

**Context**: Enable autonomous self-correction

**Candidates**:
- `/complete-task`: Iterate on lint/test failures
- `/create-test`: Iterate until tests pass
- `/review-code`: Iterate on Spec violations

**Requirements**:
- Iteration cap (20-50 max)
- Progress tracking
- Context rotation at 60-80% capacity
- External verification (not self-assessment)

**Effort**: 13 points (major pattern implementation)

---

## Prioritized Story List

### Must Complete Before Schema Lock (Critical Path)

1. **FB-37** - Refactor `/refine-task` focus (2 points) ← User feedback
2. **FB-24** - Migrate plans to Specs (8 points) ← Blocks multiple
3. **FB-37-NEW** - Add Constitutional Review to `/complete-task` (5 points) ← Quality Control
4. **FB-38** - Align `/create-test` with Contract (5 points) ← Depends on FB-24, FB-25
5. **FB-39** - Implement Adversarial Code Review in `/review-code` (8 points) ← Core pattern
6. **FB-40** - Add Constitutional Review to `/review-code` (3 points) ← Depends on FB-39
7. **FB-41** - Enforce PBI structure (5 points) ← Depends on FB-24

**Total Effort**: ~36 points (~5-6 sprints for single developer)

### Can Proceed in Parallel with Schema Work

**Track 1: Schemas (Current)**
- FB-18: Define schemas (current structure)
- FB-19: Validation script
- FB-20: CI/CD validation

**Track 2: Refinements (New)**
- FB-37: Refactor `/refine-task`
- FB-24: Migrate to Specs
- FB-37-NEW, FB-38, FB-39, FB-40, FB-41

**Benefit**: Accelerates alignment, schemas evolve as patterns are implemented

---

## Command-to-ASDLC Mapping

### Artifact Production

| Command | Produces | Should Produce | Gap |
|---------|----------|----------------|-----|
| `/create-task` | Issues | PBIs (with 4-part structure) | Missing PBI enforcement |
| `/decompose-task` | Issues | PBIs (with pointers) | Missing PBI structure |
| `/refine-task` | Updated issues | Refined PBIs | Missing Context/Verification Pointers |
| **`/create-plan`** | **Plan files** | **Specs (Blueprint+Contract)** | **Wrong artifact type** |
| `/start-task` | Branch | Branch (correct) | None |
| `/complete-task` | Commit, PR | Commit, PR (correct) | Missing Review Gates |
| `/create-test` | Test files | Test files (from Contract) | Code-driven, not Contract-driven |
| `/review-code` | Review report | Review Gate verdict | Not acting as gate |

### Pattern Coverage

| ASDLC Pattern | Implemented By | Status | Gap |
|---------------|----------------|--------|-----|
| **The Spec** | None | ❌ Not implemented | Plans exist, not Specs |
| **The PBI** | `/create-task`, `/decompose-task` | ⚠️ Partial | Missing 4-part structure |
| **Context Gates (Input)** | `/mcp-status`, validation in all commands | ✅ Implemented | None |
| **Context Gates (Quality)** | `/complete-task` (lint/tests) | ✅ Implemented | None |
| **Context Gates (Review)** | None | ❌ Not implemented | No Review Gates |
| **Adversarial Code Review** | None | ❌ Not implemented | `/review-code` doesn't implement pattern |
| **Constitutional Review** | None | ❌ Not implemented | No Constitution validation |
| **Ralph Loop** | None | ❌ Not implemented | No self-correction |
| **Agent Constitution** | AGENTS.md | ✅ Implemented | Not enforced by commands |
| **Living Specs** | None | ❌ Not implemented | Plans are not evolved |

### Phase Coverage

| ASDLC Phase | Commands | Coverage | Gap |
|-------------|----------|----------|-----|
| **Product** | `/create-task`, `/decompose-task`, `/refine-task` | ✅ Good | PBI structure enforcement |
| **Planning** | `/create-plan` | ⚠️ Partial | Produces plans, not Specs |
| **Development** | `/start-task`, `/complete-task` | ✅ Good | Missing Review Gates |
| **Quality** | `/create-test`, `/review-code` | ⚠️ Partial | Tests not Contract-driven, review not gate |
| **Verification** | `/complete-task`, `/review-code` | ⚠️ Partial | Only Quality Gates, missing Review |

---

## Recommended Story Creation

### Stories to Create Immediately

#### 1. FB-37: Refactor /refine-task to Focus on Planning Context

**Why**: User feedback indicates current output doesn't serve planning phase well

**Changes**:
- Shift emphasis from estimation to planning readiness
- Output should inform `/create-plan` with intent, constraints, context
- Story points become secondary (still present, not primary focus)
- Refinement report structured for plan consumption

**Blocks**: Nothing
**Blocked by**: Nothing
**Effort**: 2 points

---

#### 2. FB-37-NEW: Add Constitutional Review to /complete-task

**Why**: Critical gap in Quality Control - missing Review Gate

**Changes**:
- Add Constitutional Review step before PR creation
- Validate against AGENTS.md Operational Boundaries
- Report violations, block on Tier 3 (NEVER)
- Implement Critic Agent pattern (fresh context session)

**Blocks**: Nothing
**Blocked by**: AGENTS.md (FB-17) ✅ Complete
**Effort**: 5 points

---

#### 3. FB-38: Align /create-test with Spec Contract Pattern

**Why**: Tests should verify Spec contracts, not code behavior

**Changes**:
- Read Spec's Contract section for Gherkin scenarios
- Generate tests that verify Contract (BDD approach)
- Link tests to Contract criteria
- Fall back to code analysis if no Spec exists

**Blocks**: Nothing
**Blocked by**: FB-24 (Specs must exist), FB-25 (Gherkin in Specs)
**Effort**: 5 points

---

#### 4. FB-39: Implement Adversarial Code Review in /review-code

**Why**: `/review-code` should act as Review Gate with Builder/Critic separation

**Changes**:
- Implement fresh context session for Critic
- Read Spec and validate compliance
- Output structured violation report (not suggestions)
- Act as blocking gate (PASS/FAIL)
- Use reasoning model for Critic (if available)

**Blocks**: Nothing
**Blocked by**: FB-24 (Specs must exist)
**Effort**: 8 points

---

#### 5. FB-40: Add Constitutional Review to /review-code

**Why**: Dual-contract validation (Spec + Constitution)

**Changes**:
- Extend FB-39 to add Constitution validation
- Read AGENTS.md Operational Boundaries
- Report constitutional violations separately
- Validate against 3-tier system

**Blocks**: Nothing
**Blocked by**: FB-39 (Adversarial Code Review infrastructure)
**Effort**: 3 points

---

#### 6. FB-41: Enforce PBI Structure in /create-task and /decompose-task

**Why**: Issues should be pointers (not containers) per ASDLC PBI pattern

**Changes**:
- Enforce 4-part PBI structure:
  - Directive
  - Context Pointer (link to Spec)
  - Verification Pointer (link to Contract)
  - Refinement Rule
- Create PBI template
- Update validation logic
- Add Jira custom fields or format enforcement

**Blocks**: Nothing
**Blocked by**: FB-24 (Specs must exist to reference)
**Effort**: 5 points

---

### Future Stories (Phase 2+)

#### Create /constitutional-review Command

**Why**: Dedicated command for Constitution validation

**Scope**:
- Standalone command (not just part of `/complete-task`)
- Can be run on-demand for any branch/PR
- Outputs detailed constitutional analysis
- Useful for pre-commit validation and CI/CD

**Effort**: 5 points

---

#### Create /update-spec Command

**Why**: Specs are living documents that need evolution workflow

**Scope**:
- Update Spec when implementation changes contracts
- Called during or after `/complete-task`
- Detects contract changes in code
- Updates Spec's Blueprint or Contract sections

**Effort**: 8 points

---

#### Implement Ralph Loop Pattern

**Why**: Enable autonomous self-correction and L3-L4 autonomy

**Scope**:
- New epic for Ralph Loop implementation
- Affects multiple commands (`/complete-task`, `/create-test`)
- Requires iteration logic, progress tracking, context rotation
- Major architectural addition

**Effort**: Epic (21+ points)

---

## Updated Phase 1 Backlog

### Current Phase 1 (Foundation)
- FB-17: ✅ AGENTS.md (Done)
- FB-36: 🔄 Command Audit (In Progress)
- FB-18: Define schemas ← GO (with updates after refinements)
- FB-19: Validation script ← GO
- FB-20: CI/CD validation ← GO

### Additional Phase 1 Stories (Critical Gaps)
- **FB-37**: Refactor `/refine-task` (2 points) ← Immediate
- **FB-24**: Migrate to Specs (8 points) ← CRITICAL PATH
- **FB-37-NEW**: Constitutional Review in `/complete-task` (5 points) ← HIGH
- **FB-38**: Contract-driven `/create-test` (5 points) ← After FB-24, FB-25
- **FB-39**: Adversarial Code Review in `/review-code` (8 points) ← After FB-24
- **FB-40**: Constitutional Review in `/review-code` (3 points) ← After FB-39
- **FB-41**: PBI structure enforcement (5 points) ← After FB-24

**Total Additional Effort**: ~36 points

**Revised Phase 1 Total**: ~50 points (was ~15 points)

---

## Execution Recommendations

### Parallel Execution Strategy

**Week 1-2**: Critical path (blocks everything)
1. FB-37: Refactor `/refine-task` (2 points)
2. FB-24: Migrate to Specs (8 points) ← Start immediately

**Week 3-4**: Quality Control (can parallelize)
1. FB-18: Define schemas (5 points) ← Parallel to pattern work
2. FB-37-NEW: Constitutional Review in `/complete-task` (5 points)
3. FB-19: Validation script (3 points)

**Week 5-6**: Review Gates (depends on FB-24)
1. FB-25: Gherkin scenarios (3 points)
2. FB-38: Contract-driven tests (5 points)
3. FB-39: Adversarial Code Review (8 points)

**Week 7-8**: Finalization
1. FB-40: Constitutional Review in `/review-code` (3 points)
2. FB-20: CI/CD validation (3 points)
3. FB-41: PBI structure (5 points)

**Timeline**: ~8 weeks for full Phase 1 completion (including refinements)

---

## Success Criteria for ASDLC Alignment

### Phase 1 Complete When:
1. ✅ Specs exist (Blueprint + Contract) in `specs/` directory
2. ✅ Commands produce/consume Specs (not plans)
3. ✅ PBIs follow 4-part structure (pointers, not containers)
4. ✅ Quality Gates + Review Gates + Acceptance Gates all implemented
5. ✅ Constitutional Review validates code against AGENTS.md
6. ✅ Tests verify Spec Contract (not just code)
7. ✅ Schemas validate command structure
8. ✅ CI/CD enforces schemas and quality gates

### Validation:
- All commands reference ASDLC patterns in documentation
- Command execution produces ASDLC-compliant artifacts
- Quality Control pillar fully implemented (3-tier gates)
- Factory Architecture + Standardized Parts + Quality Control = ✅

---

## Alternative Approaches Considered

### Option A: Complete Refactor (Rejected)

**Approach**: Scrap current commands, rebuild from scratch against ASDLC patterns

**Pros**:
- Clean slate, no legacy constraints
- Perfect ASDLC alignment from start

**Cons**:
- Throws away excellent work (command structure, validation logic)
- High risk (may not improve on current quality)
- Long timeline (3+ months)
- Loss of momentum

**Decision**: Rejected - iterative refinement better than rewrite

---

### Option B: Schema First, Patterns Later (Rejected)

**Approach**: Complete FB-18-20 (schemas), then address pattern gaps

**Pros**:
- Linear execution (simple)
- Schemas provide structure for later work

**Cons**:
- Locks in wrong structure (plans, not Specs)
- Schemas need rewrite after Spec migration
- Delays critical pattern implementations

**Decision**: Rejected - parallel execution more efficient

---

### Option C: Parallel Execution (SELECTED)

**Approach**: Schema work + pattern refinements in parallel

**Pros**:
- Accelerates alignment timeline
- Schemas and patterns inform each other
- Incremental progress on both fronts
- Flexible iteration (update schemas as patterns evolve)

**Cons**:
- More complex coordination
- Schemas may need updates mid-stream

**Decision**: SELECTED - Best balance of speed and quality

---

## Next Steps

### Immediate Actions (This Week)

1. ✅ **Complete FB-36** (this audit spike)
   - Finalize audit report
   - Create command-ASDLC mapping
   - Post findings to Jira

2. **Create new stories**:
   - FB-37-NEW: Constitutional Review in `/complete-task`
   - FB-38: Contract-driven `/create-test`
   - FB-39: Adversarial Code Review in `/review-code`
   - FB-40: Constitutional Review in `/review-code`
   - FB-41: PBI structure enforcement

3. **Update FB-37** (existing `/refine-task` story):
   - Enhance description with audit findings
   - Emphasize planning context over estimation
   - Mark as HIGH priority (user feedback)

4. **Update FB-24** (existing Spec migration story):
   - Enhance with audit findings
   - Mark as CRITICAL PATH (blocks multiple stories)
   - Add details about Blueprint + Contract structure

5. **Update FB-18** (schema definition):
   - Note that schemas will evolve as commands are refined
   - Confirm GO decision with parallel execution
   - Add note about schema updates post-refinement

### Next Sprint Planning

1. **Start FB-24 immediately** (Spec migration) - CRITICAL PATH
2. **Start FB-37** in parallel (refactor `/refine-task`) - User feedback
3. **Continue FB-18** as planned (schemas) - Parallel track

---

## Conclusion

**Our homegrown commands are well-designed** and provide a solid foundation for ASDLC alignment. The core structure (Definitions, Prerequisites, Steps, Tools, Guidance) is excellent and should be preserved.

**Critical gaps exist** in artifact production (plans vs Specs) and pattern implementation (no Review Gates, no PBI enforcement). These gaps are addressable through targeted refinements, not wholesale rewrites.

**Recommendation**: Proceed with FB-18 (schemas) in parallel with critical gap resolution (FB-24, FB-37-41). This accelerates alignment while maintaining momentum.

**Expected Outcome**: Full ASDLC alignment achievable in ~8 weeks with parallel execution strategy.

---

**Audit Complete** ✅

**Review**: Ready for stakeholder review and story creation
**Next Step**: Create identified stories (FB-37-NEW through FB-41) and update existing stories (FB-18, FB-24, FB-37)
