---
name: sync-session
description: Sync only the work of the current session, commit the hunks this session wrote and what they need to stand on feature branches and open pull requests, and leave every other local change untouched. Use when the user asks to "sync this session", "sync session", "commit this session", "land what we did", "commit what you just changed", "push only this session's changes", or wants the session's edits landed without the rest of the exogram workspace.
argument-hint: [repository folder ...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

# Sync Session

Land the work of this session as self-contained commits. This skill builds the list of what the session wrote, by file and by hunk, and hands it to `exogram:sync-workspace`, which runs every git command behind its gates. This skill runs no state-changing git itself. The exogram workspace root is `${CLAUDE_PLUGIN_ROOT}/../../..`.

## Inputs

- `$ARGUMENTS`: optional repository folders to limit the run, passed on unchanged.

## Workflow

### 1. Collect

Session work is what this session wrote through Edit, Write, NotebookEdit, a Bash command, or a subagent: every file it created, renamed, or deleted, and of a file it edited only its own hunks. A generated file counts when a session command rewrote it (`just templates`, `just init`).

Build the list from the transcript, never from memory.

```bash
transcript=$(ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/projects/*/${CLAUDE_SESSION_ID}.jsonl)
tool_calls='select(.type == "assistant") | .message.content[]? | select(.type == "tool_use")'
jq -r "$tool_calls | select(.name == \"Edit\" or .name == \"Write\" or .name == \"NotebookEdit\") | .input.file_path // .input.notebook_path" "$transcript" | sort -u
jq -r "$tool_calls | select(.name == \"Bash\") | .input.command" "$transcript"
```

The first query prints the files edited by tool; the `old_string` and `new_string` of each Edit name its hunk. Read every command of the second and add each file it wrote: `sed -i`, a redirect, `mv`, `rm`, a `just` recipe that generates files. Add what a subagent reported as changed.

### 2. Check

Per listed file, with read-only git:

| Finding | Action |
| --- | --- |
| outside the exogram workspace root | drop, report as not synced |
| ignored by git | drop, report |
| no change in `git status --porcelain -- <file>` | drop: already committed or reverted |
| `git diff --no-ext-diff HEAD -- <file>` holds a hunk the session did not write | run `python3 ${CLAUDE_SKILL_DIR}/scripts/session-patch.py <transcript> <file> > <scratch patch>` and list the file with the patch; if it fails, a session edit stands on a foreign hunk: list the file whole, with the reason |
| refers to an uncommitted file | add that file, with the reason |

The session's edits seed the list; everything they need to stand joins it.
Ask, as the Decisions section of `exogram:sync-workspace` demands, only when an addition carries an intent unrelated to the session's work.

### 3. Hand over

An empty list: stop and say the session left nothing uncommitted.

Otherwise:

1. Print the list grouped by repository, a note with its alias, a file with a patch marked `hunk only`, and every added or dropped file with its reason.
2. Redirect the list into a scratch file by absolute path, one line per file: its path relative to the exogram workspace root, then a tab and the absolute path of its patch when it has one.
3. Invoke `exogram:sync-workspace` with `--files-from <scratch file> $ARGUMENTS`.

The package gate of `exogram:sync-workspace` is where the user corrects the list.

## Anti-patterns

- A state-changing git command in this skill
- An Edit or Write call: a scratch file comes from a Bash redirect
- A list built from memory, without the transcript
- A file or hunk listed because it is changed, not because the session wrote or needs it
- A commit that refers to something uncommitted
