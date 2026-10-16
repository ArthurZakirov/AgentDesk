<a id="unresolved-implementation-decisions"></a>
# 🧩 Unresolved implementation decisions

| When | Then |
| --- | --- |
| A change depends on unanswered requirements, domain rules, interface contracts, or stakeholder decisions. | Resolve material uncertainty **before implementing dependent behavior**. Follow the steps below. |

1. **Investigate first.** Check available specifications, documentation, prior decisions and chats, code, tests, and other relevant evidence.
2. **Surface the missing decision.** If uncertainty remains, give the user the precise question and relevant evidence so **the user can consult the accountable person**. Do not contact stakeholders on the user's behalf.
3. **Do not implement guesses.** Avoid provisional implementations, speculative branches, or abstractions covering possible answers. Support multiple outcomes only when that flexibility is itself a confirmed requirement.
4. **Continue independent work.** Pause only implementation that depends on the missing answer. Implement a confirmed subset only if it is useful independently and future additions are strictly additive without rework.
5. **Keep routine choices autonomous.** Resolve ordinary engineering details using evidence and established conventions; do not manufacture stakeholder approvals.
