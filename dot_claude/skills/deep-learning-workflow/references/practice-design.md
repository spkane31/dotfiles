# Practice Problem Design

Practice is for capabilities that cannot be created by verbal recall alone.

## Design rule

Start from a target capability:
`After this section, the learner should be able to ____ without copying the source.`

Then make the learner perform that behavior.

## Engineering-first practice

For an unfamiliar technical concept, default to work an engineer would plausibly perform:

- interpret configuration, output, diagrams, logs, metrics, or documentation;
- choose among options under concrete constraints;
- configure or design a small realistic example;
- predict behavior before running a normal tool;
- diagnose a symptom or flawed configuration;
- explain a tradeoff, boundary, or failure mode;
- connect the concept to an adjacent system or operational responsibility.

Use the tools engineers would normally use. Ask for manual arithmetic, bit manipulation, symbolic derivation, or detailed show-work only when it reveals a mechanism needed for the target capability, when the learner must perform it unaided, when the supplied material makes it central, or when the learner requests it. Do not use calculation difficulty as a substitute for practical depth.

## Problem ladder

Choose the lowest level that is not trivial:

1. **Reproduce**: perform the demonstrated technique on a new small example.
2. **Vary**: change one assumption or input and predict the effect.
3. **Diagnose**: debug a flawed implementation, model, derivation, or design.
4. **Choose**: select among competing techniques and justify the choice.
5. **Design**: solve an open-ended problem with constraints.
6. **Transfer**: apply the idea in a different domain or to the learner's real work.

Do not jump to an open-ended project when the learner still lacks the basic mechanism.

## Interaction pattern

When interactive:

1. Present the problem and expected deliverable.
2. Ask for a prediction/plan before tool use when relevant.
3. Let the learner attempt it.
4. Offer hints progressively:
   - Hint 1: point to the governing concept;
   - Hint 2: narrow the next step;
   - Hint 3: provide a partial scaffold.
5. Reveal a full solution only after an attempt or explicit request.
6. Compare the attempt with the solution.
7. Identify the smallest misconception or missing retrieval that caused trouble.
8. When cards are part of the study, label the resulting card action as **Add**, **Revise**, **Keep**, **Retire**, or **No change**.
9. Show 0-3 affected cards. Use zero only when the attempt exposed no durable knowledge change, and say so explicitly.
10. Present one next exercise rather than starting several new threads.

## Technical problem patterns

### Data science / machine learning
- Use a fresh or synthetic dataset with the same concept but different surface details.
- Ask for a baseline, metric choice, preprocessing rationale, validation strategy, and error analysis.
- Require predictions about what changing a hyperparameter or feature will do before running the experiment.
- Include at least one failure mode such as leakage, imbalance, miscalibration, or distribution shift when appropriate to studied material.

### Algorithms
- Trace on a hand-sized input.
- State invariant/recurrence before implementation.
- Implement from a blank file.
- Construct a counterexample for a wrong variant.
- Compare complexity under changed constraints.

### Systems
- Inject a failure at a boundary and ask for resulting states.
- Ask which invariant is violated and how recovery works.
- Give metrics/log symptoms and ask for ranked hypotheses.
- Review a small pseudo-diff for concurrency, compatibility, or retry hazards.

### Programming/frameworks
- Complete a small feature from a behavioral specification.
- Fix a deliberately broken implementation.
- Explain the runtime behavior before execution.
- Refactor while preserving tests.

## Calibration

A good exercise should be solvable with the studied material plus established prerequisites, but should require decisions rather than transcription.

Check that the exercise rehearses the stated target capability. If the learner wants operational fluency but the exercise mainly tests hand calculation or notation manipulation, redesign it around a realistic decision, artifact, tool, or failure scenario.

If the learner succeeds effortlessly, increase transfer or ambiguity slightly. If they cannot start, reduce scope and expose one more cue rather than immediately giving the answer.
