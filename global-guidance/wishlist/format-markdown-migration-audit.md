# 🧾 Format Markdown migration audit

Purpose: prevent rules from the older `format-markdown` material from disappearing during decomposition into newer guidance/components/skills. This file is an audit queue, not active production guidance.

## Known source scope

Recovered from prior migration discussion: meaning preservation, Markdown syntax, frontmatter, heading levels, inline code, relative links, code fences, escaping, and local/global table-of-contents behavior.

Recovered from the pasted legacy chapters 9/10: anchoring, snippets, links, row-shaped data, diagrams, concrete wording, code-block layout, before/after code changes, call-order arrows, interleaving, heading hierarchy, and docstring shape examples.

## Status

| Area | Current status | Destination / action |
| --- | --- | --- |
| Meaning preservation | Partially represented elsewhere; not audited rule-by-rule | Verify against original `format-markdown` wording before closing migration. |
| Global TOC | Implemented in AgentDesk generator | Keep. |
| Local TOCs for nested chapters | Implemented for AgentDesk nested component groups | Preserve the broader Markdown/document rule for later audit against the original source. |
| Heading hierarchy | Partially implemented / currently being expanded by nested manifest work | Verify exact original constraints. |
| Frontmatter | Not verified as migrated | Audit and place in Markdown-specific skill/guidance. |
| Inline code | Not verified as migrated | Audit and place in Markdown-specific skill/guidance. |
| Relative links | Partially implemented in AgentDesk-generated guidance | Audit broader Markdown rule, not just AGENTS.md generation. |
| Code fences / language tags | Not verified as migrated | Audit against legacy layout rules. |
| Escaping | Not verified as migrated | Audit and place in Markdown-specific skill/guidance. |
| Anchoring / reader never searches | Implemented globally | Keep platform/repository-specific anchor construction separate. |
| Representation selection | Implemented globally | Continue under Information Presentation hierarchy. |
| Visual semantic signifiers | Implemented globally | Continue under Information Presentation hierarchy. |
| Before/after code-change presentation | Not verified as migrated | Audit; likely detailed technical-response guidance rather than global invariant. |
| Interleave artifacts with explanation | Not verified as migrated | Audit placement. |
| Call-order arrows | Not verified as migrated | Audit placement. |
| Data/diagram-specific legacy rules | Only partially represented | Audit each rule; do not silently generalize KONUX-specific examples globally. |

Do not mark this audit complete until the original `format-markdown` source (or a complete recovered copy) has been compared rule-by-rule and every item is either promoted, deliberately rejected with rationale, or parked in an explicit destination.