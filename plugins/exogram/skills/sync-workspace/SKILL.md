---
name: sync-workspace
description: Sync every repository of the exogram workspace, pull remote changes, then commit local ones on feature branches and open pull requests for the user to merge, behind approval gates. Use when the user asks to "sync workspace", "sync the exogram", "pull everything", "commit everything", "land my changes", "push all repos", or wants the root repository and every member up to date and committed.
argument-hint: [--files-from <file>] [repository folder ...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

# Sync Workspace

Sync the exogram workspace: pull what the remotes have, then land what the host has. Every repository follows one strategy: commits on a feature branch, one pull request per branch, rebase merge onto `main`. `main` never takes a direct commit. The skill opens pull requests and never merges them: the user merges elsewhere. Between runs a repository stays on its feature branch, and new changes join its open pull request. No branch is ever force-pushed. The exogram workspace root is `${CLAUDE_PLUGIN_ROOT}/../../..`; every path below is relative to it.

This skill is the one place an agent runs state-changing git, and only past a gate the user approved.
Every gate covers all repositories at once.
Every git command takes the form `git -C <folder>`, and every command runs outside the sandbox: commit signing and SSH fail inside it.
A state-changing command is never piped or filtered; after each one assert the state it should have produced, and stop at the first mismatch.
A command whose state already holds is skipped, without a remark.
Scratch files use absolute paths, since `$TMPDIR` differs inside and outside the sandbox.

## Inputs

- `$ARGUMENTS`: optional repository folders to limit the run. Default is every repository.
- `--files-from <file>`: optional absolute path of a file that lists one path per line, relative to the exogram workspace root, each optionally followed by a tab and the absolute path of a patch. It limits the run to those files, and a file with a patch to that patch, see File Scope.

## Repositories

The root repository (`.`) and every member. The members are the `namedExogram` entries of the Workspace note, the note typed `Type Workspace` in the exogram workspace root: the label is the folder, the link target the remote. Read them from the note, never from this file.

## File Scope

With `--files-from` the run covers only the listed files. `exogram:sync-session` calls the skill this way. The steps change:

| Step | Change |
| --- | --- |
| Repositories | only those that hold a listed file: `just pull` and `just survey` take `--files-from <file>` |
| Pull | `just validate` takes the listed files that still exist, not the whole exogram workspace |
| Survey | `changes` counts the listed files, `(+n other)` the rest |
| Package | only listed files are read, grouped, and committed, a file with a patch as that patch, shown as `hunk only` with no question. Each patch first passes `git -C <folder> apply --cached --check <patch>`; one that fails stops the run before the gate. The gate names every other changed file as left out |
| Commit | a file with a patch, listed or built from hunks the user picked, is staged with `git apply --cached <patch>`, never with `add -A` |
| Remote Settings | skipped |

Every file and hunk not listed stays uncommitted in the working tree, through the branch switch and the rebase.

## Decisions

The user has not seen the diff. Every decision is one markdown chat message that ends the turn; the user answers free-form.
No command runs while any question of a decision is open; a partial answer gets a follow-up on the open part only.

The message holds, in this order:

- what changed: file paths and aliases, counts, the before and after or a short diff excerpt
- why it is a question: the risk or conflict found, one line per risk
- the recommendation and its reason
- the question in one line, then numbered options of at most five words, each with its consequence; an option that resolves a risk names it

Never name a change only by id, step, or label.
A risk is only what the user probably did not intend: a secret, junk, a failing validation. Never an edit they made, a deletion included.

## Workflow

### 1. Pull

`just pull [folder ...]` checks the SSH agent and the forge logins before any network command, runs `just init`, and removes every empty, read-only `.git/*.lock` the sandbox left behind while no git process runs.
It then, per repository in parallel, empties every dataview result block in its notes, fetches, fast-forwards `main` with `--autostash`, and moves a branch whose pull request is merged back to `main`.
Git only ever holds empty result blocks, so generated output never conflicts.
On missing credentials relay the printed `!` command and stop.
A row marked `stopped` ends the run, the autostash left for the user; a row marked `skipped` stays out of the run, a diverged `main` never merged or reset.

After the pull, `just validate`. On any failure stop and report; a stale generated file means `just init` or `just templates` first.

### 2. Survey

`just survey [folder ...]` prints one row per repository with local changes, unmerged commits, or a feature branch; skip the repositories its `skip` column names.
Below the table, `Generated` lists the files changed only inside dataview result blocks, `Edited` every other change.

### 3. Package

An empty remote gets one `Initial commit` of every file, unread except for a scan for secrets and junk.
`Generated` files, whose filled result blocks the pull emptied, form one `chore: clear serialized dataview results` commit per repository, unread.
Otherwise read the full diff of every `Edited` file (`git diff HEAD`, untracked files whole), one parallel Sonnet subagent per large repository.
Group the changes into commits with one intent each, as `dev:commit-message` step 3 defines. A file belongs to exactly one commit; split a file by hunk only with the user's word or a listed patch.

Gate: the user approves, moves files, edits messages, or drops a repository. The approval covers the branch, the commits, the push, and the pull request: steps 4 to 7 run without another gate. The evidence is one block per commit:

```markdown
### <repository> → <branch>

<commit message>

| File | Change |
| --- | --- |
| <path> | <alias, or what changed, and `hunk only` for a split file> |

Pull request: <title and body that `--fill` gives, or `joins #<number>`>
Left out: <count> files (<kinds>)
```

`Pull request` and `Left out` appear once per repository, `Left out` only with `--files-from`. Risks follow the last block.

### 4. Branch

Per repository with an approved grouping:

- Empty remote: stay on `main`. The first push to an empty remote is the one direct push to `main`; the pre-push hook lets it through.
- On `main`: `git switch -c <type>/<slug> origin/main`, where type and slug name the main intent of the repository's commits. Uncommitted changes carry over.
- On a feature branch with an open pull request: stay; the new commits join that pull request. Never branch from it: GitHub's rebase merge gives the merged commits new ids, so a branch built on them would need a force push.

### 5. Commit

Clear the index first (`reset -q`, never `--hard`); earlier staged changes would leak into the first commit.
Per approved commit, no further gate:

1. Assert the index is empty and the current branch is the approved one, then `add -A -- <files>`.
2. Scan `diff --staged` for secrets. On a hit stop and warn.
3. `commit -F -` with the approved message on stdin.

### 6. Rebase

Only a branch never pushed: `git fetch origin`, then `git rebase --autostash origin/main` when `origin/main` is no ancestor of `HEAD`. A pushed branch is never rebased; GitHub rebases at merge. On a conflict stop, report the files, and leave the rebase for the user.

### 7. Land

No gate: the package gate approved the push and the pull request. Per repository:

| Remote | Commands |
| --- | --- |
| empty | `git push -u origin main` |
| GitHub | `git push -u origin HEAD`; `gh pr create --base main --fill` when the branch has no pull request |
| GitLab | `git push -u origin HEAD`; `glab mr create --fill --target-branch main --remove-source-branch --yes` when the branch has no merge request |

Stop there. The user merges elsewhere; the repository stays on the branch. GitHub rebases at merge; GitLab needs the Rebase button or `glab mr rebase` when `main` moved.

### 8. Serialize

`just serialize` fills the result blocks again for Obsidian and the note listings.
The output stays uncommitted; the next pull empties it. A failure goes into the report.

### 9. Remote Settings

Once per repository, read the settings and offer every fix behind one gate:

- GitHub, `gh api --method GET repos/<owner>/<name>`: `allow_rebase_merge` true, `allow_merge_commit` and `allow_squash_merge` false, `delete_branch_on_merge` true. Fix with `gh api --method PATCH repos/<owner>/<name> -F <field>=<value>`.
- GitHub, public repository only: a ruleset on the default branch with the rules `deletion`, `non_fast_forward`, `required_linear_history`, and `pull_request` with `allowed_merge_methods: ["rebase"]` and one approval, the Admin role (`actor_id` 5) on the bypass list, since an author cannot approve their own pull request. Read with `gh api --method GET repos/<owner>/<name>/rulesets`, create with `gh api --method POST repos/<owner>/<name>/rulesets --input -`. Private repositories on GitHub Free have no rulesets; the pre-push hook stands in.
- GitLab, `glab api --method GET projects/<url-encoded path>`: `merge_method` is `ff`; `main` is protected with push access `No one` (level 0). Changing it needs the Maintainer role; report when the user lacks it.

### 10. Report

One table: repository, commits pulled, commits pushed, pull request link and state, skipped with reason.

## Anti-patterns

- Committing on `main` of a remote that already has one
- Committing a filled dataview result block
- Merging a pull request, or switching to `main` while its pull request is open
- `--no-verify`, `--force`, `--force-with-lease`, `reset --hard`, `rebase -i`, `stash drop`, `clean`
- A branch created from another feature branch
- Switching, rebasing, or deleting a branch the user was working on
- A commit mixing intents, or a message not drafted by `dev:commit-message`
- `gh api` or `glab api` without an explicit `--method`
- A question without the evidence to decide it
- With `--files-from`, committing a file or hunk that is not listed
