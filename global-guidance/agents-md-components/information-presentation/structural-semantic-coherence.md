<a id="structural-semantic-coherence"></a>
# 🧱 Structural and semantic coherence

When modifying an existing artifact, identify the **organizing principle of each affected group** before adding a sibling element. A group may be a directory of files, a section of headings, a sequence of workflow steps, a list of bullets, a collection of tests, a table of records, or a navigation hierarchy. Its peer elements should share a coherent **semantic role and level of abstraction** relative to that group's purpose. An ordered group also has a meaningful sequence.

**Placement rule:** Determine what existing peers have in common and what each peer represents. Then decide whether the new information belongs **inside an existing element**, **as a new peer at the appropriate position**, or **in a separate group or parent**. Do not append an item or create a new file merely because it is convenient. Do not elevate a detail to the rank of its container, or mix a rule's subject matter with its applicability/scope as if they were instances of the same category.

**Coherence checks:**

- **Sequence vs. branch:** In an ordered workflow, peer steps represent successive stages. Keep `if/else` outcomes under the step where the decision occurs; do not turn an alternative outcome or a cross-cutting principle into another stage.
- **Information flow and ownership:** Trace where each input enters, how it is classified, and where it is handled. If an existing stage already covers it, use or refine that stage rather than repeat the source, special-case the input, or duplicate the behavior downstream.

| Existing organization | Incoherent addition | Coherent integration |
| --- | --- | --- |
| Numbered items represent successive workflow stages. | Add a new numbered step for an alternative outcome of an earlier decision. | Nest conditional outcomes under the decision step; reserve peer numbers for subsequent stages. |
| A workflow collects input sources before evaluating the accumulated inputs. | Reintroduce one already collected source as a special case in the evaluation stage. | List the source where inputs enter; apply the evaluation criteria to all collected inputs without redundant source-specific handling. |
| Each BDD `.feature` file owns the scenarios for one domain object. | Create a peer feature file for one scenario of an existing object. | Add the scenario to that object's feature file. |
| A bullet list enumerates coding-style dimensions such as typing, formatting, and naming. | Add `new functions only` as another dimension, although it describes scope. | State the applicability rule separately; retain only style dimensions as list peers. |
| A test directory groups files by module or component. | Create a new top-level file for a single regression case of an already covered component. | Put the test in the existing component's test file, unless it warrants a distinct test category. |
| A code directory groups handlers by domain resource. | Create an action-specific file as a peer of resource-specific modules without architectural justification. | Extend the appropriate resource module, or deliberately revise the overall organization. |
| A table has one row per invoice line item. | Insert an invoice grand total as though it were another line item. | Put the aggregate in a summary/footer, preserving the row schema. |
| Top-level navigation entries represent product areas. | Put a sub-feature page beside those product areas. | Nest the page under its owning area, unless it genuinely constitutes a new area. |

These examples illustrate the **same cross-medium principle**, not special-case rules. Diverse elements may coexist when the group's actual organizing criterion supports them; do not enforce superficial uniformity or preserve an unsuitable structure merely because it already exists. Respect explicit requirements for a different organization.
