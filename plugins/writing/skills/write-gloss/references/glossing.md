# Glossing rules

Sourced rules for one-line glosses of formally defined things, distilled from five traditions: ISO terminology standards, learner lexicography, ontology textual definitions, mathematical writing, and technical glossaries.

## Form

- the bare definiens: never the defined term, never the copula; one logically unitary fragment (Seppälä/Ruttenberg/Smith, guideline 1)
- lowercase, no final period, no opening article without a reason (ISO 10241)
- same grammatical form as the name: a noun gets a noun phrase, a predicate a claim (ISO 10241, 5.2.5)
- one concept per gloss; a name with two senses gets two entries (ISO 10241, 6.2.2)
- one typographic and phrasing convention across all glosses of a document (Seppälä, guideline 1.1)

## Content

- genus first: the nearest defined superordinate in the system, a single singular noun (ISO 704; Seppälä, 3.1); an empty head noun such as "a type of", "a kind of", "a structure of" is a categorizer, not a genus (Seppälä, 3.1.4)
- a name with no defined superordinate is a top term: an elucidation with examples in place of a forced genus (OBO principle 6)
- then the delimiting characteristics only: the minimal set that parts the thing from its siblings; minimum information outranks full transliteration, so a formula part or side condition enters the gloss only when it delimits (ISO 704 minimum information)
- within that set, a faithful reading of what each part stands for, drawn from the target's remarks and pictures where the formula is silent; never a vague paraphrase, never a transliteration of the type (ISO 704 substitution principle; Knuth, rule 11)
- a role clause, when the house wants one, states the job a named rule or remark of the target gives the thing, and cites that site; the traditions themselves route role to notes fields (ISO 10241) or a separate informal layer (Steenrod), so an uncited role is not a gloss, it is drift
- defines the thing, never the word: no "refers to", "denotes", "a term for" (Wikipedia MOS:REFERS; Seppälä, 4)
- necessary conditions, jointly sufficient where possible; what cannot be a necessary condition goes to a note or example, never into the gloss (Seppälä, 5)
- exactly true to the current formal definition: the gloss and the formula convey the same content, since readers classify by the text and tools by the logic (Seppälä, 11; OBO principle 6)
- a primitive gets an elucidation and examples instead of a definition (OBO principle 6)

## Vocabulary

- closed: content words are the system's defined terms, each in its defined sense (ISO 704 closure; Seppälä, 2 and 6.2), plus plain words, each plainer and more familiar than the name being glossed, in its ordinary English sense (Landau); plainness is the verifier's judgment, no enumerated list
- a defined term is a definiendum, a name a definition line binds; a word the target's prose merely uses carries no license, so a prose echo never sanctions a word the plain test rejects
- the defined terms are read from the target's definition sites at ground time; a derived table is a copy, not a source
- each symbol has one fixed verbal translation, used everywhere (Halmos, sec. 16)
- bound variable names stay out: "every continuous function is bounded", not "f is bounded" (Halmos, sec. 15)

## Banned

- the glossed name, its synonyms, its derivatives, its aliases, the target's deprecated names, and mutual definition loops (Wiktionary; Seppälä, 2)
- "any": it flips between every and some (Halmos, sec. 13)
- deictics and generalizers: "this", "there", "today", "etc.", "such as", "usually" (Seppälä, 9.1-9.4)
- negatives where a positive works (ISO 704, 6.5; Seppälä, 5.2)
- operators, expressions, metaphors

## Checks

Each candidate, run by a fresh verifier that reads only the definition sites, the candidate, and this list:

1. Substitution: the gloss stands in for the name in a real sentence of the target and the sentence keeps its meaning (ISO 704 substitution principle)
2. Circularity: the candidate holds neither the name nor a derivative, synonym, or alias, and closes no mutual loop (Landau; Wiktionary)
3. Closure: every content word is a definiendum of the target in its defined sense or a plain word plainer than the name in its ordinary English sense; an echo of the target's prose sanctions nothing; no banned word appears; the per-name ban entries are the name, its derivatives, its aliases, and the target's deprecated names; a load-bearing word of the target's own prose that fails the plain test is reported as a canon finding beside the divergences
4. Scope: against the formula, neither too broad nor too narrow, conditions jointly satisfiable; a gloss that matches the extension but names no part by what it stands for fails; every clause delimits, and a clause that parts the thing from no sibling is surplus and fails; a role clause agrees with the site it cites and with every sibling definition, and a conflict with the canon is reported as such, not passed (ISO 704, 6.5; Seppälä, 5.3, 6.1, 8, 11)
5. Read-aloud: spoken, the gloss runs smoothly and forces no symbol; a stumble fails (Halmos; Open University)

## Sources

- ISO 704, Terminology work, principles and methods: https://htaglossary.net/Extraits%20des%20normes%20ISO%2010241%20et%20704
- ISO 10241, terminological entries, same extract page as above
- Pavel and Nolet, Handbook of Terminology: https://publications.gc.ca/collections/collection_2007/pwgsc-tpsgc/S53-28-2001E.pdf
- Seppälä, Ruttenberg, Smith, Guidelines for writing definitions in ontologies: https://revista.ibict.br/ciinf/article/view/4015
- OBO Foundry, principle 6, textual definitions: https://obofoundry.org/principles/fp-006-textual-definitions.html
- Landau, Dictionaries: The Art and Craft of Lexicography, per https://linguistlist.org/issues/12/2156/
- Rundell, More than One Way to Skin a Cat (Euralex 2006): https://euralex.org/elx_proceedings/Euralex2006/040_2006_V1_Michael%20RUNDELL_More%20than%20one%20Way%20to%20Skin%20a%20Cat_Why%20Full_Sentence%20Definitions%20Have%20not%20been.pdf
- Halmos, How to Write Mathematics: https://i11www.iti.kit.edu/~awolff/lehre/scientific_writing/h-hwm-70.pdf
- Knuth, Larrabee, Roberts, Mathematical Writing: https://www.phys.uconn.edu/~rozman/Courses/P2400_14S/downloads/knuth_mathematical_writing.pdf
- Wikipedia, MOS:REFERS: https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Lead_section
- Wiktionary, Help:Writing definitions: https://en.wiktionary.org/wiki/Help:Writing_definitions
- Open University, Language, notation and formulas: https://www.open.edu/openlearn/science-maths-technology/mathematics-statistics/language-notation-and-formulas/content-section-2.1
