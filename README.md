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

## 📐 Smarter Scheduling

Beyond building a basic daily plan, PawPal+ implements four "smarter scheduling"
features. Each is documented below with the method that implements it (all live in
`pawpal_system.py`).

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | 'Scheduler.sort_by_time()', `Scheduler.order_by_priority()` | Chronological + high→low priority ordering |
| Filtering | `Owner.filter_tasks()`, `Owner.task_by_status()`, `Owner.tasks_for_pet()` | By pet name and/or completion status |
| Conflict detection | `Scheduler.find_conflicts()`, `Scheduler.conflict_warning()` | Flags overlapping time windows |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()`, `Owner.mark_task_complete()` | Auto-creates the next daily/weekly instance |


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



## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
