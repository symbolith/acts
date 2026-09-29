---
name: normalize-argument
description: Reduce a verbose note into normalized Toulmin/AMO argument notes, one Claim note linking deduped Evidence/Warrant/Rebuttal element notes and carrying its qualifier as a field. Use when the user asks to "reduce a note", "decompose an argument", "split into Toulmin", "normalize an argument", or "turn this note into a Claim".
argument-hint: <note id or path>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Reduce Argument

Reduce one verbose note into one Claim note linking separate Evidence, Warrant, and Rebuttal element notes, carrying its qualifier in the Claim's `hasQualifier` field.
Shared elements dedup to one note reused across claims.
One sentence per line; cut anything not load-bearing.

## Reading

Running this skill is permission to read non-ground-of-truth notes the reduction needs: the target note, dedup candidates (frontmatter), and the link context of notes that reference or are referenced by the target (inbound links, the paper outline, slot wiring).
The repo's "do not read other notes" rule does not block these; still read the canon notes named in AGENTS.md first, and read nothing beyond what the reduction requires.

## Roles (each must earn its note)

- Claim: the assertion. See Claim test.
- Evidence: the fact or data, not the inference. Relevant, verifiable, traced to a primary source.
- Warrant: the inference rule linking evidence to claim. Name its type (generalization, analogy, sign, causality, authority, principle); make it one a reader struggles to deny.
- Qualifier: the force and scope ("guaranteed for X", "only at layer Y"). Goes in the Claim's `hasQualifier` list as a plain value, distilled to fit the quality bar; a Qualifier is a field, never its own note. If a supposed qualifier cannot fit one short field value (it rests on a citation, or is a counter that stands on its own), it is not a qualifier; classify it as its real role. Skip when plain from the claim.
- Rebuttal: the condition under which the claim fails, the strongest counter not a strawman. Always its own note, never a field; skip when merely hypothetical.

Default: the Claim plus only the elements that carry weight, never a five-role spread to trim.
The `hasEvidence`, `hasWarrant`, and `hasRebuttal` slots are lists linking an element note or another Claim used as grounds; `hasQualifier` is a list of plain values, not links.

## Claim test

A Claim must be contestable, specific, falsifiable, and strong: a non-obvious assertion that costs something if false.

- Relocation/restatement ('X in A not B', 'this is like that'): trivial. Ask 'so what?' and lift to the consequence that makes it matter.
- Mechanism as spine (predicate is how it works: merges, wires, reuses, queries): that is Evidence. Raise to the consequence ("reuses the merge step" → "needs no separate calculus").
- True by construction (one step from a definition or invariant): demote to Evidence.
- Defensive (what the system lacks, a hedged residue): demote to Qualifier or Rebuttal.

Defend-or-fold before presenting: write the claim's consequence and the one sentence that would refute it.
Cannot name a disagreeing reader and a falsifier? Fold to a sharper claim or drop the note.

## Quality bar

Every sentence: clear, accurate (no overclaim), precise (no "robust"/"various"), relevant, deep, brief (one sharp adjective, not stacked modifiers).
Editorializing (novelty self-assessment, hedging, "useful for framing") is not a Toulmin element; delete it.
Gate every element comment: one sentence, names a kind not a source token, strictly load-bearing; distill or cut whatever fails.
An element carries a conclusion, never enumeration or source tokens like class or property names; those belong in the body or chat.

## Grounding

- Base every claim and its evidence on the project's ground-of-truth notes (named in AGENTS.md/CLAUDE.md), not the source's loose framing. An external citation is never the evidence.
- Provenance always includes the formalism note: whatever a note is grounded in or derived from, `[Factors Formalism](20260518150627.md)` must be among its `wasDerivedFrom` sources (see Note shapes).
- Term diff: check the source's load-bearing terms against the ground-of-truth vocabulary. Re-ground a stale term to the canonical one, or drop it if the concept is absent. Never carry a term the ground-of-truth does not use.
- Respect its hedges: a TODO, a simplification, or an out-of-scope remark bounds the claim. Reflect it in the `hasQualifier` list; do not assert past it.

## Note shapes

Frontmatter comes from the type's template in `~/repositories/symbolith-exogram/facts/.templates/`, read at run time; this skill states none.
Element: short alias, one self-contained sentence in `comment` (no reference to its claim, so it stays reusable), empty body.
`wasDerivedFrom` must always contain the formalism note `[Factors Formalism](20260518150627.md)`, on every Claim, Evidence, Warrant, and Rebuttal, no exceptions; when a source note is rewritten in place, add the formalism note to its existing provenance, keeping both.
It may hold more than the formalism note: list every note the content was actually built from, such as the note reduced or a cited `Source`, and never drop one to leave a single source standing.
A note consulted only to check the result, not to build it, is grounding, not derivation: keep it out of `wasDerivedFrom`.
Mirror a cited `Source` in `references` as well.
The Claim body adds only reasoning the comment and slots do not capture, never repeats them.

Citations: put `references` on the element that rests on the work, never blanket on the Claim.
Mint a `Source` via `/factors:create-source`, never by hand, never as prose. If the work can't be identified, leave it out and flag it.

## Procedure

1. Read the target note.
2. Classify. It may be a single Evidence/Warrant/Rebuttal, not a Claim; if so reduce to that one element. Drop instead of reducing when a load-bearing term is ungrounded or a sharper note already covers it (dedup, step 5).
3. State and sharpen the claim (Claim test). Split multiple points into multiple Claims. Raise the comment to meet whatever Evidence/Warrant you can ground (altitude match); a sharper claim often pulls in its Qualifier and Rebuttal.
4. Assign each surviving sentence to a role and write each `comment`. Keep Claim + Evidence + Warrant by default; set `hasQualifier` and add a Rebuttal note only when each earns it.
5. Place every note among its neighbors before creating it: grep a few key terms across notes of any type, read only candidates' frontmatter (`aliases`/`comment`), and name each candidate's relation to the new note by meaning, not string.
   ```
   grep -rli '<key term>' --include='*.md' --exclude-dir='.claude' --exclude-dir='.templates' .
   ```
   - same: reuse its link, mint nothing.
   - broader or narrower: `broader` on the specific note, `narrower` on the general one.
   - grounds: an element goes into the slot of the claim it supports, existing or new.
   - adjacent: link it in `relation`.
6. Confirm the claim wording with the user first, then the plumbing (AskUserQuestion). Show the source beside the proposed set, each sentence marked kept/cut/re-grounded, the candidates with their relations, plus the claim's consequence and falsifier. Prefer folding over defending a weak claim; recommend dropping if too thin, ungrounded, or duplicative.
7. Mint one id per note with `just ulid` from the exogram root. Write new notes with `wasDerivedFrom`, then rewrite the source in place as the Claim/element with the Edit tool, swapping its `type`, deleting frontmatter keys the schema does not know (paper slots such as `motivation`, `problem`, `contribution`, `field`, `gap`, `claim` become body prose or elements), ensuring `wasDerivedFrom` includes the formalism note per the Note shapes rule (kept alongside the source's own), keeping existing index metadata (`qualityRating`, `publish`), and setting `reviewLevel: unread`. Validate each finished note with `just validate 'factors/<id>.md'` from the exogram root.
8. Report: ids written, reused vs created.
9. Propose the next candidate. Name the single most likely note to reduce next, preferring an un-reduced `Idea` or other verbose note surfaced during dedup (step 5) whose `comment` bundles several claims, especially one an element just written links to or sits adjacent to. Give a one-line reason for the pick, or state that none surfaced; never reduce it without a fresh go-ahead.

## Anti-patterns

- Mechanism as claim spine: the claim frames how, not what is true; the mechanism is evidence.
- Warrant that only stands by its claim: it restates the evidence-claim link instead of a general rule. If it borrows the claim's words or licenses no other claim, it is wiring, not a note.
