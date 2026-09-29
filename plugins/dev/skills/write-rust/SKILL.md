---
name: write-rust
description: Rust design and coding discipline. MANDATORY: invoke immediately in any session that reads, discusses, or edits Rust code or a Cargo workspace, before the first substantive reply.
---

# Rust

## Modes

- Default is discussion: the user is exploring an idea, asking "could I", weighing options, or replying with corrections. Read `discuss.md`.
- Implementation needs an explicit go-ahead in a reply containing no corrections. Then read `implement.md`.
- A skeleton must be approved before implementing; prior prose discussion never waives the gate.

## Research first

- For any non-trivial design choice (crate selection, API shape, error handling strategy, parsing approach), research current best practices online: docs.rs, official Rust API guidelines, crate READMEs, community consensus. Never rely on memory for third-party APIs.
- Verify exact signatures against `~/.cargo/registry/src/*/<crate>-<version>/` and `Cargo.lock`. Batch checks into one or two commands.
- Prefer crates already in the lock file over new dependencies.

## Design decisions belong to the user

- Every genuine design decision belongs to the user: vocabulary and naming of public API, which crate to build on, configuration surface, data formats, fallback behavior. Present options with a recommendation and ask before implementing.

## Naming is an art

- Names carry the design; treat them as design decisions worth real effort and user input. A wrong name misleads forever, a right name replaces documentation.
- Use the domain's vocabulary (`subject`, `frontmatter`, `triple`), not implementation noise (`data`, `result`, `helper`, `process`).
- Precise verbs with honest semantics: `parse` returns a structure, `as_` is a free view, `to_` is an expensive conversion, `into_` consumes; iterators come from `iter`, `iter_mut`, `into_iter`. Follow the official guidelines: https://rust-lang.github.io/api-guidelines/naming.html and the checklist at https://rust-lang.github.io/api-guidelines/checklist.html.
- Full words, no abbreviations (`message`, not `msg`). A long correct name beats a short vague one; a short exact one beats both.
- If a good name is hard to find, the abstraction is probably wrong; restructure until the name becomes obvious. Propose alternatives to the user when a public name is contested.
