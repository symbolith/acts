---
name: check-frontmatter
description: Validate exogram note YAML frontmatter against the exogram schemas and fix every fixable issue. Use when the user asks to "cleanup yaml", "check frontmatter", "validate frontmatter", "fix yaml", "lint notes", or after adding or changing a schema property.
argument-hint: [file-or-glob]
allowed-tools: Read, Edit, Glob, Grep, Bash(just validate:*), Bash(just templates:*), AskUserQuestion
---

# Check Frontmatter

Validate YAML frontmatter of exogram notes against the exogram schemas and fix what can be fixed.

## Validator

Never check notes by reading them. Run the validator from `/home/beavis/repositories/symbolith-exogram`:

```sh
just validate [glob]
```

It runs `~/repositories/symbolith-exogram/exogram/scripts/validate.py` in the podman image `exogram-skills` and validates each note against `facts/exogram.yaml`, `facts/properties.yaml`, and `facts/types/*.yaml`. It also reports `missing superclass` when a note's `type` list lacks a superclass of one of its types; the fix is to append the missing entries to `type`, as the type's template shows. A run without a glob also checks the schema itself: `domain does not cover the type` on a type file that attaches a property whose note's `domain` names neither that type nor a supertype (fix the attachment or the domain, never guess which), and `stale type file`, `stale schema file` or `stale template` when `types/<Title>.yaml`, `exogram.yaml`, `properties.yaml` a template, or a type note's `template` link differs from what `facts/scripts/templates.py` renders from the type and property notes; the fix is `just templates`. Output is one tab-separated line per issue: level, file, property, message. An `error` violates the schema and sets exit code 1. A `warning` marks a property the schema does not know; the schema allows those, so a warning never fails a note. Treat warnings as hints for misspelled or not yet defined properties. A known property is valid on every note whether or not a type file attaches it; attachment only feeds templates, and a `then.required` entry is a constraint, not an attachment. No glob: every note, i.e. every `*.md` directly in the root, in a `<name>-exogram/` folder, or in a `<repository>/exogram/` folder, except inside `.git/`, `.obsidian/`, `.claude/`, `.templates/`, `node_modules/`, `target/`.

## Workflow

1. Run `just validate $ARGUMENTS`.
2. Group the issues by message. Report the groups with counts before touching anything.
3. Fix only what has one derivable answer: a string where the schema wants an array, a date not in `YYYY-MM-DD`, a number where the schema wants a string, a `type` link missing `.md`.
   Never edit type files, `exogram.yaml` or `properties.yaml`; all three are generated. Attachment lives on the type note (`requiredProperty`, `optionalProperty`), a property's value shape on its property note (`range`, `characteristic: functional`). Change the note, run `just templates`, then `just validate`.
4. Never guess. Missing required values, invalid enum values, and unknown properties are reported, not fixed. The notes may be right and the schema wrong: ask with `AskUserQuestion` when one decision settles a whole group.
5. On every edited note set `reviewLevel: unread`. Never edit a `reviewLevel: canon` note without asking; a canon edit also gets `documentStatus: draft`.
6. Run `just validate` again on the edited files.
7. Report as a table: issue group, count, fixed or open.
