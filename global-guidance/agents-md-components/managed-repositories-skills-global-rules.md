<a id="managed-rules"></a>
# 🧰 Managed repositories, skills, and global rules

- Treat every physical computer as an independent checkout state. Use that computer's safe Git refresh to receive committed changes. Inspect local changes and divergence first and never discard local work.
- Edit managed skills only in the canonical repository `skills/` directory, never in generated global installations or legacy aliases. The repository source must be reviewed, validated, committed, and pushed before generated installations are refreshed.
- Generated skill installs are per operating system and are not independent editing sources. Use SkillPort's documented maintenance commands and the canonical registry's explicit skill subset; do not duplicate operational commands in this guidance.
- Global rules are composed from the ordered files declared in `agents-md-manifest.yaml`. Edit those canonical component sources, not the generated global `AGENTS.md`.
- Preserve and reconcile existing global instructions before first replacement. SkillPort's composer backs up non-generated prior guidance and updates later generated output atomically.
- Keep storage harness-neutral. Adding a harness must not create another editable copy of skills. Check its supported skill discovery and global-rule conventions rather than assuming one universal path or import syntax.
- Before deciding repository ownership, publication/privacy boundaries, or where Arthur's reusable personal context belongs, read [agents-md-references/repository-routing-and-data-boundaries.md](agents-md-references/repository-routing-and-data-boundaries.md).
- Before downloading, creating, editing, merging, converting, signing, scanning, exporting, or otherwise processing Arthur's personal documents or personal data files (including PDFs, CSVs, spreadsheets, or bank exports), read [agents-md-references/personal-document-workflow.md](agents-md-references/personal-document-workflow.md).
