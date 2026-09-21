# Card Lifecycle and Iteration

Use this workflow when working cards change during deep study or when the learner revisits cards after real reviews. The purpose is to improve the mental model and retrieval cue while keeping scheduling history attached to the same memory.

## Start with review evidence

Useful evidence includes:

- the current card id, prompt, and answer;
- what the learner actually recalled;
- hesitation, ambiguity, or a recurring wrong answer;
- whether the answer felt like a memorized phrase or a usable idea;
- a changed source, mental model, or desired application;
- review history when available.
- a new distinction, boundary, or application discovered during study;
- success or difficulty using a provisional card in the next exercise.

Do not require every item. When evidence is sparse, prefer a conservative revision and explain the uncertainty.

## Diagnose before rewriting

Distinguish among:

- **Cue problem**: the prompt is ambiguous, underspecified, or accidentally gives away the answer.
- **Answer problem**: the expected answer is bloated, ungradeable, or no longer expresses the core idea.
- **Atomicity problem**: several independent retrieval targets were combined.
- **Representation gap**: the learner can recite words but cannot visualize, derive, diagnose, or apply the idea.
- **Knowledge gap**: the card is sound, but recall is not yet established.
- **Practice mismatch**: the desired capability requires derivation, implementation, judgment, or transfer rather than another card.
- **Staleness**: the source or system changed.
- **Redundancy**: another card now trains the same retrieval route.
- **Maturity**: a once-useful scaffold has become unnecessary because it is contained in a larger chunk.

A lapse alone is not evidence that a card needs rewriting.

## Choose an action

Use the smallest action supported by the evidence:

- **Add**: create a card for newly exposed durable knowledge with a distinct retrieval target.
- **Keep**: the card is sound; continue reviewing it.
- **Revise in place**: improve the cue or answer while preserving the retrieval target.
- **Split**: separate overloaded retrieval targets.
- **Merge**: consolidate cards that have become genuinely redundant.
- **Change representation**: replace verbal recall with a scenario, reconstruction, diagram, derivation, or practice task.
- **Suspend or retire**: remove low-value, stale, redundant, or mature scaffolding from active review.

## Preserve identity correctly

Scheduling history is meaningful only when the card still tests substantially the same memory.

| Change | Id rule |
|---|---|
| Clarify wording; same retrieval target | Keep id and original authoring date |
| Shorten or improve the answer; same target | Keep id and original authoring date |
| Add a genuinely different retrieval direction | Create a new id and date |
| Split an overloaded card | Keep the old id for the semantic core if one successor clearly preserves it; give other targets new ids |
| Replace the original target entirely | Retire the old id; create a new id and date |
| Merge redundant cards | Keep the id matching the surviving target; retire the others |
| Update a mutable fact without changing its purpose | Keep id; update the answer and `verified` value |

Never reuse a retired id. Do not create a duplicate merely because the wording changed.

## Iteration loop

1. Ask the learner to answer before showing the back when practical.
2. Capture the observed problem in the learner's words.
3. Compare the current card with its source and intended future use.
4. Diagnose the failure type.
5. Choose one lifecycle action and apply the identity rules.
6. Check that the revised prompt still has a clear, gradeable answer.
7. If the issue is procedural or representational, add practice or a distinct companion card rather than overloading the original.
8. Reassess after later reviews; do not expect a single rewrite to be final.

During an interactive deep-study session, run steps 2-7 after each substantive learner attempt and report only the affected cards. At synthesis checkpoints, report the complete keep/revise/add/retire decision set.

## Revision output

When proposing or making revisions, include:

```markdown
## Revision decisions

| Card id | Review evidence | Action | Id decision | Reason |
|---|---|---|---|---|
| retry-ambiguity | Recalled "retry" but missed the unknown outcome | Revise in place | Keep id and date | Same target; cue should emphasize ambiguity |
```

Then show the revised card, new companion cards, and ids to suspend or retire. This report, plus version control when available, provides enough history for a future iteration without adding lifecycle fields to the active deck schema.
