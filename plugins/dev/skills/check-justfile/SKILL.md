---
name: check-justfile
description: Check that a Rust project has the default justfile structure and clippy.toml, and create or repair them when missing. Use when the user asks to "add a justfile", "fix the justfile", "maintain this project", "add a lint job", "set up project tooling", or when entering a Rust crate whose justfile deviates from the default recipes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Maintain Rust Project

## Default justfile structure

Every Rust crate's justfile must contain these recipes; workspace roots delegate with `just <member>/<recipe>`:

```just
build:
    cargo build

test:
    cargo test

lint:
    cargo +nightly fmt --check
    cargo +nightly clippy -- -D warnings -W clippy::cognitive_complexity -W clippy::excessive_nesting
    cargo +nightly udeps

install-dev-dependencies:
    rustup install nightly
    rustup component add rustfmt clippy --toolchain nightly
    cargo install --locked cargo-udeps

pre-commit-check: lint test
```

## Workflow

1. Locate the justfile of the current crate and of the workspace root. No justfile: create one from the template above. Existing justfile: diff its recipes against the template.
2. Keep project-specific recipes (`run`, `convert-*`, `develop-*`, `install`, deployment jobs) untouched; only add missing default recipes and align the `lint` recipe with the template. Ask before rewriting a recipe that exists with different content.
3. Ensure a `clippy.toml` at the workspace root:

```toml
cognitive-complexity-threshold = 10
excessive-nesting-threshold = 4
```

4. Binary crates additionally get `install: cargo install --path .`.
5. Verify with `just lint` (report failures, do not silence them) and `just test`.
6. Never run state-changing git commands; the user commits.

Reference layout: `~/repositories/symbolith-exogram/rdf-diagram-framework/justfile` (workspace delegation) and `~/repositories/symbolith-exogram/rdf-diagram-framework/rdf-diagram-lib/justfile` (member crate).
