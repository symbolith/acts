---
name: plan
description: Forces an understand-research-outline-then-write workflow before drafting any substantive text. Use when the user asks to write, draft, compose, rewrite, or polish an email, README, PR description, doc, blog post, paragraph, reply, wiki note, or any prose they will read or send. For commit messages use the dev:commit-message skill instead. Stops generic AI-slop by requiring topic, audience, and purpose to be clear, and genre best practices to be researched, before the first sentence.
allowed-tools: WebSearch, WebFetch, AskUserQuestion, Read, Write, Edit, Grep, Glob
---

# Plan Before Write

Use this skill for any text the user will read, paste, or send: emails, docs, READMEs, PR descriptions, blog posts, prose paragraphs, wiki notes, replies. Skip it for one-line chat replies, code edits without prose, direct factual answers, and commit messages (use dev:commit-message).

## The Iron Rule

No sentence reaches the user until all four gates have passed:

1. UNDERSTAND. What is this text actually about?
2. RESEARCH. What makes great writing of this genre?
3. OUTLINE. What 3 to 6 points carry the message?
4. WRITE. Only now produce prose.

Skipping a gate produces generic tokens. The point of this skill is to refuse to write before knowing what to write.

## Gate 1: Understand

Before drafting, answer these in your head:

1. Topic. What is this text about? Name the specific subject, not the category.
2. Audience. Who reads it? What do they already know? What do they want from it?
3. Purpose. What should the reader do or believe after reading?
4. Constraints. Length cap, tone, format, deadline, channel.
5. Stakes. High (PR review, public doc, customer email, published essay) or low (internal note)?

If any answer is unknown and material, call `AskUserQuestion`. Do not invent.

## Gate 2: Research

For any genre you cannot describe in three concrete properties without thinking, research the craft before drafting. See [references/genres.md](references/genres.md) for notes on:

1. PR descriptions
2. READMEs
3. Technical docs and tutorials
4. Cold emails and replies
5. Bug reports
6. Blog posts and essays
7. Academic prose
8. API reference
9. Release notes

If the genre is not covered there, run 2 to 3 `WebSearch` queries against authoritative sources (project style guides, books on the craft, top forum threads). Examples:

1. `pr description best practices site:github.com`
2. `how to write a great README hacker news`
3. `cold email outreach reddit advice`

Prefer primary sources (style guides, the project's own conventions, books) and community discussion over listicles. Look at 2 to 3 real high-quality examples of the same genre when you can. Do not search if you can already state three concrete properties of great writing in this genre.

## Gate 3: Outline

Write 3 to 6 bullets in this form:

```
- [Point]. [Why it belongs or what it proves.]
```

The outline is for you, not the user. It exists to prevent rambling. If a bullet does not earn its place, cut it before drafting.

For texts longer than a paragraph, name the spine in one line: opening, middle, close.

## Gate 4: Write

Apply the universal craft rules from [references/anti-slop.md](references/anti-slop.md) plus the genre-specific patterns from [references/genres.md](references/genres.md).

After the draft, self-review with these questions:

1. Does the first sentence carry weight, or is it warming up?
2. Does every sentence after the first earn its place?
3. Can any word be cut without changing meaning? Cut it.
4. Did the draft violate the user's CLAUDE.md anti-slop rules (em-dashes, slop words, fake-balance "not just X but Y", `**Bold:** description` lists)?
5. Read it aloud. Are there sentences you dread reading? Fix them.

If the draft fails self-review, revise before showing it. A revised second draft is cheaper than a back-and-forth on a bad first one.

## Ask vs. Research

1. Ask the user when the answer depends on their context: audience, stakes, tone preference, hidden constraints, sensitive details.
2. Research the web when the answer depends on craft norms: what good commit messages look like, what cold emails get replies, what a strong README opens with.
3. Never substitute one for the other. A user clarification cannot tell you the genre norms; web research cannot tell you the user's audience.

## When to skip this skill

1. The user asked for a one-line chat reply.
2. The task is a code edit with no prose deliverable.
3. The user asked a direct factual question.
4. The user is in fast iteration mode and explicitly says "just write it".
5. The deliverable is a commit message (use dev:commit-message).

When skipping, still apply [references/anti-slop.md](references/anti-slop.md) to whatever prose does appear.

## Anti-patterns

1. Skipping Gate 1 because "the request is obvious".
2. Padding Gate 2 by searching for what you already know.
3. Writing the outline after the draft, so the outline rationalizes the prose.
4. Reaching for AI-slop words to sound smart.
5. Producing five paragraphs when two would carry the message.
6. Showing the user a first draft you would not send yourself.
7. Auto-formatting every list as `**Bold:** description` when plain prose would be clearer.
8. Calling `AskUserQuestion` for craft norms the user has no reason to know.

## References

1. [references/genres.md](references/genres.md). Per-genre craft notes for READMEs, PR descriptions, emails, bug reports, blog posts, academic prose, API reference, release notes.
2. [references/anti-slop.md](references/anti-slop.md). Universal craft rules drawn from Orwell, Strunk and White, Paul Graham, and the user's CLAUDE.md bans.
