---
name: create-ascii-dag
description: Draw the net of a Factor as an ASCII DAG into its net note, with a legend beside the drawing and links to every act and place. Use when the user asks to "draw the dag", "draw the net", "diagram this factor", "render the factor", or "update the net diagram".
argument-hint: <factor note id or path>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(just:*)
---

# Create ASCII DAG

Draw the acts and places of one Factor as a single ASCII DAG in the note `Net <factor alias>`, typed `Type Description`.
Run every `just` recipe from the exogram workspace root.
In the factors exogram, reading follows rule 1 of Premise Writing the formalism (`factors/exogram/01M3MDCW62YHXPX8TK4AB47QJY.md`).

## Workflow

1. Resolve the factor: the note given.
2. Render it:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/render-dag.py --block <factor note path>
   ```
   The script reads the factor's parts live from their frontmatter and prints one block between `<!-- render-dag -->` and `<!-- render-dag-end -->`: the drawing with its legend in a `text` fence, then one link per act and place.
   It exits with `has no acts` while the factor has no parts; stop there.
3. Grep for the `Type Description` note (`01M614NPMSPXAE9ERTZASRZBT0`) whose `wasDerivedFrom` links the factor.
   - Found: replace everything between the markers with the new block, with the Edit tool, and set `vetting: unread`.
   - Missing: fill `facts/.templates/Description.md` with alias `Net <factor alias>`, `wasDerivedFrom` the factor and `vetting: unread`, and put the block as the body. Write it as `<ULID>.md`, the id from `just ulid`, into the factor's folder.
4. Run `just validate '<note path>'` until clean.
5. Report the note path.

## Notation

`(a)` a place, `━A━` an act, `{a}` a link to `(a)` drawn above an act that reads `(a)` from more than one row above.
`+` above an arrow marks a map arc, `-` a collect arc.
Time runs top to bottom; an act takes its inputs left to right in the order they arise.
