#!/usr/bin/env bash
# Symlinks repo files into their local machine paths, backing up any
# pre-existing non-symlink file into .backup/<hostname>/ first.
# To add a new file or directory: append "repo/path:$HOME/local/path" to FILES.
# Missing repo paths are skipped, allowing optional configuration to be added
# incrementally without creating broken symlinks.

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
HOSTNAME="$(hostname -s 2>/dev/null || hostname)"

if [[ "$(uname)" == "Darwin" ]]; then
  VSCODE_SETTINGS="$HOME/Library/Application Support/Code/User/settings.json"
elif grep -qi microsoft /proc/version 2>/dev/null; then
  WIN_APPDATA="$(wslpath "$(cmd.exe /c 'echo %APPDATA%' 2>/dev/null | tr -d '\r\n')")"
  VSCODE_SETTINGS="$WIN_APPDATA/Code/User/settings.json"
else
  VSCODE_SETTINGS="$HOME/.config/Code/User/settings.json"
fi

FILES=(
  ".zshrc:$HOME/.zshrc"
  "vscode-settings.json:$VSCODE_SETTINGS"
  "claude/settings.json:$HOME/.claude/settings.json"
  "claude/CLAUDE.md:$HOME/.claude/CLAUDE.md"
  "claude/skills:$HOME/.claude/skills"
  "codex/config.toml:$HOME/.codex/config.toml"
  "codex/rules/default.rules:$HOME/.codex/rules/default.rules"
  "codex/AGENTS.md:$HOME/.codex/AGENTS.md"
  "codex/skills:$HOME/.codex/skills"
)

linked=0
backed_up=0
ok=0
skipped=0
for entry in "${FILES[@]}"; do
  repo_file="${entry%%:*}"
  local_file="${entry#*:}"
  repo_path="$REPO_DIR/$repo_file"

  if [ ! -e "$repo_path" ] && [ ! -L "$repo_path" ]; then
    echo "SKIPPED        $repo_file (not in repository)"
    ((skipped++))
    continue
  fi

  if [ -L "$local_file" ] && [ "$(readlink "$local_file")" = "$repo_path" ]; then
    echo "OK             $repo_file"
    ((ok++))
    continue
  fi

  if [ -e "$local_file" ] || [ -L "$local_file" ]; then
    backup_path="$REPO_DIR/.backup/$HOSTNAME/$repo_file"
    mkdir -p "$(dirname "$backup_path")"
    mv "$local_file" "$backup_path"
    echo "BACKED UP      $local_file -> .backup/$HOSTNAME/$repo_file"
    ((backed_up++))
  fi

  mkdir -p "$(dirname "$local_file")"
  ln -sfnv "$repo_path" "$local_file"
  ((linked++))
done

echo ""
echo "$ok already linked, $linked newly linked, $backed_up backed up, $skipped skipped."
