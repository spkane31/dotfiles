---
name: self-review-pr
description: Reviews the current PR for common issues based on patterns from 90 days of actual code review feedback in temporalio/temporal. Catches issues that reviewers like bergundy, stephanos, and yycptt repeatedly flag before the PR is submitted.
---

## Your Task

You are doing a pre-submission self-review of the current PR on behalf of the author (spkane31). Your goal is to surface the same issues that reviewers in this repo repeatedly flag, so they can be fixed before review.

### Step 1: Gather PR Information

Run these commands to understand the PR:
```
gh pr view
gh pr diff --name-only
gh pr diff
```

If there is no open PR for the current branch, say so and stop.

### Step 2: Read Changed Files

For any non-trivial changed files (especially new `.go` files or heavily modified ones), read the full file content to understand context beyond the diff alone.

### Step 3: Evaluate Against These 8 Themes

Check each theme carefully and note findings with specific file+line references where possible.

---

#### Theme 1: Architecture / Design Clarity
*Reviewers flag this when a PR is large or introduces new abstractions without explanation.*

Ask:
- Is this PR large (>300 lines of logic) or does it introduce a new pattern/abstraction?
- If so, is there a design doc, PR description section, or inline comment explaining *why* this approach was chosen over alternatives?
- Would a reviewer understand the motivation from reading the PR description alone?

Flag if: The PR introduces significant new behavior, a new interface, or a new component without documented motivation.

---

#### Theme 2: Test Quality & Patterns
*This repo uses testify suites. Reviewers flag missing tests, wrong test patterns, and brittle assertions.*

Ask:
- Are new code paths covered by tests?
- Do new tests use `suite.T()` / testify suite patterns (not standalone `testing.T` functions in suite files)?
- Are `assert` vs `require` used correctly? (`require` when the test can't continue; `assert` for non-fatal checks)
- Do tests use `suite.Equal` / `suite.NoError` rather than `assert.Equal(t, ...)` in suite methods?
- Are there hardcoded line numbers or brittle string matches in test assertions?
- Do tests actually test the intended scenario (not just that it doesn't panic)?

Flag if: New logic is untested, tests use wrong suite patterns, or assertions are brittle.

---

#### Theme 3: Code Duplication (DRY)
*Reviewers flag copy-pasted logic and unexported functions that should be shared.*

Ask:
- Is there any logic duplicated from elsewhere in the codebase (especially in the same package)?
- Are there two near-identical functions that could share a helper?
- Is there unexported logic in a file that is also copied into a test file?
- Could any repeated patterns be extracted into a shared utility?

Flag if: Identical or near-identical code blocks appear more than once, or the change duplicates existing functionality.

---

#### Theme 4: API / Interface Surface Area
*Reviewers push back on unnecessary exported symbols and methods that leak internals.*

Ask:
- Are there newly exported functions, types, or methods that don't need to be exported?
- Are there parameters on functions/methods that are always passed the same value by all callers?
- Are there methods added to an interface that could instead be standalone functions?
- Does the interface change break callers in a way that wasn't necessary?

Flag if: Exported surface area grew unnecessarily, or function signatures have redundant parameters.

---

#### Theme 5: Documentation Updates
*Reviewers flag when behavior changes but comments, doc strings, or architecture docs are not updated.*

Ask:
- Did any existing comments or doc strings become inaccurate due to the change?
- If a non-trivial exported function or type was added, does it have a doc comment?
- Are there any architecture docs (e.g., in `docs/` or inline `// Design:` comments) that describe behavior this PR changes?
- If a config option or dynamic config key was added, is it documented?

Flag if: Behavior changed but nearby documentation was not updated, or new public API lacks doc comments.

---

#### Theme 6: Backward Compatibility & Feature Flags
*Reviewers push hard on breaking changes that lack feature flags or rollback support.*

Ask:
- Does this PR change any wire-format, storage format, or API contract?
- Are there new features that, once deployed, cannot be safely rolled back without data loss or errors?
- If a new behavior is risky or hard to roll back, is it gated by a dynamic config flag?
- Does the PR description call out the rollout/rollback story?

Flag if: A breaking or hard-to-roll-back change lacks a feature flag or rollout documentation.

---

#### Theme 7: Error Handling Completeness
*Reviewers flag silent error ignoring and missing error propagation.*

Ask:
- Are there any `_` assignments that discard errors (other than clearly benign cases like `defer f.Close()`)?
- Are errors from new function calls propagated up (or at minimum logged)?
- In new goroutines, are errors handled or reported?
- Are there code paths that silently succeed when they should fail?

Flag if: Errors are discarded with `_`, not returned, or not logged when they should be.

---

#### Theme 8: Performance & Race Conditions
*Reviewers flag unnecessary lock re-acquisition, races in tests, and concurrency issues.*

Ask:
- Are locks acquired, released, and re-acquired in a way that adds latency when a single critical section would suffice?
- In tests with goroutines, are shared variables accessed without synchronization?
- Are there `time.Sleep` calls in tests that could be replaced with proper synchronization?
- Are there channels or WaitGroups used correctly (no goroutine leaks)?

Flag if: Lock patterns add unnecessary latency, tests have data races, or concurrent code is unsynchronized.

---

#### Theme 9 (Minor): Scope Creep
Ask: Are there unrelated changes mixed into this PR (refactors, cleanups, or bug fixes that could be a separate PR)? Flag as a nit if scope is mixed.

#### Theme 10 (Minor): Code Style Nits
Ask:
- Should `EqualValues` be used instead of `Equal` for numeric type comparisons?
- Are there commented-out code blocks that should be removed?
- Do comments accurately describe what the code currently does?

---

### Step 4: Output Findings

Structure your output as follows:

```
## PR Self-Review: [PR title]

**Branch:** [branch name]
**Files changed:** [N files, +X/-Y lines]

---

### Blocking Issues
Issues that will very likely draw a blocking review comment. Fix before submitting.

[List findings with file:line references, or "None found."]

---

### Should Fix
Issues that reviewers will ask you to fix, though they may not block merge.

[List findings with file:line references, or "None found."]

---

### Nits
Minor style, clarity, or scope issues. Fix if time allows.

[List findings with file:line references, or "None found."]

---

### Summary
[2-3 sentence overall assessment. Be direct — is this PR ready to submit, or does it need work first?]
```

**Tone:** Mirror actual reviewer tone — constructive but direct. Use "nit:" prefix for minor issues. Be specific: "this function is exported but only called internally" is better than "consider reducing exported surface area." If you find nothing for a severity level, say so explicitly.
