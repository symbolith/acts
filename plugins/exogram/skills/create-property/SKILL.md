---
name: create-property
description: Add a new frontmatter property to the exogram schema. Use when the user wants to "add a property", "add a field", "new frontmatter field", "add metadata", or extend the exogram schema with a new property.
argument-hint: [property-name-or-description]
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(just ulid:*), Bash(just templates:*), Bash(just validate:*), WebSearch, WebFetch, AskUserQuestion
---

# Add Exogram Property

Add a new property to the exogram schema, assign it to relevant note types, and update templates.

## Inputs

- `$ARGUMENTS`: either a property name (e.g. `birthDate`) or a natural language description (e.g. "date when a person was born")

## Workflow

### 1. Resolve Property Name

If `$ARGUMENTS` looks like a property name (camelCase, single word), use it directly.

Look the term up as `/exogram:create-type` step 1 does, never from memory, and read its definition, domain and range from the vocabulary before choosing it.
A term is fit only when its subject matches the note that will carry it.
Prefer a term from a vocabulary the exogram already uses; coin a camelCase name only on no hit.

Present the candidate, its URI and definition to the user for confirmation.

### 2. Define the Property

The value shape lives on the property note (step 2b); `properties.yaml` is generated from it by `just templates` and never edited. Decide:

- One value or a list: `characteristic: functional` means one value, absent means a list.
- The value type, from `range`:

| `range` | schema |
|---|---|
| `xsd:string`, `xsd:language` | string |
| `xsd:boolean`, `xsd:integer`, `xsd:decimal` | that type |
| `xsd:date`, `xsd:dateTime` | date string |
| `rdfs:Literal` | any literal |
| `rdfs:Resource` | a link or a literal |
| a type note whose instances all carry an `iri` in one namespace (State, ReviewLevel, DocumentStatus) | enum of those local names |
| any other class, or absent | a link |

- A fixed set of values is a value-set class: a type note plus one note per value carrying the value's `iri`, made with `/exogram:create-type`; the property's `range` names that type note.
- No `description` anywhere: the one-line definition lives only in the note's `comment`.

### 2b. Write the Property Note

Every property has a note in `facts/exogram/`, typed `Type Property`. File: `facts/exogram/<ULID>.md`, the id from `just ulid` run in the exogram root. Fill `file:~/repositories/symbolith-exogram/facts/.templates/Property.md`, alias `Property <name>`, drop every key still set to `optional`, add `reviewLevel: unread`. `comment` is the single home of the definition, `properties.yaml` carries no `description`. When `iri` is a term of an existing vocabulary, `comment` is that vocabulary's own definition of the term, verbatim, taken from the vocabulary's RDF file, in this order: `prov:definition` or `prov:editorsDefinition` (PROV-O), `skos:definition`, `rdfs:comment`, `schema:description`; when the file carries none, the Definition field of the vocabulary's specification (PRISM 2.0 spec PDF, PROV-DM for PROV-O terms without one), the Wikidata English description, or the ESCO description. Untouched: never paraphrased, trimmed, or written from memory. Only a `fctrs:` or `exogram:` term gets a definition written here: one sentence, no example, never naming the term (the `iri` carries it). The sentence states only what no key states: no inverse, derivation, usage rule, or what the term is not; those live in `inverseOf`, `hasPrimitive`, and `characteristic`. Body: copy the template body verbatim, the `Superproperties`, `Subproperties`, `Inverse of`, and `Usage` query blocks. Write only the query comments, never a result block; the plugin generates results once the note is saved in Obsidian.

- `iri` is the first key: the IRI the property denotes, as a markdown link labelled with the compact IRI, e.g. `iri: "[dcterms:subject](http://purl.org/dc/terms/subject)"`. Never a bare prefixed term. The `@context` of `properties.yaml` is generated from the compact IRIs on the type and property notes; a new prefix needs nothing beyond its first use.
  - Ontology term: `iri` is that term.
  - Factors Vocabulary term: `[fctrs:<name>](https://symbolith.org/factors#<name>)`. The Vocabulary IS the note `Ontology Factors` (`20260919181803.md`), derived from the notes that carry `isDefinedBy` Ontology Factors; the Formalization (`factors/20260518150627.md`) says what a term means.
  - Coined here: `[exogram:<name>](https://symbolith.org/exogram#<name>)`.
- `sameAs` holds further equivalent terms only. Never repeat the `iri` there.
- `subPropertyOf`, `inverseOf`: one link to a property note, or a full-URI link for a term without a note. `inverseOf` goes on both sides.
- `hasPrimitive`: only on a `fctrs:` property absent from the Formalism, the primitive properties it is defined by, e.g. `proposedBy` by `claimedBy`. Never `wasDerivedFrom`, which is note provenance.
- `domain`, `range`: lists of links to type notes, or full-URI links for terms without a note. Every listed type holds at once: each `domain` type applies to the subject, each `range` type to the object, as RDFS reads it. Never list alternatives; a property that applies to Person or Organization gets their nearest common supertype, Agent. When the exogram has none, take what the term's ontology declares, or omit the key; absent means any.
- `isDefinedBy`: required, a list of the ontology notes the property belongs to, e.g. `"[Ontology Factors](20260919181803.md)"`. Each Ontology note's `comment` states the test for membership; read every one and apply them, never guess from `domain` or the term's vocabulary. An Ontology note lists its properties through it.
- `domain` and `range` link the exogram type note whenever one exists for the term, also when the type note only carries the term as `iri` or `sameAs` (Type Entity for prov:Entity, Type Agent for prov:Agent, foaf:Agent, dcterms:Agent). Never list a type next to its supertype.
- `characteristic`: OWL characteristics, e.g. `functional`, `inverseFunctional`, when the property has them.

### 3. Decide the Attachment

Attachment only feeds templates. The root declaration in step 5 already makes the property valid on every note.
A property with a `domain` is attached to that domain type, required or optional.
A property without a `domain` that fits any note stays unattached, like `reviewLevel`.
A property without a `domain` that fits some unrelated types is attached to each of them.

### 4. Ask User for Assignment

Ask only what the lookup left open: required or optional, and the types when there is no `domain`.

### 5. Update Schema

`just templates` adds the property to the root `properties` of `exogram.yaml` and its shape to `properties.yaml`; never edit either. Every property is valid on every note through that root declaration.

Attach it on the type note: a link to the property note under `requiredProperty` or `optionalProperty`. `just templates` writes `then.required` and `then.properties` of `types/<Title>.yaml` from those lists; never edit a type file. Attach it once, at the type decided in step 3; subtypes inherit it through their `type` chain and never repeat it in `optionalProperty`. A subtype may still list it in `requiredProperty`: that is a constraint, not an attachment. Every type it is attached to must be the property's `domain` or a subtype of it, or the property has no `domain`; `just validate` fails otherwise.

### 6. Regenerate Templates

Run `just templates` in the exogram root. It writes `properties.yaml`, `exogram.yaml`, the type files and the templates from the notes; none is edited by hand. Then `just validate` without a glob, until clean.

### 7. Summary

Report what was done:
- Property note written, with its `iri`, `range`, and whether it is functional
- Type notes it is attached to, required or optional
- Generated files that changed: `properties.yaml`, `exogram.yaml`, type files, templates
