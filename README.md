# dotfiles

Config files, symlinked into place on any machine via `install.sh`.

## Install

    git clone https://github.com/spkane31/dotfiles.git ~/dotfiles
    ~/dotfiles/install.sh

Existing files at the destination are backed up to `.backup/<hostname>/`
inside this repo before being replaced with a symlink. Re-running is safe —
files already linked correctly are left untouched. Optional entries that are
not yet present in the repository are reported as `SKIPPED`.

## Claude and Codex

The installer links only the portable configuration below. Copy those files
and directories into the matching repository paths; do not copy a whole local
tool directory wholesale.

| Tool | Local source | Repository path | Notes |
| --- | --- | --- | --- |
| Claude | `~/.claude/settings.json` | `claude/settings.json` | Already managed. Review permissions and plugin settings before committing. |
| Claude | `~/.claude/CLAUDE.md` | `claude/CLAUDE.md` | Global instructions. |
| Claude | `~/.claude/skills/` | `claude/skills/` | Your custom skills only. |
| Codex | `~/.codex/config.toml` | `codex/config.toml` | Remove machine-specific project paths, app paths, and generated plugin/marketplace sections first. |
| Codex | `~/.codex/rules/default.rules` | `codex/rules/default.rules` | Remove rules containing personal absolute paths before committing. |
| Codex | `~/.codex/AGENTS.md` | `codex/AGENTS.md` | Optional global instructions, if you use one. |
| Codex | `~/.codex/skills/` | `codex/skills/` | Your custom skills only; do not copy `.system/`. |

Do **not** add authentication, history, caches, session state, databases, logs,
or installed/bundled plugin files. In particular, exclude
`~/.claude/.credentials.json`, `~/.claude.json`, `~/.codex/auth.json`, and
Codex's `cache/`, `plugins/`, `.tmp/`, `sessions/`, `shell_snapshots/`, and
`*.sqlite*` paths.

The rest of each tool directory remains local, so runtime state such as
sessions, history, caches, logs, and databases is not written into this
repository.

## Adding a new file

Append an entry to the `FILES` array in `install.sh`:

    "path/in/repo:$HOME/local/path"

Both files and directories can be linked. The source must exist in the
repository before the installer will link it.
