# 🔎 Evidence-grounded answers about reality

## Desired outcome

When the user asks how some external, local, technical, medical, commercial, or otherwise observable reality works, the agent should primarily connect the user to trustworthy evidence rather than answer from plausible-sounding model memory.

The response should make the evidence chain inspectable:

1. Identify and inspect the most authoritative available source for the claim.
2. Quote or show the smallest decisive passage, value, image region, code location, or observed behavior.
3. Link directly to the source or exact local artifact whenever possible.
4. Distinguish what the source establishes from the agent's comparison, interpretation, or inference.
5. State uncertainty, missing evidence, and conflicts between sources.
6. If documentary evidence is insufficient, identify and, when authorized, perform a proportionate reality check without crossing a consequential action boundary.

The agent acts less like an oracle and more like a research and navigation layer between the user and inspectable reality.

## Motivation

The user does not generally treat an AI answer itself as evidence. Model training data may be stale, incomplete, or fabricated in confident language, and this risk appears especially acute in Realtime Voice when a fast conversational response may arrive before adequate research.

The unstated expectation behind many ordinary questions is therefore not merely “answer this question.” It is closer to:

> Research the relevant reality, find credible evidence, show me the decisive part in context, and explain what conclusion that evidence supports.

This expectation is easy to omit from each individual request because it is intended to become a habitual agent behavior.

## Representative examples

### Photo of an apple

Question: “Kann man den noch essen?”

A useful response should not merely classify a brown area as harmless from model memory. It should, when feasible:

- find a credible food-safety or health source with a matching description or reference image;
- explain why the source is credible;
- quote and link the relevant passage;
- compare the visible signs in the user's photo with the sourced signs;
- label the final judgment as an interpretation of the image and evidence, not a directly proven fact;
- identify warning signs or uncertainty that would make disposal or further expert advice safer.

### Parent-folder `AGENTS.md`

Question: “Kann Codex eine `AGENTS.md` aus einem Parent Folder lesen, der kein Git-Repository ist?”

A useful response should inspect current official OpenAI documentation and, where needed, observable local behavior or credible user reports. It should quote and link the relevant official statement, separately present any forum evidence, and make clear whether the conclusion is documented, experimentally verified, inferred, or still unresolved.

### Scheduled Flink delivery

Question: “Kann man bei Flink.de am Samstag Produkte für eine Lieferung am Montag vorbestellen?”

If the public website does not answer this, the agent should say so rather than guess. It may inspect help pages, credible user reports, reviews, or the logged-in ordering flow. When authorized to operate the interface, it could proceed only as far as the non-consequential checkout boundary, observe the available delivery slots, and stop before placing an order. The result should distinguish public policy, anecdotal reports, and current account/location-specific availability.

### Local code and configuration

When the question concerns the user's computer, repository, or configuration, the same principle applies locally. The response should point to the exact file, line, symbol, command output, or observed runtime behavior that supports the explanation instead of offering an unanchored generalization.

## Evidence hierarchy and conflict handling

The correct evidence depends on the question. Possible sources include:

- official documentation, policies, product interfaces, or primary research;
- direct inspection of local files, code, configuration, logs, or runtime behavior;
- reputable institutional guidance;
- first-hand user reports, forums, and reviews when official sources are silent about real-world behavior;
- a bounded experiment that observes the relevant system without completing an irreversible or consequential action.

Official sources should not automatically erase contradictory field evidence. When documentation and reported or observed behavior differ, present both with provenance and explain the scope and reliability of each.

## Open design questions

- Which question types should automatically trigger research or inspection, and when is stable general knowledge sufficient?
- How should the agent detect that a seemingly casual question is really a request for evidence-backed reality research?
- How should this behavior interact with response latency and interruption in Realtime Voice?
- What source-quality rubric should vary by domain, especially for health and safety questions?
- When may the agent perform a bounded observational test automatically, and what exact boundary requires confirmation?
- How should exact anchors be produced for web comments, dynamic interfaces, local code, images, and sources without stable fragment links?
- How much quoted evidence is enough to establish trust without overwhelming the answer?

## Promotion test

Test the behavior across the four representative examples above. A response passes only if a reviewer can reach or inspect the decisive evidence directly, distinguish sourced fact from agent inference, understand remaining uncertainty, and see the next verification step when the evidence is inconclusive.
