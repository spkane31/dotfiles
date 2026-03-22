#!/usr/bin/env bash
# Maps repo files to their local machine paths.
# To add a new file: append "repo/file:$HOME/local/path" to FILES.

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

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
)

changes=0
for entry in "${FILES[@]}"; do
  repo_file="${entry%%:*}"
  local_file="${entry#*:}"
  if [ ! -f "$local_file" ]; then
    echo "MISSING  $local_file"
    ((changes++))
  elif ! diff -q "$REPO_DIR/$repo_file" "$local_file" > /dev/null 2>&1; then
    echo "DIFFERS  $repo_file <-> $local_file"
    # diff "$REPO_DIR/$repo_file" "$local_file"
    ((changes++))
  else
    echo "OK       $repo_file"
  fi
done

echo ""
[ "$changes" -eq 0 ] && echo "All files match." || echo "$changes file(s) differ or missing."
