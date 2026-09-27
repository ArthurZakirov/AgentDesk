# 🎙️ Continuous voice work orchestration

## Desired outcome

The user can keep speaking without waiting for research, edits, tests, or delegated work. Every meaningful request is durably captured before execution, can be split into independent work items, and remains recoverable even if the speaking/orchestrator session is interrupted, compacted, blocked, or restarted.

Default scheduling is FIFO, but explicit user priority commands can move an item ahead of older work. Independent items should run in parallel when safe. Work that changes state may prepare a plan first and pause at an approval gate when human review is required.

## Required invariants

- No accepted spoken request exists only in transient chat context; persist a durable intake record and receipt first.
- Separate intake from execution: the speaking coordinator must stay responsive while workers run.
- Preserve the original utterance/transcript plus a normalized task decomposition so details are auditable.
- Maintain explicit states such as captured, triaged, researching, planned, awaiting approval, executing, blocked, and done.
- Support one utterance producing multiple independent tasks with shared provenance.
- Support FIFO by default plus explicit priority/reordering commands from the user.
- Never treat creating a Goal, subagent, or stronger prompt wording as proof that responsiveness or persistence has been implemented.
- Worker completion must return through a durable event/status channel rather than relying on the coordinator to poll continuously.
- After restart or context compaction, reconcile open work from persistent state and surface unanswered decisions.

## Observed problem to investigate

In prior ChatGPT Desktop voice/subagent use, launching or monitoring delegated work could make the coordinator effectively non-responsive: speech entered during worker execution was sometimes not acted on until the user explicitly asked the coordinator to reread it. This is user-observed behavior, not yet a documented product contract. Treat it as a runtime behavior to reproduce and measure rather than something prompt wording can fix.
## Current research findings

- OpenAI currently documents Voice in Desktop as able to start tasks, check progress, ask about agents, and coordinate multiple agents through one conversation. Live can accept interruptions, but Voice transcripts are not guaranteed verbatim and only one Voice conversation can run at once.
- OpenAI documents Work Voice tasks as able to continue in text after the call ends, but does not document a durable FIFO intake queue or a guarantee that every utterance spoken while delegated work is active becomes a separately processed work item.
- `firstmate` implements a close architectural analogue: one liaison agent, isolated parallel workers, persistent on-disk state, event-driven supervision, and a voice relay that queues real work through one inbox owner with request-id deduplication and receipts.
- `firstmate` also documents an important boundary: its open-mic continuous-listening mode is not finished because reliable end-of-speech detection and interruption semantics are part of the hard problem. Its present voice relay deliberately separates speech/status from project mutation.
- `firstmate` does not currently expose Codex Desktop as a full runtime backend because it lacks a supported shell-callable create/send/read/archive bridge for the same visible Desktop-owned thread.

## Solution families to evaluate

The durable-intake invariant is more important than any one UI or orchestration pattern. Evaluate these families independently and in hybrids:

| Family | Routing model | Strength | Main risk / unknown |
| --- | --- | --- | --- |
| **Single voice orchestrator** | One conversation semantically splits requests and dispatches workers. | Lowest cognitive switching; matches firstmate-style liaison architecture. | Requires the coordinator surface to remain responsive and to persist intake before delegation. |
| **Fast switching between specialized voice chats** | The user explicitly selects the destination chat/context, potentially from phone/watch/headset controls. | Human routing avoids classifier mistakes and keeps contexts clean. | Current ChatGPT supports only one Voice conversation at a time; friction of ending/resuming/selecting chats may dominate unless a reliable shortcut/remote-control surface exists. |
| **Capture inbox, route later** | Phone/watch/headset captures a note immediately; an asynchronous router later assigns it to a chat, project, or worker. | Strongest separation of lossless capture from execution; can work even if an AI session is blocked. | Adds a custom inbox/transcription/routing system and delayed conversational feedback. |
| **Continuous recorder/transcription pipeline** | Always-on or push-to-talk audio is chunked/transcribed into a persistent event stream, then routed to agents. | Closest to uninterrupted thinking; independent of any one chat UI. | End-of-thought detection, interruption semantics, privacy, audio retention, and false task boundaries are hard. |
| **Multi-channel ingress / agent OS** | Voice, messaging, web, phone/watch shortcuts, and other surfaces all write into the same durable task/memory layer. | The user can pick the lowest-friction input surface moment by moment without changing the backend work model. OpenYabby and TaskChad OS are current examples of this architectural family. | More infrastructure and identity/routing policy; each ingress has different latency, privacy, and conversational affordances. |
| **Custom realtime voice client** | A purpose-built client uses a realtime speech API directly and writes every accepted turn to the durable inbox before any agent work starts. | Full control over interruption, receipts, hardware controls, routing commands, and rendering rather than inheriting one product's Voice UX. | Highest build cost; audio/VAD, device handoff, auth, background execution, and playback state become our responsibility. |

A likely hybrid is: **fast capture everywhere → durable inbox → optional human/automatic routing → independent workers → one notification/approval stream**. ChatGPT Voice, Work/Codex, specialized chats, messaging apps, a watch/phone shortcut, or a custom realtime client can all be ingress surfaces without being the system of record.

## Shared backend primitives

1. **Durable inbox** — append-only SQLite or JSONL event log with request id, raw transcript, normalized task(s), priority, dependencies, state, timestamps, and receipt.
2. **Intake router** — semantic splitter/classifier turns one utterance into one or more work items; explicit user-selected destinations bypass automatic routing.
3. **Scheduler** — FIFO among equal-priority ready items; explicit user commands can reprioritize, pause, cancel, or force-next.
4. **Workers** — terminal/cloud agents (Codex CLI, Agents API, Claude Code, OpenCode, firstmate-style workers, or another harness) in isolated worktrees or scoped environments.
5. **Event return channel** — workers update durable task state; coordinators read notifications instead of supervising through blocking waits.
6. **Human decision queue** — plans/irreversible actions become explicit approval items surfaced through whichever device is convenient.
7. **Recovery** — on startup/session refresh, reconstruct in-flight work and unanswered decisions from the durable store.

## MVP acceptance test

While two independent worker tasks are running, speak three additional requests without waiting. Verify that all three receive durable request ids immediately, remain visible after restarting the coordinator, execute in FIFO order unless one is verbally reprioritized, and no worker monitoring step prevents new capture. The test fails if any accepted utterance exists only in chat history or must be manually rediscovered later.

## Research sources

- OpenAI Help — ChatGPT Voice: https://help.openai.com/en/articles/20001274-chatgpt-voice
- OpenAI Help — ChatGPT Work and Codex: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- firstmate repository: https://github.com/kunchenguid/firstmate
- firstmate architecture: https://github.com/kunchenguid/firstmate/blob/main/docs/architecture.md
- firstmate voice relay: https://github.com/kunchenguid/firstmate/blob/main/docs/voice-relay.md
- firstmate Codex App backend boundary: https://github.com/kunchenguid/firstmate/blob/main/docs/codex-app-backend.md
