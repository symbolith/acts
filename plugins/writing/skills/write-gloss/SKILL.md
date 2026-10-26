---
name: write-gloss
description: Write a gloss of one of three kinds, the definition of a general concept (a definitions table row, a formalism construct, an ontology term), the one-line description of an individual (the `comment` of a Software, Person or Organization note), or the abstract of a resource, with clean-context writers and fresh verifiers running sourced checks. Use when the user asks to "write a gloss", "gloss this", "fix a gloss", "the gloss needs work", "rewrite the glosses", "write a comment", "write a description", "write an abstract", "describe this software", or rejects a gloss.
argument-hint: <note path and the names to gloss, or the note to describe>
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, Bash(just:*), Bash(rg:*), Bash(cat:*), Bash(find:*), Bash(git log:*), Bash(git show:*), Bash(git ls-files:*)
---

# Write a gloss

Gloss the names or notes in `$ARGUMENTS` by the process below.

You orchestrate and never touch the text: writers draft in fresh contexts, verifiers check in fresh contexts, you relay both verbatim. Mechanical reshaping of a candidate, down to stripping a copula, is a writer's job, not yours. The map and the interview's draft answers are not the text: write, sort and align them yourself. This skill belongs to the write-prose family; the shared discipline is [../write-prose/references/discipline.md](../write-prose/references/discipline.md).

## Kinds

The target decides the kind, and the kind decides the rules file every writer and verifier prompt carries.

| Kind | Target | Rules |
|---|---|---|
| Definition | a general concept: a definitions table row, a formalism construct, a type or property note | [references/glossing.md](references/glossing.md), with Form and Vocabulary below |
| Description | an individual, one named thing: the `comment` of a Software, Person, Organization or Exogram note | [references/describing.md](references/describing.md) |
| Abstract | the `abstract` of a note | [references/abstracting.md](references/abstracting.md) |

A note that names one thing is an individual; a note whose type is Type or Property names a class. An abstract is written after its description is accepted, and its writers get that description.

## Form of a definition

A definition gloss is the bare definiens: no defined name, no copula, lowercase, no final period, one sentence worth of content. It gives what the thing means in the system: genus first, then only the characteristics that part it from its siblings; a formula part enters only when it delimits, named by what it stands for, never by its type or mechanics. The genus is a defined superordinate of the target; an empty head noun such as "structure of" or "a type of" is a categorizer, not a genus, and a name with no defined superordinate is a top term, glossed as an elucidation with no forced genus. A role clause may follow, and it claims no job the target does not state: it traces to a rule or remark of the target, and the verifier checks it there.

## Vocabulary of a definition

A definition draws its content words from the target's defined terms, each in its defined sense, plus plain words. A defined term is a definiendum: a name a definition line binds. A word the target's prose merely uses carries no license, so a prose echo sanctions nothing; every other word must pass the plain test on its own, plainer than the name being glossed, in its ordinary English sense. The defined terms are read at ground time from the target's definition sites, the places the system binds names: a formalism's definition lines, a spec's defined-terms section, an ontology's type and property notes. A derived table is not a source; when a copy disagrees with its source, the verifier reports the divergence. When a load-bearing word of the target's own prose fails the plain test, the verifier reports it as a canon finding beside the divergences; that word's fix belongs at its source, never in the gloss.

Banned in every kind: the glossed name inside its own definition or description, its derivatives, its aliases, the target's deprecated names; "any"; deictics and generalizers such as "this", "there", "usually", "etc.", "such as"; "refers to", "denotes", "a term for"; negatives where a positive works; operators, expressions, metaphors.

## Process

Steps 1 and 2 run once per target; a rejection reruns from step 3 on the same files, a remark on the grounding from step 1.

1. Ground. Read the target from disk now, never from conversation memory; files change mid-session, and a gloss is checked against what the target says today. For a definition, read the definitions, the definition sites, and the target's style rules. For a description or an abstract, read whole the note, its repository README, the note of the target property, and every note whose `subject` or `hasOutput` lists the individual, since they say how it works, except the interview ledger, which is read live; of every other note that links the individual, read the frontmatter and every line that links it, with two lines around it; of every note it links, read only the frontmatter. Find the links with `rg -n -C2 <note id> -g '*.md'` from the exogram workspace root. Read also the Claude Code sessions of the workspace from the last month whose user messages name the individual, found with `rg -l` in its transcript folder under `~/.config/claude/projects/`: the user messages that name it and the replies they answer, quoted with the session id, since decisions live there before they reach a note. Snapshot those files whole, verbatim, with line numbers, into one grounding file in the scratchpad, written once and later only appended to: every prompt names it first and the agent reads it, so all agents see one state of the files and no prompt retypes them.
2. Map. For a description or an abstract only. When the notes do not say what the individual is, or contradict each other on it, interview the user first by [references/interviewing.md](references/interviewing.md); the accepted answers join the grounding, and the map is then built as below. A map the user gives fixes the terms, not their understanding: one fresh `general-purpose` agent per term, all spawned in one message and each given the grounding file and the map, first learns on the web, sending its searches and fetches in parallel, what the term means in general, in its field, as an expert knows it: what such a thing is and does, how it works, known instances, and the neighbouring terms it is told apart from; only then how it holds of the individual and how it relates there to the other terms of the map. Show their results with each contradiction found in the notes; the user corrects them, and they go to an understanding file beside the grounding file. Otherwise fresh `general-purpose` agents, given the grounding file and the describing rules, build the concept map of the individual by the rules' Concept map section, every term verified on the web. Show the map as its property tree only, one term per line, drawn with `├─`, `└─` and `│`, no gloss beside a term, the tables left in the map file; the user corrects and accepts it. The accepted map joins the grounding file verbatim, and the user picks the genus from its class terms and the differentiae from its property tree.
3. Write. One fresh `writing:prose-writer` per target returns three candidates. Its prompt names the map and the understanding file when there is one, else the grounding file, and the rules file of the kind, then holds the Banned line above and every rejection verbatim under `Rejected`.
4. Show. Candidates verbatim, labelled A, B and C, then the question. Nothing else: no take, no recommendation, no option of your own, no reworded candidate. The user picks, combines, or rejects. A combination goes to one fresh writer and comes back for a yes or no; a rejection and its reason carry into every later prompt; a remark on the process or the grounding is acted on there and never reaches a writer.
5. Check. Only when the user asks for it, since their pick is the verdict: one fresh `general-purpose` verifier, given no conversation and no brief, reads the same grounding file and runs the checks of the kind's rules file on the picked candidate only, opening every source it cites. Show the results; a failed check goes back to the user with the candidate.
6. Apply. `Edit` only, after an explicit yes; realign a table; run `just validate <file>` on an edited note; never write into the file before acceptance.
