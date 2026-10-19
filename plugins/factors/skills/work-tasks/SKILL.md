---
name: work-tasks
description: Work through the intended Act notes that change the Factors formalism note, one at a time; analyze currency, then present the issue with worked-out solution previews in one question, implement the pick. Use when the user says "work the formalism tasks", "work through the tasks", "next formalism task", "process the task backlog", or names an act note to work on.
argument-hint: [act-note-id] (optional; default asks which workable task)
allowed-tools: Read, Grep, Glob, Edit, Bash, AskUserQuestion
---

# Work formalism tasks

Interactive processor for Act notes that change the formalism note, the canon root Premise Writing the formalism (`factors/exogram/01M3MDCW62YHXPX8TK4AB47QJY.md`) names; `<formalism>` below is its id.
One task file per run, two gates, the user decides with the fix in view. The user reruns the skill for the next task.
SPEED TO THE GATES: reach each gate in the same turn, working alone and inline. The hard work comes AFTER the user picks, never before. A turn reads only what its closing message uses.

## Setup (once per run, silent)

1. The tracker is the Project note Writing the formalism (`factors/exogram/01M3MDS7RXMKZQYPV8HB9Y7R69.md`); a task is an Act note whose `isPartOf` names it. Never read its serialized query result, it is stale between Obsidian runs; this one call lists the workable tasks, `hasActState: intended` with every `follows` settled, oldest first with titles.

```
for f in $(grep -l 'isPartOf:' exogram/*.md | xargs grep -l '01M3MDS7RXMKZQYPV8HB9Y7R69' | xargs grep -l 'hasActState: intended' | sort); do
  sed -n '/^follows:/,/^[^ ]/p' "$f" | grep -o '([^)]*\.md)' | tr -d '()' | sed 's|^|exogram/|' | xargs -r grep -L -E 'hasActState: (succeeded|failed)' | grep -q . \
    || printf '%s %s\n' "$f" "$(awk '/^aliases:/{getline; sub(/^  - /,""); gsub(/"/,""); print; exit}' "$f")"
done
```

If `$ARGUMENTS` names a task note, take that one. Else end the turn at once with that list numbered, one line each as title and `file:./exogram/<task>.md:1:1`, the first marked recommended, and ask which number to work; claim nothing before the answer.
2. Claim the task at once: on the pick, read the task note, set `hasActState: claimed` with the Edit tool, then think; the claim is the lock, other agents work this exogram.
3. Read the canon, `grep -l 'noteRole: canon' exogram/*.md`, the style guide included, no other list of it.

The task in hand is the only extra note this skill may read; of the others, grep frontmatter only, open none.
The task note is never deleted; it is settled with the Edit tool: `hasActState: succeeded` when its issue is resolved in the formalism, `hasActState: failed` when it is skipped or closed, and `noteRole: scratch` either way.
Whenever a task note leaves `intended`, on claim or on settling, set `lead: "[Gordian Dziwis](3f1909e2-5284-4d40-a1ed-8bf222238d03.md)"` if absent; Type Act requires it from then on.
The canon notes carry `vetting: unread` between validations; that is this workflow's normal state. Never mention it, never ask about it.

## Per task: two gates

Every message to the user opens with the task's title and link, `file:./exogram/<task>.md:1:1`, alone on the first line; `file:` paths are relative to Claude's working directory, so never `cd`, it stays `factors/` where the session starts.
Other agents edit the formalism during the run: read it anew at the start of every turn, and take every quote, diff line, and line number from that read.

### Gate 1 — Currency

Read the task note; it is a snapshot of an older formalism, so take its intent, never its wording or line numbers.
Read what the formalism changed since the task was written, committed or not:
`git diff --no-ext-diff -U0 $(git log --diff-filter=A --format=%h -1 -- exogram/<task>.md) -- exogram/<formalism>.md`
Those changes are the user's picks and outrank the task: a line they wrote stands, a term they cut never returns, and every fix uses the idioms they introduced.
Check its issue against the current formalism:

- Already resolved there, by a fix or by the removal of the text it faults → say so in one sentence with the resolving line as `file:./exogram/<formalism>.md:LINE:COL`, settle the task note as succeeded, STOP; the run is over.
- Obsolete (unresolved, and the construct it would change no longer exists) → say why, ask the user whether to close it as failed.
- Still current → Gate 2.

### Gate 2 — Present issue with solutions, then implement

Never ask a question without substance: the user decides once, with the fix visible.
No AskUserQuestion here: chat text before a tool call is swallowed, so the presentation must be the turn's FINAL message and the user answers free-form in their next message.
Build the presentation yourself, in the same turn as Gate 1.
Before the pick: NO Workflow, NO Agent, NO subagents, NO background tasks, NO design panels, NO critics, NO status message followed by waiting. Ultracode does NOT override this.
Your own analysis is enough for the gate. The user's pick is the review; verification and sweeps belong to implementation.

End the turn with one message, at most one page (about 40 lines), in exactly these headed sections:

```
## Problem
## Option A <name> (recommended)
## Option B <name>
## Open
```

- Problem: one or two sentences that quote the formalism text they talk about inline, as code spans, each sentence that names a defect followed by its `file:./exogram/<formalism>.md:LINE:COL` reference on the next line.
  NEVER cite a line number, rule clause number, or section in prose ("line 325", "need (6)", "at 222"): the user must follow every sentence without opening the note. `file:` references sit on their own line, under the sentence or diff they locate, never inside a sentence.
- Option: one sentence why, then its ```diff blocks, one per site, verbatim lines, minus old plus new, its `file:./exogram/<formalism>.md:LINE:COL` reference beneath; every rule line it changes, every new name spelled out.
  Prose never describes an edit or an option; the user must never have to imagine what an option writes.
  The formalism appears only as the minus and context lines of a diff; never quote it on its own, a line that does not serve the pick is noise.
  One heading per distinct design; a committed design has one option section and no alternative.
- Open: only what no option settles, one bullet each with the recommended answer.
- Headings are the only structure between sections; bullets live inside a section; a diff never sits under a bullet; no setup report, no preamble, no findings outside the task.

Ask only what is actually undecided. If the task note already commits to a solution, that design is settled; list only its own open decisions with recommendations. Only for a task with no committed solution work out the genuinely distinct designs yourself (as many as the problem has, no padding).
Weigh options on merit alone; entrenchment, diff size, or sweep cost never count for or against (PERFECTION OVER CHURN).

Then STOP and wait. Edit only on an explicit go or skip; any other reply reopens Gate 2: rebuild the presentation from this turn's read and end the turn with it in full, the note's write time under the title, never a delta against an earlier message, never a report that nothing changed.

On skip, settle the task note as failed; the tracker's dataview block regenerates in Obsidian.

On a pick, implement. The hard work lives here: under ultracode, Workflow and subagents are allowed now, for the sweep and its checks, never for re-deciding the pick.

1. Edit the formalism with the Edit tool, following the style guide, a complete consistency sweep (PERFECTION OVER CHURN), and every repo rule.
2. Set the formalism note `vetting: unread` and STOP; do not validate it yourself.
3. Settle the task note as succeeded.
4. Align the two summary views and, on contradiction, the vocabulary, per the Premise Writing the formalism alignment rule.

Then STOP; the run is over. Never take a second task, never ask whether to continue.

## Hard rules

- Never edit the formalism without the user having picked a solution at Gate 2.
- Never launch Workflow, Agent, or any background task before the Gate 2 pick, ultracode or not. Gates come fast; heavy work comes after.
- Never rewrite notes with Write or shell; Edit only.
- One task file per run. Read no other task note, work no other task.
- Report nothing outside the task in hand: no on-sight findings, no draft notices, no backlog listing beyond the pick question.
