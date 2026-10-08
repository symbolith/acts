---
name: create-act
description: Create an Act note, or a note of one of Act's subtypes (Project, Job Application, whatever the facts exogram declares), in an exogram. Use when the user asks to "create an act", "new act", "add an act", "record a task as a note", "create a project note", "new project", "add a job application", or wants one unit of work captured as a note.
argument-hint: [subtype] <title or description> [in: <exogram>]
allowed-tools: Read, Write, Glob, Grep, Bash(just:*), AskUserQuestion
---

# Create Act

Create one note typed `Type Act` or a subtype of it; several acts in one request share one research pass, one question round and one preview. The exogram workspace root is `/home/beavis/repositories/symbolith-exogram`; every path below is absolute or relative to it. Preview first, write only on approval. Type chain, field set, and enums come from the facts schema at run time, never from this file.

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

Read the `AGENTS.md` in the root of that exogram's repository, when it has one, and the `hasPremise` notes of the acts it imports, and obey them. Where a premise forbids reading notes without permission (factors does), link only by grepping `aliases` lines, never open a note body.

### 3. Research and Fill

Derive a value for every key of the template before asking anything; the fields are the template's keys, never a list from this file. The sources are:

- the conversation: a value the user gave is taken verbatim, never asked again, never reworded
- the values that notes of the same type in the exogram already hold for that key
- everything the work will read, found without being told: the canon of the act's subject (the Exogram note's `canon`), its indexes, and the notes on the subject, by alias
- the premises that govern this kind of work, and every rule the user states for it
- people and software the description names, grepped in the exogram and in `facts/exogram/`
- for an enumerated range (`state`: the notes typed `Type State`) its members, each by the local name of its `iri`

Read every source the act names, a URL or a note, before filling a key.
Read the `comment` of each key's property note in `facts/exogram/` and write the value as the answer to that definition asked of this act itself, never of what its output is later used for; a sentence that does not answer it is no value.

Confirm a note by alias and `comment` only. A literal stays a literal.
An input, output or premise is always a note, never a bare URL or loose text: an external resource is a note of the fitting type (`Type Source` for a text), stated rules are a `Type Premise` note. A missing one is drafted from its template and created with the act.
Acts created together share their premises, and an act that continues another reads what the other read.
A value of the wrong type is resolved along the graph, never flagged back: a parent that is a Task gives its own `hasProject` and takes this act into its `requires`.

Acts relate only as the formalism relates transitions, through what they read and write (`requires`) and potentials (`hasPotential`), never through `isPartOf`. NEVER write `precedes`: it is the inverse of `requires`, derived by query. Derive the edges, never ask them:

- This act's `requires`: every act in the exogram whose outputs name a note among this act's inputs.
- Another act's `requires`: this act goes into every act in the exogram whose inputs name a note among this act's outputs.

Grep the frontmatter for these and write the edges. For every other note edited, set its `reviewLevel: unread` and validate it with the new note.

An act that is a potential of another act goes into that act's `hasPotential`: edit the parent note, set its `reviewLevel: unread`, and validate it with the new note.

An `optional` key with no derivable value is dropped, never asked.

### 4. Ask Design Questions Only

Ask with `AskUserQuestion`, in one round, only what step 3 could not settle:

- a blocker, asked first: a type or property the act needs and the exogram lacks. Name the skill that creates it (`/exogram:create-type`, `/exogram:create-property`) and change no schema here.
- a `required` key with no derivable value or with several equally good ones, each option a candidate from step 3
- a conflict between two derived values

Nothing left to ask means no question: go to the draft. A derived value is corrected in the preview, never confirmed by a question.
A rejected value is derived again from the reason given and shown in a new preview, never asked back; this overrides the global stop-and-ask rule.

### 5. Draft

The note is the template, filled; nothing the template lacks is added, and the body stays as the template has it.

- `aliases[0]`: a title the user gave, verbatim; else the template's alias line decides the shape, and the title of an Act is an imperative sentence naming the state change, e.g. `Add CI for the TLC checks`.
- `type`: the template chain, verbatim.
- Every other key: the value from steps 3 and 4, a link as `"[<alias>](<id>.md)"`, a literal as a plain string.
- `reviewLevel: unread`.

### 6. Preview

Print the complete note, every input, output or premise note to create, the target paths, and every derived value with one line of justification, as chat text, then end the turn.
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

- Never edit content between dataview-serializer markers.
- Filename is a ULID from `just ulid`, never invented, never descriptive.
- Never set `reviewLevel` above `unread`.
- No note is written before the user approved the preview.

## Anti-patterns

- Hardcoding the subtype list, the type chain or the field set instead of reading `facts/`
- Naming a property the template does not have
- Asking a value that the exogram or the conversation already answers
- Offering optional fields as a menu
- Asking the user to supply a value after they rejected one
- Leaving the user to add inputs or premises the exogram already holds
- Raising a caveat the user's own rule already settles
- Writing a body, a heading or a key the template does not have
- Opening note bodies in an exogram whose premise forbids it
