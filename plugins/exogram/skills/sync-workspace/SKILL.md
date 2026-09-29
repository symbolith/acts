---
name: sync-workspace
description: Sync every repository of the exogram workspace, pull remote changes, then commit and land local ones, one pull request per repository, rebased on main, behind approval gates. Use when the user asks to "sync workspace", "sync the exogram", "pull everything", "commit everything", "land my changes", "push all repos", or wants the root and every nested repository up to date, committed, and merged.
argument-hint: [repository folder ...]
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion, Skill
---

# Sync Workspace

Sync the workspace: pull what the remotes have, then land what the host has. Every repository follows one strategy: commits on a branch from `origin/main`, rebased on `origin/main`, merged by pull request with rebase. `main` never takes a direct commit. The exogram root is `/home/beavis/repositories/symbolith-exogram`; every path below is relative to it.

This skill is the one place an agent runs state-changing git, and only past a gate the user approved.

## Inputs

- `$ARGUMENTS`: optional repository folders to limit the run. Default is every repository.

## Repositories

The root (`.`) and every `namedExogram` of the Workspace note, the root note typed `Type Workspace`: the label is the folder, the link target the remote. Read them from the note, never from this file.

## Decisions

The user has not seen the diff. Every question carries, in the question itself:

- what changed: file paths and aliases, counts, the before and after or a short diff excerpt
- why it is a question: the risk or conflict found, with the evidence
- every option with its consequence
- the recommendation and its reason

Never name a change only by id, step, or label. A deletion shows the note's alias, its comment, and every note that links to it.

## Workflow

### 1. Preflight

- `just init` clones every missing repository and installs the pre-push hook.
- Skip, and say why, a repository mid-rebase or mid-merge.

### 2. Pull

Per repository, `git fetch --prune origin`, then:

- on `main` and behind `origin/main`: `git pull --ff-only --autostash`
- local `main` diverged from `origin/main`: skip, never merge or reset
- on another branch: fetch only; a branch whose pull request merged elsewhere, its upstream gone, is reported for the user to delete
- the autostash does not apply cleanly: stop, report the files, leave the stash for the user

After the pull, `just validate`. On any failure stop and report; a stale generated file means `just init` or `just templates` first.

### 3. Survey

One table, one row per repository with local changes, unmerged commits, or pulled commits:

| Column | Source |
| --- | --- |
| branch | `git -C <folder> branch --show-current` |
| changes | `git -C <folder> status --porcelain` count |
| pulled | commits the pull brought in |
| ahead / behind | `git -C <folder> rev-list --left-right --count origin/main...HEAD` |
| remote | `empty` when `git ls-remote --heads origin main` prints nothing |
| open pull request | `gh pr list --head <branch>`, or `glab mr list --source-branch <branch>` for a GitLab remote |

Skip, and say why, a repository that:

- is on a branch other than `main`, unless the branch is `origin/main` plus unmerged commits from an earlier run of this skill
- has local `main` ahead of `origin/main` on a non-empty remote

### 4. Package

Read the full diff of each repository (`git diff HEAD`, and every untracked file). Group the changes into commits with one intent each, as `dev:commit-message` step 3 defines. A file belongs to exactly one commit; split a file only with the user's word, by hunk.

Gate: show the grouping per repository, files per commit. The user approves, moves files, or drops a repository.

### 5. Branch

Per repository with an approved grouping:

- Empty remote: stay on `main`. The first push to an empty remote is the one direct push to `main`; the pre-push hook lets it through.
- Otherwise: `git switch -c <type>/<slug> origin/main`, where type and slug name the main intent of the repository's commits. Uncommitted changes carry over.

### 6. Commit

Per commit of the grouping:

1. `git add -- <files>`; nothing else is ever staged.
2. Scan `git diff --staged` for secrets. On a hit stop and warn.
3. Draft the message with the `dev:commit-message` skill.
4. Gate: show `git diff --staged --name-status` and the message. The user approves, edits the message, or regroups.
5. `git commit -F -` with the message on stdin.

### 7. Rebase

`git fetch origin`, then `git rebase --autostash origin/main`. On a conflict stop, report the files, and leave the rebase for the user.

### 8. Land

Gate: show `git log --oneline origin/main..HEAD`, the pull request title and body. Then:

| Remote | Commands |
| --- | --- |
| empty | `git push -u origin main` |
| GitHub | `git push -u origin HEAD`, `gh pr create --base main --fill`, `gh pr merge --rebase --delete-branch` |
| GitLab | `glab mr create --fill --target-branch main --remove-source-branch --yes`, `glab mr merge --rebase --yes` |

Afterwards `git switch main`, `git pull --ff-only`, `git branch -d <branch>` when it still exists.

### 9. Remote Settings

Once per repository, read the settings and offer every fix behind one gate:

- GitHub, `gh api --method GET repos/<owner>/<name>`: `allow_rebase_merge` true, `allow_merge_commit` and `allow_squash_merge` false, `delete_branch_on_merge` true. Fix with `gh api --method PATCH repos/<owner>/<name> -F <field>=<value>`.
- GitHub, public repository only: a ruleset on the default branch with the rules `deletion`, `non_fast_forward`, `required_linear_history`, and `pull_request` with `allowed_merge_methods: ["rebase"]` and zero approvals. Read with `gh api --method GET repos/<owner>/<name>/rulesets`, create with `gh api --method POST repos/<owner>/<name>/rulesets --input -`. Private repositories on GitHub Free have no rulesets; the pre-push hook stands in.
- GitLab, `glab api --method GET projects/<url-encoded path>`: `merge_method` is `ff`; `main` is protected with push access `No one` (level 0). Changing it needs the Maintainer role; report when the user lacks it.

### 10. Report

One table: repository, commits pulled, commits landed, pull request link, skipped with reason.

## Anti-patterns

- Committing on `main` of a remote that already has one
- `--no-verify`, `--force`, `push --force-with-lease`, `reset --hard`, `rebase -i`, `stash drop`, `clean`
- Switching, rebasing, or deleting a branch the user was working on
- A commit mixing intents, or a message not drafted by `dev:commit-message`
- Running a state-changing command before its gate was approved
- `gh api` or `glab api` without an explicit `--method`
- A question without the evidence to decide it
