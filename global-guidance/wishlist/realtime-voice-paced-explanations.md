# 🎧 Realtime Voice paced explanations

## Desired outcome

In Realtime Voice, when an explanation requires the user to inspect something, learn unfamiliar terminology, follow a multi-file code path, or otherwise spend significant attention on each step, the agent should switch to an interactive micro-step mode.

It should give one cognitively actionable unit, then stop speaking. The user inspects, thinks, asks a question, or confirms readiness before the agent continues. This behavior is specifically intended for Realtime Voice; normal text chat can continue to present a complete, well-structured explanation unless the user asks otherwise.

## Interaction shape

A useful opening could be:

> Das ist ein komplexerer Zusammenhang. Ich gehe mit dir in kleinen Schritten durch und pausiere nach jedem Schritt, damit du nachschauen oder nachfragen kannst.

Then the agent should provide only the next unit required for progress, such as:

> Öffne `infra/main.tf` und gehe zu Zeile 37. Sag mir Bescheid, sobald du dort bist.

It should stop there. After the user confirms, it can direct attention to the next location or explain one relationship. It should again stop rather than preload later steps that the user cannot yet process.

## Why this matters

In live speech, the user may encounter an unfamiliar term in the first sentence or may need to navigate to a file and inspect a symbol. While doing that, later spoken sentences are effectively lost. A five-sentence explanation is therefore not merely verbose; it can be unusable even when every sentence is correct.

This has occurred in several kinds of discussion:

- tracing code across Terraform files, functions, call sites, folders, and line numbers;
- discussing a paper by Engelbart;
- discussing vaccinations and unfamiliar medical terminology;
- any explanation in which the user must visually locate evidence or resolve a concept before the next relationship makes sense.

Repeated “Stopp, stopp, stopp” interruptions in prior ChatGPT conversations may provide diagnostic examples of where the conversational pacing exceeded the user's available attention. These chats should be researched during design rather than assuming the transcript description alone captures every failure pattern.

## Adaptive trigger

The behavior should depend on cognitive demand, not merely explanation length. Signals may include:

- a new technical, scientific, or domain-specific term that may need clarification;
- a request to navigate to or visually inspect a file, line, function, diagram, image, or interface;
- a causal chain whose later step depends on understanding the earlier one;
- a multi-location code flow that the user is following manually;
- evidence that the user is currently operating another interface while listening;
- the user's use of “Stopp,” requests to slow down, or questions about the first part of an unfinished explanation.

Ordinary conversational answers that do not impose this attention cost should remain natural and need not be reduced to one sentence at a time.

## Micro-step contract

When the mode is active:

1. Announce the paced interaction briefly when that helps set expectations.
2. Give one instruction, concept, observation, or relationship at a time.
3. Stop speaking after the unit; do not append “while you do that” explanations.
4. Let the user control continuation through confirmation or a follow-up question.
5. Answer the follow-up at the current layer before returning to the larger flow.
6. Preserve the larger explanation state so the thread can resume without losing the path.
7. Increase chunk size only when the user's responses show that the material no longer requires micro-steps.

## Open design questions

- What reliable runtime signal distinguishes Realtime Voice from dictated text or ordinary chat?
- What is the right unit: one sentence, one concept, one visual action, or one dependency edge?
- How should the agent pause technically so it genuinely yields the floor instead of immediately continuing?
- Can historical “Stopp” moments be retrieved and classified to derive better triggers and chunk sizes?
- How should the agent remember the pending explanation path across interruptions and tangential questions?
- When should it ask whether the user wants micro-step mode versus entering it automatically?
- How should citations and source inspection work when the user is listening rather than reading?

## Promotion test

Run live tests for a Terraform call-flow explanation, a paper discussion, and a medical-term explanation. The behavior passes only if the user can locate or understand each unit before the next begins, interrupt with a question without losing the overall path, and complete the explanation without needing repeated “Stopp” corrections.
