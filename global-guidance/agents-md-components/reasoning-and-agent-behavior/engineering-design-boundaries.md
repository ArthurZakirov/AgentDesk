<a id="engineering-design-boundaries"></a>
# 🧱 Engineering design boundaries

Apply these standards when writing or reviewing code, tests, scripts, configuration, and reusable instructions:

- **Separate concerns by change boundary.** Keep reusable logic and durable rules apart from runtime data, environment configuration, temporary observations, and entry-point mechanics.
- **Make choices and dependencies explicit.** Expose behavior-affecting inputs at the boundary where they vary. Require inputs where no meaningful default exists. Name domain concepts and policy values rather than burying decisions inside implementations.
- **Honor real contracts.** Fail clearly on invalid or missing required values instead of inventing substitutions or silent fallbacks. Retain compatibility for actual consumers, published interfaces, or persisted data—not unshipped branch-local history.
- **Prefer justified simplicity.** Choose the smallest coherent design, not necessarily the smallest edit. Avoid hidden hardcoding, speculative future support, and mechanical abstraction or injection without a real reason.

For deeper reasoning and cross-domain examples, use the [SystemSmith `software-design` skill](https://github.com/ArthurZakirov/SystemSmith/blob/main/skills/software-design/SKILL.md) when installed. The principles above remain applicable even when that skill is unavailable.
