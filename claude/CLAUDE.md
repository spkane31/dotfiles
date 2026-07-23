## Code References
- When referencing code (explaining, discussing, or pointing to specific logic), always use clickable Markdown links with the fully qualified file path and line numbers
- Format: `[file.go:42](file:///full/path/to/file.go:42)` or `[file.go:42-50](file:///full/path/to/file.go:42)` for ranges
- Never use relative paths or omit line numbers when referring to specific code
- Always use `file://` URI scheme so links are clickable in the terminal/IDE

## Give feedback
- If you find any of my instructions too verbose/not clear enough/have gaps/mislead you, dump your feedback in .local/aifeedback and let me know. Give clear examples so that I can improve

## When Asked To Plan
- Look for `.local/aitasks` directory
- Create task folder: `/<YYYY-MM-DD>/<task-name>/`
- Always create `plan.md` with the implementation plan
- Don't code anything outside of the plan doc. Consult the user before executing the plan

### Task Status
Track status at the top of `plan.md`:
```
Status: in-progress | blocked | completed | abandoned
```

### Plan Style Guide
- Break down plans into clear sections with headings
- Break down implementation steps into phases
- Add examples and code snippets in each implementation phase

## Code Changes

When fixing bugs or implementing changes, prefer minimal, scoped changes. Do not refactor or over-engineer beyond what was explicitly requested. If asked to fix a race condition, only fix the race condition.

## Build & Generation 

For proto/generated files, always use the project's Make targets (e.g., `make proto`) instead of manually generating or editing proto output files.

## Testing

- Only write new tests for bug fixes or new features. Do not add tests for refactors or other changes unless instructed to.
- Every new test must fail without the change and pass with the change. Agents must verify this directly: run the test against the code before the fix/feature (confirm it fails), then again after (confirm it passes). Do not assume this without running it.
- For new features, tests must exercise the feature itself, not the underlying framework or library, and must be high quality, reusing existing test patterns and frameworks already present in the codebase.

## Go Development 

When reviewing or modifying Go code, always check for revive/golangci-lint compliance before submitting. Run `make lint` or equivalent after edits. Watch for: assertions in goroutines, deprecated APIs, nesting depth violations.

## Workflow 

When asked to implement a plan, start implementing immediately. Do not spend time re-exploring or re-planning unless explicitly asked. Bias toward action over analysis.