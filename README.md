# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

# Sample
```
09:30-09:50  Litter box cleanup (low priority, 20 min)

Scheduled tasks (chronological):
  08:00  Morning walk - Rex (priority: high)
  08:45  Feed breakfast - Milo (priority: high)
  09:00  Evening walk - Rex (priority: medium)
  09:30  Litter box cleanup - Milo (priority: low)
```

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## ✨ Features

The scheduling logic lives in `pawpal_system.py`. Each feature below describes the
actual algorithm implemented, not just the name.

- **Priority-first greedy scheduling** — `Scheduler.build_schedule()` gathers every
  unfinished task that is due on the chosen day, orders them highest → lowest
  priority, then places each into the *earliest* free slot in the 08:00–20:00 day
  window (scanned in 15-minute steps) that doesn't overlap a blocked time or an
  already-placed task. Tasks that can't fit anywhere stay unscheduled.
- **Sorting by time and by priority** — `Scheduler.sort_by_time()` orders tasks
  chronologically by `scheduled_at` (unscheduled tasks sort to the end via
  `datetime.max`); `Scheduler.order_by_priority()` sorts by a rank map
  (high=0, medium=1, low=2), with unknown priorities sorted last.
- **Conflict warnings** — `Scheduler.find_conflicts()` sorts scheduled tasks by start
  time and sweeps neighbor-by-neighbor, flagging a pair whenever one task is still
  running when the next begins (half-open `[start, end)` intervals, so a task ending
  exactly when the next starts is *not* a conflict). `Scheduler.conflict_warning()`
  formats those pairs into a human-readable string (empty when there are none).
- **Filtering** — `Owner.filter_tasks()` filters by pet name and/or completion
  status, each filter optional; `Owner.task_by_status()` and `Owner.tasks_for_pet()`
  are the single-axis shortcuts.
- **Daily & weekly recurrence** — completing a recurring task via
  `Pet.complete_task()` / `Owner.mark_task_complete()` auto-spawns its next instance
  through `Task.next_occurrence()` (daily → +1 day, weekly → +7 days) with a fresh id
  and any deadline rolled forward keeping its time of day. `Task.is_due_on()` decides
  whether a task appears in a given day's plan.
- **Blocked times, overdue, and progress** — `Owner.block_time()` reserves ranges the
  scheduler refuses to place into (`Scheduler.fits_in_window()`); `Task.is_overdue()`
  / `Owner.overdue_tasks()` flag past-deadline unfinished tasks; `Pet.progress()`
  reports the fraction of a pet's tasks completed.

| Feature | Method(s) |
|---------|-----------|
| Sorting | `Scheduler.sort_by_time()`, `Scheduler.order_by_priority()` |
| Filtering | `Owner.filter_tasks()`, `Owner.task_by_status()`, `Owner.tasks_for_pet()` |
| Conflict detection | `Scheduler.find_conflicts()`, `Scheduler.conflict_warning()` |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()`, `Owner.mark_task_complete()` |


## Testing PalPaw+.

# run: 
python -m pytest

# Testing: 
1. program should mark the task_done to be done after the task is completed
2. adding a task should increase the task count foor that pet by 1
3. Schedule should be sorted by most important to least important when being placed into the schedule 
4. a recurr task should be listed again on the schedule when completed
5. 2 task with same time should be listed as "conflict"

# result:
(.venv) PS C:\Users\11791\OneDrive\Desktop\ai110-module2show-pawpal-starter> python -m pytest
========================================================================== test session starts ==========================================================================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\11791\OneDrive\Desktop\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 5 items                                                                                                                                                        

test\test_pawpal.py .....                                                                                                                                          [100%]

=========================================================================== 5 passed in 0.06s ===========================================================================

# Confidence level:
4



## Demo Walkthrough

Launch the Streamlit app with:

```bash
streamlit run app.py
```

### What you can do in the UI

- **Set up owner & pet** — enter an owner name, a pet name, and pick a species
  (dog / cat / other).
- **Add tasks** — give each task a title, duration (minutes), and priority
  (low / medium / high), and choose how it repeats (daily / weekly / once). Weekly
  tasks also pick the weekday they recur on.
- **Browse the task list** — filter by **pet**, by **status** (all / todo / done),
  and re-sort by **priority** or **scheduled time**. Results render as a table
  showing pet, duration, priority, repeat rule, scheduled time, and done status.
- **Generate the schedule** — one click builds today's plan, shows it as a
  time-ordered table, surfaces a conflict warning (or a green "no conflicts" note),
  and offers a "Why this plan?" expander with the scheduler's reasoning.

### Example workflow

1. Enter owner **Jordan** and pet **Mochi** (dog).
2. Add a few tasks — e.g. "Morning walk" (30 min, high), "Feeding" (10 min, high),
   "Evening play" (25 min, medium) — some set to repeat **daily**.
3. In **Current tasks**, filter to Mochi and sort by **priority** to confirm the
   high-priority tasks lead.
4. Click **Generate schedule** to place the tasks into today's 08:00–20:00 window.
5. Read the time-ordered plan; if two tasks collide, the app shows a conflict warning.
6. Mark a daily task complete to watch its next occurrence appear automatically.

### Key scheduler behaviors on display

- **Sorting** — the plan is always shown in chronological order, and the task list
  can be flipped between priority and time ordering.
- **Priority-first placement** — the highest-priority task claims the earliest slot.
- **Conflict warnings** — overlapping time windows are flagged in plain language.
- **Recurrence** — completing a daily/weekly task spawns its next instance.

### Sample CLI output

Running the terminal demo shows the same sorting, filtering, and conflict logic
without the UI:

```text
$ python main.py

PawPal+ demo for Alex (Tuesday, July 07, 2026)

[sort] schedule in scrambled order:
  09:30  Midday play
  09:00  Evening walk
  08:45  Feed breakfast
  08:00  Morning walk

[sort] after scheduler.sort_by_time():
  08:00  Morning walk
  08:45  Feed breakfast
  09:00  Evening walk
  09:30  Midday play

[filter] not-yet-done tasks (filter_tasks(done=False)):
  Evening walk
  Morning walk
  Midday play
  Feed breakfast

[filter] completed tasks (filter_tasks(done=True)):
  Litter box cleanup

[filter] Rex's tasks (filter_tasks(pet_name='Rex')):
  Evening walk
  Morning walk
  Midday play

[filter] Rex's unfinished tasks (both filters combined):
  Evening walk
  Morning walk
  Midday play

[conflict] two tasks placed at 08:00 (different pets):
WARNING: 1 scheduling conflict(s) detected:
  'Extra walk' (08:00) overlaps 'Extra feeding' (08:00)

[conflict] a non-overlapping pair (sanity check):
  No conflicts detected.
```
