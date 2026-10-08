---
name: do-actable
description: Enact an Actable note by the premise of the act Doing an Actable. Prepares by building the DAG of what it requires and enacting the leaves first, then claims, does and settles the act. Use when the user asks to "do this act", "do this task", "do actable", "work on this task", "enact", or names an Act, Task or Project note to work on.
argument-hint: <actable note id or alias>
allowed-tools: Read, Grep, Glob, Edit, Bash(just:*)
---

# Do Actable

`$ARGUMENTS` names one Actable note, by id or alias. The exogram workspace root is `/home/beavis/repositories/symbolith-exogram`; a note id is unique across it, so `**/<id>.md` finds the file.

## Prepare

### Act or Task

1. Build the DAG of its `requires`, transitively, leaving out every `succeeded` actable.
2. Take a leaf of the DAG.
3. Enact a blocker with Prepare and Do of its own.
4. Repeat from 1 until the leaf is the actable asked for.

### Factor, a Project included

1. Build the DAG of every actable whose `hasProject` names it and their `requires`, transitively, leaving out every `succeeded` actable.
2. Take a leaf of the DAG.
3. Enact it with Prepare and Do of its own.
4. Repeat from 1 until the DAG is empty.

## Do

### Act or Task

5. Read the act's `hasIntent`, `hasApplicability`, and every `hasInput` and `hasPremise` note in full.
6. Set `state: claimed` and `lead` to the current agent.
7. Do the act: produce every note `hasOutput` names. When it needs acts that do not exist yet, create them with `/exogram:create-act`, link them in `hasPotential`, and enact them by this skill.
8. Set `state: succeeded` when every `hasOutput` exists, else `failed`, then `just validate <file>`.

### Factor, a Project included

5. Set `state: succeeded`.
