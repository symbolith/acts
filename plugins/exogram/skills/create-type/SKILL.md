---
name: create-type
description: Add a new note type to the facts exogram, with its type note, schema enum entry, type file, and template. Use when the user wants to "add a type", "create a note type", "new type note", "add a class", "add a supertype", or make existing types subtypes of a new one.
argument-hint: [type-name-or-description]
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(just ulid:*), Bash(just templates:*), Bash(just validate:*), Bash(curl:*), WebSearch, WebFetch, AskUserQuestion
---

# Create Note Type

Add a note type to `/home/beavis/repositories/symbolith-exogram/facts/exogram/`. All relative paths below are relative to `/home/beavis/repositories/symbolith-exogram/facts/`. A type is complete when its type note exists and `just templates` has written the rest from it: the enum entry and `allOf` reference in `exogram.yaml`, the type file, the template, and the type note's `template` link. A type note exists exactly once and only in `facts/exogram/`. A type note found in another exogram is moved here, or merged into its duplicate and deleted.

## Inputs

- `$ARGUMENTS`: a type name (e.g. `Note`) or a description (e.g. "supertype for the generic note kinds")

## Workflow

### 1. Resolve the Name

- Title is PascalCase, e.g. `DailyNote`. It names the type file and the template.
- A note has one alias. Rename in place, never keep the old name as a second alias.
- Alias is `Type <Title>`, without a vocabulary prefix: `Type Activity`, not `Type prov:Activity`. EXCEPTION, a title clash: when a Factors or exogram term and a borrowed term share a name, the exogram's own term keeps the plain alias and the borrowed one carries its prefix in the alias, e.g. `Type Plan` is `fctrs:Plan` and `Type prov:Plan` is `prov:Plan`. The prefixed one's Title, which names its type file and template, drops the colon: `ProvPlan`. The alias string is what the enum, the type file `const` and every `type` list carry, so a clash rename sweeps all of them.
- Every type note carries exactly one `iri`, the IRI the note denotes, as a markdown link labelled with the compact IRI: `iri: "[prov:Activity](http://www.w3.org/ns/prov#Activity)"`. Never a bare prefixed term. The `@context` of `properties.yaml` is generated from the compact IRIs on the type and property notes; a new prefix needs nothing beyond its first use.
  - Type equals an ontology class: `iri` is that class.
  - Type is defined by the Factors Vocabulary (`fctrs:`): `iri` is `[fctrs:<Title>](https://symbolith.org/factors#<Title>)`. The Vocabulary IS the note `Ontology Factors` (`20260919181803.md`), derived from the type and property notes that carry `isDefinedBy` Ontology Factors; there is no separate vocabulary file to edit. The Formalization (`factors/20260518150627.md`) is the authority on what a Factors term means.
  - Type is coined here: `iri` is `[exogram:<Title>](https://symbolith.org/exogram#<Title>)`.
- `sameAs` holds further equivalent classes only, e.g. `Type Agent` has `iri fctrs:Agent` and `sameAs prov:Agent`. Never repeat the `iri` in `sameAs`.
- Look up an existing RDF vocabulary term for the concept BEFORE naming anything. Never answer from memory. Work through the sources in this order and report each one as hit, no hit, or unreachable:
  1. Linked Open Vocabularies, term search inside about 800 vocabularies: `https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=<word>&type=class`
  2. DBpedia Archivo, a registry of about 1,900 ontologies, no term search: find a fitting ontology in `https://archivo.tools.dbpedia.org/list`, then download it with `curl -sL "http://archivo.dbpedia.org/download?o=<ontology URI>&f=ttl"` into the scratchpad and grep the file for the term. Never read an ontology through `WebFetch`: it truncates large files and reports false misses.
  3. Wikidata, and ESCO for occupations and roles.
  4. Free `WebSearch`.
  5. schema.org, last: `https://schema.org/<Term>`.
- Prefer a term from a vocabulary the exogram already uses (PROV-O, the SPAR ontologies, ORG, FOAF, dcterms) over an equal term elsewhere. Open the term's page and confirm the URI and its definition.
- Report the hits to the user: term, URI, definition, and whether it is equal to the concept (`iri`, or `sameAs` for a second equal term) or broader (`subClassOf`). No hit is a valid result: say so, then coin a plain name. Reuse beats invention.
- Grep the `type.enum` in `exogram.yaml` for a type that already covers the concept. Stop and report if one does.

### 2. Place the Type

Read the ontology notes (`type: Type Ontology`) and the existing type notes. Decide:

- `isDefinedBy`: a list with exactly one ontology note. Every type has one. Generic note kinds and types that describe the exogram itself belong to Ontology Exogram.
- `subClassOf`: a list of links, usually one, to type notes, e.g. `"[Type Activity](20260426153348.md)"`, or a markdown link to the full URI when the superclass has no note, e.g. `"[prov:Entity](http://www.w3.org/ns/prov#Entity)"`. Never a bare prefixed term.
- Subtypes: existing types that become subclasses of the new type. Their current `subClassOf` moves up to the new type when it still holds for all of them.
- `disjointWith`: types no note may carry together with this one, e.g. Success, Plan and Failure pairwise. Set it on BOTH sides.
- Own properties: the properties this type attaches, each required or optional. Only what the type adds; what a supertype attaches is inherited through the `type` chain. Each property must have a property note, and that note's `domain` must name this type or a supertype of it, or be absent. Use `/exogram:create-property` for new ones and for a domain that needs widening.
- `comment`: the single home of the definition; `exogram.yaml` and `types/<Title>.yaml` carry no `description`. When `iri` is a class of an existing vocabulary, `comment` is that vocabulary's own definition of the class, verbatim, taken from the vocabulary's RDF file, in this order: `prov:definition` or `prov:editorsDefinition` (PROV-O), `skos:definition`, `rdfs:comment`, `schema:description`; when the file carries none, the Definition field of the vocabulary's specification (PRISM 2.0 spec PDF, PROV-DM for PROV-O terms without one), the Wikidata English description, or the ESCO description. Untouched: never paraphrased, trimmed, or written from memory. Only a `fctrs:` or `exogram:` class gets a definition written here: one sentence, what it is in the ontology view, no example, never naming the term (the `iri` carries it). The sentence states only what no key states: no listing of subtypes, supertypes, disjoint types, second names, or what the term is not; those live in `subClassOf`, `disjointWith`, and `aliases`.

### 3. Show the Design

Present the type note frontmatter, the subtype edits, and the schema edits. Wait for approval before writing.

### 4. Write the Type Note

File: `facts/exogram/<ULID>.md`, the id from `just ulid` run in the exogram root.

Frontmatter: fill `/home/beavis/repositories/symbolith-exogram/facts/.templates/Type.md`. `iri` is the first key. The alias is `Type <Title>`. Leave `template` out: `just templates` in step 6 writes it. Drop every property still set to `optional`. Add `reviewLevel: unread`.

Body: copy the body of `.templates/Type.md` verbatim, the `Supertypes`, `Subtypes`, `Domain of`, `Range of`, and `Instances` query blocks. Write only the query comments, never a result block; the plugin generates results once the note is saved in Obsidian.

### 5. Update the Schema

`exogram.yaml` is generated, never edited: `just templates` appends `'[Type <Title>](<id>.md)'` to `properties.type.items.enum` and `- $ref: types/<Title>.yaml` to `allOf`.

`types/<Title>.yaml` is generated, never written by hand. Its `then.required` comes from the type note's `requiredProperty`, its `then.properties` from `optionalProperty`, both lists of links to property notes. That is where a property is attached to a type. Never repeat in `optionalProperty` what a supertype attaches: a note carries the whole `type` chain, so every supertype's file applies to it. `requiredProperty` may name an inherited property; that is a constraint, not an attachment. Never define a property on a type note; a property is defined by its property note, from which `properties.yaml` is generated.

The link string must be byte-identical in the enum, the type file `const`, and the template.

### 6. Generate the Type File and the Template

Run `just templates` in the exogram root. It writes the enum entry and `allOf` reference in `exogram.yaml` and `types/<Title>.yaml` from the type note, then `.templates/<Title>.md` from the type files: `type` lists the type and then EVERY superclass reachable through `subClassOf` links to type notes, nearest first, URI superclasses left out; below it every property attached anywhere in that chain, own type first, then each ancestor, marked `required` when any type in the chain requires it, else `optional`, in list form when the property is an array. The generator rewrites the frontmatter except the first alias line, which it keeps; `just validate` fails on a stale one.

Only the alias line and the body are hand-written and the generator keeps them. The alias line carries the type's alias prefix when its notes use one, e.g. `- Project {{title}}`. Write one only for a type whose notes carry query blocks (Type, Property, Ontology): dataview-serializer query comments, never result markers. The blocks stay inert inside `facts/.templates` because Obsidian never indexes a dot folder, so Dataview cannot see templates and no query needs an exclusion clause; they run only once the body is copied into a note.

### 7. Rewire the Subtypes

For each subtype note set `subClassOf` to the single item `"[Type <Title>](<id>.md)"` and `reviewLevel: unread`. Touch nothing between dataview-serializer result markers.

Then materialize the new chain: `just templates` rewrites the subtypes' templates; in EVERY existing note whose `type` contains a subtype, insert `"[Type <Title>](<id>.md)"` into `type` right after the subtype entry. `just validate` reports every note whose `type` misses a superclass; run it until clean. A canon note gets `documentStatus: draft` instead of a `reviewLevel` change.

### 8. Verify

- Grep the id: it appears in the type note filename, the enum, the type file, the template, and each subtype.
- `just validate` without a glob, until clean. Besides the notes it checks that no template is stale and that every attached property's `domain` covers its type.

Report inconsistencies found on the way. Do not fix them unasked.
