# Factors formalism check catalog

What each tier covers, by method. The specific sets, axioms, rules, and
theorems are read live from the note `20260518150627.md`; none are copied
here, and no standalone script is shipped, so this catalog does not drift.

## Tier 1 — Mechanical self-consistency (inline commands in SKILL.md)

Deterministic, high-precision, no judgement. The commands read the live note,
so they track structure changes. Coverage:

| check | rule | severity |
| --- | --- | --- |
| citation balance | every `[^id]` Cite resolves to a `[^id]:` Source, every Source is cited | error / warn (dead) |
| note-link resolution | every `](NNNN.md)` target file exists in the exogram | error |
| em dash | `—` forbidden anywhere by STYLE | error |
| en dash | `–` allowed only inside a numeric range (page spans); elsewhere flagged | error |
| slop words | the STYLE slop list, body only | error |
| bold labels | `**X:**` forbidden by STYLE, body only | error |
| "not just X" | the forbidden construction, body only | error |
| gloss length | a definition gloss over the STYLE length cap | warn |
| frontmatter | required keys present | error |

Prose-pattern scans start at the first `## ` heading, after the frontmatter.
Source footnote lines are exempt because they are citation-exact.

## Tier 2 — STYLE-grammar conformance (subagent)

The style guide note AGENTS.md names defines the grammar of every element. A
subagent reads that note and checks each body block of the formalism against it, plus the "All"
constraints and NO USE BEFORE DEFINE. Do not restate the grammar here; read it
from the note so the check always matches the current rules.

## Tier 3 — Cross-reference and define-before-use (subagent)

Resolve every internal pointer: each parenthetical name that refers to an
axiom, rule, lemma, or theorem must resolve to its definition site, and each
operator the note defines must be applied within its declared signature. Needs
judgement, because parenthetical prose is not always a cross-reference. Tagged
results hold; do not report them as unproven.

## Tier 4 — Soundness and cross-artifact consistency (subagent + TLC)

Soundness: reason over the note's own axioms, rules, and theorems. Are the
axioms jointly satisfiable, is each rule well-typed and consistent with the
invariants it claims to preserve, is each obligation plausibly dischargeable.

Cross-artifact:
- The other canon notes must agree with the formalism: the state and step
  summaries restate its predicates and rules, and the vocabulary, the `fctrs:`
  type and property notes in `../../facts/exogram/`, is checked term by term (each class
  against a set, each property against a signature; `subClassOf`,
  `disjointWith` and `characteristic` against ⊎, the axioms and the function
  arrows). A term with no set or function behind it, or of another sort, is an
  error; `exogram:` ids and the exogram's own supers are conventions, skipped.
- TLA+ spec under `formal/tla/`, model-checked with TLC. A TLC verdict speaks
  to the note's theorems only if the spec faithfully encodes the formalism;
  establish that with the `check-tla` skill first. Map each harness to the
  theorem it asserts by reading its `.cfg` and the note. A failing run is a
  counterexample and is critical.

## Reading discipline

Read only the canon notes (`reviewLevel: canon`, roles in AGENTS.md) plus
non-note files. Open no other note without permission. Citation inconsistencies are always critical.
