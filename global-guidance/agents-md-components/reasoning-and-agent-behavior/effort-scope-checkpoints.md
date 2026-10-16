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

1. **Find the baseline.** Inspect the controlling ticket, specification, refinement notes, or recorded decision for the agreed effort and remaining budget. For team tickets without a more specific agreed effort, use the working capacity model above for a rough story-point planning estimate.
2. **Estimate the remainder.** Identify the work and existing reusable approaches. Include execution, verification, human understanding/review, and coordination where applicable, accounting for work already completed. Use a plausible range rather than spurious precision.
3. **Compare.** Compare estimated remaining effort with the remaining agreed budget and scope. Proceed if they still fit. A large diff, difficult task, or single clarification is not sufficient evidence of an overrun.
4. **Clarify with stakeholders.** If the baseline is missing or the expected work materially exceeds the agreement, pause the affected work. Present the original expectation, revised effort (including human review), trade-offs, and the decision needed. Ask the relevant stakeholder rather than silently expanding scope.
5. **Evaluate stakeholder input.** Determine what each response actually validates using the table below. Resume affected work only when existing acceptance criteria cover it or the appropriate authority approves the deviation. While a decision is pending, continue only independent, already-authorized work. Assess the user’s authority in the context of the specific work, not merely their status as requester.

| Source | What it can validate | What it does not validate by itself |
| --- | --- | --- |
| Colleague, end user, or requester | The problem exists and the outcome would be useful | Priority, opportunity cost, available capacity, or expanded scope |
| Technical expert | Feasibility, system constraints, and simpler implementation routes | Priority or expanded scope, unless authority was explicitly delegated |
| Manager or accountable scope owner | Priority, opportunity cost, capacity, and scope | Technical feasibility without appropriate expert evidence |
| User as owner of a personal tool | Priority, personal time budget, and scope for work they control | Technical feasibility, other people’s capacity, or changes affecting shared systems or external commitments |
| Recorded acceptance criteria | The implementation explicitly required by the work item | Additional behavior not stated in the criteria |
| Explicitly delegated authority | The decisions covered by the delegation | Decisions outside the recorded delegation |
