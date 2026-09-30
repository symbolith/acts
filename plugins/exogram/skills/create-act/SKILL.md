---
name: create-act
description: Create an Act note, or a note of one of Act's subtypes (Project, Job Application, whatever the facts exogram declares), in an exogram. Use when the user asks to "create an act", "new act", "add an act", "record a task as a note", "create a project note", "new project", "add a job application", or wants one unit of work captured as a note.
argument-hint: [subtype] <title or description> [in: <exogram>]
allowed-tools: Read, Write, Glob, Grep, Bash(just:*), AskUserQuestion
---

# Create Act

Create one note typed `Type Act` or a subtype of it. The exogram root is `/home/beavis/repositories/symbolith-exogram`; every path below is absolute or relative to it. Preview first, write only on approval. Type chain, field set, and enums come from the facts schema at run time, never from this file.

## Inputs

- `$ARGUMENTS`: an optional subtype title (`Project`, `JobApplication`), the title or a description of the act, optionally `in: <exogram folder>`. Everything missing comes from the conversation, then from a question.

## Workflow

### 1. Resolve the Type

- Act is `facts/exogram/20260608023505.md`. Its subtypes are the type notes in `facts/exogram/` whose `subClassOf` names that id; grep for it, never trust the type note's `Subtypes` result block, it may be stale.
- Take the subtype the user named or implied ("project" means `Type Project`). Default is Act itself.
- Read `facts/.templates/<Title>.md` for the type chain and the field set. The `type` list is copied verbatim.

### 2. Resolve the Exogram

The note lives in the exogram of its subject: the folder from `in:`, else the folder of the notes the act reads and writes, else the current working directory when it is an exogram. Otherwise ask.

Read that exogram's `AGENTS.md` and obey it. Where it forbids reading notes without permission (factors does), link only by grepping `aliases` lines, never open a note body.

### 3. Find Related Notes

Grep the exogram, and `facts/exogram/` for types and people, for:

- the facts the act reads and writes, by alias; a note that exists and is only read is linked by `hasInputFact`, a note that exists and is changed by `used`, one that does not exist yet gets a Place, linked by `hasInput` / `hasOutput`
- other acts in the folder that write what this one reads, or read what this one writes, by fact or place: the candidates for `requires` and `precedes`; acts this one may fuse: the candidates for `hasPotential`
- people and software the description names

Cap at the top five candidates per property, confirm by alias and `comment` only.

### 4. Ask, Every Run

Ask with `AskUserQuestion`; the fields are the template's keys, never a list from this file, and `aliases`, `type` and `reviewLevel` are set without asking.

- Ask each `required` field; it has no default and no empty answer.
- Offer all `optional` fields as one selectable list, then ask only the selected ones; the rest are dropped.
- Every question suggests values: the candidates from step 3, and for an enumerated range (`state`: the notes typed `Type State`) its members, each by the local name of its `iri`.
- A field whose schema allows a literal takes free text; no note is created for it.
- A field the user already answered is never asked again and its answer never reworded.
- One question settles one field. A conflict between an answer and a rule or another field is asked as that field's question, never deferred to the preview.
- An answer the schema cannot hold stops the run: name the property and `/exogram:create-property`, change no schema.

Acts relate only as the formalism relates transitions, through shared facts (`requires`, `precedes`) and potentials (`hasPotential`), never through `isPartOf`.

Each input or output takes one of three forms, settled in the same question: an existing note, linked in `hasInputFact` when read, in `used` when changed; the data itself, a literal in `hasInputFact` / `hasOutputFact`; a fact that does not exist yet, a new Place linked in `hasInput` / `hasOutput`, or `hasInputs` / `hasOutputs` when the place closes or opens a map.

`hasOutput` and `hasOutputFact` are `generated` in PROV-O: the entity did not exist before the act. A note the act edits existed before, so it is `used`, never an output.

When `requires` or `precedes` comes back empty but the inputs or outputs did not, derive the edges:

- `requires`: every act in the exogram whose outputs name a place or fact among this act's inputs.
- `precedes`: every act in the exogram whose inputs name a place or fact among this act's outputs.

Grep the frontmatter for these, list what was derived in the preview, and write the edges into this note only; the other acts stay untouched.

### 5. Draft

The note is the template, filled; nothing the template lacks is added, and the body stays as the template has it.

- `aliases[0]`: a title the user gave, verbatim; else the template's alias line decides the shape, and the title of an Act is an imperative sentence naming the state change, e.g. `Add CI for the TLC checks`.
- `type`: the template chain, verbatim.
- Every other key: the answer from step 4, a link as `"[<alias>](<id>.md)"`, a literal as a plain string.
- `reviewLevel: unread`.
- A key answered empty is dropped.

### 6. Preview

Print the complete note, every new Place note, their target paths, and the related notes found with one line of justification each, as chat text, then end the turn.
No `AskUserQuestion` here: text before a tool call is swallowed. The user approves or corrects free-form.

### 7. Write

Only after approval:

```bash
just --justfile /home/beavis/repositories/symbolith-exogram/justfile ulid
```

One ULID per file. Write `<exogram>/<ULID>.md` for the act and one for each new Place, from `facts/.templates/Place.md`, alias the fact it will hold, `reviewLevel: unread`, `optional` keys dropped. Check no file exists first. Then:

```bash
just --justfile /home/beavis/repositories/symbolith-exogram/justfile validate '<exogram>/<ULID>.md'
```

for every file written.

Fix what it reports and rerun until clean.

### 8. Report

The paths of the notes written and the fact, place, `used`, `requires` and `precedes` links set. Nothing else.

## Hard Rules

- Never write a canon note (`reviewLevel: canon`) and never edit any existing note; this skill creates the act note and its new places, nothing else.
- Never edit content between dataview-serializer markers.
- Filename is a ULID from `just ulid`, never invented, never descriptive.
- Never set `reviewLevel` above `unread`.
- No note is written before the user approved the preview.

## Anti-patterns

- Hardcoding the subtype list, the type chain or the field set instead of reading `facts/`
- Linking a fact that does not exist yet instead of creating its place
- Putting a note the act edits into `hasOutput` or `hasOutputFact`; an edited note is `used`
- Asking every optional field one by one
- Writing a body, a heading or a key the template does not have
- Opening note bodies in an exogram whose `AGENTS.md` forbids it