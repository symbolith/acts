# Conventional Commits v1.0.0

Source: conventionalcommits.org/en/v1.0.0

## Structure

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Spec rules (condensed, RFC 2119)

1. Commits MUST be prefixed with a type (a noun), then optional scope, optional `!`, then required `: ` (colon and space)
2. `feat` MUST be used for a new feature (SemVer MINOR)
3. `fix` MUST be used for a bug fix (SemVer PATCH)
4. Scope MUST be a noun describing a codebase section, in parentheses: `fix(parser):`
5. Description MUST immediately follow the colon and space
6. A body MUST begin one blank line after the description; it is free-form paragraphs
7. Footers MUST appear one blank line after the body. Each is `Token: value` or `Token #value` (git trailer convention)
8. Footer tokens MUST use `-` instead of whitespace (`Acked-by`); exception: `BREAKING CHANGE`
9. Breaking changes MUST be indicated by `!` before the colon and/or a `BREAKING CHANGE: <description>` footer
10. With `!`, the BREAKING CHANGE footer MAY be omitted and the description covers the break
11. Types other than feat and fix MAY be used
12. Everything is case-insensitive except `BREAKING CHANGE`, which MUST be uppercase; `BREAKING-CHANGE` is a synonym

FAQ guidance, not a numbered rule: a commit conforming to more than one type should be split into multiple commits.

## Types

The spec mandates only `feat` and `fix`. The extended set comes from the Angular convention via @commitlint/config-conventional:

build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test

Angular meanings: build = build system or external dependencies; ci = CI config and scripts; docs = documentation only; perf = performance improvement; refactor = neither fixes a bug nor adds a feature; test = adding or correcting tests; style = formatting with no meaning change. Commitlint adds chore = other changes touching neither src nor test files, and revert.

## Reverts

Spec recommendation: revert type, free-form description, footer `Refs: <SHAs>`. Angular form: `revert: <header of reverted commit>` with a body line `This reverts commit <SHA>.` plus the reason.

## Commitlint style rules (config-conventional)

- Type: lowercase, from the enum above, never empty
- Subject: never empty, lowercase (never sentence/start/pascal/upper case), no trailing `.`
- Header max 100 chars; body and footer lines max 100 (URLs exempt)
- Blank line before body and before footers

## Version bump inference (commitizen)

- Type/scope prefix ending in `!` (the `!` before the colon) or a BREAKING CHANGE footer: MAJOR
- `feat`: MINOR
- `fix`, `refactor`, `perf`: PATCH

## Parser patterns

- Header: `^(\w*)(?:\(([\w$@.\-*/ ]*)\))?: (.*)$` capturing type, scope, subject
- Issue-closing keywords: close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved

## Beams rules for the non-conventional case

When a repo uses plain subjects instead of Conventional Commits:

1. Separate subject from body with a blank line
2. Subject limit 50 chars soft, 72 hard
3. Capitalize the subject
4. No trailing period
5. Imperative mood ("If applied, this commit will ...")
6. Wrap the body at 72
7. Body explains what and why, not how

Under Conventional Commits, rules 4 and 5 still apply to the description (lowercase overrides rule 3) and rules 6 and 7 to the body.
