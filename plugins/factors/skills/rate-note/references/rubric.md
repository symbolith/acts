# Concept-Merit Quality Rubric

The rating measures the merit of the concept a note captures, not how complete,
sourced, linked, or well-written the note is. A one-line stub can hold a 5; a
polished, fully-sourced, well-linked note can hold a 1. Execution is out of scope.

## Criteria

Six virtues, drawn from Kuhn's theoretical virtues (accuracy, consistency, scope,
simplicity, fruitfulness) and peer-review contribution axes (novelty, significance,
soundness).

| Criterion | Asks | Role |
|---|---|---|
| Soundness | Is the concept correct and internally consistent? | Principal (gate) |
| Significance | Does it carry weight, does it matter to the argument? | Principal |
| Novelty | Is it original against prior work? | Principal |
| Scope | How broadly does it reach or unify? | Amplifier |
| Parsimony | Does it explain more with fewer assumptions? | Amplifier |
| Fruitfulness | Does it generate further concepts or results? | Amplifier |

## Roll-up rule

The stored `qualityRating` (integer 1-5) is one holistic verdict, not an average:

1. Soundness gates. An unsound or incoherent concept caps at 2, whatever its other virtues. A wrong idea is not a good one.
2. The principal three set the band. Among sound concepts, significance and novelty decide 3 vs 4 vs 5.
3. The amplifiers tune within the band. Scope, parsimony, and fruitfulness lift a borderline concept to the top of its band and break a 4-vs-5 tie. They cannot rescue a weak or unsound one.

## Scale

| Rating | Meaning |
|---|---|
| 1 | Trivial or unsound. Restates the obvious or does not hold up. Adds nothing. |
| 2 | Weak. Sound but minor: narrow, derivative, low significance. Footnote-level. |
| 3 | Solid. Correct and useful, real but bounded significance. Carries its weight. |
| 4 | Strong. Sound, novel, and significant, with reach beyond its immediate use. Load-bearing. |
| 5 | Foundational. Sound, original, far-reaching, and generative. Anchors or reframes the work. |

## Calibration

Rate against the strongest concepts in the exogram, not in the abstract. Treat the
most rigorous, load-bearing notes you can identify as the 5 anchors, and rate
others relative to them so scores stay consistent across a batch.

## Ratability

The rubric applies only to `Claim` notes. A Claim asserts the single contestable
proposition whose merit the rating measures; no other note carries an
independently ratable concept. Every other type is not-applicable. The Toulmin
support elements (`Evidence`, `Warrant`, `Rebuttal`) earn their place only
relative to a Claim; a `Source` records an external work, not the exogram's own
concept; and entity, administrative, or container notes hold no single rated
assertion. For any non-Claim note, report not-applicable rather than forcing a
rating.
