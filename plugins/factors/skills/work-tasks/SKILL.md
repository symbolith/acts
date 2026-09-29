---
name: work-tasks
description: Work through the intended Act notes that change the Factors formalism note, one at a time; analyze currency, then present the issue with worked-out solution previews in one question, implement the pick. Use when the user says "work the formalism tasks", "work through the tasks", "next formalism task", "process the task backlog", or names an act note to work on.
argument-hint: [act-note-id] (optional; default walks the intended backlog)
allowed-tools: Read, Grep, Glob, Edit, Bash, AskUserQuestion
---

# Work formalism tasks

Interactive processor for Act notes that change the formalism note, the canon root AGENTS.md names; `<formalism>` below is its id.
One task file per run, two gates, the user decides with the fix in view. The user reruns the skill for the next task.
SPEED TO THE GATES: reach each gate in the same turn, working alone and inline. The hard work comes AFTER the user picks, never before.

## Setup (once per run, silent)

1. Read the canon notes (`reviewLevel: canon`; AGENTS.md names them and their roles), the style guide included.
2. The tracker is the Index note whose `relation` names the formalism; its dataview query defines the task set. Take one task: the oldest note the query selects with `state: intended`. Mirror the query with grep, one `grep -l` per `contains` clause; never read the serialized result, it is stale between Obsidian runs. A `potential` act is not yet intended; never work it.

```
grep -l '<key of clause 1>:' *.md | xargs grep -l '<id of clause 1>' | xargs grep -l '<key of clause 2>:' | xargs grep -l '<id of clause 2>' | xargs grep -l 'state: intended' | sort | head -1
```

If `$ARGUMENTS` names a task note, take that one instead.
The task in hand is the only extra note this skill may read; open no other task note, list none.
The canon notes carry `documentStatus: draft` between validations; that is this workflow's normal state. Never mention it, never ask about it.

## Per task: two gates

### Gate 1 — Currency

Read the task note. Check its issue against the current formalism:

- Already resolved there → say so in one sentence with the resolving line as `file:./<formalism>.md:LINE:COL`, delete the task note (`rm`), STOP; the run is over.
- Obsolete (the construct it targets no longer exists) → say why, ask the user whether to close it.
- Still current → Gate 2.

### Gate 2 — Present issue with solutions, then implement

Never ask a question without substance: the user decides once, with the fix visible.
No AskUserQuestion here: chat text before a tool call is swallowed, so the presentation must be the turn's FINAL message and the user answers free-form in their next message.
Build the presentation yourself from the notes already read, in the same turn as Gate 1.
Before the pick: NO Workflow, NO Agent, NO subagents, NO background tasks, NO design panels, NO critics, NO status message followed by waiting. Ultracode does NOT override this.
Your own analysis is enough for the gate. The user's pick is the review; verification and sweeps belong to implementation.

End the turn with one message holding:

- The problem in one or two sentences that quote the formalism text they talk about inline, as code spans.
  NEVER cite a line number, rule clause number, or section in prose ("line 325", "need (6)", "at 222"): the user must follow every sentence without opening the note. `file:` references sit only under code blocks, never in sentences.
- The relevant formalism lines quoted as code blocks with `file:./<formalism>.md:LINE:COL` references.
- Every change as one flat diff block per site, verbatim lines, minus old plus new; prose never describes an edit; no nesting under bullets.
- The open questions as a short plain list, each with a recommended answer.
  Each option of a question shows its own verbatim lines in a code block: the definition, the step or rule lines it changes, every new name spelled out.
  Prose never describes an option; the user must never have to imagine what an option writes.
- Bullets throughout, no prose paragraphs.
- Nothing else: no setup report, no preamble, no findings outside the task.

Ask only what is actually undecided. If the task note already commits to a solution, that design is settled; list only its own open decisions with recommendations. Only for a task with no committed solution work out the genuinely distinct designs yourself (as many as the problem has, no padding).
Weigh options on merit alone; entrenchment, diff size, or sweep cost never count for or against (PERFECTION OVER CHURN).

Then STOP and wait. Edit only on an explicit go or skip; a reply that corrects or disputes the fix reopens Gate 2 with a revised presentation holding the complete current change set in one view, never a delta against an earlier message.

On skip, delete the task note (`rm`); the tracker's dataview block regenerates in Obsidian.

On a pick, implement. The hard work lives here: under ultracode, Workflow and subagents are allowed now, for the sweep and its checks, never for re-deciding the pick.

1. Edit the formalism with the Edit tool, following the style guide, a complete consistency sweep (PERFECTION OVER CHURN), and every repo rule.
2. Set the formalism note `documentStatus: draft` and STOP; do not validate it yourself.
3. Delete the task note (`rm`).
4. Align the two summary views and, on contradiction, the vocabulary, per the AGENTS.md alignment rule.

Then STOP; the run is over. Never take a second task, never ask whether to continue.

## Hard rules

- Never edit the formalism without the user having picked a solution at Gate 2.
- Never launch Workflow, Agent, or any background task before the Gate 2 pick, ultracode or not. Gates come fast; heavy work comes after.
- Never rewrite notes with Write or shell; Edit only.
- One task file per run. Read no other task note, work no other task.
- Report nothing outside the task in hand: no on-sight findings, no draft notices, no backlog listing.
