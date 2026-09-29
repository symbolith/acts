---
name: fix-formalism
description: Fold a lesson back into the Factors formalism (20260518150627.md) after the user explains something it got wrong or unclear: fix the imprecise text, or add a Remark if the point is correct but surprising. Use on "capture the lesson", "extract the lesson", "add a remark", or after correcting a misreading of the math.
argument-hint: [--dry-run] (default proposes then applies on approval)
allowed-tools: Read, Edit, Bash, Grep, Glob, Agent, AskUserQuestion
---

# Capture a Factors formalism lesson

The lesson is the gap between what you read in `file:./20260518150627.md:1:1`
and what the user just corrected. Operate on THIS conversation; do not fork it.
Repo CLAUDE.md and the style guide note it names (STYLE) already bind you; read
STYLE live, do not restate it.

## Decide

The formalism stays lean. Precision is free; commentary accretes. So default to
the fix; a Remark is the rare exception, only when the text is already exact.

> Reading ONLY the formalism, would a careful reader have made the same mistake?

- Yes -> **fix** the imprecise/wrong/ambiguous Definition, Formula, Gloss, or
  Rule. Reword in place; net length should not grow.
- No, the text was exact but the consequence is genuinely surprising -> a
  **Remark** (STYLE `>` element). First extend an existing nearby Remark; add a
  new one only if none fits. Never restate what the fixed text already implies.
- It belongs in another canon note (AGENTS.md names them: the vocabulary, the
  state and step summaries) or to the daemon (the AGENTS.md daemon rule) -> do not touch the
  formalism; say where it goes and stop.

Both may apply, but add nothing the fix already settles. Unsure -> `AskUserQuestion`.

## Do

1. State the lesson in one line: what was misread, the correct reading. Not crisp -> ask.
2. Draft the smallest exact edit, conforming to STYLE's All constraints and to
   NO USE BEFORE DEFINE.
3. Show the `file:./20260518150627.md:LINE:COL` site and the verbatim change;
   note it edits a ground-of-truth note; get approval. `--dry-run` stops here.
4. Apply with Edit only (the AGENTS.md Edit rule: never Write/`sed`/`echo`,
   never the dataview-serializer blocks).
5. Validate the change: an `Explore` subagent checks it against STYLE (the
   AGENTS.md style rule); confirm the other canon notes still agree, flag any
   divergence.

Report: lesson, classification, site, edit, verdict (`captured` / `dry-run` /
`out of scope`).
