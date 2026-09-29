# Naming Reference

Derive a name by the process in section 1, test it against section 2, and settle the field's term by section 3.
Every rule cites its source; section 4 lists the sources with URLs.

## 1. Process

1. Fix the subject field and the kind of thing to name: predicate, function, set, element, type, value, action, or relation. [Karsch, doublettes; Google C++]
2. In a formal text, lay out the whole alphabet before writing, never mid-sentence. [Halmos 1970, Sec. 5]
3. Write the concept before its name: the nearest generic concept and the characteristic that parts it from its siblings. [Karsch, doublettes; ISO 1087, 3.3.2; Halmos 1970, Sec. 10]
4. List the concepts the name must carry: what the thing holds, what it is for, and a kind qualifier where confusion looms. [Feitelson 2021, step 1]
5. Search the field's reference works (its standard, survey, textbook, W3C document, or language style guide) for the established term before coining one. [Halmos 1970, Sec. 14; Steenrod 1973; Noy and McGuinness, step 2; Pavel and Nolet 2001]
6. Record every variant found, one row per concept and one column per work, and mark which work is the standard. [Pavel and Nolet 2001; OMG MVF]
7. Check the document's or codebase's own lexicon for a word already bound to the concept and reuse it. [Feitelson 2021, step 2; Hilton and Hermans 2017, 7.6; Knuth 1989; Lamport 2002]
8. If no term exists, pick one dictionary word per concept, no synonym, and mark a finer distinction with an added word. [Feitelson 2021, step 2; Hilton and Hermans 2017, 6.3; Valeontis and Mantzari 2006; Pavel and Nolet 2001]
9. Order the words by the grammar of the kind: verb phrase for an action, noun phrase for a function result, singular noun for a set or type, adjective before noun. [Feitelson 2021, step 3; Lamport 2002; Lamport 2012; Hilton and Hermans 2017, 9.1, 10.1]
10. Apply the target's casing and separator convention for that kind. [Google JS, 6.3; Noy and McGuinness; OBO FP-012]
11. When a thing has no name yet, extract it under an obvious placeholder, then rename it to one true thing it does, marking doubt with `probably_` and gaps with `_AndStuff`. [Belshee, Obvious Nonsense; Belshee, Honest]
12. Test the name for honesty by asking whether a reader could regenerate everything the thing does from the name alone, and add each missing clause. [Belshee, Completely Honest; Samman]
13. If the honest name still holds a clause that can be split off, split the thing, not the name. [Belshee, Does the Right Thing]
14. Rename to intent: say why the caller cares, not what the code does or when it runs. [Belshee, Intent Revealing; Feitelson 2021, step 1]
15. Look for a domain concept behind shared prefixes, paired methods, or narrowing names on generic types, and extract it as its own type. [Belshee, Domain Abstraction]
16. Run the checklist in section 2 and rename on any no. [Karsch, ISO 704 questions; Hilton and Hermans 2017]
17. Define the name at first use, keep dropped variants as synonyms, and rate rejected ones deprecated. [Knuth 1989; OBO FP-012; ISO 704:2022, 7.7.7]
18. Strike any symbol used once and referenced nowhere. [Halmos 1970, Sec. 15; Knuth 1989]

## 2. Criteria

Answer each question. A no means rename.

### Form

- Predicate. Does the name assert something a reader can judge true or false, in positive form, with the field's convention on an `Is` prefix (`IsIncreasingOn`; `done`, `found`, not `isValid`)? [Lamport 2012; Hilton and Hermans 2017, 8.1, 8.6, 8.7; .NET members]
- Function. Is a pure function or operator named by a noun phrase for its result and kept apart from its value (`the function f defined by f(z)`, `AbsoluteValue(a)`, `units()` not `getUnits()`)? [Halmos 1970; Lamport 2012; Henney; Hilton and Hermans 2017, 10.1]
- Set. Is a set a singular noun (`Message`, `PositiveReal`, `SetOfIntervals`) so `m ∈ Message` reads "m is a Message", uppercase in mathematics? [Lamport 2002; Lamport 2012; Knuth 1989, 14]
- Element. Is an element lowercase, singular, named only when needed, and, as a variable, named by how this instance differs from others of its type? [Knuth 1989, 14, 15; Hilton and Hermans 2017, 8.2; Belshee, Intent Revealing]
- Collection. Is a collection a plural or a collective noun (`calendar`, `harvest`), never singular plus `List`? [Hilton and Hermans 2017, 8.3, 8.4; .NET members]
- Type. Is a class or type a singular noun phrase that completes "This class' constructor returns a new ...", allows all its states, with interfaces as adjective phrases? [Hilton and Hermans 2017, 9.1, 9.2; .NET classes; Ambler; Lamport 2002]
- Value. Is a constant named by its concept, not its number (`pi`, not `ONEHUNDRED`), with qualifiers as suffixes (`APPLE_COUNT_MINIMUM`), and a property or attribute a noun, noun phrase, or adjective? [Hilton and Hermans 2017, 6.6, 6.11; .NET members; Open Data Support]
- Action. Is a method with effects an active verb phrase with a strong verb, and does any `get`, `is`, `has`, `set`, `validate`, or `convert` prefix match the behaviour it promises? [Hilton and Hermans 2017, 10.1 to 10.8; .NET members; Ambler; Henney]
- Relation. Does an object property read as a verb sense so the triple reads as a sentence, or, in ER, as a preposition in "Each A must be <relation> one B"? [W3C LD-BP; Open Data Support; metaphacts; Hay on Barker]
- Subclass. Does a subclass name show its differentia from the parent, and do all siblings include or all omit the parent's name? [Schober 2009, 3.2; Noy and McGuinness]
- Proof step. Does every step, assumption, and reused expression carry a name, defined before use (`<3>4`, `Assumption 1.2`, `let ... in`)? [Lamport 1993; Lamport 1994; Lamport 2012]

### Meaning

- Transparency. Can a reader tell what the concept is from the term alone? [Karsch, ISO 704 questions, 7.3.2; Pavel and Nolet 2001; Belshee]
- Intent. Does the name say what the thing is for and why the caller cares, not when it runs or how it works? [Belshee, Intent Revealing; Feitelson 2021, step 1]
- Completeness. Could a reader regenerate everything the thing does from the name, nothing more and nothing less? [Belshee, Completely Honest; Samman]
- One concept, one name. Is the concept written the same way at every occurrence, by every author, in every module? [Knuth 1989, 14; Hilton and Hermans 2017, 7.6; Lamport 2002; ISO 704:2022, 7.7.1; Schober 2009, 3.1]
- One name, one concept. Does the name mean the same thing at every use, with no homonym in the field or the codebase (`∈` never doubles as `ε`)? [Knuth 1989, 14; Schober 2009, 2.1; ISO 704:2022, 7.7.1; Halmos 1970]
- Words, not letters. Is the concept named by descriptive words, not a letter, a formula, or a person (`commutator`, `closed graph theorem`; not `property L`, `K-theory`)? [Halmos 1970, Sec. 19; Steenrod 1973]
- Precision. Is every word right for this thing only, with no placeholder (`foo`, `temp`, `data`) and no catch-all? [Hilton and Hermans 2017, 7.1, 7.2; Schober 2009, 2.5]
- Single concern. Does the name join no two concerns with `and` or `or`? [Belshee, Does the Right Thing; Schober 2009, 2.2]
- Positive. Is the name free of negation? [Hilton and Hermans 2017, 8.7; Schober 2009, 2.4]
- Comment test. If the thing would need a comment, is the comment's wording in the name? [Feitelson 2021]
- Qualifier. Where two things of one type could be confused, does the name carry the dimension or safety qualifier (horizontal, unsafe user input)? [Feitelson 2021]
- No metadata. Is the name free of status, version, and representational words? [Schober 2009, 1.3, 1.4]
- Context free. Does the name explain itself outside its parent's context? [Schober 2009, 1.2; OBO FP-012]

### Fit

- Field term. Is this the term the field's standard, survey, or textbook uses for the concept? [Karsch, ISO 704 questions, 7.3.3; Halmos 1970, Sec. 14; Ambler; Ed-Fi]
- Field pattern. Does the term follow the field's formation pattern for its kind (deverbal noun for a procedure, deadjectival noun for a property, the same ending as its coordinate species)? [Valeontis and Mantzari 2006]
- Own lexicon. Does the name use the document's or codebase's own word for the concept, and not a synonym? [Feitelson 2021, step 2; Hilton and Hermans 2017, 7.6; Knuth 1989]
- Reuse first. Was an existing term from a shared vocabulary or module reused before a new one was minted? [Noy and McGuinness, step 2; Open Data Support; Lamport 2002]
- Convention. Does the style of the name announce its kind under the target's convention (case, separator, prefix)? [Google C++; Hilton and Hermans 2017, 6.1; Noy and McGuinness; OBO FP-012; ISO/TC 211, R11]
- Frozen letters. Does a symbol respect the field's frozen letters (`e`, `i`, `π`; `n` not complex) and freeze no new ones? [Halmos 1970, Sec. 5]
- Index roles. Do index letters keep fixed roles throughout (`i` over 1..m, `j` over 1..n)? [Knuth 1989, 14]
- Definition. Is the term defined at or before first use, and in a vocabulary given a label, a definition, and a comment? [Knuth 1989; Lamport 1994; W3C LD-BP]

### Economy

- Short. Is the name as short as possible without arbitrary abbreviation, within four words and twenty characters in code? [Karsch, ISO 704 questions, 7.3.5; Hilton and Hermans 2017, 6.9, 6.10; Pavel and Nolet 2001]
- No filler. Does anything remain once `Manager`, `Object`, `Service`, `get`, `do`, `check`, `Exception` and their kin are stripped? [Henney; Hilton and Hermans 2017, 7.3]
- Full words. Is every word a correctly spelled dictionary word, except `id` and documented domain abbreviations, with no letters dropped inside a word? [Hilton and Hermans 2017, 6.3; Google C++; Google JS; .NET general; Schober 2009, 3.4; Noy and McGuinness]
- Pronounceable. Can the name be read aloud and told from its neighbours by ear? [Feitelson 2021; Hilton and Hermans 2017, 7.10; Pavel and Nolet 2001]
- Distinct. Does the name differ from every neighbour by more than one or two letters, word order, or a synonym, with no alphabetical dissonance (`ax1 + bx2`)? [Hilton and Hermans 2017, 7.7 to 7.9; Knuth 1989; Halmos 1970, Sec. 5]
- Memorable. Is the name easy to retain? [Feitelson 2021; Pavel and Nolet 2001]
- Earned. Is the symbol or label used more than once and referenced later? [Halmos 1970, Sec. 15; Knuth 1989]
- Symbol budget. Are nonstandard global symbols held to about five, with an index of notation at ten? [Steenrod 1973]
- No type noise. Is the name free of Hungarian prefixes, type words, and the strings `class`, `property`, `slot`? [Hilton and Hermans 2017, 8.1; Google Python; .NET general; Noy and McGuinness]
- Unique. Is the name unique in its namespace, with no shadowing? [Hilton and Hermans 2017, 6.12; ISO/TC 211, R16; OBO FP-012]
- Scope. Is descriptiveness scaled to scope, with single letters only in a block of ten lines or less or in cited mathematics? [Google Python; Google JS]
- Domain word. Does one domain word replace a phrase (`calendar` for `appointment_list`, `employee` for `company_person`)? [Hilton and Hermans 2017, 7.5; Hilton, smells]

### Correctness

- Linguistic. Does the name follow the language's morphological, syntactic, and phonological norms? [Karsch, ISO 704 questions, 7.3.7]
- Word order. Do adjectives precede nouns and does the phrase read in natural order (`HorizontalAlignment`, `max_points`)? [Feitelson 2021, step 3; .NET general]
- Derivability. Can compounds and derivatives be formed from it (`email`, `emails`, `emailing`)? [Karsch, ISO 704 questions, 7.3.6; Valeontis and Mantzari 2006; Pavel and Nolet 2001]
- Native. Is the word native, not a borrowing or jargon where an everyday word exists? [Karsch, ISO 704 questions, 7.3.8; Hilton, slides]
- Connotation. Are the connotations the term evokes intended? [Karsch, ISO 704 questions, 7.3.4]
- Pairs. Are opposites drawn from standard pairs (`add`/`remove`, `begin`/`end`, `open`/`close`)? [Hilton and Hermans 2017, 8.5]
- Plain text. Is the name plain ASCII with no subscripts, superscripts, or accents? [Schober 2009, 4.2]
- No blend. Is the term free of blends that hide the concept's characteristics? [Valeontis and Mantzari 2006]
- Reading. Does each symbol keep one verbal reading, and does no sentence start with a symbol? [Halmos 1970, Sec. 16; Knuth 1989]

## 3. Finding the field's term

Search online. Never take the term from memory.

Reference works by field kind:

- A formal model with a standard (Petri nets, UML, geographic schemas): the ISO/IEC or OMG standard. ISO documents number their terms in clause 3, Terms and definitions, and define the concepts later in order (ISO/IEC 15909-1 clause 3, then Concepts 1 to 32 in clause 5). The free iTeh sample PDF carries the scope, the table of contents, and clause 3. [ISO 15909-1; ISO 1087]
- A field with a canonical survey: the survey's interpretation table, its definition tuple, and its named rules (Murata's Table 1, Table 2, transition (firing) rule, dot notation). [Murata 1989]
- A field taught from lecture notes or a textbook: the definitions of the opening section (net, pre-set, occurrence rule). [Desel and Reisig 1998]
- A web vocabulary or ontology: the W3C Recommendation or Working Group Note, the working group wiki, the OBO Foundry principle, and the vocabulary's own rdfs:label, definition, and comment. [W3C LD-BP; W3C RIF; OBO FP-012]
- A programming language: the naming section of the language's style guide. [Google C++; Google JS; Google Python; .NET general]
- A term with no field of its own: the ISO 704 formation principles, a terminology database, a dictionary, a thesaurus, and a few experts. [Karsch, ISO 704 questions; Pavel and Nolet 2001; Steenrod 1973; Halmos 1970, Sec. 14]

Search recipe:

1. Query `<field> terms and definitions` and `<field> ISO` or `<field> OMG` to find the standard; open the sample PDF; read clause 3.
2. Query `<field> survey` and `<field> lecture notes` to find the survey and the textbook; read their definition tables.
3. Query `"<candidate word>" "<field>"` to see whether the word is in use and with which meaning.
4. For a vocabulary, query `<vocabulary> naming conventions` and open the namespace document.
5. For a language, query `<language> style guide naming`.

Recording variants:

- One table per sweep: a row per concept, a column per work.
- A cell holds the exact term, its symbol, and the clause, section, or table it comes from.
- Write `none` when a work has no name for the concept, and note what it uses instead.
- Note where one work uses two words for one concept (ISO/IEC 15909-1 titles the rule "firing" but phrases reachability by "occurrence").
- Rate the standard's term preferred and the others admitted, and keep them as synonyms on the record. [ISO 704:2022, 7.7.7; OMG MVF; OBO FP-012; Pavel and Nolet 2001]

### Example: Petri nets

| Concept | ISO/IEC 15909-1:2019 (15909-3 for arcs) | Murata 1989 | Desel and Reisig 1998 |
|---|---|---|---|
| places before and after a transition | precondition, postcondition of a transition (Concepts 4, 5); input place, output place (3.13, 3.22) | `•t` input places of t, `t•` output places of t (Sec. V) | pre-set `•x`, post-set `x•` |
| a transition acts | fire (net firing rule, Concept 7); occurrence in reachability (3.30, 3.31) | fire, firing (transition (firing) rule) | occur (occurrence rule) |
| the set of places | `P` (Concept 1) | `P` (Table 2) | `S` |
| arc that tests tokens without taking them | read arc (15909-3, 3.5) | none; a self-loop plays the role; inhibitor arc for the negative test | none; a place in `•t ∩ t•` |
| a run | not in the sample pages; "transition occurrences" (3.30) | firing or occurrence sequence `σ` | occurrence sequence; causal net or process net when concurrent |

Pick: precondition, fire, `P`, read arc, occurrence sequence; the standard's word where it names the concept, else the survey's.
Record pre-set, occur, `S` as admitted.

### Example: RDF vocabularies

Rows drawn from the convention sources in section 4.

| Concept | W3C RIF wiki | Open Data Support | metaphacts | Noy and McGuinness | OBO FP-012 |
|---|---|---|---|---|---|
| class name | noun phrase, capital initial | capital initial, singular (`skos:Concept`) | singular capitalized noun | capital common; singular or plural, but one throughout | plain English, lower-case start, proper names capitalized |
| object property (relation) | noun phrase, lower initial; reads "<instance> has <property> <value>" | verb (`org:hasSite`) | verb or verb phrase (`manages`) | prefix `has` or suffix `of` | none |
| datatype property (attribute) | noun phrase, singular even with cardinality above one | noun (`dcterms:description`) | lower-case noun (`birth date`) | lower case | none |
| word separator | CamelCase as in Java | camel case (`foaf:isPrimaryTopicOf`) | spaces or camelCase, one throughout | one of space, CamelCase, underscore, dash | spaces; no CamelCase, no underscores |
| abbreviation | whole words unless the short form is better known (`XML`) | none | none | avoid (`Cabernet Sauvignon`, not `Cab`) | spell out; short form as synonym |

W3C LD-BP adds: object properties as verb senses (`hasProperty`); every term carries a label, a definition, and a comment.
No single work governs here, and the W3C wiki and OBO disagree on separators.
Pick the convention of the target namespace and hold to it throughout. [Noy and McGuinness]

## 4. Sources

Reading notes:

- ISO 704 body text is paywalled; its principle wording here follows Karsch's question form and Valeontis and Mantzari's restatement, with clause numbers from the 2000 table of contents and 7.7.x from the 2022 table of contents.
- Steenrod was read through a summarizing fetch, not a scan.
- Belshee was read from the Deep Roots republication, not the original series.
- Google C++ was read from a mirror of an older revision.
- Henney was read from slides and third-party talk notes.
- Feitelson was read from the arXiv preprint, not the TSE version.
- Desel and Reisig was read up to the definition of conditions and events.

List:

- Halmos 1970. Paul R. Halmos, How to Write Mathematics, L'Enseignement Mathematique 16. https://www.di.ens.fr/~bouillar/Stages/Halmos-How-To-Write.pdf
- Knuth 1989. Donald E. Knuth, Tracy Larrabee, Paul M. Roberts, Mathematical Writing, MAA Notes 14. https://jmlr.csail.mit.edu/reviewing-papers/knuth_mathematical_writing.pdf
- Lamport 1993. Leslie Lamport, How to Write a Proof. https://lamport.azurewebsites.net/pubs/lamport-how-to-write.pdf
- Lamport 1994. Leslie Lamport, How to Write a Long Formula, Formal Aspects of Computing 6. https://lamport.azurewebsites.net/pubs/lamport-howtowrite.pdf
- Lamport 2002. Leslie Lamport, Specifying Systems, Sec. 4.2 p. 36 and Sec. 11.1.1 p. 171. https://lamport.azurewebsites.net/tla/book-02-08-08.pdf
- Lamport 2012. Leslie Lamport, How to Write a 21st Century Proof, J. Fixed Point Theory Appl. 11. https://lamport.azurewebsites.net/pubs/proof.pdf
- Steenrod 1973. Norman E. Steenrod, How to Write Mathematics, AMS booklet, pp. 1 to 17. https://djvu.online/file/VH9yTkHTk3vBO
- Belshee. Arlo Belshee, Naming as a Process, articles 1 to 8. https://www.digdeeproots.com/articles/on/naming-process/
- Samman. Samman Technical Coaching, Reading by Renaming. https://sammancoaching.org/learning_hours/testable_design/naming.html
- Hilton and Hermans 2017. Peter Hilton, Felienne Hermans, Naming Guidelines for Professional Programmers, PPIG 2017. https://ppig.org/files/2017-PPIG-28th-hilton.pdf
- Hilton, smells. Peter Hilton, Naming smells. https://hilton.org.uk/blog/naming-smells
- Hilton, get better. Peter Hilton, Get better at naming things. https://hilton.org.uk/blog/get-better-at-naming
- Hilton, slides. Peter Hilton, How to name things: the hardest problem in programming. https://www.slideshare.net/slideshow/how-to-name-things-the-hardest-problem-in-programming/39383508
- Hilton, science. Peter Hilton, What science says about naming. https://hilton.org.uk/blog/science-on-naming
- Feitelson 2021. Dror G. Feitelson et al., How Developers Choose Names, IEEE TSE, arXiv 2103.07487. https://arxiv.org/abs/2103.07487
- Henney. Kevlin Henney, Seven Ineffective Coding Habits of Many Programmers, slides. https://www.slideshare.net/slideshow/seven-ineffective-coding-habits-of-many-programmers-45312038/45312038
- Google C++. Google C++ Style Guide, General Naming Rules. https://google.github.io/styleguide/cppguide.html#General_Naming_Rules
- Google JS. Google JavaScript Style Guide, Sec. 6 Naming. https://google.github.io/styleguide/jsguide.html#naming
- Google Python. Google Python Style Guide, Sec. 3.16 Naming. https://google.github.io/styleguide/pyguide.html#316-naming
- .NET general. Cwalina and Abrams, Framework Design Guidelines, General Naming Conventions. https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/general-naming-conventions
- .NET members. Cwalina and Abrams, Names of Type Members. https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/names-of-type-members
- .NET classes. Cwalina and Abrams, Names of Classes, Structs, and Interfaces. https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/names-of-classes-structs-and-interfaces
- ISO 704:2000. Terminology work, Principles and methods, preview with table of contents. https://cdn.standards.iteh.ai/samples/31696/b62b1a16b573494f9d3a8cb84ccd308e/ISO-704-2000.pdf
- ISO 704:2009. Preview with scope and table of contents. https://cdn.standards.iteh.ai/samples/38109/0e99a6f2c8b54a838b0bdd14a73a3412/ISO-704-2009.pdf
- ISO 704:2022. Preview with scope and table of contents. https://cdn.standards.iteh.ai/samples/79077/2dd50250582e4a9fa3420af5da705572/ISO-704-2022.pdf
- Karsch, ISO 704 questions. Barbara Inge Karsch, You say Aaaazure, I say Azuuuure. https://bikterminology.com/you-say-aaaazure-i-say-azuuuure/
- Karsch, doublettes. Barbara Inge Karsch, Avoiding doublettes, report from the ISO/TC 37 meetings. https://bikterminology.wordpress.com/tag/iso-704/
- Valeontis and Mantzari 2006. The Linguistic Dimension of Terminology: Principles and Methods of Term Formation. https://www.eleto.gr/download/BooksAndArticles/HAU-Conference2006-ValeontisMantzari_EN.pdf
- Pavel and Nolet 2001. Silvia Pavel, Diane Nolet, Handbook of Terminology. https://www.kufunda.net/publicdocs/handbook.pdf
- ISO 1087. ISO 1087:2019 Terminology work and terminology science, Vocabulary, preview. https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf
- OMG MVF. OMG, MVF ISO 1087 Vocabulary for Terms and Definitions. https://www.omg.org/spec/MVF/ISO1087-VocabularyForTermsAndDefinitions/
- Schober 2009. Schober et al., Survey-based naming conventions for OBO Foundry ontology development, BMC Bioinformatics 10:125. https://pmc.ncbi.nlm.nih.gov/articles/PMC2684543/
- OBO FP-012. OBO Foundry Principle FP-012: Naming Conventions. https://obofoundry.org/principles/fp-012-naming-conventions.html
- W3C RIF. W3C RIF Working Group, Arch/Naming Conventions. https://www.w3.org/2005/rules/wg/wiki/Arch/Naming_Conventions
- W3C LD-BP. W3C, Best Practices for Publishing Linked Data, Working Group Note. https://www.w3.org/TR/ld-bp/
- Open Data Support. Training module 2.4, Designing and developing vocabularies in RDF, slide 16. https://data.europa.eu/sites/default/files/d2.1.2_training_module_2.4_designing_and_developing_vocabularies_in_rdf_en_edp.pdf
- metaphacts. Semantic knowledge modeling best practices. https://blog.metaphacts.com/semantic-knowledge-modeling-best-practices
- Noy and McGuinness. Ontology Development 101, Sec. 6. https://protege.stanford.edu/publications/ontology_development/ontology101.pdf
- Ambler. Scott W. Ambler, UML Class Diagrams: Diagramming Guidelines. https://agilemodeling.com/style/classdiagram.htm
- ISO/TC 211. Naming of packages, classes and attributes, UML Best Practices wiki. https://github.com/ISO-TC211/UML-Best-Practices/wiki/Naming-of-packages,-classes-and-attributes
- UCT. University of Cape Town, UML notation and conventions. https://www.cs.uct.ac.za/mit_notes/software/htmls/ch05s09.html
- Ed-Fi. Ed-Fi Alliance, UML Notation and Conventions. https://docs.ed-fi.org/reference/data-exchange/udm/uml-notation-and-conventions/
- Hay on Barker. David C. Hay, Richard Barker's ERD notation. https://www.essentialstrategies.com/publications/modeling/barker.htm
- Red Gate. Barker's Notation. https://www.red-gate.com/blog/barkers-erd-notation/
- ISO 15909-1. ISO/IEC 15909-1:2019 High-level Petri nets, Part 1, sample pages. https://cdn.standards.iteh.ai/samples/67235/ee85c618a85a478792bf4321c923174b/ISO-IEC-15909-1-2019.pdf
- ISO 15909-3. ISO/IEC 15909-3:2021 High-level Petri nets, Part 3, sample pages. https://cdn.standards.iteh.ai/samples/81504/e326c15077514ebb8149912ec0fed2cf/ISO-IEC-15909-3-2021.pdf
- Murata 1989. Tadao Murata, Petri Nets: Properties, Analysis and Applications, Proc. IEEE 77(4). http://people.disim.univaq.it/adimarco/teaching/bioinfo15/paper.pdf
- Desel and Reisig 1998. Jörg Desel, Wolfgang Reisig, Place/Transition Petri Nets, LNCS 1491. https://www.cmi.ac.in/~madhavan/courses/acts2010/desel-reisig-ptnets.pdf
