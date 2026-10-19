---
name: create-table
description: Create or realign a markdown table that reads cleanly in source, with padded columns, aligned pipes, rows at most 98 characters wide, and a vim modeline that sets conceallevel to 1. Use when the user asks to "make a table", "create a markdown table", "tabulate this", "align the table", "format the table", "fix the table", or adds rows to an existing table.
argument-hint: [what to tabulate or which table to realign]
allowed-tools: Read, Edit, Bash, Grep
---

# Create Table

A table must be readable in the raw file, not only when rendered. Every pipe sits in the same column and no row exceeds 98 characters.

## Step 1: Shape the Table

- First column is the key the reader scans for. Sort by it unless the request names another order.
- Prefer few narrow columns. Width 98 is a hard cap that includes the pipes and padding.
- No prose cells. Rewrite a sentence as a term, a number, or a link. Move anything longer into a list under the table.
- Escape a pipe inside a cell as `\|`. Links, code spans, and bold are fine.
- Right-align number columns with a `--:` separator. Everything else is left-aligned, which is the default.
- A cell left empty stays empty. Never fill it with a dash or "n/a" unless the request says so.

## Step 2: Align It

Never pad cells by hand. Write the draft rows and pipe them through the script:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/align_table.py <<'TABLE'
| Name | Count |
| --- | --: |
| alpha | 1 |
TABLE
```

The script pads every cell to its column width, rebuilds the separator row, and exits non-zero when a row exceeds 98 characters. On that failure shorten cells or drop a column, then rerun. Paste only the script's stdout into the file.

Realign the whole table after any edit, including a one-cell change.

## Step 3: Add the Vim Hint

Neovim conceals the pipes at `conceallevel` 2, which breaks the alignment on screen. Every file that holds a table ends with this line:

```
<!-- vim: set conceallevel=1: -->
```

- Check with `grep -n 'vim: set conceallevel' <file>` before adding it. Add it once.
- It goes on the last line of the file, after one blank line. Neovim reads modelines from the first or last five lines only, and frontmatter occupies the top.
- The HTML comment keeps Obsidian and other renderers from showing it.

## Check Before Reporting

1. Every row starts and ends with a pipe and the pipes line up in a fixed-width view.
2. No row is wider than 98 characters.
3. Header, separator, and every body row have the same number of cells.
4. No prose cell.
5. The modeline is the last line of the file and appears exactly once.
