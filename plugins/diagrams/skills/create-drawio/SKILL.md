---
name: create-drawio
description: Use this skill when the user asks to "create a diagram", "create an RDF diagram", "generate a .drawio file", "make a drawio diagram", or wants to convert RDF/Turtle data into a visual .drawio diagram. Only works in the rdf-diagram-framework project.
---

# Create RDF Diagram

Generate valid `.drawio` RDF diagram files from natural language descriptions or RDF/Turtle data.

## Workflow

### Step 1: Analyze Input

Accept user input as either:
- Natural language description of RDF data
- RDF/Turtle/N-Triples data

Parse and analyze the structure: count subjects, predicates per subject, objects, blank nodes, literals, collections.

### Step 2: Propose Layout

Use `AskUserQuestion` to present 2-3 layout options based on the data analysis:

- **Flat graph**: All subjects/objects as separate nodes connected by edges. Best for sparse graphs with few triples per subject.
- **Triples containers**: Group properties under subject containers. Best for subjects with many predicates.
- **Mixed**: Containers for complex subjects, flat nodes for simple triples.
- **Compact**: Properties containers inside Triples containers to minimize visual elements.

Also consider orientation:
- **Vertical** (`horizontal=1;horizontalStack=0;`): children stack top-to-bottom. Best for deep hierarchies.
- **Horizontal** (`horizontal=0;horizontalStack=0;`): children stack left-to-right. Best for wide graphs.

### Step 3: Generate the `.drawio` File

Use the reference below to construct valid DrawIO XML. Write the file using the Write tool.

### Step 4: Validate

Use `rdf-diagram-cli` to verify the generated file. Run multiple checks:

```bash
# Check that the .drawio parses and converts to Turtle without errors
rdf-diagram-cli -i <file>.drawio -s turtle

# Check roundtrip: drawio → turtle → drawio (should not error)
rdf-diagram-cli -i <file>.drawio -s turtle | rdf-diagram-cli -f turtle -s drawio > /dev/null

# Pretty-print Turtle for human review
rdf-diagram-cli -i <file>.drawio -s turtle-pretty
```

CLI reference (`rdf-diagram-cli --help`):
- `-i <PATH>`: input file (drawio or turtle), stdin if omitted
- `-f <FORMAT>`: input format override (`drawio`, `turtle`, `rdf-xml`, `json-ld`)
- `-o <PATH>`: output file, stdout if omitted
- `-s <FORMAT>`: output serialization (`turtle`, `turtle-pretty`, `n-triple`, `drawio`)

If validation fails, read the error message carefully, fix the XML, and re-validate. Common issues:
- Missing or malformed label escaping (check `&amp;lt;` vs `&lt;`)
- Wrong `parent` attribute (must reference an existing container ID or `"1"` for root)
- Missing `vertex="1"` on nodes or `edge="1"` on edges
- Property node placed outside a Triples container
- Container label type mismatch (e.g., literal label on a Triples container)

## Reference Documentation

For questions about element semantics, composition rules, or label syntax, consult these project files:

- `file:./docs/src/rdf-diagram.md` — Full element reference with containment rules
- `file:./docs/src/diagram.md` — Abstract diagram syntax and composition rules
- `file:./docs/src/iri.md` — IRI syntax (absolute, relative, prefixed)
- `file:./docs/src/literal.md` — Literal syntax (strings, numbers, typed, language-tagged)
- `file:./docs/src/turtle.md` — Embedded Turtle syntax
- `file:./docs/src/triples.md` — Triples container docs
- `file:./docs/src/properties.md` — Properties container docs
- `file:./docs/src/terms.md` — Terms container docs
- `file:./docs/src/collection.md` — Collection container docs
- `file:./docs/src/link.md` — Edge/triple link docs
- `file:./docs/src/property.md` — Property node docs
- `file:./docs/src/blank-node.md` — Blank node docs
- `file:./rdf-diagram-lib/src/formats/drawio.rs` — DrawIO XML types
- `file:./rdf-diagram-lib/src/transforms/diagram_to_drawio.rs` — Style constants and serialization
- `file:./rdf-diagram-lib/tests/rdf-diagram/` — Test fixtures (paired `.drawio` + `.ttl` files)
- `file:./rdf-diagram-tree-sitter/grammar.js` — Label grammar (for valid label syntax)

## DrawIO XML Skeleton

Every diagram needs this boilerplate:

```xml
<mxfile host="agent">
    <diagram>
        <mxGraphModel>
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <!-- elements go here -->
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

The two `mxCell` entries are mandatory: `id="0"` is the root node, `id="1"` is the default layer (parent of all top-level elements).

## Element Styles

### Node (rectangle)

```
points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;
```

Attributes: `vertex="1"`, `parent` is `"1"` (root layer) or a container ID.

### Named Container (swimlane with header)

Concatenate in this order: `CONTAINER_STYLE` + `startSize=30;` + `NODE_STYLE` + orientation flags.

```
swimlane;collapsible=1;childLayout=stackLayout;swimlaneFillColor=default;resizeParent=1;resizeLast=0;resizeParentMax=0;marginBottom=10;marginTop=10;marginRight=10;marginLeft=10;spacingLeft=5;spacingRight=5;fontStyle=0;stackSpacing=10;startSize=30;points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;horizontal=1;horizontalStack=0;
```

Attributes: `vertex="1"`, label is the subject IRI or blank node.

### Anonymous Container (swimlane without header)

Same as named but with `startSize=0;` and no label attribute.

```
swimlane;collapsible=1;childLayout=stackLayout;swimlaneFillColor=default;resizeParent=1;resizeLast=0;resizeParentMax=0;marginBottom=10;marginTop=10;marginRight=10;marginLeft=10;spacingLeft=5;spacingRight=5;fontStyle=0;stackSpacing=10;startSize=0;points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;horizontalStack=0;
```

### Edge (arrow)

```
html=1;edgeStyle=elbowEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;endSize=5;spacingBottom=20;shadow=1;fontSize=14;labelBackgroundColor=none;
```

Attributes: `edge="1"`, `source` and `target` reference element IDs. Geometry uses `relative="1"`.

## Label Escaping

Labels use HTML-inside-XML double escaping because styles include `html=1`:

1. First HTML-encode special characters: `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&apos;`, `&` → `&amp;`
2. Then XML-encode the attribute value: `&` → `&amp;`

Result: `<subject>` becomes `&amp;lt;subject&amp;gt;` in the XML attribute.

Line breaks in labels use `<br>` (HTML tag inside the label, which gets XML-encoded to `&lt;br&gt;` only at the XML level — write it as `<br>` in the label value before XML serialization, or `&lt;br&gt;` in the raw XML attribute).

Labels that don't contain `<`, `>`, `"`, `'`, or `&` need no escaping (e.g., `ex:subject`, `_:blank`, `42`, `true`).

## RDF Element Types and Label Syntax

### Term Nodes

| Type | Label Examples |
|------|---------------|
| Absolute IRI | `<http://example.org/thing>` |
| Relative IRI | `<thing>` (requires `@base`) |
| Prefixed IRI | `ex:thing`, `:thing` (requires `@prefix`) |
| Named blank node | `_:name` |
| Anonymous blank node | `[]` |
| No label | (omit `label` attribute entirely) |
| String literal (double) | `"hello"` |
| String literal (single) | `'hello'` |
| Language-tagged | `'text'@en` |
| Typed literal | `'value'^^xsd:type` |
| Integer | `42` |
| Decimal | `4.0` |
| Double | `1.663E-4` |
| Boolean | `true`, `false` |
| Multi-line literal | `'''line1<br>line2'''` |

### Property Nodes (inside Triples containers)

Label format: `<predicate> <object1>, <object2>`

Examples:
- `<p> <o>` — single property-object pair
- `a ex:Class` — rdf:type shorthand
- `<p> <o1>, <o2>, <o3>` — multiple objects

### Turtle Nodes

Full Turtle syntax in a single node label. Example:
`<http://s> <p> ex:o .`

Can include `@base`, `@prefix`, and multiple statements separated by `.`

### Directive Nodes

- `@base <http://example.org/> .`
- `@prefix ex: <http://example.org/> .`
- `BASE <http://example.org/>`
- `PREFIX ex: <http://example.org/>`

Multiple directives can go in one node separated by `<br>`.

### Edge Labels

- IRI predicates: `<predicate>`, `ex:predicate`
- `a` (shorthand for `rdf:type`)

## Containment Rules

### Nodes Allowed in Each Container

| Node | Terms | Properties | Triples | Collection |
|------|:-----:|:----------:|:-------:|:----------:|
| IRI | Y | Y | N | Y |
| Blank Node | Y | Y | N | Y |
| Literal | Y | Y | N | Y |
| Property | N | N | Y | N |
| Turtle | N | N | N | N |

### Nested Container Rules

| Child | Terms | Properties | Triples | Collection |
|-------|:-----:|:----------:|:-------:|:----------:|
| Properties | N | N | Y | N |
| Terms | Y | Y | N | Y |
| Triples | Y | Y | N | Y |
| Collection | Y | Y | N | Y |

### Container Labels

| Container | Valid Label |
|-----------|------------|
| Terms | (none — anonymous only) |
| Properties | IRI or `a` |
| Triples | IRI or Blank Node |
| Collection | Blank Node |

### Edge Endpoints

| | Valid Subjects | Valid Objects |
|---|---|---|
| Edge | IRI, Blank Node, Terms, Triples | IRI, Blank Node, Terms, Triples, Literal |

## Layout Guidelines

- Node height: `30` (single line), taller for multi-line labels
- Node width: minimum `120`, scale with label length (~8px per character)
- Container header: `30px` (`startSize=30`)
- Stack spacing: `10px` between children in containers
- Container margins: `10px` on all sides
- Position elements on a grid (multiples of 10)
- Directive/prefix nodes at top (`y=0`), diagram content below
- Leave `~20px` gap between sibling elements
- Edge geometry uses `relative="1"` and `as="geometry"` — no manual coordinates needed

## Worked Examples

### Example 1: Simple Triple with Edge

Three nodes (directive, subject, object) connected by one edge.

Turtle output: `<http://base.org/subject> <http://base.org/predicate> <http://base.org/object> .`

```xml
<mxfile host="agent">
    <diagram>
        <mxGraphModel>
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <UserObject id="d1" label="@base &amp;lt;http://base.org/&amp;gt; .">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry width="240" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="n1" label="&amp;lt;subject&amp;gt;">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry y="50" width="120" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="n2" label="&amp;lt;object&amp;gt;">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry x="240" y="50" width="120" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="e1" label="&amp;lt;predicate&amp;gt;">
                    <mxCell style="html=1;edgeStyle=elbowEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;endSize=5;spacingBottom=20;shadow=1;fontSize=14;labelBackgroundColor=none;" parent="1" source="n1" target="n2" edge="1">
                        <mxGeometry as="geometry" relative="1"/>
                    </mxCell>
                </UserObject>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

### Example 2: Prefixed IRIs with Edge

Uses `@prefix` directive and prefixed names for compact labels.

Turtle output: `ex:subject ex:predicate ex:object .`

```xml
<mxfile host="agent">
    <diagram>
        <mxGraphModel>
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <UserObject id="d1" label="@prefix ex: &amp;lt;http://ex.org#&amp;gt; .">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry width="240" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="n1" label="ex:subject">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry y="60" width="120" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="n2" label="ex:object">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry x="240" y="60" width="120" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="e1" label="ex:predicate">
                    <mxCell style="html=1;edgeStyle=elbowEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;endSize=5;spacingBottom=20;shadow=1;fontSize=14;labelBackgroundColor=none;" parent="1" source="n1" target="n2" edge="1">
                        <mxGeometry as="geometry" relative="1"/>
                    </mxCell>
                </UserObject>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

### Example 3: Triples Container with Property and Nested Properties

Subject `<s>` has a property `<p> <o>` and a Properties container `<p2>` containing objects `<o3>` and `<o4>`.

Turtle output:
```turtle
<http://base.org/s> <http://base.org/p> <http://base.org/o> ;
                    <http://base.org/p2> <http://base.org/o3>, <http://base.org/o4> .
```

```xml
<mxfile host="agent">
    <diagram>
        <mxGraphModel>
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <UserObject id="d1" label="@base &amp;lt;http://base.org/&amp;gt; .">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="1" vertex="1">
                        <mxGeometry width="240" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="c1" label="&amp;lt;s&amp;gt;">
                    <mxCell style="swimlane;collapsible=1;childLayout=stackLayout;swimlaneFillColor=default;resizeParent=1;resizeLast=0;resizeParentMax=0;marginBottom=10;marginTop=10;marginRight=10;marginLeft=10;spacingLeft=5;spacingRight=5;fontStyle=0;stackSpacing=10;startSize=30;points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;horizontal=1;horizontalStack=0;" parent="1" vertex="1">
                        <mxGeometry y="50" width="200" height="120" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="p1" label="&amp;lt;p&amp;gt; &amp;lt;o&amp;gt;">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="c1" vertex="1">
                        <mxGeometry y="30" width="180" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="c2" label="&amp;lt;p2&amp;gt;">
                    <mxCell style="swimlane;collapsible=1;childLayout=stackLayout;swimlaneFillColor=default;resizeParent=1;resizeLast=0;resizeParentMax=0;marginBottom=10;marginTop=10;marginRight=10;marginLeft=10;spacingLeft=5;spacingRight=5;fontStyle=0;stackSpacing=10;startSize=30;points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;horizontal=0;horizontalStack=0;" parent="c1" vertex="1">
                        <mxGeometry y="60" width="180" height="60" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="o3" label="&amp;lt;o3&amp;gt;">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="c2" vertex="1">
                        <mxGeometry x="30" width="140" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
                <UserObject id="o4" label="&amp;lt;o4&amp;gt;">
                    <mxCell style="points=[];html=1;shadow=1;perimeterSpacing=3;spacingLeft=10;spacingRight=10;allowArrows=1;rotatable=0;overflow=hidden;whiteSpace=wrap;fontSize=14;" parent="c2" vertex="1">
                        <mxGeometry x="30" y="30" width="140" height="30" as="geometry"/>
                    </mxCell>
                </UserObject>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

Key points in this example:
- `c1` is a **Triples** container (named, label=`<s>`, `startSize=30`)
- `p1` is a **Property** node inside `c1` (label=`<p> <o>`, `parent="c1"`)
- `c2` is a **Properties** container inside `c1` (named, label=`<p2>`, `parent="c1"`, `startSize=30`)
- `o3` and `o4` are term nodes inside `c2` (`parent="c2"`)
- The Properties container `c2` uses `horizontal=0` for horizontal child layout
