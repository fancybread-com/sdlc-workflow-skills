# Review Code

## Overview
Perform comprehensive AI-assisted code review on a pull request or branch changes.

## Definitions

- **{PR_KEY}**: Pull Request identifier (e.g., `PR-12`, `#12`, `12`). Can be specified as:
  - Full format: `PR-12` or `#12`
  - Numeric only: `12`
  - The command should accept any format and normalize it for API calls (extract numeric ID)
- **{BRANCH_NAME}**: Branch name to review (e.g., `feat/FB-12`, `main`, `develop`)
  - Can be local branch or remote branch
  - Format: `{type}/{TASK_KEY}` for feature branches (consistent with other commands)
- **PR (Pull Request)**: A GitHub pull request containing proposed changes to merge into a branch
  - Referenced using {PR_KEY} format (e.g., PR-12, #12, or 12)
  - Contains changes, metadata, comments, and review history
- **Branch**: A Git branch containing changes to review
  - Can be local (checked out in workspace) or remote (on GitHub)
  - Referenced using {BRANCH_NAME} format
  - For feature branches, follows `{type}/{TASK_KEY}` naming convention
- **Diff**: The difference between two versions of code showing additions, deletions, and modifications
  - Shows line-by-line changes in files
  - Indicates what was added (+), removed (-), or modified
  - Essential for understanding the scope of changes
- **Review Categories**: Classification system for organizing code review findings:
  - **Critical Issues** 🔴: Security vulnerabilities, data loss risks, breaking changes, critical bugs
  - **Major Issues** 🟡: Performance problems, design flaws, missing tests, poor error handling
  - **Minor Issues** 🟢: Style violations, documentation gaps, code smells, minor optimizations
  - **Suggestions** 💡: Best practices, refactoring ideas, alternative approaches
- **Severity Levels**: How to assign severity to findings:
  - **Critical**: Issues that must be fixed before merging (security, data loss, breaking changes)
  - **Major**: Issues that should be addressed but may not block merging (performance, design, tests)
  - **Minor**: Issues that are nice to fix (style, documentation, code quality)
  - **Suggestion**: Optional improvements (best practices, optimizations, refactoring)
- **Review Report Format**: Structured output containing:
  - Summary of findings by category
  - Detailed findings with file paths and line references
  - Specific suggestions for improvement
  - Approval recommendation (approve, request changes, or comment)

## Prerequisites

Before proceeding, verify:

1. **MCP Status Validation**: GitHub MCP connection required (see `mcp-status.md` for detailed steps)
   - Use `mcp_github_get_me` to verify GitHub MCP connection
   - **If GitHub MCP connection fails, STOP and report: "GitHub MCP connection failed. Please verify MCP configuration (see mcp-status.md)."**

2. **PR/Branch Existence**: Verify {PR_KEY} or {BRANCH_NAME} is valid and accessible
   - **For PR ({PR_KEY}):**
     - Normalize {PR_KEY} format (extract numeric ID from PR-12, #12, or 12)
     - Use `mcp_github_pull_request_read` with method="get" to verify PR exists
     - **If PR not found or inaccessible, STOP and report: "Pull Request {PR_KEY} not found or inaccessible."**
   - **For branch ({BRANCH_NAME}):**
     - Use `mcp_github_list_branches` to check if branch exists on remote
     - Use `run_terminal_cmd` with `git branch -a` to check local branches
     - **If branch not found, STOP and report: "Branch {BRANCH_NAME} not found."**

3. **Access Verification**: Verify user has access to PR/branch (read permissions)
   - Attempt to retrieve PR details or branch information
   - **If access denied, STOP and report: "Access denied to {PR_KEY} or {BRANCH_NAME}. Please verify permissions."**

## Steps

1. **Retrieve changes**
   - **Determine if PR ({PR_KEY}) or branch ({BRANCH_NAME}):**
     - Check if input is a PR format (PR-12, #12, 12) or branch name
     - **Decision point:** PR vs branch determines which tools to use
   - **If PR ({PR_KEY}):**
     - Normalize {PR_KEY} format: Extract numeric ID from PR-12, #12, or 12
       - Example: PR-12 → 12, #12 → 12, 12 → 12
     - Use `mcp_github_pull_request_read` with method="get" to retrieve PR details
       - Parameters: `owner`, `repo`, `pullNumber` = normalized numeric ID
     - Use `mcp_github_pull_request_read` with method="get_files" to get list of changed files
       - Parameters: `owner`, `repo`, `pullNumber` = normalized numeric ID
     - Use `mcp_github_pull_request_read` with method="get_diff" to get the full diff
       - Parameters: `owner`, `repo`, `pullNumber` = normalized numeric ID
     - **STOP condition:** If PR not found or inaccessible, report error and stop
   - **If branch ({BRANCH_NAME}):**
     - Verify branch exists:
       - For remote: Use `mcp_github_list_branches` to check
       - For local: Use `run_terminal_cmd` with `git branch -a | grep {BRANCH_NAME}`
     - Get diff using `run_terminal_cmd`:
       - `git diff main...{BRANCH_NAME}` (compare branch to main)
       - Or `git diff {BRANCH_NAME}` (compare to current HEAD)
     - Get list of changed files using `run_terminal_cmd`:
       - `git diff --name-only main...{BRANCH_NAME}`
     - **STOP condition:** If branch not found, report error and stop
   - **Read all changed files:**
     - Iterate through list of changed files
     - Use `read_file` to read each changed file
     - **STOP condition:** If any file is unreadable or doesn't exist, report warning but continue with available files
   - **Understand scope of changes:**
     - Review file paths to understand which parts of codebase are affected
     - Count lines changed, files changed
     - Identify change types: new files, modifications, deletions
     - Note related files that might need review (tests, documentation)

2. **Analyze code quality** (integrated with Review Categories)
   - **Critical Issues Analysis 🔴:**
     - **Security vulnerabilities:**
       - Check for SQL injection risks, XSS vulnerabilities, authentication/authorization issues
       - Look for hardcoded secrets, credentials, or API keys
       - Verify input validation and sanitization
       - Check for insecure dependencies or outdated packages
     - **Data loss risks:**
       - Verify proper error handling in data operations
       - Check for missing transaction handling or rollback logic
       - Ensure proper backup or recovery mechanisms
       - Verify data validation before destructive operations
     - **Breaking changes:**
       - Check for API contract changes (function signatures, return types)
       - Verify backward compatibility for public interfaces
       - Check for changes to shared utilities or common code
       - Review database schema changes for migration requirements
     - **Critical bugs:**
       - Look for null pointer exceptions, undefined access
       - Check for infinite loops or recursion without base cases
       - Verify proper exception handling for critical operations
     - **Categorize findings:** Tag each critical finding with appropriate severity

   - **Major Issues Analysis 🟡:**
     - **Performance problems:**
       - Check for N+1 query patterns, inefficient algorithms
       - Look for missing indexes, unnecessary database queries
       - Review loop complexity and nested iterations
       - Check for memory leaks or resource cleanup issues
     - **Design flaws:**
       - Verify separation of concerns, single responsibility principle
       - Check for tight coupling, circular dependencies
       - Review code duplication and opportunities for abstraction
       - Assess overall architecture and design patterns
     - **Missing tests:**
       - Check if new code has corresponding tests
       - Verify test coverage for critical paths
       - Review test quality (unit tests, integration tests)
       - Note areas where tests should be added
     - **Poor error handling:**
       - Check for swallowed exceptions or silent failures
       - Verify appropriate error messages and logging
       - Review error recovery mechanisms
       - Check for proper validation of error conditions
     - **Categorize findings:** Tag each major finding with appropriate severity

   - **Minor Issues Analysis 🟢:**
     - **Style violations:**
       - Check code formatting, indentation consistency
       - Review naming conventions (variables, functions, classes)
       - Verify consistent code style with project standards
       - Check for unnecessary complexity or verbosity
     - **Documentation gaps:**
       - Check for missing JSDoc/TSDoc comments on public APIs
       - Review inline comments for clarity and necessity
       - Verify README updates for new features
       - Check for missing or outdated documentation
     - **Code smells:**
       - Look for long methods, large classes
       - Check for magic numbers or strings
       - Review variable naming clarity
       - Identify dead code or unused imports
     - **Minor optimizations:**
       - Check for unnecessary computations or operations
       - Review opportunities for code simplification
       - Look for minor performance improvements
     - **Categorize findings:** Tag each minor finding with appropriate severity

   - **Suggestions Analysis 💡:**
     - **Best practices:**
       - Suggest design pattern improvements
       - Recommend coding best practices
       - Propose architectural improvements
     - **Refactoring ideas:**
       - Suggest code extraction or simplification
       - Recommend better abstractions
       - Propose structural improvements
     - **Alternative approaches:**
       - Suggest different algorithms or implementations
       - Recommend library alternatives
       - Propose different design choices
     - **Categorize findings:** Tag each suggestion appropriately

3. **Check compliance**
   - **Verify coding standards adherence:**
     - Check against project coding standards and style guide
     - Review linter configuration and compliance
     - Verify consistent patterns across codebase
   - **Check style guidelines:**
     - Review formatting, naming conventions
     - Verify comment style and documentation standards
     - Check file organization and structure
   - **Validate project conventions:**
     - Verify file naming conventions
     - Check directory structure and organization
     - Review import/export patterns
     - Verify testing conventions and patterns
   - **Review documentation completeness:**
     - Check for updated README files
     - Verify API documentation updates
     - Review inline code comments
     - Check for changelog or release notes updates

4. **Generate review report**
   - **Categorize findings by severity:**
     - Group findings by Review Categories (Critical, Major, Minor, Suggestions)
     - Count findings per category
     - Prioritize critical and major issues
   - **Provide specific line references:**
     - Include file paths for each finding
     - Reference specific line numbers or code sections
     - Quote relevant code snippets where helpful
     - Link findings to specific changes in diff
   - **Suggest improvements:**
     - Provide actionable suggestions for each finding
     - Include code examples or references where appropriate
     - Explain why the suggestion improves the code
   - **Make approval recommendation:**
     - **Approve:** No critical or major issues, code is ready to merge
     - **Request Changes:** Critical or major issues found that should be addressed
     - **Comment:** Minor issues or suggestions only, can merge but improvements recommended

## Tools

### MCP Tools (GitHub)
- `mcp_github_get_me` - Verify GitHub MCP connection
  - Use to validate GitHub MCP is configured and accessible
  - **If this fails, STOP workflow - GitHub MCP is required for PR operations**
- `mcp_github_pull_request_read` - Retrieve pull request information
  - **method="get"**: Get PR details (title, description, status, author, etc.)
    - Parameters: `owner`, `repo`, `pullNumber` = normalized {PR_KEY} (numeric ID)
    - Returns: PR metadata, status, labels, assignees
  - **method="get_diff"**: Get the diff showing all changes in the PR
    - Parameters: `owner`, `repo`, `pullNumber` = normalized {PR_KEY} (numeric ID)
    - Returns: Full diff of changes (additions, deletions, modifications)
  - **method="get_files"**: Get list of files changed in the PR
    - Parameters: `owner`, `repo`, `pullNumber` = normalized {PR_KEY} (numeric ID)
    - Returns: List of changed files with paths, status (added, modified, deleted)
- `mcp_github_list_branches` - List branches in repository
  - Parameters: `owner`, `repo`
  - Use to verify branch exists on remote
- `mcp_github_add_comment_to_pending_review` - Add review comments to a pending review
  - Parameters: `owner`, `repo`, `pullNumber`, `path` = file path, `body` = comment text, `line` = line number, `side` = "RIGHT" (new code), `subjectType` = "LINE"
  - Use to add specific line-by-line review comments

### Codebase Tools
- `codebase_search` - Find related code and understand context
  - Query: "How is [similar feature] implemented?"
  - Query: "Where is [component] used?"
  - Query: "What are the patterns for [error handling/testing/API design] in this codebase?"
  - Use to understand codebase patterns, find similar implementations, and ensure consistency
- `read_file` - Read changed files and related files for context
  - Parameters: `target_file` = path to file
  - Use to read changed files and related files (tests, dependencies) for full context

### Filesystem Tools
- `read_file` - Read local files when reviewing branch changes
  - Parameters: `target_file` = path to file
  - Use when reviewing local branch changes (not PR)

### Terminal Tools
- `run_terminal_cmd` - Execute git commands for branch operations
  - `git branch -a` - List all branches (local and remote)
  - `git diff main...{BRANCH_NAME}` - Get diff between main and branch
  - `git diff --name-only main...{BRANCH_NAME}` - List changed files between main and branch
  - `git log {BRANCH_NAME} ^main` - View commit history on branch

## Pre-flight Checklist
- [ ] MCP status validation performed (GitHub MCP connection verified, see `mcp-status.md`)
- [ ] PR ({PR_KEY}) or branch ({BRANCH_NAME}) is accessible and exists
- [ ] {PR_KEY} normalized to numeric ID if PR review (extract from PR-12, #12, or 12)
- [ ] Changed files retrieved and readable
- [ ] Scope of changes understood (file count, line count, change types)
- [ ] Codebase context reviewed (related files, patterns, conventions)

## Review Categories

### Critical Issues 🔴
**Severity:** Must be fixed before merging. These issues pose serious risks to security, data integrity, or system stability.

**Types:**
- **Security vulnerabilities:**
  - SQL injection, XSS, CSRF vulnerabilities
  - Hardcoded secrets, credentials, or API keys
  - Missing authentication or authorization checks
  - Insecure dependencies or outdated packages
  - Input validation and sanitization failures
- **Data loss risks:**
  - Missing error handling in data operations
  - Lack of transaction handling or rollback logic
  - Missing backup or recovery mechanisms
  - Data validation failures before destructive operations
- **Breaking changes:**
  - API contract changes without versioning or migration
  - Backward compatibility violations for public interfaces
  - Changes to shared utilities affecting other components
  - Database schema changes without migration plans
- **Critical bugs:**
  - Null pointer exceptions or undefined access
  - Infinite loops or recursion without base cases
  - Missing exception handling for critical operations
  - Logic errors causing incorrect behavior

**Action:** Request changes - these must be addressed before approval.

### Major Issues 🟡
**Severity:** Should be addressed. These issues impact code quality, maintainability, performance, or reliability.

**Types:**
- **Performance problems:**
  - N+1 query patterns or inefficient database access
  - Missing indexes or unnecessary queries
  - High complexity algorithms or nested iterations
  - Memory leaks or missing resource cleanup
- **Design flaws:**
  - Violations of separation of concerns or single responsibility
  - Tight coupling or circular dependencies
  - Code duplication without abstraction
  - Architectural inconsistencies
- **Missing tests:**
  - New code without corresponding tests
  - Missing test coverage for critical paths
  - Poor test quality or incomplete test scenarios
  - Missing integration tests for complex workflows
- **Poor error handling:**
  - Swallowed exceptions or silent failures
  - Missing or inadequate error messages
  - Missing error recovery mechanisms
  - Insufficient error validation

**Action:** Request changes or approve with comments - address these issues or document why they're acceptable.

### Minor Issues 🟢
**Severity:** Nice to fix. These are code quality improvements that don't impact functionality.

**Types:**
- **Style violations:**
  - Code formatting inconsistencies
  - Naming convention deviations
  - Code style inconsistencies with project standards
  - Unnecessary complexity or verbosity
- **Documentation gaps:**
  - Missing JSDoc/TSDoc comments on public APIs
  - Unclear or missing inline comments
  - Missing README updates for new features
  - Outdated or incomplete documentation
- **Code smells:**
  - Long methods or large classes
  - Magic numbers or strings
  - Unclear variable naming
  - Dead code or unused imports
- **Minor optimizations:**
  - Unnecessary computations or operations
  - Opportunities for code simplification
  - Minor performance improvements

**Action:** Approve with comments - address these in future iterations.

### Suggestions 💡
**Severity:** Optional improvements. These are enhancements that could improve code quality or maintainability.

**Types:**
- **Best practices:**
  - Design pattern improvements
  - Coding best practice recommendations
  - Architectural enhancement suggestions
- **Refactoring ideas:**
  - Code extraction or simplification opportunities
  - Better abstraction recommendations
  - Structural improvement suggestions
- **Alternative approaches:**
  - Different algorithm or implementation suggestions
  - Library or tool alternatives
  - Different design choice recommendations

**Action:** Approve with comments - consider for future work.

## Review Checklist
- [ ] All changed files reviewed
- [ ] Code quality assessed (Critical, Major, Minor issues identified)
- [ ] Security checked (vulnerabilities, authentication, authorization)
- [ ] Performance evaluated (algorithms, queries, resource usage)
- [ ] Tests reviewed (coverage, quality, completeness)
- [ ] Error handling assessed (exception handling, validation, recovery)
- [ ] Documentation checked (inline comments, API docs, README updates)
- [ ] Compliance verified (coding standards, style guidelines, conventions)
- [ ] Findings categorized (Critical 🔴, Major 🟡, Minor 🟢, Suggestions 💡)
- [ ] Review report generated with line references
- [ ] Approval recommendation made (Approve, Request Changes, or Comment)

## Guidance

### Role
Act as a **Senior Engineer/Code Reviewer** responsible for thorough code review. You are methodical, detail-oriented, and focused on code quality, security, and maintainability while ensuring changes align with project standards and best practices.

### Instruction
Execute the review-code workflow to perform comprehensive code review on a pull request or branch. This includes:
1. Retrieving and understanding the scope of changes
2. Analyzing code quality across all Review Categories (Critical, Major, Minor, Suggestions)
3. Checking compliance with project standards and conventions
4. Generating a detailed review report with categorized findings and specific recommendations

### Context
- The review may be for a GitHub Pull Request ({PR_KEY}) or a local/remote branch ({BRANCH_NAME})
- {PR_KEY} can be specified in multiple formats (PR-12, #12, or 12) and should be normalized to numeric ID for API calls
- {BRANCH_NAME} follows `{type}/{TASK_KEY}` format for feature branches (consistent with other commands)
- The codebase has established patterns, conventions, and architectural decisions that should be respected
- GitHub MCP integration provides access to PR data, diffs, and file lists
- Review findings should be categorized according to severity (Critical, Major, Minor, Suggestions)

### Examples

**Example 1: Review Pull Request with {PR_KEY}**
```
Input: /review-code PR-12
Process:
1. Normalize PR-12 to numeric ID: 12
2. Use mcp_github_pull_request_read with method="get" to get PR details
3. Use mcp_github_pull_request_read with method="get_files" to get changed files
4. Use mcp_github_pull_request_read with method="get_diff" to get full diff
5. Read all changed files using read_file
6. Analyze code quality across all Review Categories
7. Generate review report with categorized findings
8. Make approval recommendation
```

**Example 2: Review Branch with {BRANCH_NAME}**
```
Input: /review-code feat/FB-12
Process:
1. Verify branch exists using mcp_github_list_branches or git branch -a
2. Get diff using git diff main...feat/FB-12
3. Get changed files using git diff --name-only main...feat/FB-12
4. Read all changed files using read_file
5. Analyze code quality across all Review Categories
6. Generate review report with categorized findings
7. Make approval recommendation
```

**Example 3: {PR_KEY} Normalization**
```
Input formats and normalization:
- PR-12 → 12 (extract numeric ID)
- #12 → 12 (remove # prefix)
- 12 → 12 (already numeric)
All formats result in pullNumber=12 for API calls
```

**Example 4: Review Report Format**
```
## Code Review Report

### Summary
- Critical Issues: 2
- Major Issues: 3
- Minor Issues: 5
- Suggestions: 2

### Critical Issues 🔴
1. **Security: Hardcoded API Key** (src/services/api.ts:45)
   - Issue: API key exposed in code
   - Suggestion: Move to environment variable or secrets management

2. **Breaking Change: API Signature Changed** (src/api/users.ts:23)
   - Issue: Function signature change breaks existing callers
   - Suggestion: Add versioning or maintain backward compatibility

### Major Issues 🟡
[Detailed findings...]

### Minor Issues 🟢
[Detailed findings...]

### Suggestions 💡
[Detailed suggestions...]

### Recommendation
**Request Changes** - Critical security issue must be addressed before merging.
```

### Constraints

**Rules (Must Follow):**
1. **MCP Validation**: GitHub MCP connection is required. If validation fails, STOP and report the failure (see `mcp-status.md`).
2. **{PR_KEY} Normalization**: Always normalize {PR_KEY} to numeric ID (extract from PR-12, #12, or 12 format) before making API calls.
3. **Comprehensive Analysis**: Review all code changes across all Review Categories (Critical, Major, Minor, Suggestions).
4. **Specific Line References**: Include file paths and line numbers for all findings to make issues actionable.
5. **Severity Assignment**: Assign severity correctly:
   - **Critical 🔴**: Security, data loss, breaking changes, critical bugs (must fix)
   - **Major 🟡**: Performance, design, tests, error handling (should fix)
   - **Minor 🟢**: Style, documentation, code smells (nice to fix)
   - **Suggestions 💡**: Best practices, refactoring, alternatives (optional)
6. **Approval Recommendation Logic**:
   - **Approve**: No critical or major issues found
   - **Request Changes**: Critical or major issues found (must address)
   - **Comment**: Only minor issues or suggestions (can merge with improvements)
7. **Codebase Context**: Use `codebase_search` to understand patterns and ensure consistency with existing code.
8. **Preserve Existing Patterns**: Respect established codebase patterns, conventions, and architectural decisions.
9. **Stop Conditions**: STOP and report if:
   - GitHub MCP connection fails
   - PR ({PR_KEY}) not found or inaccessible
   - Branch ({BRANCH_NAME}) not found
   - Critical files are unreadable (warn but continue with available files)

**Existing Standards (Reference):**
- MCP status validation: See `mcp-status.md` for detailed MCP server connection checks
- Branch naming: Type prefix format (`{type}/{TASK_KEY}`) as shown in `start-task.md`
- PR creation: See `complete-task.md` for PR context and workflow
- Review standards: Follow project-specific code review guidelines and conventions

### Output
1. **Review Report**: Comprehensive report containing:
   - Summary of findings by category (counts for Critical, Major, Minor, Suggestions)
   - Detailed findings with:
     - File paths and line references
     - Code snippets or quotes where helpful
     - Specific suggestions for improvement
     - Explanation of why the issue matters
   - Approval recommendation (Approve, Request Changes, or Comment)
   - Rationale for recommendation based on findings
2. **Review Comments (if PR)**: Optional line-by-line comments using `mcp_github_add_comment_to_pending_review` for specific code locations
3. **Categorized Findings**: All findings organized by Review Categories with appropriate severity indicators (🔴 🟡 🟢 💡)
