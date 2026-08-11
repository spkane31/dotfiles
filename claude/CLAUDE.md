## Code References
- When referencing code (explaining, discussing, or pointing to specific logic), always use clickable Markdown links with the fully qualified file path and line numbers
- Follow the agent runtime's required link format. For this runtime, use `[file.go:42](/full/path/to/file.go:42)` or `[file.go:42-50](/full/path/to/file.go:42)` for ranges.
- Never use relative paths or omit line numbers when referring to specific code.
- Do not use `file://` URIs when the runtime prohibits them. A local IDE preference for `file://` links yields to higher-priority runtime instructions.

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

When reviewing or modifying Go code, always check for `go vet` and `go fmt` and basic formatting issues.

### Go Proverbs

1. Design & Interfaces
* Accept interfaces, return structs: Keep inputs flexible and outputs concrete. This decouples packages, simplifies mock testing, and prevents rigid, over-engineered abstractions.
* The bigger the interface, the weaker the abstraction: Small interfaces with only 1 or 2 methods (like io.Reader) are highly reusable. Interfaces with dozens of methods force callers into rigid boxes.
* `interface{}` / `any` says nothing: An empty interface provides zero type safety or structural context, forcing complex runtime type assertions.
* Make the zero value useful: Types should be safely ready to use right after declaration without forcing explicit initialization (e.g., a `sync.Mutex` or `bytes.Buffer` works immediately without a constructor function).

2. Concurrency
* Don't communicate by sharing memory, share memory by communicating: Instead of protecting global variables across threads using complex locks, pass the data itself through channels.
* Concurrency is not parallelism: Concurrency is about program structure (breaking a problem down into independently executing tasks). Parallelism is about physical execution (simultaneously running tasks on multiple CPU cores).
* Channels orchestrate; mutexes serialize: Use channels to coordinate the broader architectural flow and data ownership of your program. Use mutexes for tiny, low-level data locking to prevent race conditions on single data structures.

3. Simplicity & Maintainability
* Clear is better than clever: Write readable, boring code. Avoid complex clever tricks that make the application hard to maintain or debug for the next engineer.
* Reflection is never clear: The reflect package makes code hard to understand, strips away compile-time type safety, and degrades runtime performance. Avoid it unless building deep structural frameworks.
* A little copying is better than a little dependency: Do not pull in a heavy third-party library just to use a 10-line utility function. Duplicate those few lines locally to avoid dependency bloat and supply chain risks.
* Gofmt's style is no one's favorite, yet gofmt is everyone's favorite: Automated, unified formatting eliminates useless debates over tabs vs. spaces, brackets, or code layouts.

4. Errors
* Errors are values: Errors are treated as standard programmable values, not exceptional crashes. You can inspect, wrap, log, and pass them around like any other piece of data.
* Don't just check errors, handle them gracefully: Simply wrapping `if err != nil { return err }` blindly down the stack is poor code. Add context to errors so the root problem is clear when it surfaces.
* Don't panic: Reserve panic exclusively for unrecoverable system failures (like division by zero or index out of bounds). Always return an standard error for expected runtime failures.

5. Low-Level & Environment
* Cgo is not Go: Calling C libraries from Go breaks cross-compilation, degrades performance due to thread switching overhead, and bypasses Go's memory safety guarantees.
* With the unsafe package there are no guarantees: Using unsafe breaks type safety and exposes your program to undefined behavior. It can break silently between compiler versions.
* Syscall must always be guarded with build tags: Platform-specific code should be kept isolated in dedicated files using Go build constraints so your application remains portable.
* Architecture-independent variants of syscall are the responsibility of the package: High-level packages should provide a unified, abstract interface to the developer, completely hiding the low-level operating system variations underneath.
* Documentation is for users: Public comments and docstrings should explain the what and why for the person consuming the package, not reveal the complex inner implementations of the code.

## Workflow

When asked to implement a plan, start implementing immediately. Do not spend time re-exploring or re-planning unless explicitly asked. Bias toward action over analysis.
