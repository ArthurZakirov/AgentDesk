# 🧭 Orchestrator chat discoverability

## Desired outcome

The user can immediately find and resume the human-facing orchestrator chat even when Codex or ChatGPT has created many delegated chats. Worker chats should remain available for audit or troubleshooting without competing visually with the conversations the user intends to continue.

The important distinction is the chat's **interaction role**, not merely whether it was technically created by a subagent mechanism:

- **Orchestrator** — the user-facing conversation that owns the overall outcome, decisions, and synthesis.
- **Delegated worker** — a separate chat created to perform a bounded subtask whose details normally return to the orchestrator.
- **Standalone** — an ordinary chat that is neither the coordinator nor a delegated child.

## Promotion status

The default title prefix for separate user-visible delegated worker chats has been behaviorally validated and promoted to [Delegation](../agents-md-components/runtime-and-interaction/delegation.md). The broader grouping, provenance, notification-routing, and lifecycle requirements in this wishlist entry remain under investigation.

## Observed problem

The current sidebar presents orchestrator and delegated worker chats as similar peer records. Completed workers can leave several unread indicators, so recent activity and unread state amplify low-value threads while the orchestrator becomes harder to locate. Titles usually describe the task but do not reliably expose the interaction role. In the inspected thread data, the blue-dot condition is represented as `isUnread`; it is not itself a semantic “completed” status.

The user's September 2026 screenshot shows several similarly styled recent chats with blue unread dots and no visible, consistent orchestrator-versus-worker marker. This screenshot is evidence of the experienced navigation problem, not proof of the underlying implementation or parent-child relationships.

## Required experience

- Make orchestrators visually recognizable without opening each chat.
- Keep delegated workers out of the primary attention stream by default.
- Route worker completion, required input, and meaningful failures back to the orchestrator instead of requiring the user to visit each worker.
- Preserve worker chats for drill-down when their transcript matters.
- Support Codex and ChatGPT Work chats, including delegated chats that are technically ordinary peer chats rather than native subagent threads.
- Avoid depending solely on title wording when stronger structured metadata or grouping is available.
- Keep role, unread state, execution status, and attention-required state conceptually distinct.

## Current research findings

Research snapshot: 2026-09-27. Refresh the product evidence by reopening the linked official documentation under [Research sources](#research-sources). Refresh the locally exposed sidebar capabilities and thread fields by invoking the Codex app's `list_threads` operation and comparing its schema with the claims below; product behavior may change after this snapshot.

### What the product already supports

- ChatGPT Desktop supports renaming, pinning, archiving, searching, and keyboard navigation between chats. OpenAI explicitly recommends pinning chats that are revisited often and archiving finished work.
- Codex exposes a “next chat needing attention” command and a command to clear all unread indicators. These reduce notification friction but do not distinguish orchestration roles.
- The September 2026 app changelog says delegated task titles were made clearer and adds a “Needs input” state, but it does not document a user-configurable role prefix, automatic parent grouping, or an “orchestrators only” filter.
- The current Codex app integration can rename chats, pin or move them into custom sidebar sections, change read state, archive them, and choose sidebar grouping/sorting. This establishes that the UI has useful actuators.
- The current thread-list representation exposes title, summary, source, status, project, host, timestamps, and unread state, but no documented parent thread, creator thread, or orchestrator/worker role. Therefore reliable classification after creation cannot be assumed from the current list response alone.

### Consequence

A title prefix is a useful fallback, but the durable solution should capture provenance and role **when a delegated chat is created**. Reconstructing the relationship later from similar titles, timestamps, or summaries is inherently brittle.

## Solution hierarchy

| Priority | Mechanism | Why it helps | Limitation |
| --- | --- | --- | --- |
| 1 | **Structured role and parent metadata** | Lets the product group, filter, collapse, and route notifications without parsing titles. | Requires product/runtime support or a durable external registry. |
| 2 | **Automatic sidebar routing** | Keep orchestrators in a prominent `🧭 Orchestrators` section and delegated workers in a collapsed `⚙️ Delegated` section. | Depends on recognizing the relationship at creation time. |
| 3 | **Attention routing** | Worker completion updates the orchestrator; only required input or failure creates a user-facing alert. | Requires event propagation between chats. |
| 4 | **Naming convention** | Provides an immediately scannable fallback on every surface. The validated default prefix is `[DELEGIERT]` for separate user-visible delegated worker chats; orchestrator and ordinary chat titles remain unchanged. | Titles are mutable, can be truncated, and do not encode a robust relationship by themselves. |
| 5 | **Pin/search/archive workflow** | Available now: pin orchestrators, search them, and archive completed workers. | Mostly manual and treats symptoms rather than provenance. |

## Proposed naming fallback

Use `[DELEGIERT] <topic or outcome>` only for a separate user-visible chat created by an orchestrator to perform worker work. Keep the user-facing orchestrator and ordinary standalone chats on their normal topic- or outcome-based titles. Native internal subagent threads do not receive this sidebar-chat prefix.

Do not encode completion in the title. Completion, unread, blocked, and needs-input are changing states and belong in status indicators or notifications rather than durable names.

## Candidate behavior to design and validate

When an orchestrator creates a separate delegated chat:

1. Record the child id, parent id, role, and intended notification policy at creation time.
2. Rename the child immediately with the delegated-worker marker.
3. Move it into a dedicated delegated-work section or otherwise collapse it under its parent.
4. Keep normal completion quiet in the worker's sidebar record and summarize it in the orchestrator.
5. Surface the child directly only when it needs user input, fails, or the user asks to inspect it.
6. On completion, archive it automatically only if the transcript remains reachable from the orchestrator and the user has chosen that retention policy.

The mechanism must be tested independently for native subagent threads, Codex tasks created through chat-management tools, ChatGPT Work delegation, forks, and side chats. These surfaces may not share the same provenance fields or notification behavior.

## Immediate workaround

Until automatic provenance-aware organization exists:

1. Pin active orchestrator chats or place them in a dedicated custom sidebar section.
2. Name any intentionally created separate delegated worker chat with `[DELEGIERT]` at creation time; leave orchestrator and ordinary chat titles unchanged.
3. Archive finished worker chats after their result has been incorporated into the orchestrator.
4. Use chat search for the role marker or a remembered phrase, and use the app command for the next chat needing attention when triaging genuine blockers.
5. Clear unread indicators after reviewing the orchestrator's synthesis when the remaining dots are only worker-completion noise.

This workaround improves scanning but does not solve automatic classification for chats whose origin was not captured.

## Acceptance test

Start one orchestrator that creates at least five delegated chats, with three completing normally, one failing, and one requesting input. The experience passes when:

- the orchestrator remains identifiable and reachable without opening candidate chats;
- normal worker completions do not flood the primary unread/attention stream;
- the failure and input request are visible from the orchestrator with direct drill-down links;
- every worker remains auditable and its parent can be determined reliably;
- renaming, app restart, and cross-device sync do not destroy the relationship; and
- the behavior works without inferring roles from natural-language titles after the fact.

## Open questions

- Does the internal thread model already retain delegation provenance that is merely absent from the current list surface?
- Can ChatGPT Work delegation invoke the same rename, section, read-state, and archive actuators as Codex-created chats?
- Should completed workers be auto-archived, collapsed beneath the parent, or retained in a dedicated section?
- Can worker completion avoid unread state while `needs input` and failure still demand attention?
- Should an orchestrator be pinned automatically only while it has active children?
- How should a worker with meaningful direct user interaction be promoted to a standalone or orchestrator role?

## Research sources

- [Projects and chats — organize, pin, rename, search, and archive chats](https://learn.chatgpt.com/docs/projects?surface=app)
- [ChatGPT Desktop keyboard commands — rename, pin, archive, search, clear unread, and navigate to attention](https://learn.chatgpt.com/docs/reference/commands)
- [ChatGPT and Codex changelog — clearer delegated task titles and Needs input status](https://learn.chatgpt.com/docs/changelog)
- [Developer commands — rename, archive, native subagent threads, forks, and side chats](https://learn.chatgpt.com/docs/developer-commands)
- [Use ChatGPT — ChatGPT Work delegation and Codex/Desktop distinctions](https://learn.chatgpt.com/docs/use-chatgpt)
