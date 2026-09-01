---
name: debug-failing-ci-test
description: Use when given a GitHub Actions URL for a failing CI run and asked to investigate and fix the failing test. Triggers on: "this test failed in CI", "CI is failing", given a github.com/*/actions/runs/* URL, or asked to diagnose a test failure from a CI run.
---

# Debug Failing CI Test

## Overview

Downloads JUnit XML test results from a GitHub Actions run, parses them to find the exact failure, traces the root cause in the codebase, and applies a fix. Always use `superpowers:systematic-debugging` for the root cause analysis phase.

## Workflow

### Step 1: Extract Run ID and Repo

From a URL like `https://github.com/owner/repo/actions/runs/12345678`:
- Run ID: `12345678`
- Repo: `owner/repo`

```bash
# Confirm run status and find failed jobs
gh run view 12345678 --repo owner/repo --json conclusion,status,jobs \
  --jq '.jobs[] | select(.conclusion == "failure") | {name, databaseId}'
```

### Step 2: Download Logs and JUnit XML Artifacts to /tmp

**Always download to `/tmp` and save to named files — never stream logs through `gh api` pipes.** The logs are large (100k+ lines) and piping causes truncated output.

```bash
TMPDIR=/tmp/ci-debug-12345678
mkdir -p $TMPDIR

# Download all JUnit XML artifacts
gh run download 12345678 --repo owner/repo \
  --pattern "junit-xml*" --dir $TMPDIR

# Download raw job logs to a file for searching
gh api "repos/owner/repo/actions/jobs/{job-id}/logs" > /tmp/job-12345678-{jobid}.txt 2>&1
wc -l /tmp/job-12345678-{jobid}.txt  # verify it downloaded
```

**Why /tmp files over pipes:**
- `gh run view --log-failed` often errors ("stream error: CANCEL")
- `gh api .../logs` output exceeds buffer limits when piped
- Saving to file lets you `grep -n`, `sed -n 'LINE,LINEp'`, and `wc -l` efficiently

### Step 3: Parse Failures from XML — Start Narrow

XML artifacts come from every backend/shard combination. Start with the **failed jobs specifically** (from Step 1), not all XMLs.

```bash
# Quick scan: which XMLs actually have failures?
grep -rl '<failure' $TMPDIR/

# Check for crash XMLs (test binary crashed — no test-level results)
find $TMPDIR -name "junit.crash.xml"

# Parse failures from specific failed-job XMLs only
python3 - << 'EOF'
import xml.etree.ElementTree as ET, glob, html, os

# Only look at the failing job IDs
FAILED_JOB_IDS = ["68401814964", "68401814993"]  # from Step 1

for f in glob.glob('/tmp/ci-debug-12345678/**/*.xml', recursive=True):
    if 'crash' in f:
        continue
    if not any(jid in f for jid in FAILED_JOB_IDS):
        continue
    tree = ET.parse(f)
    for tc in tree.findall('.//testcase'):
        fail = tc.find('failure')
        if fail is not None:
            name = tc.get('classname', '') + '/' + tc.get('name', '')
            text = html.unescape(fail.text or fail.get('message', ''))
            print(f"\n{'='*60}")
            print(f"TEST: {name}")
            print(f"FILE: {f}")
            print(text[:2000])
EOF
```

**If you get a crash XML with no details**, look at the raw job log (Step 2) — the binary crashed before writing test output.

### Step 4: Identify the Failure Type

There are two distinct failure modes. Identify which you have **before** reading test code:

#### Type A: Test Assertion Failure
The XML has real test results with `Error Trace`, `Error:` lines. Analyze the assertion mismatch directly.

#### Type B: Test Binary Crash (junit.crash.xml)
The test binary panicked or was killed. The XML just says `Crash`. You must dig into the raw log.

```bash
# Search the job log for the panic
grep -n "panic:\|Fail in goroutine\|DATA RACE\|WARNING: DATA RACE\|SIGKILL\|signal:" \
  /tmp/job-{run}-{job}.txt | head -30

# Once you find the panic line number, read context around it
sed -n '{LINE-5},{LINE+60}p' /tmp/job-{run}-{job}.txt
```

**Common crash causes:**
- `panic: Fail in goroutine after TestXxx has completed` — assertion called in a goroutine after test exits (see below)
- `panic: runtime error: ...` — nil pointer or index out of range
- `WARNING: DATA RACE` — race detector found concurrent access
- OOM/SIGKILL — test used too much memory (usually visible in log as memory stats going up then silence)
- `channel receive with no ctx.Done select` — goroutine blocks forever on `<-ch` after test context expires; the test times out rather than panics, but shows as a hang in CI
- `global variable write + DATA RACE` — test modifies a package-level variable; the race detector fires; look for `WARNING: DATA RACE` in the log followed by a write from a `_test.go` file

#### The "Fail in goroutine after test completed" Crash

This is a specific and common pattern in Go tests. It means a goroutine is calling `t.Fail()` (or any testify assertion) **after the test function has returned**. This panics the entire test binary.

**Stack trace pattern:**
```
panic: Fail in goroutine after TestSuiteName/TestFoo has completed

goroutine 12345 [running]:
testing.(*common).Fail(...)
    testing/testing.go:969
github.com/stretchr/testify/require.NoError(...)
    require/require.go:1398
go.temporal.io/server/tests.(*Suite).someHelper.func1()
    tests/some_test.go:LINE   ← the assertion inside the goroutine
created by go.temporal.io/server/tests.(*Suite).someHelper
    tests/some_test.go:LINE   ← where the goroutine was spawned
```

**Root cause:** A helper like this:
```go
f := func() {
    resp, err := poller.Poll(...).Handle(...)
    s.NoError(err)  // DANGEROUS — called in goroutine
}
go func() {
    f()           // calls s.NoError inside
    close(done)
}()
```

**Fix:** Move the assertion out of the closure into the sync-only path. In the async goroutine, ignore or discard the error — the test catches failures via its context timeout on `WaitForChannel`:
```go
f := func() (Response, error) {
    return poller.Poll(...).Handle(...)
}
if async == nil {
    resp, err := f()
    s.NoError(err)   // safe — on test goroutine
    return resp
}
go func() {
    _, _ = f()       // errors surfaced via WaitForChannel ctx timeout
    close(done)
}()
```

**Why it only crashes sometimes:** The goroutine polls with a 30–60s timeout but the test context is only 15s. If the workflow task never arrives, the test context expires first → test completes → goroutine eventually times out → calls `s.NoError` → panic.

### Step 5: Check Failures Across Backends

When multiple backends fail on similar tests, cross-reference to find the truly consistent failures:

```bash
python3 - << 'EOF'
import xml.etree.ElementTree as ET, glob, html, os

for f in glob.glob('/tmp/ci-debug-12345678/**/*.xml', recursive=True):
    if 'crash' in f:
        continue
    backend = os.path.basename(os.path.dirname(f))
    tree = ET.parse(f)
    for tc in tree.findall('.//testcase'):
        fail = tc.find('failure')
        if fail is not None:
            name = tc.get('classname', '') + '/' + tc.get('name', '')
            if 'SomeTestName' in name:  # filter to tests you care about
                text = html.unescape(fail.text or fail.get('message', ''))[:200]
                print(f"{backend}: {name.split('/')[-1]}: {text[:100]}")
EOF
```

If a failure appears in only one backend → likely backend-specific. If it appears in all → likely a logic bug. If it appears as a crash XML in one and assertion failure in another → the crash is hiding the underlying assertion failure.

### Step 6: Search the Raw Log Efficiently

When you need to find specific content in a large log file:

```bash
# Find line numbers first
grep -n "FAIL\|ERROR\|panic\|Error Trace" /tmp/job.txt | head -50

# Read context around a specific line
sed -n '51000,51100p' /tmp/job.txt

# Find test retry attempts
grep -n "starting test attempt\|attempt #" /tmp/job.txt

# Find when test binary actually exits
grep -n "FAIL\tgo.temporal\|exit status\|PASS\tgo.temporal" /tmp/job.txt | tail -20
```

### Step 7: Find the Failing Test Code

```bash
# Find the test file (Go)
grep -r "func.*TestName\b" --include="*.go" -l

# Find the specific helper that spawns goroutines
grep -n "go func\|go s\." tests/some_test.go | head -20
```

### Step 8: Apply Systematic Debugging

**REQUIRED:** Use `superpowers:systematic-debugging` from here.

Key questions to answer:
1. What is the test asserting? What does it expect vs get?
2. Is the failure consistent (always same wrong value) or flaky (random)?
3. Which code path sets the value that's wrong?
4. For crashes: which goroutine is calling an assertion after the test completes, and why does it outlive the test?

### Step 9: Make the Minimal Fix

After root cause is confirmed:
- Fix the production code **or** the test setup, whichever is wrong
- Prefer fixing the root cause; don't paper over it with retries or wider timeouts
- **Exception for goroutine assertion panics:** the fix IS moving the assertion — that's the root cause
- Verify the fix compiles: `go build ./...` (Go) or language equivalent

## Quick Reference

| Goal | Command |
|------|---------|
| See failed jobs | `gh run view {id} --repo {r} --json conclusion,status,jobs --jq '.jobs[] \| select(.conclusion=="failure") \| {name,databaseId}'` |
| Download JUnit XMLs | `gh run download {id} --repo {r} --pattern "junit-xml*" --dir /tmp/ci-debug-{id}` |
| Download job logs | `gh api "repos/{r}/actions/jobs/{job-id}/logs" > /tmp/job.txt` |
| Find crash XMLs | `find /tmp/ci-debug-{id} -name "junit.crash.xml"` |
| Find failures in XML | `grep -rl '<failure' /tmp/ci-debug-{id}/` |
| Find panic in log | `grep -n "panic:\|Fail in goroutine\|DATA RACE" /tmp/job.txt` |
| Read log around line N | `sed -n '{N-10},{N+50}p' /tmp/job.txt` |

## Failure Message Anatomy

### Assertion Failure
```
=== RUN   TestSuiteV2/TestFoo
    test_env.go:424: Running TestSuiteV2/TestFoo in test shard 2/3
    foo_test.go:87:
        Error Trace: foo_test.go:112          ← exact assertion location
        Error:       Not equal:
                     expected: "build_id_1"   ← first arg to Equal()
                     actual  : "build_id_2"   ← second arg to Equal()
    foo_test.go:87:
        Error Trace: foo_test.go:87
        Error:       Condition never satisfied ← EventuallyWithT timed out
```

### Crash XML
```xml
<testcase name="functional-test (crash)" classname="">
    <failure message="Crash"></failure>
</testcase>
```
→ Look in raw job log for `panic:` or `Fail in goroutine` or `DATA RACE`.

### Goroutine Panic (in raw log)
```
panic: Fail in goroutine after TestVersioning3FunctionalSuiteV2/TestFoo has completed

goroutine 2698991 [running]:
testing.(*common).Fail(0xc063e1a008)
    testing.go:969
github.com/stretchr/testify/require.NoError(...)
go.temporal.io/server/tests.(*Suite).doPollWftAndHandle.func1()
    tests/versioning_3_test.go:3891  ← assertion inside goroutine
created by go.temporal.io/server/tests.(*Suite).doPollWftAndHandle
    tests/versioning_3_test.go:3897  ← goroutine creation site
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Piping `gh api .../logs` directly | Save to `/tmp` file first, then `grep -n` |
| Using `gh run view --log-failed` | It errors on large logs; use `gh api .../jobs/{id}/logs` |
| Looking at all XMLs at once | Start with failed job IDs only; filter by job ID in the path |
| Ignoring crash.xml | Crash = binary panic; the real failure is in the raw log |
| Assuming crash = OOM | Check for `panic:` or `Fail in goroutine` first — much more common |
| Fixing assertion failures when there's a crash | Fix the crash first — it may be masking the real failures |
| Assuming flakiness from 1 failure | Check if all 3 CI shards show same wrong value → consistent bug |
| Fixing the symptom (wider timeout) | Trace why the value is wrong; fix that |
| Ignoring V0 vs V2 pass/fail difference | The version difference isolates the code path — start there |
| Missing testify arg reversal | Check which argument is "expected" vs "actual" before assuming what's wrong |
| Calling any testify assertion in a goroutine | Even `assert` (not just `require`) panics after test completion — move all assertions to the test goroutine |
| Channel receive with no `ctx.Done` fallback | Wrap with `select { case v := <-ch: ... case <-ctx.Done(): return }` |
| Global state modification in test setup | Thread the value through function parameters instead of mutating globals |
| Using `RealTimeSource` with zero-duration delay | Use mock/event time source + non-zero delay, advance clock manually |
| Using `time.Sleep` to enforce ordering | Replace with `EventuallyWithT`, channels, or `WaitGroup` |

## Hang vs Crash Distinction

Not all failures show up as crashes. A **hang** means the test timed out (CI killed after N minutes) rather than panicked. Look for:

```
FAIL    go.temporal.io/server/tests [build failed]   # after timeout
```
or a job that simply ran for the full timeout with no output.

**Common hang root causes:**
1. **Channel receive without `ctx.Done`** — goroutine is blocked on `<-ch`; the sender exited because the test context was canceled.
2. **Infinite timer loop** — `RealTimeSource` + zero-duration delay fires the timer on every iteration.
3. **Dispatcher busy-wait** — a field like `numInflightTask` is set to a non-zero value that prevents the event loop from returning.

**Diagnosis:** Download raw job log (Step 2). Search for goroutine stack dumps:
```bash
grep -n "goroutine.*\[chan receive\]\|goroutine.*\[select\]" /tmp/job.txt | head -20
sed -n '{LINE-2},{LINE+20}p' /tmp/job.txt
```
A goroutine blocked in `[chan receive]` on a channel whose sender has already returned is the canonical hang.
