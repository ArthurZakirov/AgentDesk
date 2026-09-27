# 🧱 Layered global guidance

AgentDesk can render one base manifest plus zero or more ordered overlay manifests into one generated `AGENTS.md` and one sibling `agents-md-references/` directory.

The base layer remains usable by itself. Overlays live in their own directories or repositories and are read in place; the generator never copies overlay sources into AgentDesk.

## Manifest contract

The base manifest is passed with `--manifest`. An overlay is passed with a repeatable `--overlay-manifest` argument and must declare a portable, unique `layer_id`:

```yaml
version: 2
layer_id: example-overlay
components:
  - path: agents-md-components/example.md
```

Component paths and the optional `agents-md-references/` directory are resolved relative to the manifest that owns them. Every reference filename becomes its destination filename, so two layers may not provide the same reference name. Heading anchors and `layer_id` values must also be unique.

## Render safely

Use explicit temporary harness homes for validation:

```bash
temp_root="$(mktemp -d)"
uv run python scripts/regenerate-agents-md.py \
  --overlay-manifest /path/to/overlay/agents-md-manifest.yaml \
  --codex-home "$temp_root/.codex" \
  --claude-home "$temp_root/.claude" \
  --opencode-home "$temp_root/opencode"
```

For a dry-run against an intended destination, add `--dry-run`. A first transition between base-only and layered ownership fails closed unless the caller explicitly supplies `--replace-existing` after review.

## Ownership and safety

- AgentDesk is the source of truth for the base layer and the composition implementation.
- Each overlay repository is the source of truth only for its own manifest, components, and references.
- A layered output contains an opaque layer-set marker. A different layer set cannot silently overwrite it.
- Reference destination conflicts, duplicate anchors, duplicate manifests, missing inputs, and duplicate layer IDs stop before output is written.
- The destination must have one apply owner. Do not run base-only and layered writers against the same target.
- Keep credentials, personal facts, and other data outside guidance overlays.

## Verification

Regenerate the current test result with:

```bash
uv run pytest -q tests/test_layered_agents_md.py tests/test_agents_md_preview.py
```

The checked-in shared preview remains the regression proof that base-only rendering has not changed.
