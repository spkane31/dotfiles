#!/usr/bin/env python3
"""Write a weekday morning brief using the services available to Claude."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CONFIG = Path.home() / ".config/morning-brief/config.json"
PROMPT = Path.home() / ".local/share/morning-brief/PROMPT.md"
TIME_ZONE = ZoneInfo("America/Denver")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def destination_for(output_dir: Path, now: datetime) -> Path:
    return output_dir / f"{now.astimezone(TIME_ZONE):%Y%m%d}.md"


def normalize_note(note: str) -> str:
    note = note.strip()
    if note.startswith("```") and note.endswith("```"):
        note = re.sub(r"^```[^\n]*\n", "", note)
        note = re.sub(r"\n```$", "", note).strip()
    frontmatter = re.search(r"(?m)^---\s*$", note)
    if frontmatter and frontmatter.start() > 0:
        note = note[frontmatter.start():]
    return note.rstrip() + "\n"


def validate_note(note: str, today: datetime) -> None:
    expected_date = today.astimezone(TIME_ZONE).date().isoformat()
    if not note.startswith("---\n"):
        raise ValueError("agent output has no YAML frontmatter")
    if f"date: {expected_date}" not in note.split("---", 2)[1]:
        raise ValueError(f"agent output does not contain date: {expected_date}")
    if "# " not in note or "## The day" not in note or "## Needs attention" not in note:
        raise ValueError("agent output is missing required note sections")
    if "```" in note or re.search(r"<\/?(?:html|svg)\b", note, flags=re.I):
        raise ValueError("agent output contains an unsupported artifact")


def notify(title: str, body: str, enabled: bool) -> None:
    if not enabled:
        return
    subprocess.run(
        ["/usr/bin/osascript", "-e", f"display notification {json.dumps(body)} with title {json.dumps(title)}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def create_brief(config: dict, now: datetime) -> str:
    prompt = PROMPT.read_text(encoding="utf-8")
    today = now.astimezone(TIME_ZONE)
    prompt += f"""

Run date: {today:%Y-%m-%d} ({today:%A}) in America/Denver.
Return only the completed Markdown note. Do not write files yourself, use
HTML, SVG, code fences, action buttons, or explain your work. The caller will
validate and atomically write your response to the required output file.
"""
    result = subprocess.run(config["provider_command"], input=prompt, text=True,
                            capture_output=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1:] or ["provider returned a non-zero exit status"]
        raise RuntimeError("Claude failed: " + detail[0])
    note = normalize_note(result.stdout)
    validate_note(note, now)
    return note


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="generate but do not write the note")
    args = parser.parse_args()

    try:
        config = load_json(CONFIG)
        required = {"output_directory", "provider_command", "notify"}
        if not required <= config.keys() or not PROMPT.is_file():
            raise RuntimeError(f"missing configuration ({CONFIG}) or prompt ({PROMPT})")
        now = datetime.now(TIME_ZONE)
        destination = destination_for(Path(config["output_directory"]), now)
        note = create_brief(config, now)
        if args.dry_run:
            print(f"Would write: {destination}")
            return 0
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                         prefix=".tmp-", delete=False) as f:
            f.write(note)
            temporary = Path(f.name)
        os.replace(temporary, destination)
        print(f"Created: {destination}")
        notify("Morning brief created", destination.name, config["notify"])
        return 0
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        notify("Morning brief needs action", str(error), True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
