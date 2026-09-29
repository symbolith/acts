# Implement

## Readability and conciseness are paramount

- Code must read top-down without comments: small functions, one level of abstraction per function.
- Concise but never clever: `let else`, early `continue`, `?`; no nesting pyramids, no premature generics, no speculative flexibility.
- Iterator chains are the default; write a `for` loop only when it beats the functional form in concision and elegance.
- Maximum indentation depth is three levels inside a function body; struct literals and match arms count. Deeper means extract a function; exceeding the limit needs the user's approval.
- Return owned values; never `&mut` out-parameters. Build collections by `collect`, not accumulator loops.
- No comments in final code. If code needs a comment, rename or restructure instead.
- Name intermediate results with structs and enums, not tuples. One domain concept, one type.
- File item order: types in the order the domain documentation presents them, each private helper directly below its only caller, tests last.

## Clean architecture (the principles, not the book)

- Dependencies point inward: domain logic never depends on IO, CLI, or serialization details.
- A domain crate exports only its domain: shared machinery (macros, generic helpers) lives in its own crate, never in a domain crate's public API.
- Separate policy from mechanism: what to convert vs how to read files, parse, serialize.
- Boundaries are explicit types and small trait or function surfaces, not layers of ceremony. No interfaces with one implementation, no manager or service noise.
- Prefer a pure core with an imperative IO shell over trait-heavy hexagonal scaffolding; add a trait only when a second implementation or a test double actually exists.
- Module boundaries follow domain cohesion: one domain concept per module file; an impl spanning two types lives in the module of the higher-layer type.
- A submodule tree is `parent.rs` plus a `parent/` directory; never create `mod.rs`. The crate root holds only `mod` declarations and re-exports.
- Module privacy bounds visibility: items in private modules are plain `pub`; `pub(crate)`/`pub(super)` are a smell of a boundary in the wrong place.
- Errors are part of the design: one snafu variant per failure with `#[snafu(display(...))]`; fail loud, never silently skip invalid input.

## Complexity budget

- Measure cognitive complexity and nesting with clippy after implementing:

```bash
cargo clippy -- -W clippy::cognitive_complexity -W clippy::excessive_nesting
```

- Ensure the crate root workspace has a `clippy.toml` with the thresholds; create it if missing:

```toml
cognitive-complexity-threshold = 10
excessive-nesting-threshold = 4
```

- Nesting threshold 4 because clippy counts the `impl` and `fn` blocks themselves; 4 equals two control-flow levels inside a method body.
- `excessive_nesting` sees only braced blocks; `cognitive_complexity` at 10 is what catches nesting in closures and match arms. When code slips past both, tighten the config, do not add manual review rules. Silencing (`#[allow]`, raised threshold) needs a good argument made to the user first.

## Verify

- `cargo test` and `cargo fmt` after implementing; clippy already ran in the complexity check.
- Never run state-changing git commands; the user commits.
