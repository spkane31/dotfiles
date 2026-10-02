#!/bin/bash
# Install Obsidian community plugin code (main.js / styles.css) for plugins
# whose manifest.json + data.json settings are managed by chezmoi.
#
# On a fresh machine, chezmoi applies the managed manifests and plugin
# settings, then this script downloads each plugin's code from GitHub
# Releases at the version pinned in the managed manifest.json (falling
# back to the latest release). Repo URLs are looked up in the official
# community plugin catalog. Custom plugins shipped with their main.js in
# this repo (e.g. last-modified-tracking) are skipped — their code is
# already present. The script is a silent no-op when all plugin code
# exists, so it runs on every `chezmoi apply` cheaply.

set -eu

VAULT="$HOME/Documents/Obsidian Vault"
PLUGINS_DIR="$VAULT/.obsidian/plugins"

[ -d "$PLUGINS_DIR" ] || exit 0

missing=()
for dir in "$PLUGINS_DIR"/*/; do
    [ -f "${dir}manifest.json" ] && [ ! -f "${dir}main.js" ] && missing+=("$dir")
done
[ "${#missing[@]}" -eq 0 ] && exit 0

command -v curl >/dev/null 2>&1 || { echo "obsidian plugins: curl not found, skipping install" >&2; exit 0; }
command -v python3 >/dev/null 2>&1 || { echo "obsidian plugins: python3 not found, skipping install" >&2; exit 0; }

CATALOG_URL="https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json"
catalog="$(curl -fsSL "$CATALOG_URL")"

for dir in "${missing[@]}"; do
    id="$(basename "$dir")"
    version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "${dir}manifest.json")"
    repo="$(printf '%s' "$catalog" | python3 -c '
import json, sys
try:
    catalog = json.load(sys.stdin)
    matches = [p["repo"] for p in catalog if p.get("id") == sys.argv[1]]
    print(matches[0] if matches else "")
except Exception:
    print("")' "$id")"

    if [ -z "$repo" ]; then
        echo "obsidian plugins: no community repo for '$id'; not in the catalog — manage its main.js in the dotfiles or install it manually" >&2
        continue
    fi

    installed=""
    for tag in "$version" latest; do
        if curl -fsSL -o "${dir}main.js.part" "https://github.com/$repo/releases/download/$tag/main.js"; then
            mv "${dir}main.js.part" "${dir}main.js"
            installed="$tag"
            break
        fi
    done
    rm -f "${dir}main.js.part"

    if [ -n "$installed" ]; then
        echo "obsidian plugins: installed $id ($installed)"
        if [ ! -f "${dir}styles.css" ]; then
            for tag in "$installed" latest; do
                if curl -fsSL -o "${dir}styles.css.part" "https://github.com/$repo/releases/download/$tag/styles.css"; then
                    mv "${dir}styles.css.part" "${dir}styles.css"
                    break
                fi
            done
            rm -f "${dir}styles.css.part"
        fi
    else
        echo "obsidian plugins: could not download main.js for $id from $repo (version $version)" >&2
    fi
done
