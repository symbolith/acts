# Writing Genre Notes

Concrete rules for the genres most likely to come up. Starting points, not rules of nature. Cross-check with the project's own conventions when one exists.

## Commit messages

Handled by the dev:commit-message skill. Do not draft commit messages from these notes.

## PR descriptions

1. One-sentence summary above the fold.
2. Why this change: problem, context, alternatives considered.
3. What changed at a high level. Do not re-read the diff for the reviewer.
4. Test plan as a markdown checklist.
5. Screenshots or short videos for UI changes.
6. Migration notes for breaking changes.

## READMEs

1. One-line tagline that answers "what is this?".
2. A 30-second pitch in 1 to 3 sentences above the install section.
3. Install. Quick start. Example output.
4. Link to fuller docs rather than dumping them in the README.
5. License and contribution pointer near the bottom.

Sources: makeareadme.com, Standard Readme (https://github.com/RichardLitt/standard-readme).

## Technical docs and tutorials

1. Task-oriented headings ("Send your first email") beat concept dumps.
2. Example before explanation when possible. Show the output.
3. Signpost every section with a one-sentence "what you will get".
4. Real code that actually runs end to end.
5. Common errors and recovery steps near the bottom of each task.

Sources: Diátaxis framework (https://diataxis.fr/), Google developer documentation style guide (https://developers.google.com/style), Microsoft Writing Style Guide.

## Cold emails and replies

1. Subject promises a specific thing.
2. First sentence states why the reader should care.
3. One ask per email. Make it concrete and small.
4. Personal hook tied to the recipient. One line. No flattery.
5. End with a clear next step.
6. Under 6 sentences for cold outreach.

Reply emails: lead with the answer, follow with context. Quote less than you think you need to.

## Bug reports

1. Title is a one-line summary, not "bug" or "broken".
2. Steps to reproduce, numbered, minimal.
3. Expected behavior.
4. Actual behavior.
5. Environment: OS, version, browser, anything else relevant.
6. Logs, screenshots, minimal repro link.

## Blog posts and essays

1. Open with a concrete scene, story, or surprise. Never a definition.
2. State the thesis within the first few paragraphs.
3. Each section earns its place by advancing or testing the thesis.
4. End by landing the takeaway, not summarizing what came before.
5. Read aloud before publishing.

Sources: Paul Graham essays (https://paulgraham.com/articles.html), Slate Star Codex archives.

## Academic prose

1. One paragraph, one message. Topic sentence first.
2. Cite claims close to where they appear.
3. Define every new term before using it again.
4. Reviewer-readable: structure must survive a 5-minute skim.
5. Claim-evidence map: every claim in the abstract must trace to evidence in the experiments.


## API reference

1. Function signature with types.
2. One-line summary.
3. Parameters, return value, side effects.
4. Errors thrown and the conditions that trigger them.
5. A minimal runnable example.
6. Cross-link related calls.

## Release notes

1. Group changes by impact: breaking, new, fixed, deprecated, removed.
2. Lead with what the user can now do, not the internal change that enabled it.
3. Copy-pasteable migration steps for breaking changes.
4. Link the relevant PRs or issues per item.
5. Date and version number at the top.

## Wiki notes (personal Zettelkasten)

1. Title is a claim or a noun phrase, not a question.
2. First line restates the title as a one-sentence claim.
3. Link aggressively to related notes. Notes earn their value from links.
4. Keep one idea per note. Split when a note grows two voices.
5. Cite the source at the bottom for facts and quotes.
