---
name: name-thing
description: Name a thing by a fixed process and explicit criteria, not by guessing. Works for identifiers in code (variable, function, type, constant), constructs in a formal text (set, element, predicate, operator, rule), and terms in a document, ontology, or vocabulary. Use when the user asks to "name this", "what should I call", "find a better name for", "rename X", "is this a good name", or rejects a proposed name.
argument-hint: <thing to name or rename> [--apply]
allowed-tools: Read, Edit, Grep, Glob, WebSearch, WebFetch, AskUserQuestion
---

# Name a thing

Derive the name in `$ARGUMENTS` by the process below, against the checklist in [references/naming.md](references/naming.md).
Read that file first. Every step and every criterion there cites its source.
Operate on this conversation; do not fork it.

## 1. Fix the thing

State on one line each, and stop to ask if one is unknown:

- Kind: predicate, function, set, element, collection, type, value, action, relation, rule.
- Field: the discipline whose vocabulary applies (Petri nets, RDF, a language, a business domain).
- Convention: the target's own rules for that kind. Read them live: a STYLE note, the repo `CLAUDE.md`, the language style guide. Never restate them.
- Concept: the nearest generic concept and what parts this thing from its siblings.
- Load: what the name must carry. What the thing holds, what it is for, a qualifier where two things of one kind could be confused.

A thing whose concept will not fit one line has a design problem, not a naming problem. Say so and stop.

## 2. Source the words, in this order

1. The target's own lexicon. Grep the document or codebase for the concept and for every word already bound to it. A word already in use for this concept wins.
2. The field's established term. Search online, never from memory, by the recipe in section 3 of the reference. Record variants across works and mark the standard's term.
3. A coined word. Only if 1 and 2 yield nothing. One dictionary word per concept, no synonym of a word already bound, a finer distinction by an added word.

## 3. Build candidates

At most five. For each: the words, the source (own lexicon, field, coined), and the form for its kind from the reference's Form criteria (singular noun for a set, verb phrase for an action, a claim for a predicate, and so on). Apply the target's casing and separator convention.

## 4. Test

Run every candidate through the checklist in section 2 of the reference: Form, Meaning, Fit, Economy, Correctness.
Grep the target for collisions: the same name bound to another concept, another name bound to this concept, a neighbour that differs by one letter, by word order, or by sound.
Read a neighbour's definition before flagging it; a difference the lexicon defines is a term, not a collision.
Record each no with the criterion's name.

## 5. Report

One table: candidate, source, failed criteria, verdict.
Recommend the candidate with no failures; among several, the one from the earliest source, then the shortest.
If none passes, say which criteria no candidate meets and what change to the thing would let a name pass. Do not pick the least bad.

Get approval. `--apply` skips it only when exactly one candidate passes.

## 6. Apply

A rename is a full sweep, never partial. Every occurrence, every sibling document that must stay consistent, every gloss and remark that spells the word.
Use `Edit` only. Never `Write`, `sed`, or `echo`. Never touch auto-generated blocks.
Where the target's rules require it, set its draft status and stop.
Report each site as `file:<path>:LINE:COL`.
