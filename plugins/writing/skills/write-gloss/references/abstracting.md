# Abstracting rules

Sourced rules for the abstract of a resource: the summary a reader gets before deciding whether the thing is for them. In an exogram the abstract is the `abstract` of the note, `dcterms:abstract`, "A summary of the resource".

## Form

- two to four full sentences (DOAP, `description`; Debian, 6.2.4)
- plain English for a reader who has never met the thing (Wikipedia, MOS:FIRST; Debian Policy, 3.4)

## Content, in this order

1. What it is: the first sentence names the thing and gives its description as a sentence, "<Name> is a <description>", with no other load (Wikipedia, MOS:FIRST: "tell the nonspecialist reader what or who the subject is", "Do not overload the first sentence")
2. What it does and what task it helps the reader accomplish (Debian, 6.2.4)
3. Where it sits: how it relates to the rest of its system, or how it differs from the alternatives, when the reader needs that to decide (Debian Policy, 3.4.2; Debian, 6.2.4)
4. Status, last and only when it limits use, e.g. that it does not run yet (Debian, 6.2.4: "If the package is experimental … it should be here as well")

## Banned

- instructions for installing, configuring or using: no commands, no recipes, no invocations (Debian Policy, 3.4)
- advocacy and evaluation (Debian, 6.2.2)
- the README blurb, the pitch, the problem story, the tagline (Debian Policy, footnote 3)
- a technical term the reader cannot know, unless the abstract introduces it (Debian, 6.2.2)
- an inner term of the thing's own system, a word the reader meets only in its notes

## Checks

Each candidate, run by a fresh verifier that reads the grounding block with the accepted concept map, the accepted description, the candidate, and this list:

1. Opening: the first sentence says what the thing is, agrees with the description, and carries nothing else
2. Task: one sentence answers what the thing does and which task it helps the reader with
3. Truth: every claim traces to the grounding block or a cited source; what exists is told in present tense, what is planned is marked as planned
4. Closure: every technical term is a sourced class term, a canonical proper name, or introduced in the abstract; an inner term of the system fails
5. Banned: no instruction, no command, no advocacy, no blurb, no problem story
6. Status: absent, or last and limiting use
7. Form: two to four full sentences
8. Read-aloud: spoken, it runs smoothly

## Sources

- DCMI Metadata Terms, `abstract`: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- DOAP, `description`, "Plain text description of a project, of 2-4 sentences in length": https://rdflib.readthedocs.io/en/6.2.0/_modules/rdflib/namespace/_DOAP.html
- Debian Policy Manual, 3.4 The description of a package: https://www.debian.org/doc/debian-policy/ch-binary.html
- Debian Developer's Reference, 6.2.4 The long description: https://www.debian.org/doc/manuals/developers-reference/best-pkging-practices
- Wikipedia, Manual of Style, lead section, MOS:FIRST: https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Lead_section
