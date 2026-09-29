---
name: create-skill
description: Create a new Claude Code skill (SKILL.md). Use when the user wants to create a skill, make a slash command, add a custom command, or build a new skill for Claude Code.
argument-hint: [skill-name] [description of what it should do]
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, WebSearch, WebFetch, Agent
---

# Create Skill

Create a new Claude Code skill, global in the dotfiles repo or local to a project, with proper structure and best practices.

## Workflow

### 1. Gather Requirements

If `$ARGUMENTS` provides enough context, extract:
- **Skill name**: lowercase, hyphens only, max 64 chars, no reserved words ("anthropic", "claude")
- **Purpose**: what the skill does
- **Trigger scenarios**: when it should activate

If unclear, use `AskUserQuestion` to clarify:
- What should the skill do?
- Should Claude auto-invoke it, or manual-only (`/slash-command`)?
- Does it need supporting files (scripts, references)?

Always ask where the skill goes, with `AskUserQuestion`, unless `$ARGUMENTS` says so:
Every skill lives in `~/repositories/symbolith-exogram/acts/plugins/<plugin>/skills/<skill-name>/`, a plugin of the `acts` marketplace. Ask which plugin:
- Global: a plugin enabled in the user settings (`claude-code`, `dev`, `diagrams`, `exogram`, `writing`). For skills that apply to any project.
- Project: a plugin enabled only in one project's `.claude/settings.json` (`factors`). For skills bound to one repository's files, rules, or vocabulary.

Recommend global when the skill's rules hold outside the current repository, project otherwise.

### 2. Research

Before writing anything, research what already exists and what the domain demands.

#### Local skills

Read 3-5 existing skills most relevant to the new skill's domain:

```
Glob: ~/repositories/symbolith-exogram/acts/plugins/*/skills/*/SKILL.md
```

Look for:
- Structure patterns (how `research-web` uses progressive disclosure with `references/product-research.md`)
- Tone and writing style consistent with the user's collection
- Metadata field choices similar skills make
- What works and what feels overengineered or too vague

#### Online skill repositories

Search GitHub for prior art in the same domain. Run these searches in parallel:

1. `site:github.com SKILL.md $DOMAIN` (find existing skills for the same task)
2. `site:github.com/anthropics/skills $DOMAIN` (check the official Anthropic skill collection)
3. `site:github.com awesome-claude-skills $DOMAIN` (check curated awesome lists: ComposioHQ/awesome-claude-skills, VoltAgent/awesome-agent-skills, travisvn/awesome-claude-skills)
4. `site:github.com/alirezarezvani/claude-skills $DOMAIN` (235+ production skills collection)

If a relevant skill exists online, fetch and read it with `WebFetch`. Adapt the best ideas rather than starting from scratch. Note what works about its structure, what references it includes, and what it does that the user's existing skills do not.

#### Domain research

Use web search to find authoritative sources on how to do the skill's task well:

- Official style guides and best practice documentation (Google, Microsoft, Stripe, DigitalOcean, etc.)
- Community consensus from forums, HN, Reddit
- Academic or professional standards if applicable

Decide which findings belong as `references/` files in the skill (loaded at runtime) versus one-time context that informs the skill's design but doesn't need to ship with it.

### 3. Design the Metadata

Walk through each question — skip means use the default:

1. **Side effects?** (deploys, sends, commits, deletes)
   → Yes: `disable-model-invocation: true` (manual `/slash` only)

2. **Background knowledge only?** (style guides, conventions, context)
   → Yes: `user-invocable: false`

3. **Takes arguments?**
   → Yes: `argument-hint: [descriptive placeholder]`

4. **Which tools does it actually need?**
   → List them: `allowed-tools: Tool1, Tool2, ...`
   → Omit only if the skill genuinely needs unrestricted access
   → Common sets:
     - Read-only analysis: `Read, Glob, Grep`
     - File creation: `Read, Write, Glob, Grep, AskUserQuestion`
     - Runs scripts: `Read, Bash, Grep, AskUserQuestion`

5. **Needs conversation context?**
   → No (self-contained workflow): `context: fork`
   → Yes (references prior discussion): omit

6. **If forked, what agent type?**
   → Read-only search: `agent: Explore`
   → Planning/design: `agent: Plan`
   → Full toolset: omit (defaults to `general-purpose`)

7. **Needs a specific model?**
   → Fast/cheap task: `model: haiku`
   → Complex reasoning: `model: opus`
   → Normal: omit (inherits session model)

8. **Needs different effort level?**
   → Quick lookup: `effort: low`
   → Deep analysis: `effort: max`
   → Normal: omit

### 4. Write the Description

The description is the most critical field — it controls when Claude auto-triggers the skill.

Rules:
- Write in **third person** (not "I can" or "You can")
- Include **specific trigger keywords** the user would naturally say
- State both **what** it does and **when** to use it
- Max 1024 chars, no XML tags
- Be specific, not vague

Pattern:
```
description: [What it does]. Use when [trigger scenarios], or when the user [natural phrases].
```

Bad: `description: Helps with tests`
Good: `description: Run the test suite and report failures with context. Use when the user asks to "run tests", "check tests", "test this", or after making code changes that need verification.`

### 5. Write SKILL.md Content

Structure the body following these principles:

**Conciseness**: Claude is already smart — don't explain basics. Every token competes for context. Target under 500 lines.

**Degrees of freedom**:
- High freedom (flexible tasks): text guidelines, heuristics
- Medium freedom (patterns): pseudocode, templates with parameters
- Low freedom (fragile/exact tasks): specific scripts, exact commands

**Progressive disclosure**: Keep SKILL.md as the high-level guide. Move detailed references, examples, and scripts to subdirectories:
```
skill-name/
├── SKILL.md
├── scripts/       (executable helpers)
├── references/    (detailed docs, rules)
└── examples/      (worked examples)
```

Reference supporting files from SKILL.md so Claude loads them when needed:
```markdown
See [references/api-guide.md](references/api-guide.md) for full API details.
```

**Available variables** in skill content:
- `$ARGUMENTS` — all args passed to the skill
- `$ARGUMENTS[N]` or `$N` — specific arg by 0-based index
- `${CLAUDE_SKILL_DIR}` — directory containing SKILL.md
- `${CLAUDE_SESSION_ID}` — current session ID

**Shell preprocessing**: the harness scans SKILL.md before Claude sees it and substitutes any `BANG-BACKTICK command BACKTICK` placeholder with the command's stdout. Use this to inject live data (e.g. the current git branch) into a skill at load time. Note: the pattern triggers anywhere in the file, including inside code fences — do not paste literal examples of it into a SKILL.md or loading the skill will run them.

### 6. Create Files

Create all files under the location chosen in step 1:

```
<location>/<skill-name>/SKILL.md
<location>/<skill-name>/scripts/     (if needed)
<location>/<skill-name>/references/   (if needed)
```

`<location>` is `~/repositories/symbolith-exogram/acts/plugins/<plugin>/skills`.

### 7. Validate

Before finishing, verify:
- [ ] `name` is lowercase + hyphens, max 64 chars
- [ ] `description` is third-person, specific, includes trigger keywords
- [ ] `allowed-tools` is set unless the skill genuinely needs all tools
- [ ] `argument-hint` is set if the skill accepts input
- [ ] SKILL.md body is under 500 lines
- [ ] No XML tags in name or description
- [ ] Supporting files are referenced from SKILL.md
- [ ] No deeply nested references (one level max)
- [ ] Paths use forward slashes only

### 8. Remind User

After creating the skill, tell the user where it landed.

> Skill created at `~/repositories/symbolith-exogram/acts/plugins/<plugin>/skills/<name>/SKILL.md`.
> The marketplace `acts` loads in place: the skill is available as `/<plugin>:<name>` after `/reload-plugins` or in the next session. A new plugin also needs an entry in `acts/.claude-plugin/marketplace.json` and in `enabledPlugins`.

## Anti-patterns to Avoid

- Vague descriptions that won't trigger auto-invocation
- Over-explaining concepts Claude already knows
- Windows-style backslash paths
- Time-sensitive conditionals
- Deeply nested file references
- Missing `disable-model-invocation` on side-effect skills (deploy, send, commit)
- Putting everything in SKILL.md instead of using progressive disclosure
- Missing `allowed-tools` on skills that only need a few tools — always scope down
- Adding `context: fork` to skills that need conversation context
- Omitting `argument-hint` when the skill accepts input
- Writing a skill without reading existing skills or researching the domain first
- Ignoring online skill repositories when prior art exists
