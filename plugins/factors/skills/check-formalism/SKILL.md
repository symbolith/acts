---
name: check-formalism
description: Check the Factors formalism note (20260518150627.md) for self-consistency, STYLE conformance, and soundness. Use when the user wants to "check the formalism", "validate the formal note", "lint the formalism", "verify Factors", "check 20260518150627", or after editing the Formalization of Factors note.
argument-hint: [--mechanical|--style|--refs|--sound|--tlc|--all] (default runs mechanical + style + refs + cross-note)
allowed-tools: Read, Bash, Grep, Glob, Agent, AskUserQuestion
---

# Check Factors formalism

Layered checker for the formalism note `file:./20260518150627.md:1:1`.

The note is the source of truth: it carries its own sets, axioms, step rules,
and theorems; its STYLE grammar is the style guide note AGENTS.md names. Read
them from the notes at runtime.
This skill describes how to check, never a copy of what the note says, and it
ships no standalone linter, so nothing here drifts when the note changes.

## Read-only by default: never change the formalism without asking

This skill reports; it does not edit. It must NOT modify the formalism note,
nor any other canon note, on its own. When a check turns up
something that would need a change in the formalism, report it as a finding
and stop. Make an edit only after the user approves that specific change. After
any approved edit, rerun Tier 1 and the Tier 2 STYLE subagent, which the repo
CLAUDE.md requires after touching the formalism, and re-check cross-note
consistency. State explicitly, before editing, that you are about to change a
ground-of-truth note and wait for confirmation.

## Reading discipline (non-negotiable)

Per the repo CLAUDE.md, read only the canon notes (`reviewLevel: canon`; find
them with `grep -l '^reviewLevel: canon' *.md ../../facts/exogram/*.md` run in
`factors/exogram/`, their roles are in AGENTS.md) and non-note files (schemas,
TLA+ specs, justfile).
The vocabulary among them is the `fctrs:` type and property notes in
`../../facts/exogram/` (`grep -l 'symbolith.org/factors#' ../../facts/exogram/*.md`). Open no other note
without explicit permission. Citation inconsistencies are always critical:
surface them, never resolve silently. `TODO(proof)` means proved elsewhere,
NOT an open result; tagged `[theorem]`/`[lemma]`/`[axiom]` statements hold.

## Scope

Parse `$ARGUMENTS` for a scope flag. Default runs Tier 1 + 2 + 3 + cross-note.
`--all` adds soundness and TLC.

| flag | runs |
| --- | --- |
| `--mechanical` | Tier 1 only |
| `--style` | Tier 2 |
| `--refs` | Tier 3 |
| `--sound` | Tier 4 soundness subagent |
| `--tlc` | Tier 4 TLA+ model checking |
| `--all` | every tier |
| (none) | Tier 1 + 2 + 3 + cross-note consistency |

See `references/checks.md` for what each tier covers.

## Tier 1 — Mechanical pass (always)

Run these in `factors/exogram/` against the live note (set `F=20260518150627.md`). Each reads the
current file, so it tracks structure changes. Report any hit as a finding with
its line. Body scans start at the first `## ` heading, after the frontmatter.

```
F=20260518150627.md
B=$(grep -nE '^## ' "$F" | head -1 | cut -d: -f1)   # first heading = body start

# citations: every [^id] resolves to a [^id]: Source, and back
diff <(grep -oE '\[\^[A-Za-z0-9-]+\]:' "$F" | tr -d '[]^:' | sort -u) \
     <(grep -oE '\[\^[A-Za-z0-9-]+\]' "$F" | grep -v ':' | tr -d '[]^' | sort -u)
# (no output = balanced; '<' lines are dead Sources, '>' lines are dangling Cites)

# note links resolve to existing files
grep -oE '\]\(([0-9A-HJKMNP-TV-Z]{26}|[0-9]{14}|[0-9a-f-]{36})\.md\)' "$F" | tr -d '])( ' | sort -u \
  | while read -r f; do [ -f "$f" ] || echo "MISSING LINK: $f"; done

# em dash anywhere (forbidden), en dash outside a numeric range (page spans ok)
grep -nP '\x{2014}' "$F"
grep -nP '\x{2013}' "$F" | grep -vP '\d\x{2013}\d'

# body-only style scans (skip Source footnote lines [^id]: which are citation-exact)
tail -n +"$B" "$F" | grep -vE '^\[\^' | grep -niE '\b(delve|landscape|navigate|foster|tapestry|pivotal|crucial|robust|seamless|nuanced|multifaceted|underscore|testament|realm|elevate|streamline)\b'
tail -n +"$B" "$F" | grep -nE '\*\*[^*]+:\*\*'                 # bold labels
tail -n +"$B" "$F" | grep -niE 'not just|not only .* but|less about .* and more'
```

For gloss length, flag any definition line whose gloss (the text after `` ` : ``,
minus any trailing `[^cite]`) exceeds the style guide's cap. Validate the
frontmatter with `just validate factors/exogram/20260518150627.md` from the exogram
root. Treat these scans as evidence and apply judgement on
edge cases (a hit inside a code span or a legitimate compound term is not a
violation).

## Tier 2 — STYLE-grammar pass

Spawn an `Explore` subagent. Have it read the style guide note AGENTS.md names
(the grammar lives there, do not restate it) and check every body block of the
formalism against it, including NO USE BEFORE DEFINE on the formula column. Return
`file:` findings or "clean".

## Tier 3 — Cross-reference pass

Spawn an `Explore` subagent to resolve every internal pointer: each
parenthetical `(name)` that names an axiom, rule, lemma, or theorem resolves to
its definition site, and each operator the note defines is applied within the
signature it declares. Treat tagged results as established. Return `file:`
findings or "clean".

## Tier 4 — Cross-note, soundness, and TLC

Cross-note (default): read every canon note and check that the others agree
with the formalism. The state and step summaries must restate its predicates
and rules; the vocabulary is checked term by term: every `fctrs:` type note
against a set of the formalism (`subClassOf` and `disjointWith` against ⊎ and
the axioms), every `fctrs:` property note against a signature (domain, range,
`characteristic` against the function arrows and the uniqueness axioms). A
term with no set or function behind it, or of another sort, is an error;
`exogram:` ids and the exogram's own supers are conventions, skip them. Any
divergence is critical.

Soundness (`--sound`): spawn a `general-purpose` subagent to reason over the
note's own axioms, rules, and theorems (read from the note): are the axioms
jointly satisfiable, is each rule well-typed and consistent with the invariants
it claims to preserve, is each obligation plausibly dischargeable.

TLC (`--tlc`): a TLC verdict speaks to the note's theorems only if the spec
under `formal/tla/` faithfully encodes the formalism. That is the `check-tla`
skill's job; run `/factors:check-tla` first if alignment is unknown. `tlc` and `just`
are on PATH. Run every recipe of `formal/tla/justfile` and, by reading its
`.cfg` and the note, map each harness to the theorem it asserts. A failure is a counterexample and is
critical.

## Report

One consolidated report grouped by tier, each finding a clickable
`file:./20260518150627.md:LINE:COL` reference with the rule it breaks and a
suggested fix. Separate ERRORS from WARNINGS. End with a verdict: `clean` or
`N errors, M warnings`. Propose fixes in the report; do not apply any to the
formalism without explicit approval (see the read-only rule above).
Before reporting, collect the planned Task notes targeting the formalism
(`grep -l 'hasOutput:' *.md | xargs grep -l '20260518150627' | xargs grep -l 'status: planned'`)
and drop every finding an existing task already covers; when a finding adds
detail to such a task, refine that task note instead of reporting it.
