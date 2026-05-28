# Device And Calendar Context

Arthur wants the system to work across devices, not only inside one app.

## Devices And Surfaces

- MacBook Air 15-inch M4
- Dell Windows desktop/computer with monitors
- Samsung Galaxy S24/S25 Fan Edition phone
- Google Pixel Watch 3
- Work Lenovo laptop
- Google Calendar for work meetings
- Freshservice/on-call calendar, likely to be synced into Google Calendar later
- Android/Gemini surfaces may become useful for capture and reminders

## Calendar Strategy

Use Calendar for time, not for every task.

Good calendar items:

- phone/admin windows
- medical appointments
- work meetings
- CEO/job calls
- apartment viewings
- on-call shifts
- travel/store pickup windows
- protected blocks for high-friction tasks

Avoid building perfect full-day calendars. Arthur's life is interruption-prone, so prefer flexible anchors:

```text
Morning admin window
Lunch phone call window
Saturday bike repair block
Sunday 30-minute reset
```

## Current Google Calendar Sync

Todoist's built-in Google Calendar integration is now the active bridge for task visibility in Google Calendar.

Observed on 2026-05-28:

- Todoist `Settings -> Calendars` is connected to Arthur's Google account and marked `Live`.
- `Show events in Todoist` is enabled, so Google Calendar events appear in Todoist Today/Upcoming.
- `Sync tasks to calendar` is enabled, so scheduled Todoist tasks assigned to Arthur sync to a Google Calendar named `Todoist`.
- If Todoist shows `Task sync calendar: Not found`, use `Restore synced calendar`; this recreated/restored the Google Calendar named `Todoist`.
- Google Calendar showed the `Todoist` calendar under `My calendars`, checked.
- Timed Todoist tasks appeared in Google Calendar as 30-minute events even though explicit task duration updates still showed `duration: null` through CLI/MCP.

Operationally, give calendar-worthy Todoist tasks a due date and time. Do not force every task into the calendar; use timed Todoist tasks for Red Zone calls/admin windows and other work that benefits from appearing on phone/watch calendars.

## Work Busy Blocks

Arthur added the KONUX work Google Calendar (`arthur.zakirov@konux.de`) into Google Calendar. It may show work meetings as `busy` blocks rather than full meeting details.

When suggesting, creating, or rescheduling Todoist task windows:

- Do not schedule personal tasks inside work `busy` blocks.
- Do not schedule personal tasks immediately before a work meeting; Arthur may be late to the meeting.
- Do not schedule personal tasks immediately after a work meeting; the meeting may drag on or require recovery/context switching.
- Prefer a buffer around work meetings. Use at least 15 minutes before and after by default; use 30 minutes around high-friction tasks, phone calls, travel, medical admin, or anything with real consequences.
- If the calendar only exposes `busy`, treat it as a real protected meeting block.

## Work Capacity Baseline

Arthur should usually work about 40 hours per week, roughly 8 hours per weekday from Monday through Friday. There is some flexibility across days, evenings, and weekends, but do not treat every apparent calendar gap on a workday as personal-task capacity.

When planning personal tasks on workdays:

- Preserve the rough goal of 8 hours of work per day on average.
- Keep personal tasks on workdays sparse unless they are urgent, time-sensitive, or naturally fit into a short admin/phone window.
- Prefer small windows such as lunch, end-of-day, or explicitly protected admin blocks over scattering tasks throughout working hours.
- Move flexible personal tasks to evenings or weekends before crowding the workday.
- If a day already has many meetings or fragmented work blocks, assume lower personal-task capacity even if the calendar shows gaps.
- When in doubt, schedule one important personal task rather than several.

## Calendar App Uncertainty

Arthur has used Notion Calendar and is considering Google Calendar, Todoist calendar views, and other calendar apps. Do not prematurely force a final answer. Default to Google Calendar as the canonical sync layer because it reaches phone, watch, work calendars, and likely on-call sync.

Use Todoist for tasks. Use Google Calendar for hard time. Experiment slowly with calendar frontends.

## Cross-Device Design Requirements

- Tasks must be visible or remindable on phone/watch.
- Work calendar and on-call schedule must be respected when choosing task windows.
- The system must still work from fresh AI sessions.
- AI should remain the capture layer; apps are backends.
- Keep manual app maintenance low.

## Future Experiments

Try only one experiment at a time:

- Todoist widgets/reminders on Android.
- Google Calendar blocks for Red Zone tasks.
- Notion Calendar as a frontend if it improves visibility.
- Linear only for project-like work.
- Gemini/Android voice capture only if it can feed the same backend without fragmentation.
