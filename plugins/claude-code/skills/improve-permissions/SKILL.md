---
name: improve-permissions
description: Consolidate every settings.local.json into the exogram workspace settings or the global settings and delete it. This skill should be used when the user asks to "improve permissions", "consolidate permissions", "merge local permissions", "review permission settings", or "clean up claude permissions".
---

# Improve Permissions

Consolidate every `settings.local.json` into shared settings, then delete it; no permission stays local.

## Instructions

### 1. Collect & Diff

Run the collection script:

```bash
bash ~/repositories/symbolith-exogram/acts/plugins/claude-code/skills/improve-permissions/scripts/collect-permissions.sh
```

This outputs tab-separated lines: `permission\tsource_projects`
Only permissions NOT already in global allow or deny or in `~/repositories/symbolith-exogram/exogram/settings.json` are shown.

### 2. Normalize

Before categorizing, normalize project-specific permissions into general forms:
- Strip path-specific prefixes from git commands, keeping only the subcommand: `Bash(git -C /specific/path log:*)` → `Bash(git log:*)`
- Skip `WebFetch(domain:x)` entries when bare `WebFetch` is already in global allow
- Skip permissions that are subsets of already-global ones (e.g. `Bash(cat:*)` is already global, so `Bash(cat /specific/file)` is redundant)
- Deduplicate after normalization

### 3. Categorize

Apply rules from `~/repositories/symbolith-exogram/acts/plugins/claude-code/skills/improve-permissions/references/categorization-rules.md`:
- **Safe**: read-only, no state changes
- **Maybe safe**: side effects, but controlled/reversible
- **Not safe**: destructive, never auto-add

For Bash permissions, match the command prefix (e.g. `Bash(cargo check:*)` matches "cargo check" in the rules).
For MCP permissions, check if the tool name ends with a read-type verb (read, get, list, search).

### 4. Report

Display three markdown tables with columns: Permission | Source Projects | Category

### 5. Auto-add safe

Add all **safe** permissions to their target (step 7). Inform the user what was added.

### 6. Ask about maybe-safe

Use `AskUserQuestion` to present **maybe-safe** permissions for batch approval.
Group related permissions (e.g. all cargo commands together) into multi-select questions.

### 7. Update the targets

- The exogram workspace root is `~/repositories/symbolith-exogram`. The exogram workspace settings are `~/repositories/symbolith-exogram/exogram/settings.json`.
- The target follows the source, never the command. Global settings belong to dotfiles.
- A permission from a `settings.local.json` inside the exogram workspace root goes to the exogram workspace settings; then run `just init`, which writes it into every `.claude/settings.json` there.
- A permission from outside goes to `~/.config/claude/settings.json`; one from both sides goes to both.
- Add to `.permissions.allow`, keep it sorted, preserve all other fields.

### 8. Flag deny conflicts

If any candidate permission appears in the global `.deny` list, inform the user:
> "Permission `X` is in global deny. It may be overridden locally but won't be added globally."

Do NOT add these to the allow list.

### 9. Delete the local files

After the user approved the result, delete every consolidated `settings.local.json`; a rejected permission is dropped with it.

### 10. Summary

Print final counts:
- Added (safe, auto)
- Added (maybe-safe, approved)
- Skipped (already global)
- Skipped (redundant after normalization)
- Rejected (not safe)
- Conflicts (in deny list)
