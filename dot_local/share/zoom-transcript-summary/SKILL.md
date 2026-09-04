---
name: zoom-meeting-note
description: Convert a Zoom transcript into one factual Obsidian meeting note.
---

# Zoom meeting note

Create exactly one Obsidian Markdown note from the supplied Zoom transcript. Output Markdown only: no preamble, no code fences, and no statements about this instruction.

Use this order; include a section only when the transcript supports it:

```markdown
---
title: "<meeting title>"
date: <YYYY-MM-DD>
source: "<source filename>"
---

# <meeting title>

## Action items
- [ ] Action — Owner: Unassigned; Due: Not specified; Status: proposed; Timestamp: 00:00

## Executive summary

## Key discussion points

## Decisions

## Risks

## Opportunities

## Unanswered questions

## Internal follow-up

## External email draft
```

Requirements:

- Be terse: use short bullets and compact paragraphs.
- **Executive summary** must be a short bulleted list, never a prose paragraph. Each bullet should cover one material theme, outcome, or context item.
- Put **Action items** first when any exist. Use one checkbox per action: `- [ ]` for open or proposed work and `- [x]` only when completion is explicit.
- Omit every unsupported or empty section entirely. Never write “Not applicable”, “None”, or placeholder text.
- Base every statement solely on the supplied transcript and metadata.
- Do not invent people, owners, dates, decisions, commitments, facts, or timestamps. Use **Unassigned** and **Not specified** only within a real action item when those fields are absent.
- Distinguish confirmed commitments from tentative suggestions.
- Include a transcript timestamp in each action item when available; never fabricate one.
- **Internal follow-up** is only for concrete internal work that someone needs to do after the meeting. Do not include observations, meeting logistics, future conversations, calendar events, or expectations (for example, “they will talk after this call” or “they will meet tomorrow”) unless the transcript assigns a specific preparation, decision, or deliverable for that event.
- Keep confidential or internal-only material out of the external email draft. Omit that section if no safe, useful draft exists.
