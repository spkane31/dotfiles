---
name: babysit
description: Watches a GitHub Pull Request until all checks/actions pass, and the PR can be merged cleanly.
---

After opening a pull request with `gh pr create`, you may want to continually monitor the state of the PR using `gh pr watch`, which will continually poll a GitHub PR and exit with a status code on status changes. Whenever the status changes, check on the status of the PR:

- If the actions failed, investigate the failure and form an opinion on the cause. Remember that it's possible another change has since landed in `main` that may resolve the issue; check there for a fix, first, before attempting to write a new one. If you don't believe a fix has already been committed, prepare an implementation plan for the fix, and carry out the update LOCALLY.
- If the pull request can't be merged due to a conflict, please resolve that conflict by fetching `main` (or whatever the base branch for the pull request happens to be, if not `main`) and merging in the changes.
- If the test failure looks totally unrelated, you are *strongly encouraged* to re-run/retry the GitHub action. Examples of this include a test failing due to a GitHub or Docker error, or a runner error (OOM), or a test failure wholly unrelated to the work and flaking only for a few of the many functional test shards (a flaky test). In general, it's better to try a retry first before other measures, unless the failure is obviously related to our changes (we certainly don't want to introduce new flakes of our own).
- If the pull requests fail due to trivial checks, such as linting, please prepare a fix locally, and validate that fix (but *NEVER* push without first asking permission from the operator).

**NEVER push changes without first asking the attention of an operator in this mode. NEVER merge without first asking for permission from the operator.**

You are free to attempt edits in the LOCAL copy to try to resolve build errors, however. It is a great idea to *prepare* a fix for build breaks, just not push them.

Any time you're updating the PR, if you aren't already in a cloned copy of a repo, do a fresh /clone before updating files. After every update, resume watching the PR, until all checks pass/the PR can be merged. NEVER merge the PR yourself without first asking the attention of an operator in this mode.

Once the PR is merged, this skill is complete. There is nothing more to do—do not wait for additional tasks or continue monitoring. Make sure to clean up all background tasks involved in babysitting. 