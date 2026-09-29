---
name: rate-notes
description: Rate the concept merit of a set of exogram notes in parallel, writing a 1-5 qualityRating to each. Applies the rate-note rubric across many notes at once. Use when the user asks to "rate all notes", "rate these notes", "rate the notes in <folder>", "batch rate", "rate unrated notes", "quality-rate the exogram", or "rate every note".
argument-hint: [glob | folder | note list | "unrated" | "all"]
allowed-tools: Read, Glob, Grep, Edit, Bash, Agent, AskUserQuestion
---

# Rate Notes

Apply the [rate-note](../rate-note/SKILL.md) concept-merit rubric across a set of
notes, writing each note's `qualityRating`. This is the batch form of `rate-note`
and depends on it: the shared rubric lives in the sibling skill at
`../rate-note/references/rubric.md` (resolve to its absolute path when spawning
subagents).

Rate the idea, not the artifact. Completeness, sourcing, links, and prose are out
of scope.

## Workflow

### 1. Resolve the note set

Parse `$ARGUMENTS`:

- A glob, folder, or explicit list of notes: use it directly.
- `unrated`: notes that have no `qualityRating`. Find with
  `grep -L qualityRating *.md` over the exogram.
- `all`: every `*.md` note in the exogram.
- Empty or ambiguous: ask the scope with `AskUserQuestion` (unrated, a folder, or all).

### 2. Confirm scope

Reading many notes needs the user's go-ahead. Show the resolved count and a short
sample, then confirm before reading bodies. Stop if the user declines.

### 3. Filter to ratable notes

Drop every non-`Claim` note (see Ratability in the rubric): only `Claim` notes
are rated. List the skipped notes and their types so the skip is explicit, never
silent.

### 4. Rate in parallel

Launch one subagent per note with the `Agent` tool, in parallel batches (cap
about 8 concurrent for large sets). Give each subagent:

- the note path,
- the rubric path (the sibling `rate-note` skill's `references/rubric.md`, as an
  absolute path),
- the instruction to rate the concept only, write `qualityRating: N` and
  `hasVerdict` (the one-line rationale) to that note's frontmatter, set
  `reviewLevel: unread` (preserving body and dataview blocks), and return a
  compact result: `{ path, alias, type, rating, oneLineRationale }`.

Each subagent reads and edits only its own note.

### 5. Summarize

Collect results into a table sorted by rating, highest first:

```
| Rating | Note | Type | Why |
|--------|------|------|-----|
| 5      | ...  | ...  | ... |
```

### 6. Report

State how many notes were rated, how many skipped (and why), and surface any the
subagents flagged as borderline so the user can review them. Offer to re-rate a
subset if the calibration looks off.

## Anti-patterns

- Reading the whole exogram without confirming scope first.
- Silently skipping notes instead of listing them.
- Letting subagents read or edit notes other than their assigned one.
- Duplicating the rubric here instead of pointing subagents at the shared file.
- Serial rating when the set is large (use parallel batches).
- Inconsistent calibration across the batch (anchor to the strongest notes).
