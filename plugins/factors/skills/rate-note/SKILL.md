---
name: rate-note
description: Rate a single exogram note's concept merit on a 1-5 qualityRating and write it to the note's frontmatter. Judges the idea itself (soundness, significance, novelty, scope, parsimony, fruitfulness), not how complete or polished the note is. Use when the user asks to "rate this note", "rate a note", "quality rating", "rate the concept", "score this note", or "set qualityRating".
argument-hint: [note path or reference]
allowed-tools: Read, Edit, Glob, Grep, AskUserQuestion
---

# Rate Note

Rate the merit of the concept a note captures and write it to the note's
`qualityRating` frontmatter. The rubric is in
[references/rubric.md](references/rubric.md). Read it before rating.

Key principle: rate the idea, not the artifact. Completeness, sourcing, links,
and prose are out of scope. A stub can be a 5; a polished note can be a 1.

## Inputs

- `$ARGUMENTS`: a note path or reference. If empty, use the note under
  discussion in the conversation; if still ambiguous, ask with `AskUserQuestion`.

## Workflow

### 1. Resolve the target

Resolve `$ARGUMENTS` to one note path. Invoking this skill on a note is the
permission to read it. Read only that note.

### 2. Ratability gate

Read the note's frontmatter `type`. If it is not a `Claim` note (see Ratability
in the rubric), report not-applicable and stop. Do not write a rating.

### 3. Evaluate the concept

Apply the six criteria from the rubric to the concept only. Write one short line
per criterion. Ignore whether the note is complete, sourced, linked, or
well-written.

### 4. Roll up

Apply the roll-up rule: soundness gates (unsound caps at 2), the principal three
(soundness, significance, novelty) set the band, the amplifiers (scope,
parsimony, fruitfulness) tune within it. Produce one integer 1-5.

### 5. Write the rating

Add or update `qualityRating: N` and `hasVerdict` (the one-sentence
justification) in the note's frontmatter, and set `reviewLevel: unread`.
Preserve all other frontmatter and body content. Never edit inside
`dataview-serializer` blocks or any other auto-generated region.

### 6. Report

Show the per-criterion lines, the overall rating, and a one-sentence
justification:

```
Note:    [alias] (path)
Concept: [one-line statement of the idea]

Soundness:    [n] | [note]
Significance: [n] | [note]
Novelty:      [n] | [note]
Scope:        [note]
Parsimony:    [note]
Fruitfulness: [note]

qualityRating: N - [one-sentence justification]
```

## Anti-patterns

- Rewarding a well-written or fully-sourced note for a weak idea (that is execution).
- Penalizing a strong idea because the note is a stub.
- Averaging the criteria instead of applying the soundness gate and band rule.
- Forcing a rating onto a non-`Claim` note; only Claims are rated.
- Editing note body or dataview blocks while writing the rating.
- Reading notes other than the one being rated.
