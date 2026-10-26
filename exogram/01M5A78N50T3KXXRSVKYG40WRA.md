---
aliases:
  - Working Note Affords Hierarchy
type:
  - "[Type DesignDocument](01M5HP91XPHJJ32VJFRR9BP9E1.md)"
comment: Working state of the affords hierarchy of the Factor Templates that replace the skills.
subject:
  - "[Software Acts](01M3A6328V1FZSP45F54HD1TS6.md)"
  - "[Type Factor Template](01M59Z1KXCTY0CAPX2E9WA0YAV.md)"
wasInfluencedBy:
  - "[Idea Mapping Act to Plugin and Skill](01M40Z02DWJY41ZW984T2M42DJ.md)"
  - "[Working Note READMEs and Software Acts](01M4V3WJ1H5SE988YHX2WREQX8.md)"
vetting: unread
---

## Current

<!-- dataview-serializer-js:
const pages = dv.pages();
const refers = (value, id) => String(value).includes(id + ".md");
const link = page => "[" + page.file.aliases[0] + "](" + page.file.name + ".md)";
const byAlias = (left, right) => left.file.aliases[0].localeCompare(right.file.aliases[0]);
const afforded = page => pages.where(child => refers(page.affords, child.file.name)).array();
const roots = pages
  .where(page => refers(page.type, "01M59Z1KXCTY0CAPX2E9WA0YAV"))
  .where(page => !pages.some(parent => refers(parent.affords, page.file.name)))
  .array();
const premises = page => pages
  .where(premise => refers(premise.type, "20260608023512") && refers(page.hasPremise, premise.file.name))
  .array().map(link);
const line = (page, depth) => "    ".repeat(depth) + "- " + link(page)
  + (premises(page).length ? ": " + premises(page).join(", ") : "");
const tree = (nodes, depth, path) => nodes
  .filter(page => !path.includes(page.file.name))
  .sort(byAlias)
  .flatMap(page => [
    line(page, depth),
    ...tree(afforded(page), depth + 1, [...path, page.file.name]),
  ]);
dv.paragraph(tree(roots, 0, []).join("\n"));
 -->
<!-- dataview-serializer-js-result -->
- [Applying to an open call](01M5A2MQMK5YZMVE9ZMYNSBGM6.md)
    - [Capturing an open call](01M5A2MQMMVKFHGYSKFGFHDY6Y.md): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Finding open calls](01M5A2MQMK5YZMVE9ZMYNSBGM7.md)
    - [Writing an open call application](01M5A2MQMMVKFHGYSKFGFHDY6Z.md)
- [Tending an exogram](01M3MCPACCK5HE44XPK8ZEJMHJ.md): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Adding missing reverse properties](01M412AVZKEKCM82187EZ7Z6HC.md): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Tending the facts](01M3MDS7C6G7YJX13WVMTGF6P7.md): [Premise Tending the facts](01M3MDCVSEEVSJYGKCB70ZM5YG.md)
- [Updating Workspace Symbolith](01M3WTTSCGAYT49SCF8W8SKNGA.md)

<!-- dataview-serializer-js-result-end -->

## Proposed

### Symbolith

[Software Symbolith](01M3W64E3XJNYHDY50M1RYXPGF.md)

- Operating Symbolith (Factor)
    - Updating Workspace Symbolith (Act)

### Exogram

[Software Exogram](01M3N54CGY26KTHNPDTH7D748X.md)

- Using Exogram (Factor)
    - Searching notes (Act)
    - Creating a note (Factor)
        - Naming a thing (Factor)
            - (Exogram) Searching notes (Act)
        - Resolving types (Factor)
            - (Exogram) Searching notes (Act)
        - Resolving an exogram (Act)
        - Writing a note (Factor)
            - Filling frontmatter (Factor)
                - (Exogram) Searching notes (Act)
            - Writing a body (Act)
            - Previewing a note (Act)
            - Saving a note (Act)
    - Creating a dataview block (Act)
- Operating Exogram (Factor)
    - Adding missing reverse properties (Act)
    - Checking frontmatter (Act)

### Factors

[Software Factors](01M3A631GTH86CTAD3D8PMQC7M.md)

- Using Factors (Factor)
    - Enacting an act (Factor)
        - Taking up an act (Act)
        - Preparing an act (Factor)
            - Building a follows DAG (Act)
            - (Factors) Enacting an act (Factor), recursive
        - Claiming an act (Act)
        - Previewing work (Act)
        - Producing outputs (Act)
            - (Acts) Creating an act (Factor)
        - Settling an act (Act)
    - Enacting a factor (Factor)
        - Building a member DAG (Act)
        - (Factors) Enacting an act (Factor)
        - Settling a factor (Act)
    - Enacting a factor template (Factor)
        - Joining a template into a factor (Act)
        - (Factors) Enacting a factor (Factor)

### Acts

[Software Acts](01M3A6328V1FZSP45F54HD1TS6.md)

- Using Acts (Factor)
    - Creating an act (Factor)
        - Asking design questions (Act)
        - (Exogram) Creating a note (Factor)
    - Creating a factor template (Factor)
        - Placing it in affords (Act)
        - Creating a premise (Act)
        - (Exogram) Creating a note (Factor)
    - Improving an act (Factor)
        - (Acts) Extracting a violated principle (Act)
        - (Acts) Confirming a principle (Act)
        - (Acts) Folding in a principle (Act)
    - Improving a factor template (Factor)
        - (Acts) Extracting a violated principle (Act)
        - (Acts) Confirming a principle (Act)
        - (Acts) Folding in a principle (Act)

### Facts

[Software Facts](01M3A6331BRKGA95S2MVP9QQWD.md)

- Using Facts (Factor)
    - Creating vocabulary (Factor)
        - Creating a vocabulary (Factor)
            - Defining a vocabulary (Act)
            - (Exogram) Writing a note (Factor)
        - Creating a type (Factor)
            - Defining a type (Act)
            - Placing a type in the hierarchy (Act)
            - (Exogram) Writing a note (Factor)
        - Creating a property (Factor)
            - Defining a property (Act)
            - (Exogram) Writing a note (Factor)
    - Creating a shape (Factor)
        - Requiring or allowing a property on a type (Act)
        - (Facts) Generating templates (Act)
- Implementing Facts (Factor)
    - Building Facts (Factor)
        - Generating templates (Act)

## Parked

- Updating Workspace Symbolith (Act): [Updating Workspace Symbolith](01M3WTTSCGAYT49SCF8W8SKNGA.md)
- Using Exogram (Factor): [Tending an exogram](01M3MCPACCK5HE44XPK8ZEJMHJ.md), [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
- Adding missing reverse properties (Act): [Adding missing reverse properties](01M412AVZKEKCM82187EZ7Z6HC.md)
- Enacting an act (Factor): [Type Act](20260608023505.md), [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md), `exogram:do-enactable`
- Enacting a factor (Factor): [Type Factor](20260923150308.md), [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md), `exogram:do-enactable`
- Creating an act (Factor): [Type Act](20260608023505.md), [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md), `exogram:create-act`
- Creating a factor template (Factor): [Type Factor Template](01M59Z1KXCTY0CAPX2E9WA0YAV.md), [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md), `claude-code:create-skill`
- Improving a factor template (Factor): [Type Factor Template](01M59Z1KXCTY0CAPX2E9WA0YAV.md), `claude-code:improve-skill`
- Using Facts (Factor): [Tending the facts](01M3MDS7C6G7YJX13WVMTGF6P7.md), [Premise Tending the facts](01M3MDCVSEEVSJYGKCB70ZM5YG.md)
- Creating a type (Factor): [Type Type](20251204174430.md), `exogram:create-type`
- Creating a property (Factor): [Type Property](20260920200516.md), `exogram:create-property`
- Creating a dataview block (Act): `exogram:create-dataview`
- Checking frontmatter (Act): `exogram:check-frontmatter`
- Naming a thing (Factor): `writing:name-thing`
