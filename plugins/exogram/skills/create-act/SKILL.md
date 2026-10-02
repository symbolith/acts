---
name: create-act
description: Create an Act note, or a note of one of Act's subtypes (Project, Job Application, whatever the facts exogram declares), in an exogram. Use when the user asks to "create an act", "new act", "add an act", "record a task as a note", "create a project note", "new project", "add a job application", or wants one unit of work captured as a note.
argument-hint: [subtype] <title or description> [in: <exogram>]
allowed-tools: Read, Write, Glob, Grep, Bash(just:*), AskUserQuestion
---

# Create Act

Create one note typed `Type Act` or a subtype of it. The exogram workspace root is `/home/beavis/repositories/symbolith-exogram`; every path below is absolute or relative to it. Preview first, write only on approval. Type chain, field set, and enums come from the facts schema at run time, never from this file.

## Inputs

- `$ARGUMENTS`: an optional subtype title (`Project`, `JobApplication`), the title or a description of the act, optionally `in: <exogram folder>`. Everything missing comes from the conversation, then from a question.

## Workflow

### 1. Resolve the Type

- Act is `facts/exogram/20260608023505.md`. Its subtypes are the type notes in `facts/exogram/` whose `subClassOf` names that id; grep for it, never trust the type note's `Subtypes` result block, it may be stale.
- Take the subtype the user named or implied ("project" means `Type Project`), and never question it. Default is Act itself.
- Read `facts/.templates/<Title>.md` for the type chain and the field set. The `type` list is copied verbatim.

### 2. Resolve the Exogram

The note lives in the exogram of its subject: the folder from `in:`, else the folder of the notes the act reads and writes, else the current working directory when it is an exogram. Otherwise ask.

Its notes folder is the exogram workspace root for the Symbolith exogram, the member folder for a notes-only member (`gordian-exogram`, `infai-exogram`), and `<member>/exogram/` for a software member.

Read the `AGENTS.md` in the root of that exogram's repository, when it has one, and obey it. Where it forbids reading notes without permission (factors does), link only by grepping `aliases` lines, never open a note body.

### 3. Find Related Notes

For every key of the template, the candidates are:

- the values that notes of the same type in the exogram already hold for that key
- the notes the act reads and writes, by alias: the candidates for the template's input and output keys
- other acts in the folder that write what this one reads, or read what this one writes: the candidates for `requires` and `precedes`
- people and software the description names, grepped in the exogram and in `facts/exogram/`

Cap at the top five candidates per key, confirm by alias and `comment` only.

### 4. Ask, Every Run

Ask with `AskUserQuestion`; the fields are the template's keys, never a list from this file, and `aliases`, `type` and `reviewLevel` are set without asking.

- Ask each `required` field; it has no default and no empty answer.
- Ask the template's input and output keys: which notes the act reads, which it writes.
- Offer every remaining `optional` field as a selectable list, over several questions when one cannot hold them all, then ask only the selected ones; the rest are dropped.
- Every question suggests values: the candidates from step 3, and for an enumerated range (`state`: the notes typed `Type State`) its members, each by the local name of its `iri`.
- A literal answer is written as a literal; no note is ever created to hold an answer.
- A field the user already answered is never asked again and its answer never reworded.
- One question settles one decision. A conflict between an answer and another field is asked as that field's question, never deferred to the preview.
- An answer the schema cannot hold stops the run: name the property and `/exogram:create-property`, change no schema.

Acts relate only as the formalism relates transitions, through what they read and write (`requires`, `precedes`) and potentials (`hasPotential`), never through `isPartOf`.

When `requires` or `precedes` comes back empty but the inputs or outputs did not, derive the edges:

- `requires`: every act in the exogram whose outputs name a note among this act's inputs.
- `precedes`: every act in the exogram whose inputs name a note among this act's outputs.

Grep the frontmatter for these, list what was derived in the preview, and write the edges into this note only; the other acts stay untouched.

### 5. Draft

The note is the template, filled; nothing the template lacks is added, and the body stays as the template has it.

- `aliases[0]`: a title the user gave, verbatim; else the template's alias line decides the shape, and the title of an Act is an imperative sentence naming the state change, e.g. `Add CI for the TLC checks`.
- `type`: the template chain, verbatim.
- Every other key: the answer from step 4, a link as `"[<alias>](<id>.md)"`, a literal as a plain string.
- `reviewLevel: unread`.
- A key answered empty is dropped.

### 6. Preview

Print the complete note, its target path, and the related notes found with one line of justification each, as chat text, then end the turn.
No `AskUserQuestion` here: text before a tool call is swallowed. The user approves or corrects free-form.

### 7. Write

Only after approval:

```bash
just --justfile /home/beavis/repositories/symbolith-exogram/justfile ulid
```

Write `<notes folder>/<ULID>.md`, the notes folder from step 2. Check no file exists first. Then:

```bash
just --justfile /home/beavis/repositories/symbolith-exogram/justfile validate '<notes folder>/<ULID>.md'
```

Fix what it reports and rerun until clean.

### 8. Report

The path of the note written and the links set. Nothing else.

## Hard Rules

- Never write a canon note (`reviewLevel: canon`) and never edit any existing note; this skill creates the act note, nothing else.
- Never edit content between dataview-serializer markers.
- Filename is a ULID from `just ulid`, never invented, never descriptive.
- Never set `reviewLevel` above `unread`.
- No note is written before the user approved the preview.

## Anti-patterns

- Hardcoding the subtype list, the type chain or the field set instead of reading `facts/`
- Naming a property the template does not have
- Leaving a template key out of the questions
- Asking every optional field one by one
- Writing a body, a heading or a key the template does not have
- Opening note bodies in an exogram whose `AGENTS.md` forbids it
