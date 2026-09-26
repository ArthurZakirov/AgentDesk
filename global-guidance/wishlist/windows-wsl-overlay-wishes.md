# 🪟 Windows and WSL overlay wishes

These platform-specific rules are parked here and are intentionally not active global guidance. Promote individual rules only after their need and runtime behavior are deliberately validated.

- Windows owns the canonical editable checkouts. WSL accesses those same physical directories through its mounted Windows filesystem; never create a second editable WSL clone or use Git push and pull to transfer changes between two views of one checkout.
- Legacy WSL paths may remain compatibility links only after their targets are verified. They are aliases, not additional canonical repositories.
- Use the native Windows paths supplied by the permission-restricted machine configuration. Never copy concrete checkout paths into shared guidance.
- The global Codex `AGENTS.md` is a concrete file generated from the common rules and this overlay because bare `@` references are not a Codex import mechanism. Do not edit the generated file.
- SkillPort's native Windows scheduled task owns unattended safe refresh, guidance composition, and remote skill installation. Operational PowerShell and `npx.cmd` commands live in SkillPort documentation rather than in this guidance.
- WSL and Windows generated skill installations are separate runtime outputs even though their editable sources are shared. Verify discovery in the runtime that will consume them.
