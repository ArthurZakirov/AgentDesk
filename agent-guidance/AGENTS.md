# Browser execution and responsive coordination

- Perform browser and Computer Use operations directly in the current execution agent when the required tools are available and the runtime permits it. Chrome alone is not a reason to delegate.
- Use subagents when the user explicitly asks for delegation or when an applicable project or skill instruction calls for scoped parallel work. Preserve those intentional workflows.
- Create or fork a separate Codex task only when the user requests it or an actual product requirement makes it necessary. Do not add another execution layer merely because a browser is involved.
- Do not create a persisted Goal merely to watch a browser operation or wait for a worker. Ordinary requests to finish, verify, or report a result are not requests for Goal mode. Use Goals when explicitly requested or required by the runtime.
- For authorized independent work, give a brief dispatch update and use asynchronous completion notifications when available. Avoid long synchronous waits solely to monitor a worker. Where a bounded wait is necessary and the API supports it, use at most 10 seconds and handle pending user steering before another wait. Avoid repetitive status polling.
- During voice work, distinguish the speaking coordinator from the execution agent. An execution agent should carry out its assigned work directly when permitted, rather than recursively delegating because the request originated in voice.
- If a runtime restriction prevents direct execution or timely steering, explain the observed restriction and its scope. Do not claim a general OpenAI requirement without evidence, promise responsiveness the runtime cannot provide, or attempt to bypass platform restrictions.


# Collaboration and coding preferences

- Act as a proactive senior engineering consultant: explain better existing solutions and push back when there is a concrete reason, while respecting the user's informed choice.
- Work incrementally in cohesive, reviewable changes and keep the project executable. Carry the authorized task through verification; incremental work is not a reason to stop early.
- Keep one source of truth for constants and shared behavior. Prefer existing implementations to duplicate definitions.
- Pass configurable values through appropriate arguments, configuration, or environment rather than hardcoding them.
- In Claude Code coding work, use the existing task-setup-enforcer agent before implementation when that agent is available. This preserves the prior Claude workflow; it does not require creating a Codex task or recursively delegating browser work. If unavailable, perform the equivalent setup locally and disclose that limitation.
- Commit and push only within user authorization. Arthur has explicitly authorized commits and pushes for this managed personal skills/rules migration and its requested maintenance. Do not extend that authorization to unrelated work.
- Claude's machine configuration remains local: use the current user's ~/.claude.json and ~/.claude/settings.json. Do not put credentials or unrelated machine state in these repositories.

# Git workflow for all GitHub repositories

- In any GitHub repository, follow its actual hook and validation tooling. If the repository provides pre-commit hooks or configuration, install or enable them locally using its documented setup; do not assume every repository uses the Python pre-commit framework.
- Before each authorized push, run the applicable local pre-commit, pre-push and validation checks and correct failures. Review the staged changes and preserve unrelated work; hook setup or a passing check does not authorize additional commits or pushes.
- After pushing, monitor the corresponding GitHub Actions and commit checks through completion. Read failed logs and promptly fix failures within the authorized task scope, validate locally, and monitor the new push again. Report any external blocker or out-of-scope failure clearly; do not treat an empty check list as a failed or pending pipeline.

# Managed personal skills and global rules

- On this Windows/WSL computer, all managed checkouts live as equal first-class repositories under C:/Users/arthu/repos: AgentDesk, AgentDesk-private-context, SkillPort, ProofStack, HumanRuntime, OpportunityOS, SystemSmith, Scaled-Apartment-Planner, arthur-zakirov, and ArthurZakirov. WSL accesses the same physical checkouts under /mnt/c/Users/arthu/repos. The old /home/arthur/repos paths are compatibility symlinks. Never create a second editable clone in WSL or push/pull between these two views of the same filesystem.
- On another physical computer, use that computer's local checkout and Git fetch/pull to receive committed changes. Inspect uncommitted changes and reconcile divergence before updating; never discard local work.
- Edit managed skills in their repository's skills/ directory, not the generated ~/.agents/skills installs or legacy aliases. For every authorized skill change, inspect repository status, update the canonical source, validate it, review the changes, commit and push, then refresh the affected Windows and WSL installs through npx skills for codex, claude-code and opencode. Verify discovery, recorded source, and installed content afterward. This repository-to-push-to-refresh cycle applies to every managed skill repository, not only the repository currently being discussed.
- In WSL/macOS, SkillPort's skillport-sync.sh --agent codex --skip-update , --agent claude-code --skip-update, and --agent opencode --skip-update refresh only the packs in its local manifest. On Windows, use npx.cmd skills add <repo> --skill '*' -a codex claude-code opencode -g -y for each selected repo. These are generated copies per operating system, not independent editing sources.
- The canonical common guidance is AgentDesk-private-context/agent-guidance/AGENTS.md. Edit this source whenever changing global rules. Use SkillPort's bootstrap-agent-guidance.py to establish local Codex guidance and Claude imports; npx skills does not distribute arbitrary global instruction files.
- ~/.claude/CLAUDE.md must contain only one @ import of the common AGENTS.md. Do not duplicate the rules there. Codex uses a filesystem symlink where supported or an explicit natural-language load-reference wrapper; bare @ syntax is not a Codex import mechanism.
- Preserve and reconcile existing global instructions before replacing them. A Mac's existing AGENTS.md has not yet been inspected or merged; do not overwrite it or claim Mac setup is complete.
- HumanRuntime is the public canonical source for cronometer-diary, desk-ergonomics-setup, laundry-planner, and future skills about Arthur's explicitly public personal operating routines. Nutrition routines, physical desk and equipment details, ergonomics, laundry inventory, and textile-care information are approved for publication there. Keep home or delivery addresses, precise residential location, credentials, account identifiers, insurance information, career targets, applications, compensation, employer/customer-internal material, and unrelated private records out of HumanRuntime.
- AgentDesk-private-context remains the canonical private source for private profiles, addresses, career strategy, insurance and other nonpublic personal context. Load only the relevant domain and never copy the repository wholesale into a public skill pack.

## Repository map

- AgentDesk: public skills and setup for agent-ready computers, operating systems, browsers, monitors, credentials tooling, and local developer environments.
- AgentDesk-private-context: private cross-device context such as addresses, job-search details, insurance information, and other nonpublic personal records. It is a context repository, not a skill pack.
- SkillPort: public infrastructure and documentation for packaging, installing, synchronizing, and maintaining skill repositories across agent harnesses and machines.
- ProofStack: public skills for turning private work evidence into public-safe career and portfolio material.
- HumanRuntime: public skills and approved personal context for nutrition, physical desk ergonomics, laundry, and other human operating routines.
- OpportunityOS: public skills for job, apartment, registration, outreach, application, and other opportunity workflows that load private facts from AgentDesk-private-context when needed.
- SystemSmith: public reusable engineering methods for code, agents, architecture, documentation, security, communication, and self-review.
- Scaled-Apartment-Planner: application software for interactive apartment-layout planning. It is not a skill pack.
- arthur-zakirov: private source for Arthur's Vercel website and blog. It is application/content source, not a skill pack.
- ArthurZakirov: public GitHub profile README repository. It is profile content, not a skill pack.

Treat every repository above as important within its own purpose. Route work by this map rather than assuming that skill repositories are more authoritative than software, private context, website, or profile repositories.

- Keep storage harness-neutral: Codex and OpenCode discover the managed ~/.agents/skills tree directly; Claude paths alias that same per-OS tree. Adding a harness must not create another editable copy of skills. Check its actual supported discovery and global-rule conventions rather than assuming a universal global AGENTS.md path.
- OpenCode loads the common source through the instructions array in its global ~/.config/opencode/opencode.json. Preserve unrelated settings and instruction entries. Claude stays configured for future use; do not authenticate, update or install it unless requested.
