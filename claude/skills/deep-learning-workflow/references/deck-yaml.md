# Deck YAML Reference

## Goal

Write cards in the deck schema used by the learner's personal Anki tool. This is the
**primary** card format for this skill. The stock-Anki TSV export in `anki-export.md`
remains available for importing into Anki itself.

## Schema

```yaml
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
          - championship
          - nba
        priority: 50
```

| Field | Level | Required | Meaning |
|---|---|---|---|
| `id` | deck | yes | stable kebab-case deck slug |
| `name` | deck | yes | human-readable deck title |
| `cards` | deck | yes | list of cards |
| `id` | card | yes | stable, unique, kebab-case card slug |
| `front` | card | yes | prompt shown first |
| `back` | card | yes | answer plus any folded learner context and verification date |
| `date` | card | yes | `YYYY-MM-DD` authoring date (when the card was written) |
| `tags` | card | no | semantic categories and stable search scopes |
| `priority` | card | no | importance, `0-100`, default `50`; higher = more important |

## Card ids

Prefer semantic ids that stay stable if wording changes: `nba-1976`,
`retry-ambiguity`, `btree-branching-factor`. Never renumber existing ids when adding
cards; the id is the identity the learner's tool schedules against.

The exporter fills in `{deck-id}-{NN}` when an id is absent, but authored semantic ids
are better. Duplicate ids are rejected.

## Priority

`priority` encodes importance, not scheduling state. Use the audit rubric in
`card-quality.md` to set it:

| Rubric score | Priority | Meaning |
|---|---|---|
| 9-10 | 70-90 | central idea; forgetting it breaks downstream reasoning |
| 7-8 | 50-65 | solid supporting knowledge |
| 6 | 30-45 | useful but peripheral |
| <6 | do not add | rewrite, or move to notes/practice |

Reserve 90+ for the handful of ideas that anchor a whole subsystem or chapter. Default
to `50` when unsure rather than inflating everything.

## The four learning kinds in a front/back schema

The schema has only `front` and `back`, so kinds are preserved as follows:

| Kind | front | back | tag added |
|---|---|---|---|
| `qa` | question | answer | none |
| `scenario` | situation + "what do you check?" | reasoning to retrieve | `scenario` |
| `reconstruction` | "reconstruct X" | skeleton to check against | `reconstruction` |
| `cloze` | text with `{{c1::...}}` markers intact | same text with deletions revealed | `cloze` |

Cloze cards keep valid Anki markers on the front so the same card survives a later
import into real Anki. The back shows the revealed sentence, so the card still grades
cleanly in a plain front/back reviewer.

## Source comments and folded back content

The schema has no `extra`/`source`/`verified` fields. Render `source` as a YAML comment
beside the card so provenance remains in the authored file but is not shown on the
card. Append `extra` and `verified` to `back`, separated by blank lines, in that order:

```yaml
      - id: retry-ambiguity
        # Source: payments/worker; PR #12345
        front: What must you establish before retrying an ambiguous operation?
        back: "Whether the operation is idempotent.\n\nExtra: Recognition card for partial-failure boundaries.\n\nVerified: 2026-08"
```

Keep `tags` for concepts and stable scopes such as `system::payments::worker`. Do not
author `source:` or `verified:` tags; the exporter migrates those legacy tags into the
source comment and folded back text, respectively.

## Generating the file

Author cards as JSON (see `card-quality.md`), then run:

```bash
python scripts/deck_yaml.py cards.json \
  --out decks.yaml \
  --deck-id nba-champions \
  --deck-name "NBA Champions"
```

Useful flags:

- `--date YYYY-MM-DD` — authoring date for cards without their own `date` (defaults to today);
- `--default-priority N` — default importance (defaults to `50`);
- per-card `deck` / `deck_name` in the JSON split one input file into multiple decks, emitted in first-seen order.

Writing the YAML by hand is fine for a handful of cards. When you do, quote any `front`
or `back` containing `{{`, `:`, `#`, a leading special character, or an embedded newline
(`\n` escapes inside double quotes).

## Verification

After changing the exporter, run:

```bash
python scripts/test_deck_yaml.py
```

The regression test covers all four kinds, deck grouping, id derivation and uniqueness,
date/priority validation, source comments, cloze reveal, and YAML quoting/escaping.
