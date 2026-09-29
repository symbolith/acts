---
name: improve-skill
description: Recursively improve a skill by extracting the general principles violated in the current session and folding them into its SKILL.md while shrinking, not growing, the file. Use when the user says "iterate on this skill", "update skill", "extract lesson", "the skill got this wrong", "add this lesson to the skill", or after a skill produced a wrong or suboptimal result.
argument-hint: [skill-name (optional, inferred from session)]
allowed-tools: Read, Edit, Glob, Grep, AskUserQuestion
---

# Skill Iterate

Improve a skill from what just happened in this session. The skill is loaded into context on every use, so every line costs. The goal is a smaller, sharper skill, never a longer one.

## Workflow

### 1. Identify target and failure

Target: `$0` if given, else the skill active in this session. If ambiguous, ask.

From the session, identify the concrete failure: what the skill instructed (or failed to instruct), what happened, what should have happened.

If the skill triggered at the wrong time or not at all, the bug is in the `description` metadata, not the body. Fix the trigger phrases there.

### 2. Extract the general principle

Do not record the incident. Ask: what rule, had it existed, would have prevented this failure *and* the whole class of failures like it?

- Wrong: "When exporting turtle.md, quote IRIs with spaces"
- Right: "Escape all IRI components before serialization"

One failure yields one principle. If you cannot state it in one sentence, you have not generalized enough.

### 3. Confirm with the user

Before touching the file, end the turn with one chat message, in bullets, never prose: the diagnosed failure, the extracted principle, the concrete fix, and the alternative diagnoses you considered.
No AskUserQuestion: chat text before a tool call is swallowed, so the message must end the turn and the user confirms or corrects free-form.
Edit only after the user confirms; if they correct the diagnosis, re-extract and ask again.
The user naming the failure is the trigger, never the confirmation; this step has no exemptions.

### 4. Fold it in

Find the skill's source and edit it there: `~/repositories/symbolith-exogram/acts/plugins/<plugin>/skills/<name>/SKILL.md`.

- State each rule as one short sentence; one sentence per line.
- Place the principle where it acts: amend the step that failed, don't append a "Lessons" section.
- If an existing rule almost covers it, sharpen that rule instead of adding a new one.
- Net line count must not grow beyond a few lines. Pay for additions by cutting: merge overlapping rules, delete anything Claude already knows, drop dead examples.
- No formalism: no changelogs, no rationale, no "learned on date", no meta-commentary. The skill states rules, not their history.

### 5. Verify size

After editing, the SKILL.md must still read as a minimal instruction set. If it exceeds ~150 lines, cut until it doesn't, or move detail to `references/`.

### 6. Report

State the extracted principle in one sentence, the edited path, and remind the user to re-invoke the skill for changes to take effect.
