---
aliases:
  - Working Note Affords Hierarchy
type:
  - "[Type Outline](20260609201432.md)"
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
- [Keep the hand-written lists of Workspace Symbolith in sync](01M3WTTSCGAYT49SCF8W8SKNGA.md)
- [Tending an exogram](01M3MCPACCK5HE44XPK8ZEJMHJ.md): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Adding missing reverse properties](01M412AVZKEKCM82187EZ7Z6HC.md): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Tending the facts](01M3MDS7C6G7YJX13WVMTGF6P7.md): [Premise Tending the facts](01M3MDCVSEEVSJYGKCB70ZM5YG.md)

<!-- dataview-serializer-js-result-end -->

## Proposed

- Enacting an enactable (Factor): `exogram:do-enactable`, [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - Taking up an enactable (Act)
    - Preparing an enactable (Factor)
        - Building the follows DAG (Act)
        - Enacting an enactable (Factor), recursive
    - Doing an act (Factor)
        - Claiming an act (Act)
        - Proposing a plan (Act)
        - Producing the outputs (Act)
            - Creating an enactable (Factor)
        - Settling an act (Act)
    - Settling a factor (Act)
- Creating an enactable (Factor): `exogram:create-act`, `claude-code:create-skill`, [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - Resolving the type (Act)
    - Resolving the exogram (Act)
    - Filling the fields (Act)
        - Naming a thing (Act): `writing:name-thing`
    - Asking design questions (Act)
    - Previewing a note (Act)
    - Writing a note (Act)
    - Creating a premise (Act)
    - Improving an enactable (Factor): `claude-code:improve-skill`
        - Extracting the violated principle (Act)
        - Confirming the principle (Act)
        - Folding in the principle (Act)
- [Tending an exogram](01M3MCPACCK5HE44XPK8ZEJMHJ.md) (Factor): [Premise Tending an exogram](01M3MBPMFFWAA1FYBT30FKFYDR.md)
    - [Tending the facts](01M3MDS7C6G7YJX13WVMTGF6P7.md) (Factor): [Premise Tending the facts](01M3MDCVSEEVSJYGKCB70ZM5YG.md)
        - Creating a type (Factor): `exogram:create-type`
            - Naming a thing (Act)
            - Placing the type (Act)
            - Previewing a note (Act)
            - Writing a note (Act)
            - Updating the schema (Act)
            - Generating the templates (Act)
            - Rewiring the subtypes (Act)
        - Creating a property (Factor): `exogram:create-property`
            - Naming a thing (Act)
            - Defining the property (Act)
            - Previewing a note (Act)
            - Writing a note (Act)
            - Attaching the property to a type (Act)
            - Updating the schema (Act)
            - Generating the templates (Act)
        - Checking frontmatter (Act): `exogram:check-frontmatter`
    - [Adding missing reverse properties](01M412AVZKEKCM82187EZ7Z6HC.md) (Act)
    - [Keep the hand-written lists of Workspace Symbolith in sync](01M3WTTSCGAYT49SCF8W8SKNGA.md) (Act)
    - Creating a dataview block (Act): `exogram:create-dataview`
