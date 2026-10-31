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

Run every command in `factors/`.

1. The tracker is the Project note Writing the formalism (`factors/exogram/01M3MDS7RXMKZQYPV8HB9Y7R69.md`); a task is an Act note whose `isPartOf` reaches it, directly or through nested projects other than Backlog Writing the formalism (`factors/exogram/01M69E2471P0NGEJ30HV90VHY3.md`). Never read its serialized query result, it is stale between Obsidian runs; this one call lists the workable tasks, `hasActState: actIntended` with every `follows` settled, oldest first with titles.

```
for f in $(awk 'FNR==1{s=0} /^isPartOf:/{s=1;next} /^[^ ]/{s=0} s&&match($0,/\([^)]*\.md\)/){print substr($0,RSTART+1,RLENGTH-2), substr(FILENAME,9)}' exogram/*.md \
  | awk 'BEGIN{member["01M3MDS7RXMKZQYPV8HB9Y7R69.md"]} {parent[NR]=$1; child[NR]=$2} END{do{grown=0; for(i=1;i<=NR;i++) if((parent[i] in member)&&!(child[i] in member)&&child[i]!="01M69E2471P0NGEJ30HV90VHY3.md"){member[child[i]]; grown=1; print "exogram/" child[i]}}while(grown)}' \
  | xargs grep -l 'hasActState: actIntended' | sort); do
  sed -n '/^follows:/,/^[^ ]/p' "$f" | grep -o '([^)]*\.md)' | tr -d '()' | sed 's|^|exogram/|' | xargs -r grep -L -E 'hasActState: (actSucceeded|actFailed)' | grep -q . \
    || printf '%s %s\n' "$f" "$(awk '/^aliases:/{getline; sub(/^  - /,""); gsub(/"/,""); print; exit}' "$f")"
done
```

If `$ARGUMENTS` names a task note, take that one. Else end the turn at once with that list numbered, one line each as title and `file:~/repositories/symbolith-exogram/factors/exogram/<task>.md:1:1`, the first marked recommended, and ask which number to work; write no claim before the answer.
2. Write the claim at once: on the pick, read the task note, write `hasActState: actClaimed` and `hasClaimant` (the user's Person note, which joins `contributor`) with the Edit tool, then think; the written claim is the lock, other agents work this exogram.
3. Read the canon, `grep -l 'noteRole: canon' exogram/*.md`, the style guide included, no other list of it.

The task in hand is the only extra note this skill may read; of the others, grep frontmatter only, open none.
The task note is never deleted; the user settles it and the skill writes that with the Edit tool: `hasActState: actSucceeded` when its issue is resolved in the formalism, `hasActState: actFailed` when it is skipped or closed, `hasClaimant` removed, and `noteRole: deprecated` either way.
The canon notes carry `vetting: unread` between validations; that is this workflow's normal state. Never mention it, never ask about it.

## Per task: two gates

Every message to the user opens with the task's title and link, `file:~/repositories/symbolith-exogram/factors/exogram/<task>.md:1:1`, alone on the first line.
Other agents edit the formalism during the run: read it anew at the start of every turn, and take every quote, diff line, and line number from that read.

### Gate 1 — Currency

Read the task note; it is a snapshot of an older formalism, so take its intent, never its wording or line numbers.
Read what the formalism changed since the task was written, committed or not:
`git diff --no-ext-diff -U0 $(git log --diff-filter=A --format=%h -1 -- exogram/<task>.md) -- exogram/<formalism>.md`
Those changes are the user's picks and outrank the task: a line they wrote stands, a term they cut never returns, and every fix uses the idioms they introduced.
Check its issue against the current formalism:

- Already resolved there, by a fix or by the removal of the text it faults → say so in one sentence with the resolving line as `file:~/repositories/symbolith-exogram/factors/exogram/<formalism>.md:LINE:COL`, mark the task note as succeeded, STOP; the run is over.
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

- Problem: one or two sentences that quote the formalism text they talk about inline, as code spans, each sentence that names a defect followed by its `file:~/repositories/symbolith-exogram/factors/exogram/<formalism>.md:LINE:COL` reference on the next line.
  NEVER cite a line number, rule clause number, or section in prose ("line 325", "need (6)", "at 222"): the user must follow every sentence without opening the note. `file:` references sit on their own line, under the sentence or diff they locate, never inside a sentence.
- Option: one sentence why, then its ```diff blocks, one per site, verbatim lines, minus old plus new, its `file:~/repositories/symbolith-exogram/factors/exogram/<formalism>.md:LINE:COL` reference beneath; every rule line it changes, every new name spelled out.
  Prose never describes an edit or an option; the user must never have to imagine what an option writes.
  An option adds no prose by default: a new remark, gloss, Source sentence or rewording goes in only for a reason the formulas and existing lines cannot carry, and that reason stands beside its diff.
  The formalism appears only as the minus and context lines of a diff; never quote it on its own, a line that does not serve the pick is noise.
  One heading per distinct design; a committed design has one option section and no alternative.
- Open: only what no option settles, one bullet each with the recommended answer.
- Headings are the only structure between sections; bullets live inside a section; a diff never sits under a bullet; no setup report, no preamble, no findings outside the task.

Ask only what is actually undecided. If the task note already commits to a solution, that design is settled; list only its own open decisions with recommendations. Only for a task with no committed solution work out the genuinely distinct designs yourself (as many as the problem has, no padding).
Weigh options on merit alone; entrenchment, diff size, or sweep cost never count for or against (PERFECTION OVER CHURN).

Then STOP and wait. Edit only on a plain go, ok or skip to the complete design shown; any other wording, however forceful, is no go.
Any other reply opens with the reaction to it, what it changes in one or two lines.
Then come only the diffs it changes and the context they need, taken from this turn's read.
Put one open decision in a message; the next waits for its answer.
Once a reply settles the design, show the complete design in the message, every diff in every note, never behind a link, and wait for a go to it.
Otherwise show the whole presentation only when the user asks for it.

On skip, mark the task note as failed; the tracker's dataview block regenerates in Obsidian.

On a go, implement. The hard work lives here: under ultracode, Workflow and subagents are allowed now, for the sweep and its checks, never for re-deciding the design.

1. Apply the go as one script of exact-string replacements, one approval for every note, following the style guide, a complete consistency sweep (PERFECTION OVER CHURN), and every repo rule.
2. Set the formalism note `vetting: unread` and STOP; do not validate it yourself.
3. Mark the task note as succeeded.
4. Align the two summary views and, on contradiction, the vocabulary, per the Premise Writing the formalism alignment rule.

Then STOP; the run is over. Never take a second task, never ask whether to continue.

## Hard rules

- Never edit the formalism before the user's go to the complete design.
- Never launch Workflow, Agent, or any background task before the Gate 2 pick, ultracode or not. Gates come fast; heavy work comes after.
- Never rewrite notes with Write or shell, except the replacement script the premise allows.
- One task file per run. Read no other task note and work no other task, except to close as failed a task the decision made wrong or needless.
- Report nothing outside the task in hand: no on-sight findings, no draft notices, no backlog listing beyond the pick question.
