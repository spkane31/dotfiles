# Card Quality Reference

## Purpose

Use spaced repetition for knowledge that should be retrievable quickly and repeatedly in future reasoning. Do not use it as a storage system for everything encountered.

## Representation chooser

| Knowledge | Preferred representation | Example |
|---|---|---|
| Precise concept/fact | Q/A | "Why does Dijkstra fail with negative edges?" |
| Exact term/notation/formula fragment | Cloze | "Dijkstra requires {{c1::non-negative edge weights}}." |
| Engineering recognition/judgment | Scenario | "Two workers read then conditionally write. What race should you check for?" |
| Algorithm/system structure | Reconstruction | "Sketch the stages of the write path and identify the commit boundary." |
| Procedure/skill | Practice, optionally plus cards | Implement, debug, derive, analyze, design |
| Diagram/spatial relationship | Image occlusion when available | Architecture diagram labels |

## High-value card properties

A good card:
- tests one retrievable idea or one tightly coupled relationship;
- contains enough context to be unambiguous months later;
- has an answer that can usually be judged in under 20 seconds;
- asks for production/retrieval rather than recognition;
- remains useful after superficial implementation details change;
- is connected to a reason the learner cares about.

Prefer prompts such as:
- Why does X happen?
- Under what conditions does X fail?
- What invariant is X protecting?
- How can you distinguish X from Y?
- Given this symptom, where would you investigate first and why?
- What must be true before X is safe?
- What is the next conceptual step in reconstructing X?

## Anti-patterns

Reject or rewrite cards that:
- quote a sentence and ask for a missing arbitrary noun;
- contain long lists with no natural chunking;
- ask "What does this chapter say about X?" without a precise target;
- depend on remembering the exact surrounding page;
- encode mutable filenames/line numbers as the answer when the underlying concept matters more;
- ask several independent questions at once;
- simply duplicate documentation;
- test a coding skill that can only be learned through doing.

## Cloze rules

Use cloze when exact completion is genuinely useful: terminology, short definitions, notation, formula components, short ordered relationships.

Good:
`A B-tree reduces storage I/O by using a {{c1::high branching factor}}, so each node can correspond efficiently to a storage block/page.`

Weak:
`A {{c1::B-tree}} is a {{c2::self-balancing tree}} that {{c3::maintains sorted data}} and ...`

Do not turn whole paragraphs into cloze notes. Do not hide the only cue that identifies what is being asked.

## Card audit rubric

Score each candidate 0-2 on each dimension:

1. **Importance**: Would forgetting this materially hurt understanding, debugging, review, application, or further learning?
2. **Retrievability**: Does the prompt cue one clear answer?
3. **Transfer**: Will retrieving it help beyond this exact paragraph/example?
4. **Stability**: Is it likely to remain useful long enough to justify reviews?
5. **Atomicity**: Is the recall burden appropriately small?

Interpretation:
- 8-10: strong card;
- 6-7: keep if central, otherwise revise;
- 4-5: usually rewrite or move to notes/practice;
- 0-3: do not add.

## Coverage audit

When comparing cards against a source, first identify the source's 3-7 central ideas. Then map cards to those ideas. Do not judge quality by number of cards.

Look especially for missing:
- causal explanation;
- boundary conditions;
- contrasts/confusions;
- prerequisites;
- failure cases;
- implications;
- application triggers.

## JSON schema for export

Store cards as a JSON array. The exporter accepts all four learning kinds: `qa`, `cloze`, `scenario`, and `reconstruction`. `qa`, `scenario`, and `reconstruction` use `front`/`back` and are exported to Anki's stock **Basic** note type. `cloze` uses `text` and is exported to the stock **Cloze** note type.

Use metadata consistently:
- `source`: canonical exact provenance pointer, such as a chapter/section, PR, architecture doc, or code responsibility. Do not duplicate it as a `source:` tag.
- `verified`: optional `YYYY-MM` for knowledge tied to a mutable system/codebase. The exporter renders it on the back and derives a `verified::YYYY-MM` search tag.
- `tags`: semantic categories and stable search scopes, for example `engineering`, `transactions`, or `system::payments::worker`. Do not manually encode `source:` or `verified:` provenance here.
- `extra`: learner-facing context/example that should appear on the back, not provenance.

For migration, the exporter accepts legacy `source:...` / `verified:...` tags when the dedicated field is absent, moves them into canonical metadata, and removes the legacy tags from exported tags.

```json
[
  {
    "kind": "scenario",
    "front": "A worker writes local state, then calls a remote service. The RPC times out after the remote side may have committed. What should you reason about before retrying?",
    "back": "Treat the outcome as ambiguous: determine whether the external operation is idempotent/deduplicated and how the system reconciles an unknown result before retrying blindly.",
    "extra": "Recognition card for partial-failure boundaries.",
    "tags": ["engineering", "distributed-systems", "system::payments::worker"],
    "source": "payments/worker retry path; PR #12345",
    "verified": "2026-08"
  },
  {
    "kind": "reconstruction",
    "front": "Reconstruct the payment write path and identify the durable commit boundary.",
    "back": "API -> queue -> worker -> provider call -> local persistence; verify the exact ordering in the current implementation.",
    "tags": ["system::payments"],
    "source": "payments write-path architecture",
    "verified": "2026-08"
  },
  {
    "kind": "cloze",
    "text": "Dijkstra's algorithm assumes {{c1::non-negative edge weights}}.",
    "extra": "Negative weights can invalidate the greedy finalization step.",
    "tags": ["algorithms", "graphs"],
    "source": "Algorithms chapter on shortest paths"
  }
]
```

See `anki-export.md` for the exact stock-note-type mapping and TSV import directives.
