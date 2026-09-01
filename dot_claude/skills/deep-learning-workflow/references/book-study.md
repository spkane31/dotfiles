# Technical Book Study Protocol

Combine inspectional reading, analytical reading, incremental reading, retrieval, and deliberate practice. Do not reduce a book to a pile of flashcards.

## 1. Inspectional pass

Before deep reading, build a map:
- read title/subtitle, preface/introduction, table of contents, chapter summaries, and index selectively;
- identify the book's central problem and intended audience;
- write the major parts in your own words;
- note prerequisite gaps;
- write 3-10 questions you hope the book will answer.

Output a compact `book-map.md` or equivalent note. Do not create many cards yet. Only card unusually important orientation facts.

## 2. Analytical/incremental pass

For each small unit (roughly one coherent subsection, not a fixed page count):

1. **Question before reading**: What question is this section trying to answer?
2. **Read actively**: mark definitions, claims, mechanisms, evidence, examples, and unresolved questions.
3. **Close the source**: reconstruct the important ideas in your own words.
4. **Check**: reopen and compare recall with the source.
5. **Extract**: create 0-5 high-value cards using the card-quality rubric.
6. **Apply**: if the section teaches a procedure or judgment, do 0-2 exercises.
7. **Connect**: explicitly link the idea to earlier material, another book, or a real system when the connection is legitimate.
8. **Queue a revisit**: on the next encounter, reconstruct before rereading.

## 3. Chapter synthesis

After enough subsections have accumulated, reconstruct the chapter as a whole:
- What problem does the chapter solve?
- What are its 3-7 major claims/concepts?
- How do they depend on one another?
- What examples or experiments justify them?
- What can you now do that you could not do before?
- What remains confusing?

Draw an outline, dependency graph, derivation, or architecture diagram from memory when appropriate.

Cards are not a substitute for this synthesis.

## 4. Technical practice

Match practice to the domain:

- Algorithms/data structures: trace by hand, derive complexity, implement from a blank file, compare alternatives, solve variations.
- Machine learning/data science: predict behavior before running code, fit on a fresh dataset, inspect errors, change assumptions, explain metrics, reproduce a result without copying the book.
- Distributed systems/databases: reason through failure scenarios, consistency anomalies, recovery, capacity, and tradeoffs; connect to real systems.
- Programming languages/frameworks: implement a small feature without the text open, debug a broken example, explain runtime behavior.
- Career/design books: apply frameworks to a real decision, write a concrete example, critique a counterexample.

Use exercises to produce errors. Errors reveal which mental models need repair and which cards are worth adding.

## 5. Book-level synthesis

When finishing a book or major part, answer from memory:
- What is the book fundamentally about?
- What structure does the author use to answer that problem?
- Which claims do I agree/disagree with, and why?
- What are the most generative ideas?
- What should change in how I work or reason?
- What are the 10-30 ideas I still want readily retrievable a year from now?

Prune cards that looked important locally but are not important globally.

## 6. Syntopical phase

When several books address the same question, stop treating them independently. Build a topic map:
- shared vocabulary and differing definitions;
- competing models or recommendations;
- evidence and assumptions;
- where each source is strongest;
- unresolved questions.

Create comparison cards only where fast discrimination is useful. Use essays, diagrams, or design exercises for larger synthesis.

## Avoid over-fragmentation

Incremental reading is useful only if larger structures keep being reassembled. Maintain at least three levels:
- subsection recall;
- chapter reconstruction;
- book/topic synthesis.
