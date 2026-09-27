# Agent guidance wishlist

This directory is the canonical backlog for **problem-space intent**: desired agent, computer, workflow, or broader-system behavior that matters but is intentionally **not active global guidance yet**.

Wishlist content is not evidence that the behavior is implemented. Items stay here until the relevant runtime mechanics, scope, reliability needs, and verification path are understood.

## Lifecycle

| State | Meaning |
| --- | --- |
| Captured | The desired outcome is recorded without pretending the mechanism already exists. |
| Investigating | Sensors, observables, triggers, actuators, runtime surfaces, risks, and existing solutions are being researched. |
| Designed | A concrete mechanism and verification plan exist, but production changes are not yet validated. |
| Validated | The mechanism has been implemented and tested successfully. |
| Promoted | Human-reviewed behavior has moved into the correct production surface; the wishlist entry is removed or marked as historical. |

Promotion means using `engineer-agentic-ai` to convert intent into a tested mechanism, then moving only the validated production rule/control into the appropriate canonical source. This directory must never be included directly in generated `AGENTS.md` input.

## Topics

- [Evidence-grounded answers about reality](evidence-grounded-reality-answers.md)
- [Problem intent before a proposed solution](problem-intent-before-proposed-solution.md)
- [Realtime Voice paced explanations](realtime-voice-paced-explanations.md)
- [Concrete examples and exemplification](concrete-examples-and-exemplification.md)
- [Continuous voice work orchestration](continuous-voice-work-orchestration.md)
- [Browser execution and responsive coordination](browser-execution-and-responsive-coordination.md)
- [Collaboration and coding preferences](collaboration-and-coding-preferences.md)
- [Repository layout and GitHub defaults](repository-layout-and-github-defaults.md)
- [Personal skills source of truth](personal-skills-source-of-truth.md)
- [macOS overlay wishes](macos-overlay-wishes.md)
- [Windows and WSL overlay wishes](windows-wsl-overlay-wishes.md)
- [Validation questions](validation-questions.md)
