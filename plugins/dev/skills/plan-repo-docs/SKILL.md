---
name: plan-repo-docs
description: Analyze an open source repository and recommend which documentation files it needs, then generate outlines for each. Use when the user asks to "create docs", "add documentation", "set up repo docs", "what docs does this repo need", "generate README", "create CONTRIBUTING", "documentation audit", "repo documentation", or wants to know which markdown files a project should have.
argument-hint: [path/to/repo]
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

# Create Repository Documentation

Analyze a repo, recommend which doc files it needs, let the user override, then generate tailored outlines.

## Workflow

### 1. Locate the Repo

If `$ARGUMENTS` contains a path, use it. Otherwise use the current working directory. Verify it has source files.

### 2. Analyze the Repo

Gather these signals in parallel:

- **Manifests**: `Glob: {package.json,Cargo.toml,pyproject.toml,setup.py,go.mod,Makefile,CMakeLists.txt,*.cabal,build.gradle,pom.xml,mix.exs,Gemfile}`
- **Existing docs**: `Glob: {README*,CONTRIBUTING*,LICENSE*,ARCHITECTURE*}`
- **CI/Docker**: `Glob: {Dockerfile*,.github/workflows/*,Jenkinsfile,.gitlab-ci.yml}`
- **Activity**: `git log --oneline -20` and `git shortlog -sn --no-merges | head -5`
- **Remote**: `git remote get-url origin 2>/dev/null`

From this, determine: primary language, framework, package manager, contributor count, existing docs, whether it's a library/CLI/web app/utility.

### 3. Recommend Documentation Files

Load [references/doc-catalog.md](references/doc-catalog.md) for outlines and section details.

Apply these rules:

| File | Recommend when |
|---|---|
| README.md | Always (essential) |
| LICENSE | Always (essential) |
| CONTRIBUTING.md | Contributors > 1 or project accepts external contributions |
| ARCHITECTURE.md | Multiple modules or non-obvious structure, generally > 2000 LOC |

Present the recommendation table:

```
## Documentation Audit for [repo-name]

Language: X | Type: library/CLI/app | Contributors: N

| File | Status | Recommendation | Reason |
|---|---|---|---|
| README.md | Missing/Exists | Essential | ... |
| LICENSE | Missing/Exists | Essential | ... |
| CONTRIBUTING.md | Missing/Exists | Recommended/Skip | ... |
| ARCHITECTURE.md | Missing/Exists | Recommended/Skip | ... |
```

Use `AskUserQuestion` to let the user confirm which files to generate outlines for. Skip files that already exist unless the user explicitly asks.

### 4. Generate Outlines

For each selected file, generate an outline from the catalog. Tailor it to the repo:

- Use the actual project name in headings and description formulas
- Use the actual package manager and build commands in Install/Configure/Run sections
- Reference actual test directories and linter configs
- For ARCHITECTURE.md, name actual modules and directories from the repo

Present all outlines in a single response with headers + brief notes per section (not full prose, not bare headers).

### 5. Report

List what was audited and what outlines were generated. Do not write any files.

## Rules

- Never write files. Output only.
- Tailor outlines to the repo's actual stack.
- Skip existing doc files unless the user asks for a rewrite.
- Scale to project size: a 200-line script needs README + LICENSE, not the full suite.
