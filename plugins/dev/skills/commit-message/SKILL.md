---
name: commit-message
description: Draft a git commit message from the actual diff, defaulting to Conventional Commits. Use when the user asks to "write a commit message", "commit message for this", "draft a commit", "what should the commit say", or when work is finished and the user is about to commit. Outputs the message only; the user runs git commit.
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
argument-hint: [optional context, e.g. issue number or intent]
---

# Write Commit Message

Draft a commit message from the real diff. NEVER run `git commit`, `git add`, or any state-changing git command; output the message and let the user commit. This skill, not plan-before-write, handles commit messages.

## Workflow

### 1. Detect the repo convention

Conventional Commits is the default. Override only if the repo clearly uses something else.

- Config wins: `commitlint.config.*`, `.commitlintrc*`, "commitlint" or "config.commitizen" in package.json, `cz.toml`, `[tool.commitizen]` in pyproject.toml, a commit section in CONTRIBUTING.md, project CLAUDE.md/AGENTS.md
- Else sample history: `git log --no-merges --pretty=%s -30`. A clear majority matching `^\w+(\([^()]*\))?!?: ` means Conventional Commits; mirror the observed types, scopes, and casing
- A clear non-conventional house style (majority plain subjects) means mirror that style; do not introduce prefixes unilaterally
- Empty or mixed history means Conventional Commits

### 2. Read the actual change

- `git status --porcelain` and `git diff --staged --stat`
- `git diff --staged` for content. Nothing staged: `git diff HEAD`. Asked about the last commit: `git show HEAD`
- The diff is the source of truth. Never write from filenames or session memory alone

### 3. One commit, one intent

State the change in one or two sentences before writing anything. If you cannot, or the diff mixes intents (fix plus feature, refactor plus behavior change), propose a split into atomic commits and suggest `git add -p`. The spec's FAQ says split, never squash under a vague type.

### 4. Pick type and scope

First matching row wins; behavioral production-code changes outrank auxiliary files touched alongside.

| Type | When |
|---|---|
| revert | reverts a previous commit |
| feat | new user-visible capability or API |
| fix | corrects wrong behavior |
| perf | performance change, behavior preserved |
| refactor | restructuring, no fix, no feature |
| test | only test files |
| docs | only documentation |
| ci | only CI config |
| build | build system or dependency manifests |
| style | formatting only, no semantic change |
| chore | maintenance fitting none of the above |

Scope: the crate, package, or module a changelog reader would recognize, e.g. `fix(rdf-trilith-iri): reject empty scheme`. Omit for cross-cutting changes.

### 5. Write it

Header `type(scope): description`:

- Imperative present tense. Test: "If applied, this commit will \<description\>"
- Lowercase after the colon, no trailing period
- Aim under 50 chars, hard cap 72 (stricter than commitlint's 100; this rule wins)

Body, only when it adds what the diff cannot show:

- Blank line after the header, wrap at 72
- Motivation, context, consequences only; summarizing the changed files at any granularity is paraphrase
- Bullet list for the details, at most one short lead paragraph; never a dense prose block
- Thin why means no body

Footers, blank line before:

- Breaking change: `!` before the colon and/or uppercase `BREAKING CHANGE: <description>`
- Issue refs: `Closes #123`, `Refs: #456`. An issue number or intent passed as an argument goes here and disambiguates type and body
- NEVER add AI attribution trailers (Co-authored-by, Generated-with)

Full spec: [references/conventional-commits.md](references/conventional-commits.md)

### 6. Deliver

- Scan the diff for secrets first; if found, warn and stop
- Deliver options in fenced blocks: subject-only first, then one or two body variants when a body is arguable
- Add one sentence justifying type and scope when the choice is not obvious
- The user commits. For multi-line messages suggest `git commit -F -` or a heredoc

## Anti-patterns

- Running `git commit`, `git add`, or any state-changing git command
- Guessing the type from filenames without reading the diff
- Vague subjects: "fix stuff", "update code", "wip"
- Past tense ("added", "fixed") or a trailing period
- Forcing one type onto a mixed diff instead of proposing a split
- Ignoring a house style visible in git log or commitlint config
