---
name: write-prose
description: Write prose through a staged pipeline in which clean-context agents write and the user picks between three proposals at every stage. Use when the user asks to write, draft, compose, rewrite, or polish an email, README, PR description, doc, blog post, essay, pitch, paragraph, reply, wiki note, or any prose a human will read. For commit messages use the dev:commit-message skill instead; for one-line glosses of formally defined names use writing:write-gloss.
argument-hint: <what to write, or the path of a text to rewrite>
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Write prose

Write the text in `$ARGUMENTS` by the pipeline below.

This conversation carries style rules made for terse chat answers, and they spoil prose. So you orchestrate and never write. Every sentence of the text comes from an agent that starts clean: no CLAUDE.md, no conversation.

## Rules of the pipeline

1. You never write, rephrase or tidy the text or any proposal. Show what the agents return, verbatim.
2. Every stage offers three proposals from three `writing:prose-writer` agents, spawned in one message, each with a different angle from the stage's axis.
3. A prompt to an agent holds the stage, the angle, the brief, and the accepted material, all verbatim. It holds no style advice and no instruction on tone. The user's answers go in as the user wrote them.
4. Show the three proposals side by side, labelled A, B and C, in the order returned, without ranking or comment. Then ask in plain text: A, B, C, or a combination the user describes. Never use `AskUserQuestion`.
5. If two proposals differ only in wording, discard the set and spawn it again with the angles stated more sharply.
6. When the user rejects all three, ask why and wait. Carry the reason into every later prompt as a constraint under the heading `Rejected`.
7. When the user combines proposals, spawn one writer with the parts named and show the result for a yes or no.
8. Each stage uses fresh writers. Do not resume one from an earlier stage.
9. From one page up, save each draft and revision to the scratchpad and give the plain paths next to the text.
10. Skip this skill for a one-line chat reply, a code edit without prose, a direct factual answer, or when the user says "just write it".
11. The family's shared discipline is [references/discipline.md](references/discipline.md). A one-line gloss of a formally defined name goes to `writing:write-gloss`. A recurring micro-genre without its own skill (a remark, a heading, a paragraph form) runs here only until its skill is created by the claude-code:create-skill research process; when such a genre starts arriving in volume, create that skill first.

## 0. Size

Ask first, in plain text, how long the text will be, offering the three sizes below. The answer picks the stages.

| Size | Stages |
|---|---|
| Up to one paragraph | context, short brief, draft, bans |
| Up to one page | context, brief, outline, draft, revise, bans |
| More than one page | context, brief, outline, paragraph plan, draft, revise, bans |

The user may add or drop a stage at any checkpoint.

In the same message as the size question, spawn one `writing:prose-context` with the subject from `$ARGUMENTS`. It searches the Symbolith exogram for what the notes already say, then the web for what they lack and for the case against them. Its report joins the brief verbatim as `Context` and goes to every writer.

## 1. Brief

Show the context report first, so the user answers with the notes in view. Where the report lists terms, the text uses those terms and no synonyms. Where it lists `Absent` or `Unconfirmed`, ask the user for it. Where it lists `Conflicts`, the user decides which side the text takes.

Ask the questions in plain text, in this order, and wait for the answers. Do not answer them yourself and do not guess. A question the user cannot answer goes into the brief as open.

The short brief is questions 1, 2 and 4.

1. What does the reader believe or do now, and what should they believe or do after reading?
2. Who exactly reads it? Why would they bother, and what will they doubt?
3. What is the problem, and what does it cost this reader if it stays unsolved?
4. What is the claim, in one sentence someone could dispute?
5. What does the reader already know, what must be defined, and what stays out?
6. What is the strongest fact against the claim, and whose view does the text argue against?
7. Which genre and setting, and are there limits on length or form?
8. Which points would only you make? Name them before any proposal exists.

For a rewrite, read the existing text and pass it along as material. The questions still get asked.

Read the genre's entry in [references/genres.md](references/genres.md) and add it to the brief as `Genre notes`. For a genre not listed there, look up its conventions online in primary sources and add what you find with the URLs.

Proposals at this stage are framings of the claim. Axis: what the claim puts first, namely the problem, the answer, or the consequence for the reader. The accepted framing joins the brief.

## 2. Outline

Stage `outline`. Axis: the order of the same material, namely problem then answer, strongest point first, or chronological. Use a thematic order where chronology makes no sense for the material.

Before showing the proposals, check that the points from question 8 appear in each. Tell the user which are absent.

## 3. Paragraph plan

Stage `paragraph plan`. Axis: where the point sits and what carries it, namely point first with the strongest evidence, point last after a built case, or point first with a different choice of examples.

Pass any `MISSING:` mark on to the user as a question. A paragraph with nothing to carry it is filled by the user or cut. It is never drafted empty.

## 4. Draft

Stage `draft`. Axis: the opening move, namely the problem, a concrete case, or the claim.

For a text of more than one page, draft section by section in the order of the outline, with three proposals for each section. Each writer gets the plan of its section and the sections already accepted, verbatim. From the second section on, the axis is how the section opens: on its point, on its carrying case, or on the link from the section before.

Run no checks at this stage and ask for none.

## 5. Revise

First spawn one `writing:prose-reader` with the accepted draft and the reader description from question 2, and nothing else. Show its report.

Then stage `revision`. Axis: the lens, namely `argument`, `structure` or `reader`. Each writer gets the draft, the plan and the reader's report.

Repeat the stage only when the user asks for it.

## 6. Bans

Spawn one `writing:prose-editor` with the accepted text and nothing else. Show the edited text, its `CHANGES` and its `FLAGS`. Each flag is a question for the user. Resolve a flag by passing the user's answer and the text to a fresh editor.

Ask the user to read the result aloud once before they send it. Then write the text to the place the user names.
