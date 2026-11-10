---
name: do-act
description: Do one Act note as the agent. Prepares by building the DAG of what it follows and doing the leaves first, then asks to claim the act, shows the fix and stops for the user, does it and proposes its outputs. Use when the user asks to "do this act", "work on this act", "do act", or names an Act note to work on. For a Factor or Project use step-factor.
argument-hint: <act note id or alias>
allowed-tools: Read, Grep, Glob, Edit, Bash(just:*)
---

# Do Act

`$ARGUMENTS` names one Act note, by id or alias. A note id is unique across the exogram workspace root, so `**/<id>.md` finds the file.

## Prepare

1. Build the DAG of its `follows`, transitively, leaving out every `succeeded` act.
2. Take a leaf of the DAG.
3. Do the leaf with Prepare and Do of its own.
4. Repeat from 1 until the leaf is the act asked for.

## Do

5. Read the act's `hasIntent`, `hasApplicability`, and every `hasInput` and `hasPremise` note in full.
6. Ask to claim the act. Write the claim: `hasClaimant` is the user's Person note, which joins `contributor`, and `hasState` is `claimed`.
7. Show the fix as the final chat message in this template, then STOP until the user agrees.
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

8. Do the act: produce every note `hasOutput` names. When it needs acts that do not exist yet, create them with `/exogram:create-act`, link them in `follows`, write `hasState: intended`, remove `hasClaimant`, and do them by this skill.
9. Propose the outputs. Write `hasState: succeeded` when every `hasOutput` exists, else `failed`, remove `hasClaimant`, then `just validate <file>`.

## Never

- Set a state on a Factor or Project. A factor's state is derived from its acts.
- Edit without the user's go on the fix.
