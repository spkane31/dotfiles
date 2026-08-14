# Anki Export Reference

## Goal

Export learning cards so they import into Anki's stock **Basic** and **Cloze** note types without requiring custom fields or a custom note type.

## Kind mapping

| Learning kind | Anki note type | Input fields | Exported regular fields |
|---|---|---|---|
| `qa` | Basic | `front`, `back` | Front, Back |
| `scenario` | Basic | `front`, `back` | Front, Back |
| `reconstruction` | Basic | `front`, `back` | Front, Back |
| `cloze` | Cloze | `text`, `extra` | Text, Back Extra |

`scenario` and `reconstruction` remain distinct learning kinds even though they share Anki's Basic storage shape. The exporter adds `kind::scenario` or `kind::reconstruction` so they remain searchable.

## Import-file layout

`basic.tsv` begins with Anki file directives like:

```text
#separator:Tab
#html:true
#notetype:Basic
#tags column:3
#columns:Front<TAB>Back<TAB>Tags
```

`cloze.tsv` uses the same pattern with `#notetype:Cloze` and `#columns:Text<TAB>Back Extra<TAB>Tags`.

Do **not** add a normal `Front<TAB>Back...` header row. Anki imports the first non-comment line as data; only `#...` directive/comment lines are skipped.

The third column is declared with `#tags column:3`, so it becomes Anki note tags instead of a literal third field. The two remaining regular columns therefore line up with stock Basic (`Front`, `Back`) or stock Cloze (`Text`, `Back Extra`).

## Extra and provenance

Stock Basic has no Extra or Source fields. Preserve those values without a custom note type as follows:

- `extra` is appended to Basic's `Back`; for Cloze it is placed in `Back Extra`.
- `source` is appended as provenance on `Back` / `Back Extra`.
- `verified` is appended as provenance and also exported as `verified::YYYY-MM` so stale codebase cards can be searched.
- scenario/reconstruction type is preserved with a `kind::...` tag.

Treat `source` and `verified` as canonical. Use `tags` for concepts and stable scopes such as `system::payments::worker`; do not author duplicate `source:` or `verified:` tags.

## Newlines and HTML safety

Anki renders note fields as HTML. The exporter treats JSON card content as plaintext, HTML-escapes `<`, `>`, and `&`, and converts embedded newlines to `<br>`. It emits `#html:true`, so line breaks render rather than collapsing.

This also avoids relying on quoted physical multi-line TSV cells, which are awkward for cloze notes and unnecessary when `<br>` is available.

## Custom note-type names

The defaults are `Basic` and `Cloze`. If the target profile renamed them, pass explicit names:

```bash
python scripts/anki_tsv.py cards.json --out-dir anki-export \
  --basic-notetype "My Basic" \
  --cloze-notetype "My Cloze"
```

The field layout still assumes two regular fields in Basic and two in Cloze. If the user intentionally wants richer dedicated fields such as Source or Verified, build a separate custom-note-type exporter instead of silently changing this stock-compatible format.

## Verification

After changing the exporter, run:

```bash
python scripts/test_anki_tsv.py
```

The regression test checks all four card kinds, stock note-type directives, special tag-column metadata, absence of an importable header row, provenance handling, and HTML newline conversion.
