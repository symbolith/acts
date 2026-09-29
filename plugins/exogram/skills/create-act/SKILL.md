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

One `AskUserQuestion` with:

- `state`, options are the notes typed `Type State` in `facts/exogram/`, each by the local name of its `iri`; there is no default.
- inputs: every fact the act reads, candidates from step 3; empty is a valid answer.
- outputs: every fact the act writes, candidates from step 3, each marked as created or as changed; empty is a valid answer.
- `requires`: the acts that must be done before this one, candidates from step 3; empty is a valid answer.
- `precedes`: the acts this one must be done before; empty is a valid answer.
- `hasPotential`: the acts this one may fuse; empty is a valid answer.

Acts relate only as the formalism relates transitions, through shared facts (`requires`, `precedes`) and potentials (`hasPotential`), never through `isPartOf`.

Never skip any of these questions, even when no candidate was found; then offer the free answer.

Each input or output takes one of three forms, settled in the same question: an existing note, linked in `hasInputFact` when read, in `used` when changed; the data itself, a literal in `hasInputFact` / `hasOutputFact`; a fact that does not exist yet, a new Place linked in `hasInput` / `hasOutput`, or `hasInputs` / `hasOutputs` when the place closes or opens a map.

`hasOutput` and `hasOutputFact` are `generated` in PROV-O: the entity did not exist before the act. A note the act edits existed before, so it is `used`, never an output.

When `requires` or `precedes` comes back empty but the inputs or outputs did not, derive the edges:

- `requires`: every act in the exogram whose outputs name a place or fact among this act's inputs.
- `precedes`: every act in the exogram whose inputs name a place or fact among this act's outputs.

Grep the frontmatter for these, list what was derived in the preview, and write the edges into this note only; the other acts stay untouched.

### 5. Draft

Frontmatter, from the template:

- `aliases[0]`: the template's alias line decides the shape. Act: an imperative sentence naming the state change, e.g. `Add CI for the TLC checks`. Project: `Project <Name>`. Job Application: no prefix, a noun phrase naming position and employer.
- `type`: the template chain, verbatim.
- `state`: the answer from step 4.
- `hasInputFact`, `hasOutputFact`, `used`, `hasInput`, `hasOutput`, `requires`, `precedes`, `hasPotential`: the answers from step 4; `contributor`: the links from step 3; all in the form `"[<alias>](<id>.md)"`, a literal fact as a plain string; a note in another exogram is linked as `../<exogram>/<id>.md`.
- `comment`: one sentence, only when the title does not carry the whole point.
- `lang`: omitted for English.
- `reviewLevel: unread`.
- Every other template key still `optional` is dropped.

Body, one sentence per line:

- First the situation the act changes, with the sites it concerns as `file:` references.
- Then the instruction, what done looks like.
- Every noun that names an exogram entity is a markdown link.
- Project and Job Application: a `## Tasks` list of `- [ ]` items, existing acts as links.
- Act: no headings unless the note argues alternatives; then `## Problem`, `## Solutions`, `## Open questions`.

### 6. Preview

Show the complete note, every new Place note, and their target paths, then ask for approval with `AskUserQuestion`. Include the related notes found, one line of justification each, so a false match can be vetoed.

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

- Hardcoding the subtype list or the type chain instead of reading `facts/exogram/`
- A noun-phrase Act title, or a Project title without the `Project` prefix
- Linking a fact that does not exist yet instead of creating its place
- Putting a note the act edits into `hasOutput` or `hasOutputFact`; an edited note is `used`
- Defaulting `state`
- A body without links although the description names exogram entities
- Opening note bodies in an exogram whose `AGENTS.md` forbids it
- Leaving `optional` markers in the written frontmatter
