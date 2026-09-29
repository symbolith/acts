---
name: polish-prose
description: Sweep a note for murky, run-on, or imprecise prose and tighten each passage to the note's style rules without changing its meaning. Use on "fix the prose", "polish the prose", "tighten the wording", "polish the remarks", "clean up the wording", or after spotting a head-hurting sentence.
argument-hint: <note> [--dry-run] [LINE...] (default sweeps, proposes, applies on approval)
allowed-tools: Read, Edit, Bash, Grep, Glob, Agent, AskUserQuestion
---

# Polish prose

Tighten the prose of the note given in `$ARGUMENTS` without changing what it says.

## Target

- First non-flag argument is the note path. Missing: use the note under discussion; still ambiguous: ask with `AskUserQuestion`.
- `LINE...` restricts to those lines. Otherwise sweep the whole body.
- `--dry-run` proposes and stops.

## Style source

Read style rules live, in this order, and never restate them:

1. The style guide note the repo `AGENTS.md` names, or a STYLE blockquote at the top of the note, if present.
2. The repo `CLAUDE.md` or `AGENTS.md`.
3. The global `CLAUDE.md` writing rules.

## Prose only: never change the meaning

Edit only explanatory text: remarks, glosses, headings, paragraphs. Never alter a formula, axiom, rule, code block, keyword line, citation, or any symbol and its meaning. If a wording fix would change what is true, it is not a prose fix: stop and flag it. In a formalism note, hand it to `/factors:fix-formalism` or `/factors:check-formalism`.

Respect the repo's reading rules: if `CLAUDE.md` restricts which notes may be read, open nothing beyond the target and its permitted references.

Before rewriting a passage, read the definitions it glosses so the rewrite is exactly true to what it names. Cited author, year, venue, and locus stay verbatim.

## Find

Hunt these defects:

- run-on cramming several consequences into one breath: split, one per line
- vague hand-waving ("across its levels"): state the precise point or cut it
- a claim that belongs to a different section or subject: drop it here
- an imprecise boundary or near-synonym: state exactly what is true
- a bare symbol where a defined speaking name exists: use the name
- any global writing rule violation: em dash, slop word, bold label, "not just X"
- a heading carrying math or fill words, a gloss over its length cap

## Fix

For each target:

1. State in one line what the passage must say.
2. Draft the smallest rewrite to the style rules. One sentence per line where the note does so. Cut, do not pad; net length should not grow.
3. Drop anything that does not follow from the passage's own subject.
4. Show each site as `file:<path>:LINE:COL`, verbatim before and after; get approval. `--dry-run` stops here.
5. Apply with `Edit` only. Never `Write`, `sed`, or `echo`; never touch auto-generated blocks.

## Validate

After the edits, an `Explore` subagent checks each changed passage against the style rules and confirms it still says exactly what the original said. If the note has sibling ground-of-truth notes, confirm they still agree and flag divergence. The user may waive this for a run.

Report: each site, the defect, before/after, verdict (`polished` / `dry-run` / `flagged`).
