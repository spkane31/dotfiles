---
name: create-pr
description: Create a GitHub pull request with proper formatting and content guidelines.
disable-model-invocation: true # You might want to manually invoke this
---
## Your Task
Check if there is a `.github/PULL_REQUEST_TEMPLATE.md` file for PR formatting. Write a summary of changes made to this branch.
Ensure the PR description includes:
*   A clear, active-voice title using conventional commits
*   A summary of 'Why' the change was made
*   A summary of 'How' the change was implemented
*   A summary of the testing to validate the changes
*   Links to any relevant issues or context
*   Concise and to the point wording

You can get the diff using `gh pr diff` and file names using `gh pr diff --name-only` to inform the description. Do not run `git add`, `git commit`, or `git push` commands, only generate the pull request description and output that information

Do not make any commits, any `git add`, `git commit`, or `git push` commands. Only generate the pull request description and output that information.
