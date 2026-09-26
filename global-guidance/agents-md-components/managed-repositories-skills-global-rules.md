<a id="managed-rules"></a>
# 🧰 Managed repositories, skills, and global rules

## Working across physical computers

**When**

- Using or refreshing a repository on another physical computer.

**Then**

- Treat that computer as an independent checkout state.
- Inspect local changes and divergence before receiving committed changes, and use a safe fast-forward/update path that preserves local work.

## Editing managed skills

**When**

- Creating or modifying a managed skill.

**Then**

- Edit only the canonical repository `skills/` source, never a generated global installation or legacy alias.
- Review, validate, commit, and push the repository source before refreshing generated installations.

## Refreshing installed skills

**When**

- Updating generated skill installations on a machine.

**Then**

- Use SkillPort's documented maintenance flow and the canonical registry's selected skill subset.
- Treat generated installs as per-OS outputs, not independent editing sources.

## Editing global agent rules

**When**

- Creating or changing global agent guidance.

**Then**

- Edit the canonical components declared by `agents-md-manifest.yaml`, not generated global `AGENTS.md` output.
- Preserve and reconcile existing non-generated guidance before a first replacement.

## Adding or supporting another agent harness

**When**

- Adding support for another harness or agent product.

**Then**

- Keep canonical storage harness-neutral and avoid creating another editable copy of skills.
- Verify that harness's actual skill-discovery and global-rule conventions instead of assuming universal paths or import syntax.

## Deciding repository or data boundaries

**When**

- Deciding repository ownership, publication/privacy boundaries, or where reusable personal context belongs.

**Then**

- Read [agents-md-references/repository-routing-and-data-boundaries.md](agents-md-references/repository-routing-and-data-boundaries.md) before deciding.

## Processing personal documents or data files

**When**

- Downloading, creating, editing, merging, converting, signing, scanning, exporting, or otherwise processing personal documents or personal data files, including PDFs, CSVs, spreadsheets, or bank exports.

**Then**

- Read [agents-md-references/personal-document-workflow.md](agents-md-references/personal-document-workflow.md) before acting.
