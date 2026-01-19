# Feature: {Feature Name}

> **ASDLC Pattern**: [The Spec](https://asdlc.io/patterns/the-spec/)  
> **Practice Guide**: [Living Specs](https://asdlc.io/practices/living-specs/)  
> **Status**: Active | Deprecated | Superseded  
> **Last Updated**: YYYY-MM-DD

---

## Blueprint

### Context

*Purpose: Why does this feature exist? What business problem does it solve?*

[Describe the problem and the solution. Include user impact and rationale.]

### Architecture

*Purpose: API contracts, data models, dependencies, and dependency directions.*

- **API Contracts**: [Endpoints, request/response formats, or equivalent for your domain]
- **Data Models**: [Schemas, validation rules, data structures; or "See `path/to/file`"]
- **Dependencies**: [What this depends on; what depends on this]
- **Dependency Directions**: [Inbound/outbound relationships]

### Anti-Patterns

*Purpose: What agents and developers must NOT do, with rationale.*

- [Forbidden approach 1 and why]
- [Forbidden approach 2 and why]

---

## Contract

### Definition of Done

*Purpose: Observable, testable success criteria. Each item must be verifiable.*

- [ ] [Observable success criterion 1]
- [ ] [Observable success criterion 2]
- [ ] [Observable success criterion 3]
- [ ] [Automated verification: tests pass, lint passes, builds successfully]

### Regression Guardrails

*Purpose: Critical invariants that must never break. These are non‑negotiable.*

- [Critical invariant 1]
- [Critical invariant 2 — e.g. performance, security, or correctness]

### Scenarios

*Purpose: Gherkin-style behavioral specifications (Given/When/Then). Use for acceptance tests and BDD.*

**Scenario: [Example — successful path]**
- **Given**: [Precondition — initial state]
- **When**: [Action — what the user or system does]
- **Then**: [Expected outcome — observable result]

**Scenario: [Example — failure or edge case]**
- **Given**: [Precondition]
- **When**: [Action]
- **Then**: [Expected outcome — e.g. error handling, fallback]

**Scenario: [Your scenario name]**
- **Given**: [Precondition]
- **When**: [Action]
- **Then**: [Expected outcome]

---

## Good vs Bad

- ✅ **Do** reference code and config with file paths; keep the spec focused on contracts and constraints.
- ❌ **Don’t** paste large code blocks; use minimal examples only to illustrate patterns.
- ✅ **Do** update the spec in the **same commit** when code changes behavior or contracts (Same-Commit Rule).
- ❌ **Don’t** let the spec go stale; treat it as living documentation that evolves with the feature.
