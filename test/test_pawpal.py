"""Two simple tests for PawPal+ core behavior.

Run with:  python -m pytest test/     (from the project root)
       or:  python test/test_pawpal.py
"""

import os
import sys

# Allow running this file directly (python test/test_pawpal.py) by putting the
# project root on the import path. pytest handles this on its own via conftest.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    """Completing a task changes its status from not-done to done."""
    task = Task("Morning walk", duration_minutes=30, priority="high")

    assert task.done is False, "a new task should start as not done"

    task.mark_done()

    assert task.done is True, "mark_done() should set the task to done"
    print("PASS: test_task_completion")


def test_task_addition():
    """Adding a task to a pet increases that pet's task count by one."""
    pet = Pet("Rex", "dog")

    assert len(pet.tasks) == 0, "a new pet should start with no tasks"

    pet.add_task(Task("Feed breakfast", duration_minutes=15, priority="medium"))

    assert len(pet.tasks) == 1, "add_task() should increase the task count by one"
    print("PASS: test_task_addition")


def test_schedule_sorted_chronologically():
    """build_schedule returns tasks in ascending scheduled_at order."""
    owner = Owner("Alex", Scheduler())
    rex = Pet("Rex", "dog")
    owner.add_pet(rex)

    # Added out of priority/time order on purpose so the scheduler has to reorder.
    rex.add_task(Task("Evening walk", duration_minutes=30, priority="medium"))
    rex.add_task(Task("Morning walk", duration_minutes=45, priority="high"))
    rex.add_task(Task("Midday play", duration_minutes=25, priority="low"))

    schedule = owner.scheduler.build_schedule(owner, date.today())

    assert len(schedule) == 3, "all three tasks should fit in the day"
    starts = [t.scheduled_at for t in schedule]
    assert starts == sorted(starts), "schedule must be in chronological order"
    # High priority is placed first, so it should own the earliest slot.
    assert schedule[0].title == "Morning walk", "highest priority takes the earliest slot"
    print("PASS: test_schedule_sorted_chronologically")


def test_daily_task_recurs_next_day():
    """Completing a daily task spawns a fresh follow-up dated one day later."""
    owner = Owner("Alex", Scheduler())
    rex = Pet("Rex", "dog")
    owner.add_pet(rex)

    # Give it a deadline so we can prove the follow-up is for the *following day*.
    today_deadline = datetime.combine(date.today(), time(hour=9))
    walk = Task(
        "Morning walk",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        deadline=today_deadline,
    )
    rex.add_task(walk)

    follow_up = owner.mark_task_complete(walk)

    assert walk.done is True, "the original task should be marked done"
    assert follow_up is not None, "a daily task must produce a follow-up"
    assert follow_up in rex.tasks, "the follow-up should be added to the pet"
    assert follow_up.id != walk.id, "the follow-up is a distinct task, not the same object"
    assert follow_up.done is False, "the follow-up starts not-done"
    assert follow_up.deadline == today_deadline + timedelta(days=1), (
        "the follow-up is due one day later, same time of day"
    )
    print("PASS: test_daily_task_recurs_next_day")


def test_conflict_detection_flags_same_time():
    """Two tasks at the exact same start time are reported as a conflict."""
    scheduler = Scheduler()
    clash = datetime.combine(date.today(), time(hour=8))

    a = Task("Extra walk", duration_minutes=30, priority="medium")
    b = Task("Extra feeding", duration_minutes=30, priority="high")
    a.scheduled_at = clash
    b.scheduled_at = clash  # identical start time

    conflicts = scheduler.find_conflicts([a, b])
    assert len(conflicts) == 1, "overlapping tasks at the same time should be one conflict"
    assert scheduler.conflict_warning([a, b]) != "", "a warning string should be produced"

    # Sanity check: moving them apart clears the conflict.
    b.scheduled_at = datetime.combine(date.today(), time(hour=9))
    assert scheduler.find_conflicts([a, b]) == [], "non-overlapping tasks are not a conflict"
    print("PASS: test_conflict_detection_flags_same_time")


if __name__ == "__main__":
    test_task_completion()
    test_task_addition()
    test_schedule_sorted_chronologically()
    test_daily_task_recurs_next_day()
    test_conflict_detection_flags_same_time()
    print("\nAll tests passed.")
