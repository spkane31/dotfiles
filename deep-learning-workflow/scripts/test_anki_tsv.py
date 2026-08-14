#!/usr/bin/env python3
import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("anki_tsv.py")


class AnkiTsvExportTests(unittest.TestCase):
    def test_stock_note_types_four_kinds_provenance_and_html_newlines(self):
        cards = [
            {
                "kind": "qa",
                "front": "Why can a remote RPC\ninside a transaction be risky?",
                "back": "It holds locks.\nIt also widens failure windows.",
                "extra": "if x < y then commit",
                "tags": ["engineering", "transactions"],
                "source": "chapter 7",
            },
            {
                "kind": "scenario",
                "front": "Two workers read then write. What should you inspect?",
                "back": "Look for a race between the read and conditional write.",
                "tags": ["system::payments::worker"],
                "source": "payments/worker",
                "verified": "2026-08",
            },
            {
                "kind": "reconstruction",
                "front": "Reconstruct the write path.",
                "back": "API -> queue -> worker -> store",
                "source": "architecture/write-path",
            },
            {
                "kind": "cloze",
                "text": "Dijkstra assumes {{c1::non-negative edge weights}}.",
                "extra": "Negative edges can break greedy finalization.\nCheck Bellman-Ford.",
                "tags": ["algorithms"],
                "source": "Algorithms ch. 24",
            },
        ]

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            input_path = root / "cards.json"
            out_dir = root / "out"
            input_path.write_text(json.dumps(cards), encoding="utf-8")
            subprocess.run(
                [str(SCRIPT), str(input_path), "--out-dir", str(out_dir)],
                check=True,
                capture_output=True,
                text=True,
            )

            basic_text = (out_dir / "basic.tsv").read_text(encoding="utf-8")
            cloze_text = (out_dir / "cloze.tsv").read_text(encoding="utf-8")

            self.assertTrue(basic_text.startswith("#separator:Tab\n#html:true\n#notetype:Basic\n"))
            self.assertIn("#tags column:3\n", basic_text)
            self.assertIn("#columns:Front\tBack\tTags\n", basic_text)
            self.assertNotIn("\nFront\tBack\t", basic_text)
            self.assertIn("RPC<br>inside", basic_text)
            self.assertIn("locks.<br>It also", basic_text)
            self.assertIn("if x &lt; y then commit", basic_text)
            self.assertIn("kind::scenario", basic_text)
            self.assertIn("kind::reconstruction", basic_text)
            self.assertIn("verified::2026-08", basic_text)
            self.assertIn("<b>Source:</b> payments/worker", basic_text)
            self.assertIn("<b>Verified:</b> 2026-08", basic_text)

            self.assertTrue(cloze_text.startswith("#separator:Tab\n#html:true\n#notetype:Cloze\n"))
            self.assertIn("#tags column:3\n", cloze_text)
            self.assertIn("#columns:Text\tBack Extra\tTags\n", cloze_text)
            self.assertNotIn("\nText\tBack Extra\t", cloze_text)
            self.assertIn("finalization.<br>Check Bellman-Ford.", cloze_text)

            # After comment directives, every data row has exactly 3 columns.
            basic_data = [line for line in basic_text.splitlines() if not line.startswith("#")]
            cloze_data = [line for line in cloze_text.splitlines() if not line.startswith("#")]
            self.assertEqual(3, len(basic_data))
            self.assertEqual(1, len(cloze_data))
            for row in csv.reader(basic_data, delimiter="\t"):
                self.assertEqual(3, len(row))
            for row in csv.reader(cloze_data, delimiter="\t"):
                self.assertEqual(3, len(row))

    def test_legacy_provenance_tags_are_migrated_not_duplicated(self):
        cards = [
            {
                "kind": "scenario",
                "front": "Prompt",
                "back": "Answer",
                "tags": ["source:payments/worker", "verified:2026-08", "work"],
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            input_path = root / "cards.json"
            out_dir = root / "out"
            input_path.write_text(json.dumps(cards), encoding="utf-8")
            subprocess.run(
                [str(SCRIPT), str(input_path), "--out-dir", str(out_dir)],
                check=True,
                capture_output=True,
                text=True,
            )
            text = (out_dir / "basic.tsv").read_text(encoding="utf-8")
            self.assertNotIn("source:payments/worker", text)
            self.assertNotIn("verified:2026-08", text)
            self.assertIn("<b>Source:</b> payments/worker", text)
            self.assertIn("verified::2026-08", text)

    def test_invalid_verified_rejected(self):
        cards = [
            {
                "kind": "qa",
                "front": "Prompt",
                "back": "Answer",
                "verified": "2026-13",
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            input_path = root / "cards.json"
            input_path.write_text(json.dumps(cards), encoding="utf-8")
            result = subprocess.run(
                [str(SCRIPT), str(input_path), "--out-dir", str(root / "out")],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("use YYYY-MM", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
