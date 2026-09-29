# Documentation File Catalog

## README.md

**Tier:** Essential (always)

**Source:** The Good Docs Project (thegooddocsproject.dev/template/readme)

**Outline:**

```
[Logo + badges] (optional)
Project Name - URL, owner
[Table of Contents] (optional, add if > 100 lines)
Project description
  "With {Project} you can {verb} {noun}..."
  "{Project} helps you {verb} {noun}..."
  "Unlike {alternative}, {Project} {verb} {noun}..."
  Screenshots/demos if applicable
Who this project is for
  "This project is intended for {target user} who wants to {objective}."
Project dependencies
  Prerequisites list with links to install instructions
Instructions for using {Project}
  Install {Project} - numbered steps with code samples
  Configure {Project} - numbered steps
  Run {Project} - numbered steps
  Troubleshoot {Project} - issue/solution table; links to FAQs, runbooks
Contributing guidelines - link to CONTRIBUTING.md or embed briefly
Additional documentation - links to docs, examples, planned features, sub-READMEs
How to get help - mailing list, chat, bug tracker, Stack Overflow tag
Terms of use - license name + link to LICENSE file
```

**Brief notes per section:**

- Project description: focus on WHY a user should care, not what tech was used. Use the "With X you can Y" formula. Include screenshots/demos in the repo (not external URLs).
- Who this project is for: state problems the project solves and tasks it helps accomplish. Mention when NOT to use it.
- Project dependencies: list what must be installed before the project works. Link to each dependency's install page.
- Instructions: start each step with a verb. Include code samples and expected output. The troubleshoot section uses an issue/solution table to reduce support burden.
- Additional documentation: link to separate docs, wikis, API references. Good place to mention planned features.
- How to get help: differentiate support channels from bug reporting. State what is NOT a support channel.

## LICENSE

**Tier:** Essential (always)

No outline. Flag absence and present choices:

| License | Trade-off |
|---|---|
| MIT | Maximum adoption, no patent protection, simple |
| Apache-2.0 | Permissive + patent grant, preferred by companies |
| GPL-3.0 | Copyleft, derivatives must stay open, limits corporate use |
| BSD-2-Clause | Like MIT, different legal tradition, shorter text |
| MPL-2.0 | File-level copyleft, can mix with proprietary code |

Source: choosealicense.com (GitHub-maintained).

## CONTRIBUTING.md

**Tier:** Recommended (contributors > 1 or accepts external contributions)

**Source:** contributing.md (contributing.md/how-to-build-contributing-md/)

**Outline:**

```
Welcome note - eager for contributions, glad you're here
Table of Contents - link each heading
Links to key resources
  Docs/handbook
  Bug tracker / issue tracker
  Communication channels (IRC, Slack, Discord, mailing list)
  Templates (bug report, enhancement suggestion) - make downloadable
  Test location in the repo
  How to submit changes - link to PR workflow
  Development environment setup - or link to README section
How to report a bug
  Step-by-step instructions
  Link to bug tracker
  Link to list of known/reported bugs
  Link to bug report template
  FAQs
How to fix a bug
  Types of bugs contributors can tackle
  Style guides with examples per language
  Issue and PR label descriptions
How to suggest enhancements
  Link to enhancement guidelines
  Link to related/existing suggestions
  Link to enhancement suggestion template
  Encourage testing via project config settings
Coding conventions and style guide
  Git commit message format (tense, character limits, emoji policy)
  Code style per language (link to linter configs)
  PR and issue reference conventions
Code of Conduct - inline or link to separate file
Recognition - thank you, contributor listing, badges
Project owner and contributors - core team, contact info, humans.txt
Where can I get help? - links to communication channels
```

**Brief notes per section:**

- Welcome note: set tone. Contributors should feel wanted.
- Links: centralize all important project links in one place so contributors don't hunt.
- Templates: provide structured formats for bug reports and enhancement requests. Reduces low-quality submissions.
- How to report vs. how to fix: separate paths for reporters and fixers. Reporters need templates; fixers need label guidance and style info.
- Coding conventions: be explicit about commit message format (tense, line length, emoji). Link to linter/formatter configs rather than describing rules.
- Recognition: pre-emptive thank you. List how contributors get credited (CONTRIBUTORS file, release notes, badges).
- Reference files: CONTRIBUTING.md should reference LICENSE, README, and humans.txt. Create all referenced files.

## ARCHITECTURE.md

**Tier:** Recommended (multiple modules or non-obvious structure, generally > 2000 LOC)

**Source:** matklad (matklad.github.io/2021/02/06/ARCHITECTURE.md.html), exemplified by rust-analyzer

**Outline:**

```
Bird's eye overview
  High-level description of the problem being solved
  What the system does in broad terms
Codemap
  Coarse-grained modules and their relationships
  Per module: name, purpose, key types/files
  Answers "where's the thing that does X?"
  Answers "what does this thing I'm looking at do?"
  Do NOT detail HOW each module works, just WHAT and WHERE
  Name files and types by name, do NOT link them (links go stale)
  Use symbol search to find named entities
Architecture invariants
  Important constraints, especially expressed as absences
  "Nothing in the model layer depends on views"
  "The parser never fails, it returns (T, Vec<Error>)"
  Things that are hard to discover by reading code
Boundaries between layers and systems
  Where the interfaces are
  What a boundary implies about implementations behind it
Cross-cutting concerns
  Logging, error handling, testing strategy
  Cancellation, serialization, configuration
  Anything that spans multiple modules
```

**Brief notes per section:**

- Bird's eye: one paragraph. What problem does this solve? Not how.
- Codemap: the core of the document. "A codemap is a map of a country, not an atlas of maps of its states." Use this as a chance to reflect on whether the directory layout matches the conceptual layout.
- Invariants: the highest-value section. Important invariants are often expressed as an ABSENCE of something, which is impossible to learn by reading code. Explicitly stating "X never depends on Y" saves contributors from introducing violations.
- Boundaries: finding a boundary by randomly reading code is hard because good boundaries have measure zero. Point them out explicitly.
- Cross-cutting: add after the codemap. Covers concerns that span module boundaries.
- Maintenance: only specify things unlikely to frequently change. Revise twice yearly. Delete stale bits. This document is engineered to be low-churn.
