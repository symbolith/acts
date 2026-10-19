---
name: check-prose
description: Sweep a note for murky, run-on, or imprecise prose, diagnose each passage, and route every hit to the right writer skill of the write-prose family. Finds and routes only, writes nothing itself. Use on "check the prose", "verify the prose", "fix the prose", "polish the prose", "tighten the wording", "clean up the wording", or after spotting a head-hurting sentence.
argument-hint: <note> [LINE...]
allowed-tools: Read, Grep, Glob, AskUserQuestion, Skill
---

# Check prose

Sweep the note given in `$ARGUMENTS`, diagnose, and route. This skill writes no text and edits no file; the write-prose family does the writing, under [the shared discipline](../../../writing/skills/write-prose/references/discipline.md).

## Target

- First non-flag argument is the note path. Missing: use the note under discussion; still ambiguous: ask with `AskUserQuestion`.
- `LINE...` restricts to those lines. Otherwise sweep the whole body.

## Style source

Read style rules live, in this order, and never restate them:

1. The style guide note a premise of the repo names, or a STYLE blockquote at the top of the note, if present.
2. The `hasPremise` notes of the acts the repo `AGENTS.md` imports.
3. The global `CLAUDE.md` writing rules.

## Scope

Diagnose only explanatory text: remarks, glosses, headings, paragraphs. Never flag a formula, axiom, rule, code block, keyword line, or citation as prose. If a wording fix would change what is true, it is not a prose defect: flag it for `/factors:fix-formalism` or `/factors:check-formalism` instead.

Respect the repo's reading rules: if `CLAUDE.md` restricts which notes may be read, open nothing beyond the target and its permitted references.

## Find

Hunt these defects:

- run-on cramming several consequences into one breath
- vague hand-waving ("across its levels")
- a claim that belongs to a different section or subject
- an imprecise boundary or near-synonym
- a bare symbol where a defined speaking name exists
- any global writing rule violation: em dash, slop word, bold label, "not just X"
- a heading carrying math or fill words, a gloss over its length cap

## Route

1. Report the hit list: each site as `file:<path>:LINE:COL`, the passage verbatim, the defect, and one line of diagnosis.
2. Ask the user which hits to pursue.
3. Route each pursued hit, with its passage and diagnosis verbatim:
    - a gloss of a formally defined name: `/writing:write-gloss`
    - a remark, heading, or paragraph: `/writing:write-prose`, until that genre has its own skill
    - a truth problem: `/factors:fix-formalism`
4. The receiving skill owns drafting, checks, approval, and applying. This skill ends at the handoff.
