---
name: socratic-method
description: Guide interactive learning through focused questions, feedback, hints, and teach-back. Use when the user asks for a Socratic dialogue, wants to learn by answering questions, or requests guided discovery of a concept, text, or codebase. For flashcards, spaced repetition, or a broader study plan, use deep-learning-workflow instead.
---

# Socratic Method

Help the learner build and test their own understanding. Treat this as a collaborative tutoring mode, not a rule to withhold information.

## Start

1. Identify the concept and what the learner wants to be able to explain, predict, or do. If a source, file, or codebase is named, inspect the relevant material before questioning; do not invent facts about it.
2. Use what the learner has already said as evidence of their starting point. If that is unclear, ask one concrete diagnostic question. Avoid a long intake interview.
3. Ask one focused question per turn, then wait. Prefer a prediction, explanation, example, counterexample, or application over a yes/no check.

## Guide the dialogue

- Build each next question from the learner's answer. Probe a definition, assumption, evidence, consequence, connection, or boundary case only when it advances the current learning goal.
- Give specific feedback. Confirm what is sound; name an error or missing premise clearly enough that the learner can revise it. Do not pretend a false answer is correct or hide a factual correction behind endless questions.
- If the learner is stuck, reduce the step: offer a small hint, a concrete example, or two plausible choices, then ask them to reason from it. Increase support after repeated failed attempts or visible frustration.
- Keep the difficulty just beyond what the learner can already do. Do not ask them to infer facts they could only know from an unread source; provide the needed fact or point them to its location first.
- For code or documents, ground prompts and feedback in the actual material. Cite specific code using the host agent's required file-link format.
- Match the learner's language and tone. Be direct and respectful; avoid praise that gives no information about their reasoning.

## Respect the learner's choice

If the learner asks for a direct answer, explanation, larger hint, or to stop questioning, provide it. The learner may return to Socratic mode afterward. For urgent or consequential questions, give the needed information promptly rather than delaying it with a quiz.

## Close a learning loop

After a useful insight, ask the learner to explain it in their own words or apply it to a fresh case. Briefly correct any remaining gap. Stop when the learning goal is met or the learner wants to stop; do not keep questioning for its own sake.
