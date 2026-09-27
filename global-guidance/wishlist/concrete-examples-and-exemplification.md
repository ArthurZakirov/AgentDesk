# 🧱 Concrete examples and exemplification

## Desired outcome

Human-facing information should not stop at abstract labels when a compact concrete instance would materially improve understanding, review, recall, or trust. Prefer enough concrete materialization that the reader can see what an abstraction means in practice without turning every explanation into a long tutorial.

This applies beyond code. Agent instructions, Markdown docs, design explanations, routing tables, APIs, architecture notes, recommendations, and ordinary prose may all benefit from a brief `e.g.` example when the concept would otherwise remain underspecified or cognitively expensive.

## Core idea

Use abstraction for compression and generality; use examples to ground that abstraction. The two should complement rather than replace each other.

Examples:

- `Provider-specific instruction paths` → e.g. `AGENTS.md` for Codex-style instructions, `CLAUDE.md` for Claude Code.
- `Portable path construction` → e.g. `${HOME}/...` or a repository-relative path instead of `/Users/alice/...`.
- `Identity-neutral wording` → e.g. `agent` / `user` instead of hard-coding `Codex` / `Arthur` when the rule is provider- or person-independent.
- `Deterministic control` → e.g. a pre-tool permission gate or post-edit validator rather than stronger wording such as "always do this".
- `Concrete code explanation` → name the actual function, variable, input, and resulting value rather than describing an unnamed "edge", "owner", or "prefix".

## Relationship to SEE-I

SEE-I is a useful reference model: **State → Elaborate → Exemplify → Illustrate**. It is a clarification technique associated with Gerald Nosich's critical-thinking work. Its useful lesson here is not that every paragraph must contain all four stages, but that an important abstraction often becomes clearer after at least one concrete example or illustration.

For this system, prefer a lighter adaptive form:

1. **State** the concept precisely.
2. **Elaborate** only as much as needed.
3. **Exemplify** with one or more compact concrete instances when abstraction alone would leave interpretation work to the reader.
4. **Illustrate** with a diagram, analogy, before/after, or other representation only when it adds material clarity.

## Constraints

- Examples are aids, not boundaries. Do not make a general rule appear limited to the examples named.
- Keep examples proportionate; one short example is often enough.
- Prefer examples that are representative of the actual surrounding system rather than generic toy examples when real examples are available.
- Do not duplicate large bodies of canonical information merely to provide an example; anchor or link to the canonical source when appropriate.
- Do not invent examples that imply unsupported facts about the current environment.
- A reader should still be able to distinguish the general rule from its example.

## Questions before promotion

- Should this become a child of global `Information presentation`, a dedicated reusable skill/reference, or both with a compact global router?
- Which surfaces benefit enough to justify always-loaded guidance versus conditional loading?
- How should this interact with relevance-first disclosure so examples clarify without creating persistent verbosity?
- Should Markdown-specific examples live in `format-markdown` while the broader principle remains medium-independent?
- Can review heuristics detect abstraction-heavy passages that would benefit from an example without forcing unnecessary examples everywhere?

## Research note

The SEE-I framework is commonly expanded as State, Elaborate, Exemplify, Illustrate and is described as a method for clarifying ideas. Treat it as supporting theory for this wishlist item, not as a mandatory output template.