---
name: step-factor
description: Step one Factor or Project note as the machine. Finds the member acts that are ready, does each with do-act, repeats until no act is left, and reports the factor's state as derived from its members. Use when the user asks to "step this factor", "run this project", "work the project", "do the factor", or names a Factor or Project note to work on.
argument-hint: <factor or project note id or alias>
allowed-tools: Read, Grep, Glob, Bash(just:*)
---

# Step Factor

`$ARGUMENTS` names one Factor or Project note, by id or alias. A note id is unique across the exogram workspace root, so `**/<id>.md` finds the file.

## Step

1. Collect the members: every act or factor whose `isPartOf` names the factor.
2. Find the ready members: an act not `succeeded` whose every `follows` act is `succeeded`; a member factor counts as succeeded when every act of it is.
3. No ready member and no open member: stop, the factor is done.
4. No ready member but open members: stop, name the act that blocks and what it follows.
5. Take one ready act and do it with `/exogram:do-act`. A ready member factor is stepped by this skill.
6. Repeat from 1.

## Report

- The factor's state, derived: succeeded when every member succeeded, failed when a member is `failed`, else the acts still open.
- Set nothing on the factor note.

## Never

- Write `hasState`, `hasClaimant` or `contributor` on the factor.
- Claim an act in this skill. Claiming, planning and doing belong to do-act.
