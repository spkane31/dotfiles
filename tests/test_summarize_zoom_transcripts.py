"""Tests for Obsidian metadata in Zoom transcript summaries."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ZOOM_SCRIPT = Path(__file__).parents[1] / "dot_local/bin/executable_summarize-zoom-transcripts.py"
ZOOM_SPEC = importlib.util.spec_from_file_location("summarize_zoom_transcripts", ZOOM_SCRIPT)
assert ZOOM_SPEC and ZOOM_SPEC.loader
ZOOM = importlib.util.module_from_spec(ZOOM_SPEC)
ZOOM_SPEC.loader.exec_module(ZOOM)


class ZoomObsidianMetadataTest(unittest.TestCase):
    def test_normalize_note_adds_canonical_properties(self) -> None:
        source = Path("Planning 2026-09-14.vtt")
        note = """---
title: "Planning"
date: 2026-09-14
source: "Planning 2026-09-14.vtt"
---

# Planning

## Executive summary
- Reviewed the plan.
"""

        normalized = ZOOM.normalize_note(note, source)

        self.assertIn('\nsources: "Planning 2026-09-14.vtt"\n', normalized)
        self.assertIn("\nattendees: []\n---\n", normalized)
        self.assertNotIn('\nsource: "Planning 2026-09-14.vtt"', normalized)

    def test_normalize_note_preserves_attendees(self) -> None:
        source = Path("Planning 2026-09-14.vtt")
        note = """---
title: "Planning"
date: 2026-09-14
sources: "Planning 2026-09-14.vtt"
attendees:
  - Alice
  - Bob
---

# Planning

## Executive summary
- Reviewed the plan.
"""

        normalized = ZOOM.normalize_note(note, source)

        self.assertIn("attendees:\n  - Alice\n  - Bob", normalized)

    def test_output_path_recognizes_note_with_sources_property(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "Planning 2026-09-14.vtt"
            source.write_text("WEBVTT\n", encoding="utf-8")
            candidate = root / "notes/2026/09/2026-09-14-planning.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text(
                '---\nsources: "Planning 2026-09-14.vtt"\n---\n',
                encoding="utf-8",
            )

            self.assertEqual(ZOOM.output_path(root / "notes", source), candidate)


if __name__ == "__main__":
    unittest.main()
