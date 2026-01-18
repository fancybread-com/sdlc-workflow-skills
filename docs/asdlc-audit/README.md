# ASDLC Command Audit (FB-36)

**Project**: Agentic Software Development
**Epic**: FB-16 (ASDLC Alignment)
**Spike Story**: FB-36 (Command Audit)
**Date**: 2026-01-17
**Status**: ✅ Complete

---

## Executive Summary

This audit evaluates our 9 homegrown Cursor commands against ASDLC (Agentic Software Development Life Cycle) patterns and principles.

**Key Finding**: Commands are well-structured and provide a solid foundation, but critical gaps exist in artifact production (plans ≠ Specs) and pattern implementation (missing Review Gates, no PBI enforcement).

**Recommendation**: ✅ **GO with FB-18** (schema definition) using **parallel execution** strategy - proceed with schemas while addressing critical gaps.

---

## Audit Documents

### 1. [Command Audit Report](./command-audit-report.md)
**Purpose**: Detailed analysis of all 9 commands against ASDLC patterns

**Contents**:
- Executive summary with strengths/gaps
- Command-by-command analysis (1-9)
- Pattern implementation assessment
- Field Manual alignment check
- Specific recommendations per command

**Key Sections**:
- ✅ Strengths: Excellent structure, intelligent validation, robust MCP integration
- ❌ Critical Gaps: Plans ≠ Specs, no Review Gates, PBI structure not enforced
- ⚠️ Moderate Gaps: Tests are code-driven (not Contract-driven)

**Read this first** to understand overall findings.

---

### 2. [Gap Analysis](./gap-analysis.md)
**Purpose**: Systematic identification of missing ASDLC practices

**Contents**:
- Critical gaps (blocking full alignment)
- Major gaps (significant practices missing)
- Minor gaps (nice-to-have improvements)
- Impact assessment for FB-18 (schema work)
- Gap summary table with priorities

**Key Findings**:
1. **Plans ≠ Specs** (CRITICAL) - Need Blueprint+Contract structure
2. **No Review Gates** (CRITICAL) - Missing Constitutional/Adversarial Review
3. **PBI Structure Not Enforced** (CRITICAL) - Issues are containers, not pointers
4. **Tests Code-Driven** (CRITICAL) - Should verify Spec Contract
5. **No Ralph Loop** (HIGH) - No self-correction mechanisms

**Read this** to understand what's missing and why it matters.

---

### 3. [Recommendations](./recommendations.md)
**Purpose**: Actionable refinement plan with specific stories

**Contents**:
- Go/No-Go decision for FB-18 (✅ GO with parallel execution)
- Required refinement stories (FB-37-NEW through FB-41)
- Prioritized story list with effort estimates
- Command-to-ASDLC mapping tables
- Execution strategy (8-week timeline)
- Success criteria for ASDLC alignment

**Key Recommendations**:
1. **FB-37**: Refactor `/refine-task` (2 points) - IMMEDIATE (user feedback)
2. **FB-24**: Migrate plans → Specs (8 points) - CRITICAL PATH
3. **FB-37-NEW**: Add Constitutional Review to `/complete-task` (5 points) - HIGH
4. **FB-38**: Align `/create-test` with Contract (5 points) - HIGH
5. **FB-39**: Implement Adversarial Code Review (8 points) - HIGH
6. **FB-40**: Add Constitutional Review to `/review-code` (3 points) - HIGH
7. **FB-41**: Enforce PBI structure (5 points) - MEDIUM

**Total Effort**: ~36 points (~8 weeks with parallel execution)

**Read this** for the action plan.

---

## Quick Reference

### Commands Assessed

| # | Command | Status | Recommendation |
|---|---------|--------|----------------|
| 1 | `/mcp-status` | ✅ Excellent | Keep as-is |
| 2 | `/create-task` | ⚠️ Partial | Refine (PBI structure) |
| 3 | `/decompose-task` | ⚠️ Partial | Refine (PBI structure) |
| 4 | `/refine-task` | ⚠️ Partial | Refine (focus shift) |
| 5 | `/create-plan` | 🔴 Gap | Refactor (produce Specs) |
| 6 | `/start-task` | ⚠️ Partial | Refine (Spec references) |
| 7 | `/complete-task` | 🔴 Gap | Enhance (Review Gates) |
| 8 | `/create-test` | 🔴 Gap | Refactor (Contract-driven) |
| 9 | `/review-code` | 🔴 Gap | Refactor (Review Gate) |

**Legend**:
- ✅ Excellent: No changes needed
- ⚠️ Partial: Minor refinements needed
- 🔴 Gap: Significant refactoring required

---

## ASDLC Pillar Assessment

| Pillar | Current State | Target State | Gap |
|--------|---------------|--------------|-----|
| **Factory Architecture** | ✅ 9 specialized stations | ✅ 9 specialized stations | None |
| **Standardized Parts** | ⚠️ Commands structured, artifacts not | ✅ Specs, PBIs, schemas enforced | **Critical** |
| **Quality Control** | ⚠️ Quality Gates only | ✅ Quality + Review + Acceptance Gates | **Critical** |

**Overall Assessment**: 2 of 3 pillars need significant work (Standardized Parts, Quality Control)

---

## Decision: FB-18 Schema Work

**DECISION**: ✅ **GO** (with parallel execution)

**Strategy**:
- **Track 1**: Proceed with FB-18-20 (schema definition)
- **Track 2**: Address critical gaps (FB-24, FB-37-41) in parallel
- **Iterate**: Update schemas after command refinements

**Why GO**:
1. Current structure solid enough to codify
2. Schemas catch structural issues early
3. Parallel work accelerates alignment
4. Iterative schema updates manageable

**Why PARALLEL**:
1. Critical gaps block full alignment
2. Some gaps block others (FB-24 blocks FB-38, FB-41)
3. Faster time to full ASDLC compliance

---

## Pattern Coverage

### Implemented
- ✅ **Context Gates (Input)**: MCP validation, information density checks
- ✅ **Context Gates (Quality)**: Lint, tests in `/complete-task`
- ✅ **Agent Constitution**: AGENTS.md (FB-17)
- ✅ **Factory Architecture**: 9 specialized command stations

### Not Implemented
- ❌ **The Spec**: Plans exist, not Specs (Blueprint+Contract)
- ❌ **The PBI**: Issues created, but not 4-part PBI structure
- ❌ **Context Gates (Review)**: No Constitutional/Adversarial Review
- ❌ **Living Specs**: Plans not evolved with code
- ❌ **Ralph Loop**: No self-correction mechanisms

---

## Next Steps

### Immediate (This Week)
1. ✅ Complete FB-36 audit (this document)
2. Create new stories: FB-37-NEW, FB-38, FB-39, FB-40, FB-41
3. Update existing stories: FB-18, FB-24, FB-37
4. Post audit findings to FB-36 Jira issue

### Next Sprint
1. **Start FB-24** (Spec migration) - CRITICAL PATH
2. **Start FB-37** (refactor `/refine-task`) - User feedback
3. **Continue FB-18** (schemas) - Parallel track

### Timeline
- **Week 1-2**: FB-37 + FB-24 (critical path)
- **Week 3-4**: FB-18, FB-37-NEW, FB-19 (parallel)
- **Week 5-6**: FB-25, FB-38, FB-39 (depends on FB-24)
- **Week 7-8**: FB-40, FB-20, FB-41 (finalization)

**Total**: ~8 weeks to full ASDLC alignment

---

## Related Stories

**Existing**:
- FB-17: ✅ AGENTS.md (Done)
- FB-36: 🔄 Command Audit (This spike)
- FB-18: Define schemas (Updated: GO with parallel)
- FB-24: Migrate to Specs (Updated: CRITICAL PATH)
- FB-37: Refactor `/refine-task` (Updated: HIGH priority)

**New (To Create)**:
- FB-37-NEW: Constitutional Review in `/complete-task`
- FB-38: Contract-driven `/create-test`
- FB-39: Adversarial Code Review in `/review-code`
- FB-40: Constitutional Review in `/review-code`
- FB-41: PBI structure enforcement

---

## Research Questions Answered

From FB-36 description:

### 1. Do our 9 commands map to ASDLC phases?
**Answer**: ✅ **YES** - Excellent phase coverage:
- Product: `/create-task`, `/decompose-task`, `/refine-task`
- Planning: `/create-plan` (needs refinement to produce Specs)
- Development: `/start-task`, `/complete-task`
- Quality: `/create-test`, `/review-code`
- Infrastructure: `/mcp-status`

### 2. Do we produce the correct artifacts (Spec, PBI)?
**Answer**: ⚠️ **PARTIAL**:
- PBIs: Created but missing 4-part structure (Directive, Context Pointer, Verification Pointer, Refinement Rule)
- Specs: NOT produced - we create plans (transient) instead of Specs (permanent, Blueprint+Contract)

### 3. Is our command structure itself aligned with ASDLC "standardized parts"?
**Answer**: ✅ **YES** - Excellent structure:
- Consistent format: Overview, Definitions, Prerequisites, Steps, Tools, Guidance
- Intelligent validation (information density scoring)
- Robust error handling
- **Recommendation**: Codify with schemas (FB-18)

### 4. Do we implement Context Gates correctly?
**Answer**: ⚠️ **PARTIAL**:
- ✅ Input Gates: Excellent (MCP validation, information checks)
- ✅ Quality Gates: Implemented (`/complete-task` lint/tests)
- ❌ Review Gates: NOT implemented (missing Constitutional/Adversarial Review)
- ✅ Acceptance Gates: Implicit (human PR review)
- **Gap**: Missing 2nd tier (Review Gates)

### 5. Where does Ralph Loop fit, if anywhere?
**Answer**: 🔴 **NOT IMPLEMENTED, BUT APPLICABLE**:
- Should apply to: `/complete-task` (iterate on lint/test failures), `/create-test` (iterate until tests pass)
- Current: Commands stop on first failure, require human intervention
- **Recommendation**: Add Ralph Loop in Phase 2 (after critical gaps resolved)

### 6. Are there commands we're missing that ASDLC would expect?
**Answer**: ⚠️ **SOME MISSING**:
- Missing: `/constitutional-review` (standalone command)
- Missing: `/update-spec` (Spec evolution workflow)
- Missing: Explicit Builder/Critic separation in `/review-code`
- **Note**: Most gaps are in command behavior (how they work), not command coverage (what exists)

### 7. Are there redundancies or misalignments in our command set?
**Answer**: ✅ **NO REDUNDANCIES**:
- Each command has clear, distinct purpose
- No overlapping responsibilities
- Good separation of concerns
- **Misalignments**: Artifact types (plans vs Specs), pattern implementations (no Review Gates), not redundant commands

---

## Conclusion

**Our commands provide an excellent foundation** for ASDLC alignment. The structure, validation logic, and phase coverage are solid.

**Critical gaps exist** in artifact production and pattern implementation, but these are addressable through targeted refinements (not rewrites).

**Proceed with confidence** on FB-18 (schemas) while addressing critical gaps in parallel. Full ASDLC alignment achievable in ~8 weeks.

---

**Audit Status**: ✅ Complete
**Next Step**: Create refinement stories and update existing stories
**For Questions**: Review detailed analysis in `command-audit-report.md`
