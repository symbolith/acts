---
name: check-tla
description: Align the Factors TLA+ spec (formal/tla/) to the formalism note 20260518150627.md and report drift. Use when the user wants to "align the TLA spec", "check the TLA+ matches the formalism", "align tlc to the formalism", "verify the model mirrors the math", or before trusting TLC model-checking results.
argument-hint: [report|--fix-spec] (default: report drift only, never edits)
allowed-tools: Read, Bash, Grep, Glob, Agent
---

# Align TLA+ spec to Factors formalism

Establish that the TLA+ spec under `file:./formal/tla/:1:1` faithfully encodes
the formalism note `file:./20260518150627.md:1:1`. A TLC verdict is evidence
about the note's theorems only when this alignment holds, so run this before
the TLC tier of the `check-formalism` skill.

Both sides are read live. This skill describes how to build the mapping, not a
copy of it, so it never goes stale when the note or the spec changes.

## Never change the formalism; ask before changing the spec

This skill never edits the formalism note. The note is the ground of truth, and
changes to it are the user's call. By default this skill only reports drift.
With `--fix-spec` it may edit the TLA+ files under `formal/tla/` to close
confirmed drift, but only after stating the exact edits and getting the user's
go-ahead. If a drift is actually a bug in the math rather than the spec, report
it as a finding against the note and stop; do not edit the note.

## Reading discipline

The formalism note is the ground of truth; the spec follows it, never the
reverse. Read only the formalism note among the `.md` notes; the TLA+ files
and justfile are non-note files and free to read.

## Method

Alignment is a two-way traceability check between the note's structure and the
spec's structure. Build the correspondence from what is actually there, do not
assume a fixed list.

### 1. Inventory both sides

From the note: its sets and domains, its state predicates, the axioms in its
Axioms section, the rules in its Step Relation, and its step
invariants/theorems.

From the spec: the `VARIABLES`, the defined operators, the disjuncts of the
`Next` action, the conjuncts of the well-formedness operator, the initial
state, and the `INVARIANTS`/`PROPERTIES` listed in each `MC_*.cfg`.

```
grep -nE '^[A-Za-z][A-Za-z0-9]*(\(|\b.*==)' formal/tla/Factor.tla
grep -nE 'INVARIANTS|PROPERTIES|SPECIFICATION' formal/tla/MC_*.cfg
```

### 2. Build the traceability matrix

Spawn a `general-purpose` subagent with the note and the TLA+ files. Have it
produce one row per note construct: `note construct | TLA+ counterpart |
harness (if any) | status`, plus the reverse for any spec definition with no
note origin. Match by meaning, not by name. For each non-aligned row give the
precise `file:` reference on both sides and a one-line description of the
divergence.

### 3. Check the encodings closely

- The well-formedness operator must encode exactly the axioms in the note's
  Axioms section, one conjunct per axiom, no more and no less.
- Each `Next` disjunct must encode the matching note step rule, premise for
  premise. Flag any premise present in one and absent in the other.
- Each model-checkable theorem in the note should have a harness asserting it,
  and each harness property should name a note theorem.
- Note where the spec deliberately bounds an unbounded note construct for
  finite-state checking, or abstracts an opaque payload. A faithful bound is
  not drift; record it.

### 4. Report

One drift report: the matrix, then ERRORS (a note construct with no faithful
encoding, or spec behaviour the note does not license) and WARNINGS (cosmetic
renames, harness gaps, recorded bounds). End with a verdict: `aligned` or
`N drifts`. If aligned, state that TLC results may be trusted for the mapped
theorems. If drifted, list which theorems' TLC verdicts are not yet
trustworthy.

If invoked with `--fix-spec`, propose the minimal TLA+ edits to realign, state
them, get the user's go-ahead, apply them under `formal/tla/` only, then
re-inventory. Never touch `20260518150627.md`.
