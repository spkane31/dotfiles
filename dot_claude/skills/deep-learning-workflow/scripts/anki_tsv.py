#!/usr/bin/env python3
"""Convert learning-card JSON into import-ready Anki TSV files.

The exporter targets Anki's stock Basic and Cloze note types:
- qa, scenario, reconstruction -> Basic (Front, Back)
- cloze -> Cloze (Text, Back Extra)

Tags are emitted as an Anki special tags column, and provenance is folded into
Back/Back Extra so no custom note type is required.
"""

import argparse
import csv
import html
import json
import re
from pathlib import Path

BASIC_KINDS = {"qa", "scenario", "reconstruction"}
SUPPORTED_KINDS = BASIC_KINDS | {"cloze"}
VERIFIED_RE = re.compile(r"^(\d{4})-(\d{2})$")


def clean(value):
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def to_html(value):
    """Treat input as plaintext, escape HTML, and preserve line breaks in Anki."""
    return html.escape(clean(value), quote=False).replace("\n", "<br>")


def normalize_tag(value):
    return clean(value).strip().replace(" ", "_")


def validate_verified(value, card_number):
    if not value:
        return ""
    value = clean(value).strip()
    match = VERIFIED_RE.fullmatch(value)
    if not match or not 1 <= int(match.group(2)) <= 12:
        raise SystemExit(
            f"Card {card_number} has invalid verified value {value!r}; use YYYY-MM"
        )
    return value


def canonical_metadata(card, card_number):
    """Return canonical source/verified metadata, accepting old tags for migration."""
    source = clean(card.get("source")).strip()
    verified = clean(card.get("verified")).strip()
    raw_tags = card.get("tags") or []
    if not isinstance(raw_tags, list):
        raw_tags = [raw_tags]

    regular_tags = []
    legacy_source = ""
    legacy_verified = ""
    for raw in raw_tags:
        tag = normalize_tag(raw)
        if not tag:
            continue
        if tag.startswith("source:"):
            legacy_source = legacy_source or tag[len("source:") :]
            continue
        if tag.startswith("verified:"):
            legacy_verified = legacy_verified or tag[len("verified:") :]
            continue
        regular_tags.append(tag)

    # Dedicated fields are canonical. Legacy provenance tags are accepted only
    # as migration input and are removed from the exported user tag set.
    source = source or legacy_source
    verified = verified or legacy_verified
    verified = validate_verified(verified, card_number)
    return source, verified, regular_tags


def export_tags(user_tags, kind, verified):
    tags = list(user_tags)
    if kind in {"scenario", "reconstruction"}:
        tags.append(f"kind::{kind}")
    if verified:
        tags.append(f"verified::{verified}")

    # Preserve order while removing duplicates.
    return " ".join(dict.fromkeys(tag for tag in tags if tag))


def provenance_html(source, verified):
    bits = []
    if source:
        bits.append(f"<b>Source:</b> {to_html(source)}")
    if verified:
        bits.append(f"<b>Verified:</b> {to_html(verified)}")
    if not bits:
        return ""
    return "<br><br><small>" + "<br>".join(bits) + "</small>"


def basic_back_html(card, source, verified):
    answer = to_html(card.get("back"))
    extra = to_html(card.get("extra"))
    if extra:
        answer += f"<br><br><b>Extra:</b><br>{extra}"
    return answer + provenance_html(source, verified)


def cloze_extra_html(card, source, verified):
    extra = to_html(card.get("extra"))
    return extra + provenance_html(source, verified)


def write_anki_tsv(path, notetype, columns, rows, tags_column):
    """Write Anki file directives followed by data rows; no importable header row."""
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("#separator:Tab\n")
        f.write("#html:true\n")
        f.write(f"#notetype:{notetype}\n")
        f.write(f"#tags column:{tags_column}\n")
        f.write("#columns:" + "\t".join(columns) + "\n")
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("anki-export"))
    parser.add_argument("--basic-notetype", default="Basic")
    parser.add_argument("--cloze-notetype", default="Cloze")
    args = parser.parse_args()

    cards = json.loads(args.input_json.read_text(encoding="utf-8"))
    if not isinstance(cards, list):
        raise SystemExit("Input must be a JSON array of cards")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    basic_rows = []
    cloze_rows = []

    for i, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            raise SystemExit(f"Card {i} must be an object")

        kind = clean(card.get("kind")).strip().lower()
        if kind not in SUPPORTED_KINDS:
            supported = ", ".join(sorted(SUPPORTED_KINDS))
            raise SystemExit(
                f"Card {i} has unsupported kind {kind!r}; supported kinds: {supported}"
            )

        source, verified, user_tags = canonical_metadata(card, i)
        exported_tags = export_tags(user_tags, kind, verified)

        if kind in BASIC_KINDS:
            if not card.get("front") or not card.get("back"):
                raise SystemExit(
                    f"{kind} card {i} requires front and back"
                )
            basic_rows.append(
                [
                    to_html(card["front"]),
                    basic_back_html(card, source, verified),
                    exported_tags,
                ]
            )
        else:
            text = clean(card.get("text"))
            if not re.search(r"\{\{c\d+::", text):
                raise SystemExit(
                    f"Cloze card {i} does not contain an Anki cloze marker like '{{{{c1::...}}}}'"
                )
            cloze_rows.append(
                [
                    to_html(text),
                    cloze_extra_html(card, source, verified),
                    exported_tags,
                ]
            )

    write_anki_tsv(
        args.out_dir / "basic.tsv",
        args.basic_notetype,
        ["Front", "Back", "Tags"],
        basic_rows,
        tags_column=3,
    )
    write_anki_tsv(
        args.out_dir / "cloze.tsv",
        args.cloze_notetype,
        ["Text", "Back Extra", "Tags"],
        cloze_rows,
        tags_column=3,
    )

    print(
        f"Wrote {len(basic_rows)} Basic and {len(cloze_rows)} Cloze notes to {args.out_dir}"
    )


if __name__ == "__main__":
    main()
