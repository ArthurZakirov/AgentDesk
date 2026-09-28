# ChatGPT product configuration

This directory versions ChatGPT-specific configuration that is manually applied in the ChatGPT product rather than generated into harness-level `AGENTS.md` files.

## Files

- [`personalization-instructions.md`](personalization-instructions.md): canonical text for ChatGPT Personalization / custom instructions.

## Ownership boundary

- `chatgpt/` owns manually applied ChatGPT product configuration.
- [`global-guidance/`](../global-guidance/) owns generated cross-harness agent guidance.
- [`skills/`](../skills/) owns AgentDesk skill sources.

Changes here are versioned source changes. They do not automatically update the user's ChatGPT settings; deployment is a manual copy/paste unless a supported product automation is added later.
