---
name: sync-session
description: Sync only the work of the current session, commit the files this session changed and what they need to stand on feature branches and open pull requests, and leave every other local change untouched. Use when the user asks to "sync this session", "sync session", "commit this session", "land what we did", "commit what you just changed", "push only this session's changes", or wants the session's edits landed without the rest of the workspace.
argument-hint: [repository folder ...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

# Sync Session

Land the work of this session as self-contained commits. This skill builds the list of files the session changed and hands it to `exogram:sync-workspace`, which runs every git command behind its gates. This skill runs no state-changing git itself. The exogram root is `/home/beavis/repositories/symbolith-exogram`.

## Inputs

- `$ARGUMENTS`: optional repository folders to limit the run, passed on unchanged.

## Workflow

### 1. Collect

Session work is every file this session created, edited, renamed, or deleted, through Edit, Write, NotebookEdit, a Bash command, or a subagent. A generated file counts when a session command rewrote it (`just templates`, `just init`).

Build the list from the transcript, never from memory.

```bash
transcript=$(ls ~/.config/claude/projects/*/${CLAUDE_SESSION_ID}.jsonl)
tool_calls='select(.type == "assistant") | .message.content[]? | select(.type == "tool_use")'
jq -r "$tool_calls | select(.name == \"Edit\" or .name == \"Write\" or .name == \"NotebookEdit\") | .input.file_path // .input.notebook_path" "$transcript" | sort -u
jq -r "$tool_calls | select(.name == \"Bash\") | .input.command" "$transcript"
```

The first query prints the files edited by tool. Read every command of the second and add each file it wrote: `sed -i`, a redirect, `mv`, `rm`, a `just` recipe that generates files. Add what a subagent reported as changed.

### 2. Check

Per listed file, with read-only git:

| Finding | Action |
| --- | --- |
| outside the exogram root | drop, report as not synced |
| ignored by git | drop, report |
| no change in `git status --porcelain -- <file>` | drop: already committed or reverted |
| `git diff HEAD -- <file>` holds a hunk the session did not write | keep: the file is committed whole |
| refers to an uncommitted file | add that file, with the reason |

The session's edits seed the list; everything they need to stand joins it.
Ask, as the Decisions section of `exogram:sync-workspace` demands, only when an addition carries an intent unrelated to the session's work.

### 3. Hand over

An empty list: stop and say the session left nothing uncommitted.

Otherwise:

1. Print the list grouped by repository, a note with its alias, and every added or dropped file with its reason.
2. Write the list to a scratch file by absolute path, one path per line, relative to the exogram root.
3. Invoke `exogram:sync-workspace` with `--files-from <scratch file> $ARGUMENTS`.

The package gate of `exogram:sync-workspace` is where the user corrects the list.

## Anti-patterns

- A state-changing git command in this skill
- A list built from memory, without the transcript
- A file listed because it is changed, not because the session changed or needs it
- A commit that refers to something uncommitted
