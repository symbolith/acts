---
name: write-gloss
description: Write the one-line gloss of a formally defined thing (a definitions table row, a formalism construct, an ontology term) with clean-context writers and fresh verifiers running sourced checks. Use when the user asks to "write a gloss", "gloss this", "fix a gloss", "the gloss needs work", "rewrite the glosses", or rejects a gloss.
argument-hint: <note path and the names to gloss>
allowed-tools: Agent, AskUserQuestion, Read, Edit, Grep, Glob
---

# Write a gloss

Gloss the names in `$ARGUMENTS` by the process below.

You orchestrate and never touch the text: writers draft in fresh contexts, verifiers check in fresh contexts, you relay both verbatim. Mechanical reshaping of a candidate, down to stripping a copula, is a writer's job, not yours. This skill belongs to the write-prose family; the shared discipline is [../write-prose/references/discipline.md](../write-prose/references/discipline.md).

## Form

A gloss is the bare definiens: no defined name, no copula, lowercase, no final period, one sentence worth of content. It gives what the thing means in the system: genus first, then only the characteristics that part it from its siblings; a formula part enters only when it delimits, named by what it stands for, never by its type or mechanics. The genus is a defined superordinate of the target; an empty head noun such as "structure of" or "a type of" is a categorizer, not a genus, and a name with no defined superordinate is a top term, glossed as an elucidation with no forced genus. A role clause may follow, and it claims no job the target does not state: it traces to a rule or remark of the target, and the verifier checks it there. The full rules with their sources are in [references/glossing.md](references/glossing.md); every writer and verifier prompt carries them.

## Vocabulary

A gloss draws its content words from the target's defined terms, each in its defined sense, plus plain words. A defined term is a definiendum: a name a definition line binds. A word the target's prose merely uses carries no license, so a prose echo sanctions nothing; every other word must pass the plain test on its own, plainer than the name being glossed, in its ordinary English sense. The defined terms are read at ground time from the target's definition sites, the places the system binds names: a formalism's definition lines, a spec's defined-terms section, an ontology's type and property notes. A derived table is not a source; when a copy disagrees with its source, the verifier reports the divergence. When a load-bearing word of the target's own prose fails the plain test, the verifier reports it as a canon finding beside the divergences; that word's fix belongs at its source, never in the gloss.

Banned everywhere: the glossed name, its derivatives, its aliases, the target's deprecated names; "any"; deictics and generalizers such as "this", "there", "usually", "etc.", "such as"; "refers to", "denotes", "a term for"; negatives where a positive works; operators, expressions, metaphors.

## Process, each round

1. Ground. Read the definitions, the definition sites, and the target's style rules from disk now, never from conversation memory; files change mid-session, and a gloss is checked against what the target says today. Snapshot those files whole, verbatim, with line numbers, into one grounding block: every prompt of the round opens with that identical block, so all agents share one prompt-cache prefix and see one state of the files. A file too large to paste stays a site the agent reads itself.
2. Write. One fresh `writing:prose-writer` per name returns three candidates. Its prompt opens with the grounding block, then holds the form and vocabulary rules and every rejection verbatim under `Rejected`.
3. Check. One fresh verifier per name, given no conversation and no brief, opens with the same grounding block and runs the five checks of the reference on each candidate: substitution, circularity, closure, scope, read-aloud.
4. Show. Candidates verbatim, labelled A, B and C, each with its check results, no ranking. The user picks, combines, or rejects. A combination goes to one fresh writer and comes back for a yes or no; a rejection and its reason carry into every later prompt.
5. Apply. `Edit` only, after an explicit yes; realign the table; never write into the file before acceptance.
