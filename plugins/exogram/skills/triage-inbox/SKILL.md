---
name: triage-inbox
description: Process and organize the GTD inbox by triaging items into tasks, projects, knowledge notes, ideas, or trash. Use when the user asks to "clean inbox", "process inbox", "triage inbox", "organize inbox", or "clear inbox".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
---

# Clean Inbox

Process the GTD inbox, the note typed `Type Inbox`, by triaging unprocessed items into proper exogram notes, tasks, or trash.

## Step 0: Find the Inbox

Grep the exogram for `[Type Inbox](20260923141332.md)` in frontmatter, excluding `facts/.templates/` and the type note itself. Exactly one hit is the inbox. Several hits: ask which one with `AskUserQuestion`. None: stop and say so. Never assume a path.

## Step 1: Load Context

Read these files first:

1. The inbox note found in Step 0
2. `~/repositories/symbolith-exogram/AGENTS.md` (note creation workflow, schemas, conventions)

**Important:** Only content from the `## Inbox` heading onwards is inbox material. Everything above it (frontmatter and the organized task lists) is NOT inbox. Read the task list names from the note at run time.

## Step 1.5: Resolve Sync Conflict Files

Obsidian/sync conflicts can produce duplicate inbox files matching the pattern `<inbox id> (conflict *).md` in the inbox note's folder.

1. Glob `<inbox folder>/<inbox id> (conflict *).md` to find all conflict copies
2. For each conflict file:
   - Read it and the inbox note
   - Diff their content. For each section, identify lines present in the conflict file but missing from the canonical file
   - Append those missing lines to the matching section in the inbox note (preserve section structure; do NOT duplicate lines that already exist verbatim)
   - If the conflict file has sections that the canonical file lacks, add those sections too
3. After merging, delete each conflict file with `rm`
4. Re-read the inbox note so subsequent steps see the merged content

Skip this step silently if no conflict files exist.

## Step 2: Preprocess Sections

Split the inbox content (from `## Inbox` onwards) at `##` headers into sections.

For each section, analyze the raw content and group related lines into logical items. The content is chaotic, so use these heuristics:

- **Comma-connected lines** (lines ending/starting with commas): group as one item
- **"label:" + following items**: group label with its sub-items (until next blank-line gap or next label)
- **Code blocks** (``` ... ```): one item, include surrounding description
- **Tool output** (lines with `───`, indented output blocks): one item with its description
- **Bullet lists** (consecutive `- ` lines): one group if related, separate items if distinct topics
- **Existing `- [ ]` tasks**: one item each
- **Markdown links** (`[text](file.md)`): one item, preserve link
- **Multi-paragraph prose**: one item (draft emails, ideas, reflections)
- **Standalone single words**: could be person name, topic, or trash. Flag as ambiguous.
- **Gibberish** (random characters): classify as Trash
- **`###` subsections**: treat as separate item groups within the parent section

Do NOT present groupings to the user. Proceed directly to triage.

## Step 3: Triage via Subagents

For each section, launch an Agent subagent to research and propose classifications. Launch multiple subagents in parallel (one per section or batch of sections).

Each subagent receives:
- All item contents (exact text from inbox) for its section(s)
- The section name(s)
- Instruction to read `~/repositories/symbolith-exogram/facts/exogram.yaml` and `~/repositories/symbolith-exogram/facts/properties.yaml` for note types
- Instruction to search the exogram (`~/repositories/symbolith-exogram/`) for related notes and existing projects
- Instruction to read every note typed `Type Exogram` (the exograms' `README.md` files, listed in `~/repositories/symbolith-exogram/README.md`); its `subject` names the subject matter the exogram holds

Each subagent must return per item:
- **Proposed classification**: one of the note types in the `type` enum of `~/repositories/symbolith-exogram/facts/exogram.yaml`, read live, never from a remembered list, OR "Task", OR "Trash", OR "Skip"
- **If Task**: proposed target (existing project note path, or "new project", or the name of one of the task lists above `## Inbox`)
- **If new note**: suggested alias/title and any related notes found in the exogram
- **If new note**: the target exogram, decided per item: the item's organization, person or project must match an exogram's `subject`. There is NO default exogram. If no `subject` settles it, return "undecided" and say why
- **Reasoning**: one sentence explaining the classification

The subagent must make a decision for every item. Never flag items as "ambiguous" without also providing a best-guess classification.

### Subagent Prompt Template

```
Triage these inbox items from a personal Zettelkasten exogram.

**Section:** ## {section_name}
**Items:**
{item_list_with_numbers}

Read `~/repositories/symbolith-exogram/facts/exogram.yaml` and `~/repositories/symbolith-exogram/facts/properties.yaml` for note types.
Search `~/repositories/symbolith-exogram/` for existing notes related to these items (use Grep and Glob).

For EACH item return a JSON object:
{
  "item_number": <N>,
  "classification": "<note type from exogram.yaml | Task | Trash | Skip>",
  "target": "<for Tasks: alias and path relative to the exogram root of an existing project note, 'new project', or one of these task lists: {task_list_names}>",
  "alias": "<suggested title for new notes>",
  "related_notes": [{"alias": "<alias of a related note found>", "path": "<its path relative to the exogram root>"}],
  "reasoning": "<one sentence explaining classification>"
}

You MUST pick the best classification for every item. Do not leave any unclassified.
```

## Step 4: Item-by-Item User Confirmation

Present each item one at a time using `AskUserQuestion`. Work through all items sequentially.

Every note shown to the user, here and in the Step 6 report, is `Alias file:./<path>:1:1`, alone on its line, the path relative to the working directory.

For each item, show:

```
**[N/total]** from `## SectionName`

> original text exactly as it appears in inbox

**Proposed:** Classification → new alias, or for an existing note:
Alias file:./<path>:1:1
**Exogram:** target exogram for a new note, or `undecided`
**Why:** one-sentence reasoning
**Related:**
Alias file:./<path>:1:1
```

Wait for the user's response before showing the next item:
- **y** (or empty/continuation): accept the proposal
- **n**: skip this item (leave in inbox)
- **Any other text**: treat as override instructions (e.g. "trash", "task on ProjectX", "merge with previous")

An `undecided` exogram is never accepted with **y**: ask which exogram the note goes into.

Collect all confirmed actions before executing.

## Step 5: Execute

Process all confirmed items in batch. Follow `~/repositories/symbolith-exogram/AGENTS.md` note creation workflow for new notes:
1. Read schemas (`~/repositories/symbolith-exogram/facts/exogram.yaml`, `~/repositories/symbolith-exogram/facts/properties.yaml`)
2. Search the exogram for existing related notes to link
3. Create note with proper frontmatter (ULID filename from `just ulid`, aliases, the `type` chain copied from the type's template, required properties)

For each classification:

- **Note type** → Create new note per AGENTS.md workflow, in the confirmed target exogram. Read that exogram's own `AGENTS.md` first, if it has one
- **Task + existing project** → Append `- [ ]` line to the project note
- **Task + new project** → Create Project note first (per AGENTS.md), then append task
- **Task + task list** → Append to the matching task list above `## Inbox`
- **Trash** → Just remove from inbox (no note created)
- **Skip** → Leave in place

## Step 6: Clean Up

After all items are processed:

1. Remove processed items from their `##` sections in the inbox file
2. Delete `##` sections that are now empty (header + only whitespace remaining)
3. Leave skipped items in their original sections
4. Verify the inbox file is still valid markdown

Report summary:
- Notes created
- Tasks added, with their target notes
- Items trashed
- Items skipped (still in inbox)
