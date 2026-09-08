# dotfiles

Config files, managed via [chezmoi](https://www.chezmoi.io/), applied to any
machine from this repo as the source directory.

## Install

    brew install chezmoi
    chezmoi init --source ~/path/to/this/checkout
    chezmoi diff   # review what would change
    chezmoi apply

On first `init`, you'll be prompted once "Is this a work machine" — answer
is cached locally in `~/.config/chezmoi/chezmoi.toml` (not committed) and
controls the work-only sections of `dot_zshrc.tmpl` (Datadog PATH/env setup,
and the Ansible-managed block that IT's automation also edits in place —
see note below).

Re-running `chezmoi apply` is safe; it only rewrites files that differ from
what the template would produce.

### Note on the work `.zshrc`'s Ansible-managed block

The work machine's shell config has a section between
`# BEGIN/END ANSIBLE MANAGED BLOCK` markers that IT's Ansible automation
edits directly. `dot_zshrc.tmpl` freezes a copy of that block's current
content for the `work` case. If Ansible's role changes what it writes there
in the future, `chezmoi apply` will silently overwrite that change back to
whatever is frozen in the template — there's no automatic sync. Periodically
diff the live block against the template and update the template by hand if
it drifts.

## Claude and Codex

chezmoi links only the portable configuration below into
`~/.claude`/`~/.codex`. Copy files and directories into the matching
repository paths; do not copy a whole local tool directory wholesale.

| Tool | Local source | Repository path | Notes |
| --- | --- | --- | --- |
| Claude | `~/.claude/settings.json` | `dot_claude/settings.json` | Already managed. Review permissions and plugin settings before committing. |
| Claude | `~/.claude/CLAUDE.md` | `dot_claude/CLAUDE.md` | Global instructions. |
| Claude | `~/.claude/skills/` | `dot_claude/skills/` | Your custom skills only. |
| Codex | `~/.codex/config.toml` | `dot_codex/private_config.toml` | Managed as private because Codex writes it with mode `0600`. Remove machine-specific project paths, app paths, and generated plugin/marketplace sections before committing if portability is desired. |
| Codex | `~/.codex/rules/default.rules` | `dot_codex/rules/default.rules` | Remove rules containing personal absolute paths before committing. |
| Codex | `~/.codex/AGENTS.md` | `dot_codex/AGENTS.md` | Optional global instructions, if you use one. |
| Codex | `~/.codex/skills/` | `dot_codex/skills/` | Your custom skills only; do not copy `.system/`. |

Do **not** add authentication, history, caches, session state, databases, logs,
or installed/bundled plugin files. In particular, exclude
`~/.claude/.credentials.json`, `~/.claude.json`, `~/.codex/auth.json`, and
Codex's `cache/`, `plugins/`, `.tmp/`, `sessions/`, `shell_snapshots/`, and
`*.sqlite*` paths.

The rest of each tool directory remains local, so runtime state such as
sessions, history, caches, logs, and databases is not written into this
repository.

Unlike the old symlink-based installer, chezmoi copies rendered content into
place rather than symlinking — a tool that mutates its own config at runtime
(as `dot_codex/config.toml` currently does: trusted-project paths, plugin
timestamps, hook state hashes) won't have those changes reflected back into
the repo automatically. Run `chezmoi re-add` to pull local changes back into
the source before they're lost to the next `chezmoi apply`.

## Zoom transcript meeting notes

`dot_local/bin/executable_summarize-zoom-transcripts.py` scans
`~/Documents/Zoom Transcriptions` and creates one Markdown meeting note per
completed meeting in `~/Documents/Obsidian Vault/ddog/meeting-notes`.
It uses the installed Claude CLI and the managed skill at
`~/.local/share/zoom-transcript-summary/SKILL.md`. Durable state is kept at
`meeting-notes/.processed-state/processed-meetings.json`; state is written only
after a note is atomically created.

The job is installed as the macOS `launchd` agent
`com.seankane.zoom-transcript-summary` and runs at login and every ten minutes.
It prefers `.vtt` over `.txt`, waits five minutes after a file was last
modified, skips previous state entries, and never sends mail or modifies any
external system. Media without a transcript is transcribed only when the
`whisper` CLI is installed; otherwise the job reports the precise file once and
leaves it unprocessed.

The inbox, output location, and agent command are configured in
`~/.config/zoom-transcript-summary/config.json`. This configuration currently
contains Sean's local paths; update it before applying on another machine.

## Adding a new file

Add it under the repo root using chezmoi's naming convention (`dot_` prefix
for a leading dot, `.tmpl` suffix for a templated file) at the path it should
land at under `$HOME`. See chezmoi's
[source state docs](https://www.chezmoi.io/reference/source-state-attributes/).
