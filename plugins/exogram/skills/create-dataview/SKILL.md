---
name: create-dataview
description: Create a new dataview-serializer TABLE, LIST, or TASK block. Use when the user asks to "create a dataview query", "add a dataview block", "serialize a dataview query", or wants to add a dataview-serializer block to an exogram note.
---

# Dataview Serializer

Build the query from the request, ask only what it leaves open, then output the complete block.

## Step 1: Check the Fields

Grep every field the query uses in `facts/properties.yaml` for its schema type; never read the file whole. Type ids come from the type note's filename.

## Step 2: Settle the Query

Defaults when the request does not say otherwise: `LIST WITHOUT ID link(file.link, file.aliases[0])`, filter `contains(field, this.file.name)`, `SORT file.aliases[0] ASC`, mode auto. State the defaults you took with the block.

Ask one question only for a real fork: TABLE vs LIST when columns are unclear, GROUP BY (`rows.file.link`), a specific note id, or a non-auto mode.

TASK queries filter on task metadata; checkboxes are stripped in serialized output to prevent infinite update loops.

Modes: **auto** updates on save, **manual** via command palette, **once** runs once and keeps markers, **once-and-eject** runs once and removes them.

## Step 3: Generate and Output

Output the query block only. Use multi-line format for readability. The query goes directly in the HTML comment (no dataview code fence). Do not add result markers — the plugin creates them automatically.

The marker name changes per mode:

| Mode | Marker |
|------|--------|
| auto (default) | `dataview-serializer-query:` |
| manual | `dataview-serializer-query-manual:` |
| once | `dataview-serializer-query-once:` |
| once-and-eject | `dataview-serializer-query-once-and-eject:` |

Template (substitute the appropriate marker). The query content must start on a new line after the opening comment tag and end with a newline before the closing ` -->`. Do not add blank lines between the comment tags and the content, use a single newline separator. A space before ` -->` is required due to a plugin bug. Only output the query block; the plugin generates result markers automatically.

```
<!-- MARKER
[QUERY]
 -->
```

## Dataview Query Structure

```
<QUERY-TYPE> <fields>
FROM <source>
WHERE <condition>
SORT <field> [ASC|DESC]
GROUP BY <field>
LIMIT <number>
```

Only Query Type is mandatory. Commands execute in order.

## Query Types

- **TABLE**: Table with columns - `TABLE field1, field2 FROM ...`
- **TABLE WITHOUT ID**: Table without file link column
- **LIST**: Bullet list of pages - `LIST FROM ...`
- **LIST WITHOUT ID**: List without file prefix
- **TASK**: Task list (checkboxes stripped in serialized output)

Not supported: CALENDAR

## Key Functions

### Link Creation
- `link(path, [display])` - Create link with optional display text
- `link(file.link, file.aliases[0])` - Link using first alias as display

### Containment Checks
- `contains(object|list|string, value)` - Case-sensitive check
- `icontains(...)` - Case-insensitive version
- `econtains(...)` - Exact match version

### Other Useful Functions
- `choice(condition, trueVal, falseVal)` - Conditional value
- `default(value, defaultValue)` - Provide default if null
- `dateformat(date, format)` - Format date
- `length(value)` - Length of array/string
- `filter(array, expr)` - Filter elements
- `map(array, expr)` - Transform elements
- `sort(array, [expr])` - Sort elements
- `date(today)` - Current date
- `dur(1 day)` - Duration literal

### Implicit File Fields
- `file.name` - Filename (the note id, a ULID)
- `file.link` - Clickable link to file
- `file.aliases` - Array of aliases from frontmatter
- `file.path` - Full path
- `file.tags` - All tags
- `file.ctime` / `file.mtime` - Created/modified time
- `file.cday` / `file.mday` - Created/modified date
- `file.size` - File size in bytes
- `file.outlinks` / `file.inlinks` - Outgoing/incoming links
- `file.tasks` - Array of tasks in file
- `this.file.name` - Current file's name (note id)

## Data Commands

- **FROM**: Filter source (tags, folders, links) - `FROM #tag`, `FROM "folder"`, `FROM [[note]]`
- **WHERE**: Filter by field values - `WHERE state = "claimed"`
- **SORT**: Order results - `SORT file.aliases[0] ASC`
- **GROUP BY**: Group results - `GROUP BY owner` (use `rows.file.link` to access)
- **LIMIT**: Restrict count - `LIMIT 10`
- **FLATTEN**: Expand arrays - `FLATTEN creator`

Combine sources: `FROM #tag and "folder"`, `FROM #food and !#fastfood`

## Inline Queries

For single values embedded in text:

```
<!-- dataview-serializer-iq: =expression --> result <!-- /dataview-serializer-iq -->
```

Supports: `=this.field`, `=date(today)`, `=choice(condition, a, b)`, `=embed(this.portrait)`

## DataviewJS Queries

For JavaScript-based queries:

```
<!-- dataview-serializer-js:
dv.table(["Name", "Rating"], dv.pages("#books").sort(b => b.file.aliases[0]).map(b => [b.file.link, b.rating]))
 -->
<!-- dataview-serializer-js-result -->
| Name | Rating |
| --- | --- |

<!-- dataview-serializer-js-result-end -->
```

## Table Rules

- Templates need no exclusion: they live in `facts/.templates`, a dot folder Obsidian never indexes, so Dataview cannot match them.
- Wrap every optional column in `default(field, "")`. Otherwise missing values print `null`.
- No unbounded text columns. Prose fields such as `comment` pad every row to the widest cell and wrap in editors. Use link, enum, rating, and date fields only. If prose is unavoidable, `truncate(default(comment, ""), 80)`.
- Keep rows under 120 characters: at most three columns, the first being the alias link.
- BEFORE writing a column, look up the field in `~/repositories/symbolith-exogram/facts/properties.yaml`. A field with `type: array` NEVER goes into a TABLE bare: it renders as `<ul><li>` HTML. Either `join(field, ", ")`, or, when a cell may hold more than three links, use a LIST instead: `LIST WITHOUT ID link(file.link, file.aliases[0]) + ": " + join(field, ", ")`.
- A field whose schema type is scalar but that renders as a list is a data error: fix the offending notes (`grep -n '^field:$'`), never the query. If the schema allows both, flatten: `default(choice(typeof(field) = "array", join(field, ", "), field), "")`.
- Sort by `file.aliases[0]` unless a rating or date is the point of the table.

## Check Before Reporting

Walk this list for every new or edited block. Any miss means the block is wrong, fix it before reporting:

1. Templates excluded.
2. Every array field joined or the block is a LIST.
3. Every optional column wrapped in `default`.
4. No prose column.
5. After the user regenerates, read the result block: no `<ul>`, no `[object Object]`, no `null`, no row over 120 characters.
6. Every block sorted: DQL with `SORT`, JS with `.sort(...)`, by `file.aliases[0]` unless a rating or date is the point.

## Editing an Existing Block

- Replace only the text between `<!-- dataview-serializer-query:` and its closing ` -->`. Leave the result block and the single `result-end` marker alone; the plugin rewrites them.
- Never leave two `result-end` markers. The plugin appends rather than replaces when markers are duplicated.
- After an edit, the serialized result is stale until the note is saved in Obsidian. Check the `dataview-serializer-result:` marker: it echoes the query that produced the table. If it differs from the query block, the table has not been regenerated yet.
- Notes edited outside Obsidian may stay stale in Dataview's index. If a value on disk and a value in the table disagree, ask the user to reload Obsidian before debugging the query.

## Important Notes

- Note ids (`file.name`, `this.file.name`) are stable for matching
- Display text/aliases can change, don't rely on them for filtering
- `contains(field, this.file.name)` checks if current file's id is in a link field
- When using GROUP BY, access grouped items via `rows.field`
- TASK queries strip checkboxes to prevent infinite update loops
- Do not create result markers — the plugin generates them automatically

## Troubleshooting

If something isn't working, check the official documentation:

- [Dataview Serializer docs](https://developassion.gitbook.io/obsidian-dataview-serializer) for plugin-specific behavior
- [Dataview query reference](https://blacksmithgu.github.io/obsidian-dataview/) for query syntax
- [Dataview Serializer GitHub](https://github.com/dsebastien/obsidian-dataview-serializer) for issues and changelog

## Sources

- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [Dataview Serializer Documentation](https://developassion.gitbook.io/obsidian-dataview-serializer)
- [Dataview Serializer GitHub](https://github.com/dsebastien/obsidian-dataview-serializer)
