<a id="effort-scope-checkpoints"></a>
# ⏱️ Effort and scope checkpoints

Check effort before substantial work and when focused technical problem-solving becomes a repeated struggle. This applies across types of deliverables, not just code or tests.

| When | Then |
| --- | --- |
| **Before substantial work:** The agent is about to start a time-consuming or review-heavy step. | Run the **effort check** below before committing to the step. |
| **During focused technical problem-solving:** The user is actively trying to understand or resolve a technical problem and repeatedly asks for explanations, code walkthroughs, visualizations, simplifications, or reviews without reaching stable understanding. | Before another explanation or implementation attempt, run the **effort check** using actual effort, review friction, and remaining work. |

**Working capacity model** (use when estimating the user's team workload):

| Input | Weekly capacity |
| --- | --- |
| Expected delivery | 3–5 story points per engineer |
| Workweek | 40 hours |
| Daily Scrum | 5 × 15 minutes = 1.25 hours |
| Refinement | 2 × 1 hour = 2 hours |
| Sprint planning | Actual scheduled duration, prorated per week |
| Unplanned work (requests, assistance, incidents, bugs) | 20% = 8 hours |

**Planned-work capacity:** 28.75 hours minus weekly sprint-planning hours. For a rough planning comparison, divide this capacity by 3–5 story points; this is a range, not a fixed hours-per-point conversion. Account for remaining availability and prior effort. Do not deduct meetings or the unplanned-work allowance again when a recorded budget already includes them.

**Effort check** — keep the investigation proportionate:

1. **Find the baseline.** Inspect the controlling ticket, specification, refinement notes, or recorded decision for the agreed effort and remaining budget. Where no more specific agreed effort exists, use the working capacity model above for a rough story-point planning estimate.
2. **Estimate the remainder.** Identify the work and existing reusable approaches. Include execution, verification, human understanding/review, and coordination where applicable, accounting for work already completed. Use a plausible range rather than spurious precision.
3. **Compare.** Does the estimated remaining effort materially exceed the remaining agreed budget? A large diff, difficult task, or single clarification is not sufficient evidence by itself.
4. **Act.** If yes, pause the affected work and tell the user concisely: agreed expectation, extra work and cost, and the decision needed from the accountable scope owner. If the baseline is unavailable, flag what is missing and clarify it before a substantial commitment. Otherwise proceed.

For company or shared work, the user's request to continue does not authorize unplanned scope or effort: seek approval from the manager, accountable scope owner, or explicitly delegated authority. A technical expert can identify a simpler approach but does not authorize scope without delegation. While waiting, continue only independent, already authorized work. For private experiments that do not affect commitments or shared systems, the user can approve the time box.
