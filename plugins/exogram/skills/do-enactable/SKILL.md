---
name: do-enactable
description: Enact an Act or Factor note by the premise of the act Doing an Enactable. Prepares by building the DAG of what it follows and enacting the leaves first, then claims, does and settles the act. Use when the user asks to "do this act", "do this task", "do enactable", "work on this task", "enact", or names an Act, Factor or Project note to work on.
argument-hint: <act or factor note id or alias>
allowed-tools: Read, Grep, Glob, Edit, Bash(just:*)
---

# Do Enactable

`$ARGUMENTS` names one Act or Factor note, by id or alias. The exogram workspace root is `${CLAUDE_PLUGIN_ROOT}/../../..`; a note id is unique across it, so `**/<id>.md` finds the file.

## Prepare

### Act

1. Build the DAG of its `follows`, transitively, leaving out every `succeeded` act.
2. Take a leaf of the DAG.
3. Enact a blocker with Prepare and Do of its own.
4. Repeat from 1 until the leaf is the act asked for.

### Factor, a Project included

1. Build the DAG of every act or factor whose `isPartOf` names it and their `follows`, transitively, leaving out every `succeeded` one.
2. Take a leaf of the DAG.
3. Enact it with Prepare and Do of its own.
4. Repeat from 1 until the DAG is empty.

## Do

### Act

5. Read the act's `hasIntent`, `hasApplicability`, and every `hasInput` and `hasPremise` note in full.
6. Set `hasActState: claimed` and `lead` to the current agent.
7. Propose the plan as the final chat message in this template, then STOP until the user agrees.
   Show the issue, the source lines, and the changed lines verbatim, never a description of them.

   ```
   ## Issue
   <what is wrong and what it breaks, three short sentences at most>

   ## Source
   <per place the issue shows: file link, then its lines quoted verbatim>

   ## Fix
   <per changed place: file link, then a diff of old and new lines>

   ## Open questions
   <question, then the recommended answer>
   ```

8. Do the act: produce every note `hasOutput` names. When it needs acts that do not exist yet, create them with `/exogram:create-act`, link them in `follows`, and enact them by this skill.
9. Set `hasActState: succeeded` when every `hasOutput` exists, else `failed`, then `just validate <file>`.

### Factor, a Project included

5. Set `hasFactorState` to `succeeded`.
