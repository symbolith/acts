# Describing rules

Sourced rules for the one-line description of an individual: one named thing such as a software, a person, an organization or an exogram. An individual corresponds to only one object, so it gets a description that identifies it, never a definition of a class (ISO 704, individual against general concept). In an exogram the description is the `comment` of the individual's note.

## Concept map

Built before any candidate is written, from the grounding block and the web.

- class terms: the classes the individual is an instance of, with their siblings and the items that share its label
- a property tree with one root, the individual; its first level are sets, each answering one question, ordered so each set builds on the ones before it
- in the property tree every child is a narrower kind of its parent, never a part or a trait of it (W3C SKOS, broader and narrower; ISO 704 and ISO 25964, generic relation)
- a property says what the individual is; for an artifact, a mechanism says how it is achieved and realizes a property; mechanisms form their own tree, in which every child is a part of its parent that passes the ALL/SOME test (ISO 25964, partitive relation), and never sit in the property tree
- left of each entry stands the market term, confirmed when three independent sources of the individual's field use it in that sense, else the field's term or plain words, never a dropped entry; right stands its plain meaning for this individual, with the academic term only as its source
- a marker sets apart what holds only in the planned design, never in what exists

## Form

- a noun phrase, never a full sentence (Wikidata; Debian, 6.2.3)
- never the name of the individual (Debian Policy, 3.4.1)
- the form the note of the target property sets, read at ground time
- two to twelve words (Wikidata), under 120 characters (Standard Readme)
- fits the formula "<Name> is <description>" as a true sentence (adapted from Debian, 6.2.3: "The package name provides {a,an,the} synopsis")
- the formula and the read-aloud check test truth and flow only; the line is shown on its own, in the form above

## Content

- head noun: the type the individual is an instance of, in the term practitioners use for that kind of thing, in its canonical form (Debian, 6.2.2); for software, the class term of the field, checked against a source: SEVOCAB, a Wikipedia article, a Wikidata class, or the documentation of the field
- each root of the accepted map lends at least one term, itself or a narrower one
- a map term is said of the individual itself, never recast as its user, its actor, its part or its object
- for an artifact such as a software, its function as a verb phrase, what it does to what, never its make-up and never only its users, "for <someone>"; agency stays where the grounding puts it, so a tool its users act through is never made the doer of their work (Debian Policy, 3.4.2: "describe what the package does"; Debian, 6.2.4: "what task does it help the user accomplish?")
- then the most specific information that parts the individual from the things that share its label, from its siblings of the same type, and from the known instances of its classes in the field, most specific first; what none of those instances has is the point of the line (Wikidata)
- informative on its own: the reader may see this line and nothing else (Debian Policy, 3.4.1)
- free of controversy and bias: no evaluation, no advocacy (Wikidata; Debian, 6.2.2)
- nothing that will change: no status such as "planned", "not yet", "current", "today", no version (Wikidata, on individuals)
- no problem story, no promise, no tagline, no README blurb (Debian Policy, footnote 3)

## Vocabulary

- content words are class terms with a source, proper names of related individuals in their canonical form, and plain words (Debian, 6.2.2); with a map the user gives, content words are its terms and plain words only
- a term of the individual's own system enters only when it is the name of a related individual the reader can look up; an inner term of the system, a word the reader meets only in its notes, never enters
- a word taken from the grounding material carries no license on its own: it passes only as a sourced class term, a canonical proper name, or a plain word

## Checks

Each candidate, run by a fresh verifier that reads the grounding block with the accepted concept map, the candidate, and this list:

1. Formula: "<Name> is <description>" reads as a true sentence about the individual
2. Sourced type: the head noun is a class term whose source the verifier opens, and the individual falls under that source's definition
3. Disambiguation: the description fits this individual and none of its siblings, none of the same-label items the concept map lists, and none of the known instances of its classes
4. Function: for an artifact, the description states what it is used to do; a description of its make-up fails, and so does one that names only its users or makes it the doer of their work
5. Closure: every content word is a sourced class term, a canonical proper name, or a plain word; an inner term of the system fails; a root of the accepted map that lends no term fails
6. Stability: no status, no version, no word that dates
7. Neutrality: no evaluation, no advocacy, no problem story, no tagline
8. Form: a noun phrase without the name, in the form the target property's note sets, two to twelve words, under 120 characters
9. Read-aloud: spoken after the name and "is", the line runs smoothly

## Sources

- ISO 704, individual and general concepts, as quoted in: https://arxiv.org/pdf/1609.05170
- Wikidata, Help:Description: https://www.wikidata.org/wiki/Help:Description
- Debian Policy Manual, 3.4 The description of a package: https://www.debian.org/doc/debian-policy/ch-binary.html
- Debian Developer's Reference, 6.2 Best practices for package descriptions: https://www.debian.org/doc/manuals/developers-reference/best-pkging-practices
- DOAP, `shortdesc`, "Short (8 or 9 words) plain text description of a project": https://rdflib.readthedocs.io/en/6.2.0/_modules/rdflib/namespace/_DOAP.html
- Standard Readme, short description: https://github.com/RichardLitt/standard-readme/blob/main/spec.md
- SEVOCAB, ISO/IEC/IEEE 24765 systems and software engineering vocabulary: https://pascal.computer.org/sev_display/help.jsp
- W3C SKOS Reference, semantic relations broader and narrower: https://www.w3.org/TR/skos-reference/
- ISO 25964-1, hierarchical relationships: generic, whole-part, instance: https://link.springer.com/article/10.1007/s00799-015-0162-2
