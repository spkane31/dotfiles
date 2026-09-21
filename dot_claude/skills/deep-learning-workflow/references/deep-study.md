# Deep Study Protocol

Use deep study when one theorem, mechanism, invariant, algorithm, argument, or tightly connected concept cluster is important enough to justify hours of iterative work. Do not use it for routine coverage or merely because the source is difficult.

The goal is to make the target flexible mental furniture: the learner should be able to reconstruct it, move among representations, use it in unfamiliar situations, and see where it stops working.

## Inputs and outputs

Required input:

- a topic, source, problem, or concept to study.

Optional inputs:

- the learner's intended use;
- prior knowledge or an initial explanation;
- existing cards or review evidence;
- available time and desired depth;
- a requested formal or engineering orientation.

Infer missing optional inputs when a reasonable default permits progress. Ask a setup question only when its answer would materially change the study target.

Produce these outputs during an interactive study session:

- a stated target capability and study orientation;
- a focused exercise or retrieval prompt;
- an early working batch of 2-5 provisional cards when cards are requested;
- explicit card changes after later attempts;
- a current mental-model summary and unresolved questions at synthesis checkpoints.

## Interactive delivery protocol

Follow these steps when cards are part of the request:

1. **Set up the study.** State the target capability and orientation. Present one focused scenario, question, or artifact.
   - Input: the initial request and any supplied source.
   - Output: `Study target`, `Why it matters`, and `First exercise`.
2. **Evaluate the first attempt.** Identify the smallest useful correction or missing relationship.
   - Input: the learner's first substantive response.
   - Output: `Learning feedback`, a `Working card batch` of 2-5 provisional cards, and one next exercise.
3. **Iterate visibly.** Use each later response to deepen the model and change the working set where evidence warrants it.
   - Input: the learner's attempt, the current mental model, and the working cards.
   - Output: `Learning feedback`, `Card changes`, the affected cards, and one next exercise.
4. **Run synthesis checkpoints.** After several exercises or a major conceptual shift, reconstruct the larger model and audit the cards.
   - Input: accumulated attempts, misconceptions, and working cards.
   - Output: `Current model`, `Keep`, `Revise`, `Add`, `Retire`, and `Remaining gaps`.

Do not spend more than two learner responses gathering context before producing the first working batch. If the initial request already demonstrates the learner's goal or current model, skip setup questions and produce provisional cards immediately. If no card is justified, name the missing evidence and continue with one targeted exercise; reassess after that response.

## Scope and initial state

Choose one small target and record, before rereading:

- the learner's current explanation or reconstruction;
- what they want to be able to do with the idea;
- known confusion and prerequisite gaps;
- the central question the target answers.

Preserve this initial explanation so it can be compared with the final rewrite.

## Choose the study orientation

Deep does not mean formal. Choose the orientation from the learner's intended use and the supplied material.

### Engineering-first is the default

Use engineering-first study when the learner starts with an unfamiliar technical term or concept and has not supplied a mathematical source or requested formal derivation. Build the study around:

- the concrete problem that motivated the concept;
- where it appears in systems, interfaces, configuration, and day-to-day work;
- what it lets an engineer represent, decide, configure, or debug;
- the smallest operational mental model needed to use it safely;
- common workflows and the tools engineers normally use;
- tradeoffs, scaling limits, failure modes, misleading intuitions, and signs of misconfiguration;
- connections to adjacent concepts that affect real decisions.

Order interaction from practical context toward mechanism:

1. Start with a recognizable problem or scenario.
2. Ask the learner to predict, choose, configure, interpret, or diagnose.
3. Introduce the concept as a tool for handling that situation.
4. Explore where the tool works, fails, or creates tradeoffs.
5. Add formal machinery only when it improves those capabilities.

Do not infer a formal orientation merely because the topic contains numbers, notation, binary representations, or formulas. A compact calculation may illuminate the model, but repeated hand calculation is not a proxy for engineering fluency when normal work uses a calculator, command, library, compiler, query engine, or other tool.

For example, practical study of network prefixes should prioritize interpreting a prefix in configuration, allocating non-overlapping ranges with appropriate capacity, understanding routing or access-control consequences, and diagnosing overlap or exhaustion. Manual mask conversion or bitwise arithmetic is secondary unless the learner asks for it or needs it to understand a specific mechanism.

### Use formal study when warranted

Emphasize proof, derivation, symbolic manipulation, or calculation when the learner supplies mathematical material, explicitly wants those abilities, or cannot reason about important engineering behavior without the formal mechanism. In a mixed topic, teach only as much formalism as the target capability requires, then return to use and transfer.

## Deepening lenses

Use these lenses in whatever order best serves the learner after the working card set has begun. They are not sequential gates and must not delay the first card batch.

### 1. Map the target

For engineering-first study, map the motivating problem, operating context, inputs and outputs, decisions, workflow, tooling, constraints, failure modes, and adjacent systems. For formal study, map the important objects, assumptions, claims, and dependencies. In either case, treat the target as a connected model rather than a linear script.

### 2. Graze useful details

Create provisional prompts for small observations, transitions, and relationships that are not yet comfortable. These are working material, not automatically permanent cards.

### 3. Build distinct representations

Seek representations that support the intended use. For engineering-first study, prioritize causal, operational, diagnostic, configuration, visual, and contrastive views; add symbolic or formal views when they unlock useful reasoning. Several cards may cover one underlying idea only when each trains a different retrieval route. Reject mere paraphrases.

### 4. Compress the whole

Use forcing functions and revise the answers as understanding improves:

- What is the core reason in one sentence?
- What are the two or three essential moves?
- What single diagram or compact derivation captures the mechanism?
- Which inference does most of the work?
- What becomes nearly obvious in the right representation?

For engineering topics also ask:

- What problem should make me reach for this concept?
- What is the smallest model I need to use it safely?
- What symptom, constraint, or decision should trigger it?

Compression prompts are aspirational. Early answers may be clumsy and should be rewritten rather than treated as immutable.

### 5. Push the boundaries

For each important assumption, ask:

- What do I predict if it is removed, weakened, or changed?
- Which step fails first, and why?
- Is there a counterexample?
- Can the result be generalized?
- What nearby result explains the boundary?

Record unchecked ideas as hypotheses. Verify counterexamples, generalizations, and externally enriched claims before promoting them to active cards.

For engineering topics, also vary scale, topology, workload, failure conditions, trust boundaries, compatibility constraints, and operational ownership where relevant. Ask what breaks, how it would appear in practice, and how an engineer would confirm the diagnosis.

### 6. Compare alternatives

Find alternate proofs, mechanisms, explanations, designs, or debugging routes when useful. Give each a descriptive name based on its core idea rather than referring ambiguously to "the proof" or "the approach." Compare prerequisites, insight, generality, and failure conditions.

### 7. Develop fluency through use

Cards preserve access; they do not by themselves create every capability. Match practice to the intended use. For engineering topics, prefer interpreting realistic artifacts, choosing or configuring an approach, predicting system behavior, using normal tools, debugging symptoms, explaining tradeoffs, and handling changed constraints. Use derivation or manual calculation when it exposes a mechanism the learner needs, not simply because the topic permits it. Turn errors into cards only when they expose durable missing knowledge.

### 8. Refactor and prune

Rewrite the explanation, proof, or model from scratch. Optionally write a discovery narrative: a plausible sequence of simple questions and false starts that could lead to the result. Compare the rewrite with the initial explanation.

Audit provisional cards using `card-lifecycle.md`. Promote cards that capture central relationships, distinct representations, recurring misconceptions, or important boundaries. Merge, suspend, or discard exploratory exhaust.

## Learner authorship

The construction process is part of the learning. Ask the learner to attempt important explanations, decisions, or representations when interactive context permits. Use that first attempt to draft provisional cards; do not wait for a polished learner explanation. Ask the learner to critique or use the working cards while AI exposes gaps, verifies claims, and sharpens wording.

## Review load

Deep study may eventually produce more than five useful cards, but introduce working cards in batches of at most five by default. Produce the first batch early, then keep remaining candidates in study notes until exercises or reviews provide evidence for promotion.

Pause when the learner can:

- reconstruct the target coherently;
- explain it through at least two useful representations;
- identify where the important assumptions matter;
- handle a novel variation or application;
- give a compact top-level explanation;
- and distinguish active cards from scaffolding that can be retired.

These are stopping conditions for the current pass, not a claim that understanding is finished.

## Per-turn output contracts

```markdown
## Setup turn

### Study target
[observable capability]

### Why it matters
[practical problem or formal purpose]

### First exercise
[one prompt with an explicit expected response]
```

```markdown
## Feedback and card turn

### Learning feedback
[what the attempt showed and the smallest correction]

### Card changes
- Add: [ids]
- Revise: [ids]
- Keep: [ids]
- Retire: [ids]
- No change: [when applicable]

### Working cards
[2-5 provisional or affected cards in deck YAML]

### Next exercise
[one focused prompt]
```

```markdown
## Synthesis checkpoint

### Current model
[engineering utility map or formal dependency map]

### Card audit
[keep, revise, add, retire]

### Remaining gaps
[unresolved, unverified, or not yet practiced]

### Next study target
[next capability or stopping point]
```
