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

## Pi agent

chezmoi manages only the portable config under `~/.pi/agent`:

| Local source | Repository path | Notes |
| --- | --- | --- |
| `~/.pi/agent/settings.json` | `dot_pi/agent/settings.json` | Theme, default provider/model, thinking levels, the installed package list, and the `skills` array bridging pi to the Claude skills below (`~/.claude/skills`) so both harnesses share one skill source. Pi reads the live Claude directory, so skills stay in sync for both tools. Claude-only frontmatter is ignored and skills with `disable-model-invocation: true` are still available via `/skill:<name>`. Contains absolute paths to local package checkouts (`~/dd/...`) — review before applying on another machine. |
| `~/.pi/agent/mcp-adapter.json` | `dot_pi/agent/mcp-adapter.json` | MCP servers for the `pi-mcp-adapter` package. The legacy `~/.pi/agent/mcp.json` was merged into this file and removed (neither Pi core nor the adapter reads it anymore). |

Everything else in `~/.pi` stays local: `auth.json` (credentials — never commit;
also blocked by `.chezmoiignore` and chezmoi's secret detection), `sessions/`,
caches (`mcp-cache.json`, `models*.json`), installed packages (`npm/`, `bin/`,
`git/`, `extensions/`), and runtime state (`trust.json`, approvals,
`pi-subagents/`, `powerline-footer/`). These are excluded via `.chezmoiignore`
so an accidental `chezmoi add ~/.pi/...` is a no-op.

Pi rewrites `settings.json` as you use it (e.g. `lastChangelogVersion`), so
local edits drift from the repo; run `chezmoi re-add dot_pi/agent/...` to pull
them in before the next `chezmoi apply` overwrites them.

## Obsidian

chezmoi manages the config of the main vault,
`~/Documents/Obsidian Vault/.obsidian` — never the notes themselves:

| What | Managed? | Notes |
| --- | --- | --- |
| `app.json`, `appearance.json`, `community-plugins.json`, `core-plugins.json`, `graph.json`, `hotkeys.json`, `types.json` | Yes | Core editor settings. |
| `snippets/*.css` | Yes | Custom CSS snippets; add new ones with `chezmoi add`. |
| `themes/` (future custom themes) | Addable | Not present yet; `chezmoi add "~/Documents/Obsidian Vault/.obsidian/themes/<name>.css"` works and the directory is not ignored. |
| `plugins/<id>/manifest.json`, `data.json` | Yes | Version pins + per-plugin settings. |
| `plugins/<id>/main.js`, `styles.css` | Auto-installed | Downloaded by a script (below), not stored in this repo. |
| `plugins/last-modified-tracking/` | Fully | Custom plugin (not in the community catalog) — its `main.js` ships in this repo. |
| `workspace.json` | No | Runtime UI state (open panes), excluded via `.chezmoiignore`. |
| Vault notes, `~/.local`…, everything else under `~/Documents` | No | Blocked by `.chezmoiignore` (`Documents/*` except the vault's `.obsidian`). |

### Plugin code auto-install

`.chezmoiscripts/run_after_install-obsidian-plugins.sh` runs on every
`chezmoi apply`. For each managed plugin missing `main.js` it looks up the
repo in the official community catalog and downloads the release matching
the version pinned in the managed `manifest.json` (falling back to `latest`).
It is a silent no-op when all plugin code is already present, and skips
custom plugins whose `main.js` is managed here. So the fresh-machine flow
is just `chezmoi apply` — settings arrive, then the script fills in plugin
code — no manual installs. Downloaded code can differ bytewise from an
already-installed copy when authors rebuild release assets; the pinned
version is what gets installed.

The `obsidian-backup` vault (`~/git/github.com/spkane31/obsidian-backup`)
manages its own `.obsidian` inside its own git repository and is
deliberately not managed here. Vault notes sync separately via the
obsidian-git plugin.

As with Pi/Codex, plugins rewrite their `data.json` during normal use
(e.g. Excalidraw's counters) — run `chezmoi re-add` to pull local changes
into the source before the next `chezmoi apply` overwrites them.

> **`--source` gotcha:** this checkout is not registered as chezmoi's
> default source directory (`~/.config/chezmoi/chezmoi.toml` has no
> `sourceDir`), so a plain `chezmoi add ~/.foo` silently writes to
> `~/.local/share/chezmoi` instead of this repo. Always pass
> `--source ~/git/github.com/spkane31/dotfiles` (or set `sourceDir` in
> `chezmoi.toml`).

## Adding a new file

Add it under the repo root using chezmoi's naming convention (`dot_` prefix
for a leading dot, `.tmpl` suffix for a templated file) at the path it should
land at under `$HOME`. See chezmoi's
[source state docs](https://www.chezmoi.io/reference/source-state-attributes/).
