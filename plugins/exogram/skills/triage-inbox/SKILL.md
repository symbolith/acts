---
name: triage-inbox
description: Process and organize the GTD inbox by triaging items into tasks, projects, knowledge notes, ideas, or trash. Use when the user asks to "clean inbox", "process inbox", "triage inbox", "organize inbox", or "clear inbox".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, ToolSearch, WebSearch, WebFetch
---

# Clean Inbox

Process the GTD inbox, the note typed `Type Inbox`, by triaging unprocessed items into proper exogram notes, tasks, or trash. The exogram workspace root is `${CLAUDE_PLUGIN_ROOT}/../../..`; every relative path below is relative to it.

Every proposal shown to the user is a finished, researched change, so the user only answers yes or no.

## Step 0: Find the Inbox

Search the exogram workspace root for `[Type Inbox](20260923141332.md)` in frontmatter, excluding `facts/.templates/` and the type note itself.
Member repositories are gitignored: search with `command grep -r` or `rg --no-ignore`.
Exactly one hit is the inbox. Several hits: ask which one with `AskUserQuestion`. None: stop and say so. Never assume a path.

## Step 1: Load Context

1. Read the inbox note. Only content from the heading `Inbox`, of any level, onwards is inbox material. The task lists above it are NOT inbox; read their names at run time.
2. Read `facts/exogram.yaml` and `facts/properties.yaml`.
3. Read every note typed `Type Exogram`, listed under `## Exograms` in the note Workspace Symbolith, `01M3PA7WS8GQQSWT00T1EMKTV1.md`; its `subject` names what the exogram holds.
4. Inventory the lookup tools: CLIs on the host (`gws` for Google Contacts, Gmail, Calendar), MCP tools through `ToolSearch`, web search. Never say a source is unavailable before this inventory.

## Step 2: Resolve Sync Conflict Files

Glob `<inbox folder>/<inbox id> (conflict *).md`. Skip silently if none.
For each conflict file, append the lines missing from the inbox note to the matching section, add sections the inbox note lacks, never duplicate a line, then `rm` the conflict file.
Re-read the inbox note.

## Step 3: Group

Group the raw lines into logical items, then the items into groups that need the same research: one person, one project, one topic.

- Lines that continue each other, a label with its sub-items, a code block or tool output with its description, a multi-paragraph draft: one item.
- A `##` section: one group.
- Every person named in an item gets identified: the group carries the name and every number, address or hint from the item.
- Gibberish is Trash.

Do NOT present the grouping. Proceed directly.

## Step 4: Research in Parallel

Launch one Agent per group, all in a single message. This is required whatever the inbox size.

Each agent receives the exact item text, the tool inventory, the task list names, the exogram subjects, and these instructions:

- Search the exogram workspace root for related notes, existing projects and Person notes.
- Resolve every person through Google Contacts, then mail, then Person notes. A number or address is looked up, never guessed.
- A lookup that contradicts the item is reported with what was found. Data is recorded as written in the item, never judged or corrected.
- Follow each lead to the end with the available tools before returning. Never return a question a tool can answer.
- Do NOT write files.

Each agent returns per item the finished change:

- The action: new note, append to a note, task on a project or task list, Trash, or Skip.
- For a new note: the type from the `type` enum of `facts/exogram.yaml`, the full file content, and the target exogram. The item's organization, person or project must match an exogram's `subject`. NEVER fall back to the default exogram. If no `subject` settles it, return `undecided` and say why.
- For an append or a task: the target note and the exact lines.
- What was found and with which tool, in one or two lines.
- A best guess is mandatory. What stays unverified is named as unverified.

## Step 5: Confirm and Apply

As each agent returns, show its changes with `AskUserQuestion`, one question per item. Do not wait for the other agents.

Every note shown to the user, here and in the report, is `Alias file:./<path>:1:1`, alone on its line, the path relative to the working directory.

Each question shows:

```
**[N/total]** from `## SectionName`

> original text exactly as it appears in inbox

**Change:** the exact lines and their target note, or the new note's alias, type and exogram
**Found:** what the research turned up, and what is unverified
```

On the answer:

- **yes**: apply the change at once, remove the item from the inbox, run `just validate` on every edited note.
- **no**: leave the item in the inbox. Do not invent a replacement; ask what the user wants.
- **Any other text**: treat as instructions, research again if they name a new lead, apply.

An `undecided` exogram is never accepted with yes: ask which exogram the note goes into.

Applying follows the note creation workflow of the Premise notes:

- New note: ULID filename from `just ulid`, frontmatter from the type's template. Read the `AGENTS.md` in the root of the target exogram's repository first, if it has one, and the `hasPremise` notes of the acts it imports.
- Task on a project: append a `- [ ]` line to the project note. A new project gets its Project note first.
- Task on a task list: append to the matching list above the inbox heading.
- Re-read the inbox note before each edit: the user edits it while the triage runs.

## Step 6: Report

Delete inbox sections that are now empty, then report:

- Notes created
- Tasks added, with their target notes
- Items trashed
- Items still in the inbox, each with the reason
