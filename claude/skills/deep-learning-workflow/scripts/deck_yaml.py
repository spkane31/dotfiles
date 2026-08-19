#!/usr/bin/env python3
"""Convert learning-card JSON into the personal-Anki deck YAML schema.

Output shape (one file, one or more decks):

    decks:
      - id: nba-champions
        name: NBA Champions
        cards:
          - id: nba-1976
            front: NBA Champion in 1976
            back: "Boston Celtics"
            date: 2026-08-14
            tags:
              - sports
              - nba
            priority: 50

The schema is front/back only, so:
- qa/scenario/reconstruction map straight to front/back;
- cloze keeps its {{cN::...}} markers on the front and reveals the text on the back;
- kind is preserved as a plain tag for non-qa cards;
- extra/verified are folded into the back field;
- source is rendered as a YAML comment and is not card content.

`date` is the authoring date and `priority` is importance (0-100, default 50).
"""

import argparse
import json
import re
from datetime import date as date_cls
from pathlib import Path

BASIC_KINDS = {"qa", "scenario", "reconstruction"}
SUPPORTED_KINDS = BASIC_KINDS | {"cloze"}
CLOZE_RE = re.compile(r"\{\{c\d+::(.*?)(?:::.*?)?\}\}", re.DOTALL)
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERIFIED_RE = re.compile(r"^\d{4}-\d{2}$")
PLAIN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._/()#?!'-]*$")
YAML_KEYWORDS = {"true", "false", "null", "yes", "no", "on", "off", "~"}


def clean(value):
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def scalar(value):
    """Render a string as a plain YAML scalar when safe, else double-quoted."""
    text = clean(value)
    if (
        PLAIN_RE.fullmatch(text)
        and not text.endswith(" ")
        and text.lower() not in YAML_KEYWORDS
        and not _looks_numeric(text)
    ):
        return text
    escaped = (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def _looks_numeric(text):
    try:
        float(text)
    except ValueError:
        return False
    return True


def normalize_tag(value):
    return clean(value).strip().replace(" ", "_")


def fail(message):
    raise SystemExit(message)


def validate_date(value, card_number):
    value = clean(value).strip()
    if not DATE_RE.fullmatch(value):
        fail(f"Card {card_number} has invalid date {value!r}; use YYYY-MM-DD")
    try:
        date_cls.fromisoformat(value)
    except ValueError:
        fail(f"Card {card_number} has invalid date {value!r}; use YYYY-MM-DD")
    return value


def validate_priority(value, card_number):
    if isinstance(value, bool) or not isinstance(value, int):
        fail(f"Card {card_number} has non-integer priority {value!r}; use 0-100")
    if not 0 <= value <= 100:
        fail(f"Card {card_number} has out-of-range priority {value!r}; use 0-100")
    return value


def canonical_metadata(card, card_number):
    """Return source/verified/tags, accepting legacy provenance tags as input."""
    source = clean(card.get("source")).strip()
    verified = clean(card.get("verified")).strip()
    raw_tags = card.get("tags") or []
    if not isinstance(raw_tags, list):
        raw_tags = [raw_tags]

    tags = []
    legacy_source = ""
    legacy_verified = ""
    for raw in raw_tags:
        tag = normalize_tag(raw)
        if not tag:
            continue
        if tag.startswith("source:") and not tag.startswith("source::"):
            legacy_source = legacy_source or tag[len("source:") :]
            continue
        if tag.startswith("verified:") and not tag.startswith("verified::"):
            legacy_verified = legacy_verified or tag[len("verified:") :]
            continue
        tags.append(tag)

    source = source or legacy_source
    verified = verified or legacy_verified
    if verified and not VERIFIED_RE.fullmatch(verified):
        fail(f"Card {card_number} has invalid verified value {verified!r}; use YYYY-MM")
    return source, verified, tags


def build_back(answer, extra, verified):
    parts = [clean(answer).strip()]
    if clean(extra).strip():
        parts.append(f"Extra: {clean(extra).strip()}")
    if verified:
        parts.append(f"Verified: {verified}")
    return "\n\n".join(part for part in parts if part)


def source_comment(source, indent):
    """Render source provenance as YAML comments at the given indentation."""
    if not source:
        return []
    first, *rest = source.split("\n")
    lines = [f"{indent}# Source: {first}"]
    lines.extend(f"{indent}# {line}" if line else f"{indent}#" for line in rest)
    return lines


def reveal_cloze(text):
    return CLOZE_RE.sub(lambda m: m.group(1), text)


def convert(cards, default_deck_id, default_deck_name, default_date, default_priority):
    decks = {}
    order = []
    seen_ids = set()

    for i, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            fail(f"Card {i} must be an object")

        kind = clean(card.get("kind")).strip().lower() or "qa"
        if kind not in SUPPORTED_KINDS:
            supported = ", ".join(sorted(SUPPORTED_KINDS))
            fail(f"Card {i} has unsupported kind {kind!r}; supported kinds: {supported}")

        deck_id = clean(card.get("deck")).strip() or default_deck_id
        if not deck_id:
            fail(f"Card {i} has no deck; pass --deck-id or set a per-card deck")
        if not ID_RE.fullmatch(deck_id):
            fail(f"Card {i} has invalid deck id {deck_id!r}; use letters, digits, . _ -")

        card_id = clean(card.get("id")).strip() or f"{deck_id}-{i:02d}"
        if not ID_RE.fullmatch(card_id):
            fail(f"Card {i} has invalid id {card_id!r}; use letters, digits, . _ -")
        if card_id in seen_ids:
            fail(f"Card {i} repeats id {card_id!r}; card ids must be unique")
        seen_ids.add(card_id)

        source, verified, tags = canonical_metadata(card, i)
        if kind != "qa":
            tags.append(kind)

        if kind == "cloze":
            text = clean(card.get("text")) or clean(card.get("front"))
            if not CLOZE_RE.search(text):
                fail(
                    f"Card {i} is a cloze card without an Anki cloze marker like "
                    "'{{c1::...}}'"
                )
            front = text
            answer = clean(card.get("back")).strip() or reveal_cloze(text)
        else:
            front = clean(card.get("front")).strip()
            answer = clean(card.get("back")).strip()
            if not front or not answer:
                fail(f"{kind} card {i} requires front and back")

        entry = {
            "id": card_id,
            "source": source,
            "front": front,
            "back": build_back(answer, card.get("extra"), verified),
            "date": validate_date(card.get("date") or default_date, i),
            "tags": list(dict.fromkeys(tags)),
            "priority": validate_priority(
                card["priority"] if "priority" in card else default_priority, i
            ),
        }

        if deck_id not in decks:
            decks[deck_id] = {"id": deck_id, "name": "", "cards": []}
            order.append(deck_id)
        deck = decks[deck_id]
        name = clean(card.get("deck_name")).strip()
        if name and not deck["name"]:
            deck["name"] = name
        deck["cards"].append(entry)

    for deck_id in order:
        deck = decks[deck_id]
        if not deck["name"]:
            deck["name"] = default_deck_name or deck_id
    return [decks[deck_id] for deck_id in order]


def render(decks):
    lines = ["decks:"]
    for deck in decks:
        lines.append(f"  - id: {scalar(deck['id'])}")
        lines.append(f"    name: {scalar(deck['name'])}")
        lines.append("    cards:")
        for card in deck["cards"]:
            lines.append(f"      - id: {scalar(card['id'])}")
            lines.extend(source_comment(card["source"], "        "))
            lines.append(f"        front: {scalar(card['front'])}")
            lines.append(f"        back: {scalar(card['back'])}")
            lines.append(f"        date: {card['date']}")
            if card["tags"]:
                lines.append("        tags:")
                lines.extend(f"          - {scalar(tag)}" for tag in card["tags"])
            lines.append(f"        priority: {card['priority']}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--out", type=Path, default=Path("decks.yaml"))
    parser.add_argument("--deck-id", default="", help="deck id for cards without one")
    parser.add_argument("--deck-name", default="", help="deck name for cards without one")
    parser.add_argument(
        "--date", default="", help="authoring date for cards without one (YYYY-MM-DD)"
    )
    parser.add_argument("--default-priority", type=int, default=50)
    args = parser.parse_args()

    cards = json.loads(args.input_json.read_text(encoding="utf-8"))
    if not isinstance(cards, list):
        fail("Input must be a JSON array of cards")

    default_date = args.date.strip() or date_cls.today().isoformat()
    decks = convert(
        cards,
        args.deck_id.strip(),
        args.deck_name.strip(),
        default_date,
        args.default_priority,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(decks), encoding="utf-8")
    total = sum(len(deck["cards"]) for deck in decks)
    print(f"Wrote {total} cards across {len(decks)} deck(s) to {args.out}")


if __name__ == "__main__":
    main()
