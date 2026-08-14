---
name: deep-learning-workflow
description: Turn technical books, papers, blogs, documentation, code, code reviews, incidents, and learner notes into a deep-learning workflow using active recall, incremental reading, spaced repetition, and deliberate practice. Use when studying technical material, extracting or auditing Anki cards, designing cloze or question/answer cards, generating practice problems, revisiting small codebase sections, or building durable system understanding. Prefer auditing the learner's own recall/cards before generating replacements.
---

# Deep Learning Workflow

Build durable understanding rather than maximizing card count. Use AI to select, critique, connect, and create practice; do not replace the learner's retrieval effort.

## Core rule

Separate four jobs:

1. **Understand**: build a coherent mental model of the source.
2. **Retrieve**: use spaced repetition for knowledge that should come to mind quickly later.
3. **Apply**: use exercises, coding, derivations, debugging, or design tasks for skills.
4. **Synthesize**: periodically reconstruct the chapter, subsystem, or argument as a whole.

Never assume a flashcard is the right output. Choose the learning mechanism first.

## Workflow decision tree

1. Identify the request:
   - User provides their own recall, notes, or cards -> follow **Audit**.
   - User provides a source and wants cards -> follow **Extract**.
   - User wants exercises or deeper understanding -> follow **Practice**.
   - User wants to learn a repository/module/PR -> follow **Codebase study**.
   - User wants to plan or work through a book -> follow **Book study**.
   - User wants a mixed session -> combine the relevant workflows, but keep outputs small.

2. Read the relevant reference before doing the work:
   - Card extraction/auditing -> `references/card-quality.md`
   - Books, articles, papers -> `references/book-study.md`
   - Codebases, PRs, incidents -> `references/codebase-study.md`
   - Practice problems -> `references/practice-design.md`

3. Ground everything in the provided source or repository. Distinguish clearly between:
   - **source-derived** claims,
   - **reasonable inference**, and
   - **outside enrichment**.
   Never silently invent details absent from the source.

## Audit workflow

Prefer this workflow when the learner has attempted recall or written cards.

1. Read the source and the learner's cards/summary.
2. Identify the 3-7 most important ideas in the studied unit.
3. Evaluate coverage:
   - Which important ideas are captured?
   - Which important ideas are missing?
   - Which cards test low-value trivia?
   - Which cards are ambiguous, overloaded, or answerable by recognition alone?
   - Which items should be practice instead of cards?
4. Preserve good learner-authored wording when possible. Improve rather than replace it.
5. Suggest only the smallest set of additions needed for coverage.
6. If the learner's cards are already sufficient, say so. Do not manufacture more cards to fill a quota.

Output:

```markdown
## Coverage
[short assessment]

## Keep
- [card] — [why]

## Revise
- Original: ...
  Better: ...
  Reason: ...

## Missing high-value cards
[0-5 cards]

## Better learned by practice
[0-3 items with suggested exercise]
```

## Extract workflow

When the learner has not supplied cards:

1. Delimit a small study unit. Prefer one subsection, concept cluster, or code responsibility rather than an entire long chapter.
2. Identify the unit's central question and 3-7 important ideas.
3. If interactive context allows, begin with a brief closed-book retrieval prompt before revealing the extraction:
   - "Before looking at the cards, explain X from memory and list the two ideas you think matter most."
   Do not block the task if the user explicitly wants direct extraction.
4. Choose the right representations using `references/card-quality.md`.
5. Produce **0-5 cards by default**. Treat 5 as a ceiling for a small unit, not a quota.
6. Add one synthesis/reconstruction prompt when isolated cards would fragment an important mental model.
7. Mark any useful idea that should be practiced instead of memorized.

Default card schema:

```markdown
### Card N — [QA | Cloze | Scenario | Reconstruction]
Prompt: ...
Answer: ...
Extra: [optional context or example]
Why: [one sentence explaining why this deserves retrieval]
Tags: [small semantic/search-scope set]
Source: [optional exact chapter/PR/code pointer]
Verified: [optional YYYY-MM for mutable system knowledge]
```

For cloze cards use valid Anki-style clozes such as `{{c1::...}}`. Prefer one conceptual deletion per note; use multiple clozes only when they belong to the same tightly coupled fact.

## Practice workflow

Use exercises for procedural knowledge, transfer, debugging, implementation, derivation, and judgment.

1. Identify exactly what the studied section should enable the learner to do.
2. Generate a task that uses current material and minimal unstated prerequisites.
3. Require prediction or planning before execution when useful.
4. Do not reveal the full solution before the learner attempts it unless explicitly requested.
5. Provide progressive hints.
6. After the attempt, diagnose the misconception and propose cards only for durable knowledge exposed by the mistake.

Use `references/practice-design.md` for problem types and difficulty control.

## Book study workflow

Follow `references/book-study.md`.

For each small reading unit, aim to produce:

```markdown
## Study unit
Scope: [chapter/subsection/pages]
Question: [what problem is this section answering?]

## Closed-book reconstruction
[1-3 prompts]

## Important ideas
[3-7 concise items]

## Cards
[0-5 cards]

## Practice
[0-2 exercises]

## Connections
[links to earlier chapters, other books, or work systems if grounded]

## Next revisit
[what to reconstruct before rereading]
```

At chapter boundaries, stop atomizing and synthesize: reconstruct the chapter's structure, argument, dependencies, and what it enables the learner to do.

## Codebase study workflow

Follow `references/codebase-study.md`.

Study one responsibility or call-path slice at a time. Before rereading, ask the learner to reconstruct the behavior from memory when practical.

Prefer cards about:
- ownership and boundaries,
- state and invariants,
- causality and data flow,
- failure modes and recovery,
- concurrency and retry behavior,
- observability and debugging entry points,
- design rationale and tradeoffs,
- reusable code-review patterns.

Avoid cards whose main value is memorizing filenames, line numbers, transient implementation details, or large code snippets. Put exact provenance in `source`; keep `extra` for learning context that belongs on the back of the card.

For proprietary repositories, avoid copying secrets or large proprietary snippets into external study artifacts. Prefer conceptual summaries and local source pointers unless the user explicitly chooses otherwise and their policy permits it.

## Card export

When the user asks for Anki-importable files:

1. First produce or validate cards using the workflows above.
2. Save cards using the JSON schema in `references/card-quality.md`.
3. Run:

```bash
python scripts/anki_tsv.py cards.json --out-dir anki-export
```

The exporter targets Anki's stock note types and needs no custom fields:
- `qa`, `scenario`, and `reconstruction` become **Basic** notes (`Front`, `Back`);
- `cloze` becomes **Cloze** notes (`Text`, `Back Extra`);
- tags use Anki's special tags column rather than a literal note field;
- `extra`, `source`, and `verified` are rendered into the stock back fields;
- plaintext newlines are converted to HTML line breaks.

Read `references/anki-export.md` before changing the export schema or import layout.

## Quality gates

Before finalizing any learning unit, verify:

- Cards test retrieval, not mere recognition.
- Each card has a clear, gradeable answer.
- No card contains multiple unrelated questions.
- Important context is present in the prompt, not assumed from the original reading session.
- Stable principles are favored over transient trivia.
- Clozes are not paragraph-shaped deletion exercises.
- Procedures and skills have a practice component.
- The learner periodically reconstructs larger wholes so atomic cards do not fragment understanding.
- New cards are few enough that review load remains sustainable.
