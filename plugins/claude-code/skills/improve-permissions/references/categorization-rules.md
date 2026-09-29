# Permission Categorization Rules

## Safe (read-only, no state changes)

### Tool-level
- `Read`, `Grep`, `WebSearch`, `WebFetch`, `WebFetch(domain:*)`

### Bash read-only
- `cat`, `ls`, `wc`, `env`, `fd`, `find`, `echo`, `head`, `tail`, `file`, `identify`, `tree`, `xargs ls`, `xargs jq`, `jq`

### Git read-only
- `git log`, `git show`, `git status`, `git diff`, `git branch`, `git tag`, `git remote`, `git check-ignore`, `git describe`, `git rev-parse`

### Cargo read-only
- `cargo tree`, `cargo search`, `cargo doc`, `cargo metadata`

### MCP read tools
- Patterns ending in `read`, `get`, `list`, `search` (case-insensitive)

### Package manager queries
- `mcpm` commands

## Maybe safe (side effects, but controlled/reversible)

### Cargo build/test
- `cargo test`, `cargo build`, `cargo check`, `cargo clippy`, `cargo fmt`, `cargo run`, `cargo insta accept`
- Nightly variants: `cargo +nightly clippy`, `cargo +nightly fmt`

### Package management
- `npm install`, `npx`

### Task runners
- `just`, `make`

### System
- `swaymsg`, `curl`, `mkdir`, `gh api --method GET`

## Not safe (destructive, never auto-add)

- `pkill`, `kill`, `rm`, `rmdir`, `dd`, `chmod`, `chown`, `sudo`
- Multi-line `bash -c` scripts
- Every state-changing git or gh command: `git add`, `git commit`, `git checkout`, `git switch`, `git stash`, `git fetch`, `git pull`, `git merge`, `git push`, `git reset`, `git clean`, `gh pr create`, `gh api` without `--method GET`
- Shell fragments (`do`, `done`, `for …`, `while …`, `# …`) and one-off commands naming a specific file, hash, or URL
