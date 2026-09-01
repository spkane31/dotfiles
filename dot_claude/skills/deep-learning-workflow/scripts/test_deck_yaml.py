#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("deck_yaml.py")

try:
    import yaml
except ImportError:  # PyYAML is optional; string assertions cover the rest.
    yaml = None


def run(args, expect_success=True):
    result = subprocess.run(
        [str(SCRIPT), *args], capture_output=True, text=True
    )
    if expect_success:
        assert result.returncode == 0, result.stderr + result.stdout
    return result


class DeckYamlExportTests(unittest.TestCase):
    def export(self, cards, extra_args=(), expect_success=True):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        input_path = root / "cards.json"
        out_path = root / "decks.yaml"
        input_path.write_text(json.dumps(cards), encoding="utf-8")
        result = run(
            [
                str(input_path),
                "--out",
                str(out_path),
                "--deck-id",
                "study",
                "--deck-name",
                "Study",
                "--date",
                "2026-08-17",
                *extra_args,
            ],
            expect_success=expect_success,
        )
        text = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        return text, result

    def test_all_four_kinds_map_into_the_deck_schema(self):
        cards = [
            {
                "kind": "qa",
                "id": "rpc-in-txn",
                "front": "Why is a remote RPC inside a transaction risky?",
                "back": "It holds locks.\nIt widens the failure window.",
                "extra": "if x < y then commit",
                "tags": ["engineering", "transactions"],
                "source": "chapter 7",
                "priority": 70,
            },
            {
                "kind": "scenario",
                "front": 'Two workers read then write "state". What do you inspect?',
                "back": "The race between the read and the conditional write.",
                "tags": ["system::payments::worker"],
                "source": "payments/worker",
                "verified": "2026-08",
            },
            {
                "kind": "reconstruction",
                "front": "Reconstruct the write path.",
                "back": "API -> queue -> worker -> store",
            },
            {
                "kind": "cloze",
                "text": "Dijkstra assumes {{c1::non-negative edge weights}}.",
                "extra": "Negative edges break greedy finalization.",
                "tags": ["algorithms"],
            },
        ]
        text, _ = self.export(cards)

        # Deck envelope.
        self.assertTrue(text.startswith("decks:\n"))
        self.assertIn("  - id: study\n", text)
        self.assertIn("    name: Study\n", text)
        self.assertIn("    cards:\n", text)

        # Authored id kept; missing ids derived from the deck id and position.
        self.assertIn("      - id: rpc-in-txn\n", text)
        self.assertIn("      - id: study-02\n", text)

        # Card fields.
        self.assertIn("        date: 2026-08-17\n", text)
        self.assertIn("        priority: 70\n", text)
        self.assertIn("        priority: 50\n", text)
        self.assertIn("          - engineering\n", text)

        # Kind is a plain tag for non-qa cards so front/back stays the shape.
        self.assertIn("          - scenario\n", text)
        self.assertIn("          - reconstruction\n", text)
        self.assertIn("          - cloze\n", text)

        # Newlines, quotes, extra context, and verification are folded into the
        # quoted back field. Source provenance is a YAML comment instead.
        self.assertIn("It holds locks.\\nIt widens the failure window.", text)
        self.assertIn("Extra: if x < y then commit", text)
        self.assertIn("        # Source: chapter 7\n", text)
        self.assertIn("Verified: 2026-08", text)
        self.assertIn('read then write \\"state\\"', text)

        # Cloze keeps its markers on the front and reveals the text on the back.
        self.assertIn("{{c1::non-negative edge weights}}", text)
        self.assertIn("Dijkstra assumes non-negative edge weights.", text)

    @unittest.skipIf(yaml is None, "PyYAML not installed")
    def test_source_is_a_comment_not_card_back_content(self):
        cards = [
            {
                "kind": "qa",
                "front": "What is the answer?",
                "back": "The answer.",
                "source": "chapter 7\nsection #2",
            }
        ]
        text, _ = self.export(cards)

        self.assertIn("        # Source: chapter 7\n", text)
        self.assertIn("        # section #2\n", text)
        parsed_card = yaml.safe_load(text)["decks"][0]["cards"][0]
        self.assertEqual("The answer.", parsed_card["back"])
        self.assertNotIn("source", parsed_card)

    @unittest.skipIf(yaml is None, "PyYAML not installed")
    def test_output_parses_as_the_expected_yaml_structure(self):
        cards = [
            {
                "kind": "qa",
                "front": "NBA Champion in 1976",
                "back": "Boston Celtics",
                "tags": ["sports", "nba"],
            }
        ]
        text, _ = self.export(cards)
        parsed = yaml.safe_load(text)
        deck = parsed["decks"][0]
        self.assertEqual("study", deck["id"])
        self.assertEqual("Study", deck["name"])
        card = deck["cards"][0]
        self.assertEqual("NBA Champion in 1976", card["front"])
        self.assertEqual("Boston Celtics", card["back"])
        self.assertEqual(["sports", "nba"], card["tags"])
        self.assertEqual(50, card["priority"])
        self.assertEqual("2026-08-17", str(card["date"]))

    def test_cards_group_into_multiple_decks_in_first_seen_order(self):
        cards = [
            {"kind": "qa", "front": "A", "back": "1", "deck": "algos", "deck_name": "Algorithms"},
            {"kind": "qa", "front": "B", "back": "2"},
            {"kind": "qa", "front": "C", "back": "3", "deck": "algos"},
        ]
        text, _ = self.export(cards)
        self.assertLess(text.index("  - id: algos\n"), text.index("  - id: study\n"))
        self.assertIn("    name: Algorithms\n", text)
        self.assertIn("      - id: algos-01\n", text)
        self.assertIn("      - id: algos-03\n", text)
        self.assertIn("      - id: study-02\n", text)

    def test_invalid_priority_rejected(self):
        cards = [{"kind": "qa", "front": "A", "back": "1", "priority": 101}]
        _, result = self.export(cards, expect_success=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("priority", result.stderr + result.stdout)

    def test_invalid_date_rejected(self):
        cards = [{"kind": "qa", "front": "A", "back": "1", "date": "08/17/2026"}]
        _, result = self.export(cards, expect_success=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("YYYY-MM-DD", result.stderr + result.stdout)

    def test_cloze_without_marker_rejected(self):
        cards = [{"kind": "cloze", "text": "Dijkstra assumes non-negative weights."}]
        _, result = self.export(cards, expect_success=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("cloze", result.stderr + result.stdout)

    def test_duplicate_ids_rejected(self):
        cards = [
            {"kind": "qa", "id": "dupe", "front": "A", "back": "1"},
            {"kind": "qa", "id": "dupe", "front": "B", "back": "2"},
        ]
        _, result = self.export(cards, expect_success=False)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("dupe", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
