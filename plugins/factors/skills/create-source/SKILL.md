---
name: create-source
description: Turn a citation for an external work into an exogram Source note, deduping against existing ones, and return its link. Use when the user asks to "make a citation", "cite this", "create a source note", "add a source", "turn this into a Source", or when another skill needs a Source note for a cited work.
argument-hint: <DOI, URL, or bibliographic details of the work>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Make Citation

Resolve a citation for an external work to an exogram `Source` note: reuse an existing one or mint a new one, then return the markdown link to use. One `Source` per real-world work; never duplicate.

## HARD RULE: verify every field online before writing

**NEVER write a `Source` note until ALL of its metadata is verified online against an authoritative source** (the DOI resolver, crossref, or the publisher's own page). The user's input and your memory are leads, not facts.

- Confirm `creator`, `issued`, `publicationName`, `doi` against an online record. Match the title to be sure it is the same work.
- A field you cannot verify online is NOT written. Stop, report exactly which field failed verification, and ask the user. Never guess, fabricate, or fill from the unverified input.
- No online verification possible → no note. Flag it and stop.

## Source note shape (frontmatter is RDF)

The field set is owned by the template `~/repositories/symbolith-exogram/facts/.templates/Source.md` and the conditional `~/repositories/symbolith-exogram/facts/types/Source.yaml`, both generated from the type note by `just templates`; read them at run time for the required and optional fields rather than trusting this skill. Fill every field the verified record provides, not just the required ones. `aliases[0]` is a short title handle; all bibliographic metadata lives in frontmatter, so the body is normally empty.

Conventions the template does not spell out:

- `iri` is the first key: the work's DOI as `"[doi:<doi>](https://doi.org/<doi>)"`, or, without a DOI, its URL as `"[<host>](<url>)"`.
- `issued` is a quoted string: `"YYYY"`, `"YYYY-MM"` or `"YYYY-MM-DD"`, as precise as the record allows.
- `reviewLevel: unread`.

## Procedure

1. Parse the input into leads: DOI, title, authors, venue, year.
2. Verify online (mandatory gate). Resolve the work and confirm every required field against an authoritative record. Use the **WebFetch** tool, not shell `curl`; the Crossref REST API returns JSON over a plain GET:
   ```
   WebFetch  url: https://api.crossref.org/works/<doi>
             prompt: extract title, authors, container-title, volume, issue, page, issued, DOI, publisher, ISSN
   ```
   With no DOI, WebSearch the title plus an author, then WebFetch the DOI/publisher record to read off the fields. Confirm the title matches before trusting the record. Any field not confirmed online → ask the user (AskUserQuestion); do not proceed with it unverified.
3. Dedup against the exogram. Use the **Grep** tool, not shell `grep`. Search by verified DOI first, then a distinctive title word; reuse the existing note's link on a meaning match.
   ```
   Grep  pattern: <doi-or-title-term>   glob: *.md   output_mode: files_with_matches
   ```
   A DOI or title term can appear in non-`Source` notes (the ground-of-truth notes, skill files); read only candidate frontmatter (`aliases`, `type`, `doi`) and keep matches whose `type` is `Source`.
4. If a match exists, return its `[alias](id.md)` link and stop.
5. Otherwise mint an id with `just ulid` from the exogram root and write the `Source` note using only verified fields.
6. Report: the link to use, whether it was reused or created, and the source URL each field was verified against.
