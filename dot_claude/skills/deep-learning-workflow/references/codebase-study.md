# Incremental Codebase Study Protocol

The objective is not to memorize the repository. Build durable system models and reusable engineering judgment from repeated exposure to real code.

## Choose a study unit

Prefer one coherent responsibility:
- request/command path;
- worker behavior;
- transaction boundary;
- retry mechanism;
- cache interaction;
- persistence path;
- API endpoint;
- queue publication/consumption path;
- migration;
- code-review issue;
- production incident symptom;
- unfamiliar class/module with a clear role.

A unit may be 20-100 lines or several files if that is what the responsibility requires. Semantic coherence matters more than line count.

## Before rereading

If previously seen, reconstruct from memory:
- What calls this?
- What does it call?
- What state does it read/write?
- What invariant does it protect?
- Where can it fail?
- Who retries/reconciles failures?

Then inspect the code and record what was wrong or missing.

## Read outward selectively

For a new unit, answer:

1. **Entry**: How do we get here?
2. **Exit**: What happens afterward?
3. **Ownership**: Which component owns this behavior?
4. **State**: What durable/ephemeral state is involved?
5. **Invariant**: What must remain true?
6. **Failure**: What if this step succeeds and the next fails?
7. **Concurrency**: Can several executions overlap?
8. **Retry/idempotency**: What retries, and why is it safe or unsafe?
9. **Observability**: Which logs, traces, metrics, states, or symptoms reveal trouble?
10. **Rationale**: Why this design instead of an obvious alternative?
11. **Change surface**: If behavior X changes, what else is likely affected?

Trace only 1-2 edges outward at first. Expand when an unanswered question is important; do not recursively read the whole codebase.

## Extract learning

Create 0-5 cards for the unit. Prefer:
- architecture/ownership;
- invariants;
- failure windows;
- debugging hypotheses;
- retry/idempotency semantics;
- concurrency hazards;
- design rationale;
- reusable review patterns.

Example specific card:
`Where is idempotency established for order processing in this system?`

Example generalized companion:
`Before arbitrary retries are safe, what properties must an operation or its surrounding protocol provide?`

Use both specific and generalized cards when the case is especially instructive.

## Turn reviews and incidents into cases

High-value inputs include:
- an issue another reviewer caught that you missed;
- a bug whose root cause surprised you;
- an incident where the first debugging hypothesis was wrong;
- a design tradeoff explained by a more experienced engineer;
- a subtle migration or compatibility issue.

Convert the concrete case into a scenario that preserves the recognition cues but removes incidental details. Train the trigger you want to notice next time.

## Periodic synthesis

Atomic cards can create fragmented knowledge. Periodically close the code and reconstruct:
- a request path;
- a subsystem architecture;
- ownership boundaries;
- failure/recovery path;
- key tables/queues/state machines;
- debugging flow for a common symptom.

Then verify against the current code. Update or suspend stale cards when architecture changes.

## Staleness hygiene

Keep provenance and search scope separate:
- Put the exact code/PR/doc pointer in the card's dedicated `source` field, e.g. `payments/worker retry path; PR #12345`.
- Put the last verification month in the dedicated `verified` field as `YYYY-MM`, e.g. `2026-08`.
- Use ordinary tags for stable subsystem scope, e.g. `system::payments::worker`, plus conceptual tags such as `retries` or `idempotency`.

Do not manually create `source:...` or `verified:...` tags. The exporters treat `source`/`verified` as canonical metadata. Deck YAML renders `source` as a comment and `verified` on the card back; stock-Anki TSV renders both on the back and derives `verified::YYYY-MM` for search. Legacy single-colon provenance tags are accepted only for migration.

Prefer stable invariants and rationale over exact filenames. When a subsystem changes materially, search its `system::...` tag and re-audit affected cards; update `verified` after checking them against current code.
