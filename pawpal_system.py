"""PawPal+ — pet care planning assistant.

Class skeleton generated from diagrams/uml.mmd. Method bodies are stubs;
implement the scheduling logic and wire these into app.py.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

# Hands out a unique, ever-increasing id to each Task so duplicates stay distinct.
_task_id_counter = itertools.count(1)


@dataclass
class Task:
    """A single pet care task (e.g. a morning walk)."""

    title: str  # description of the activity, e.g. "Morning walk"
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    frequency: str = "daily"  # "once" | "daily" | "weekly"
    done: bool = False
    scheduled_at: datetime | None = None  # start time, set by the Scheduler
    deadline: datetime | None = None
    id: int = field(default_factory=lambda: next(_task_id_counter))

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.done = True

    def mark_undone(self) -> None:
        """Mark this task as not yet completed."""
        self.done = False

    def is_overdue(self) -> bool:
        """True if the task has a deadline that has passed and isn't done yet."""
        if self.done or self.deadline is None:
            return False
        return datetime.now() > self.deadline


@dataclass
class Pet:
    """A pet owned by an Owner, with its own list of care tasks."""

    name: str
    species: str  # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def delete_task(self, task: Task) -> None:
        """Remove the task with the matching id (not just a look-alike)."""
        self.tasks = [t for t in self.tasks if t.id != task.id]

    def edit_task(self, updated: Task) -> None:
        """Replace the stored task that shares updated.id."""
        for i, existing in enumerate(self.tasks):
            if existing.id == updated.id:
                self.tasks[i] = updated
                return

    def progress(self) -> float:
        """Fraction of tasks completed, 0.0–1.0."""
        total = len(self.tasks)
        if total == 0:
            return 0.0
        done = sum(1 for t in self.tasks if t.done)
        return done / total


class Scheduler:
    """Builds a day's plan and holds owner-set blocked times (the calendar)."""

    def __init__(self) -> None:
        """Start with an empty task working set and no blocked times."""
        # Working set for the current schedule run, gathered from the owner's pets.
        self.tasks: list[Task] = []
        self.blocked_times: list[dict] = []  # {"start": datetime, "end": datetime, "reason": str}

    # The daily window the scheduler is allowed to place tasks in, and how
    # finely it scans for a free slot.
    DAY_START = time(hour=8)
    DAY_END = time(hour=20)
    SLOT_STEP_MINUTES = 15

    def add_blocked_time(self, start: datetime, end: datetime, reason: str) -> None:
        """Reserve a time range that no task may be scheduled into."""
        self.blocked_times.append({"start": start, "end": end, "reason": reason})

    def build_schedule(self, owner: Owner, day: date) -> list[Task]:
        """Choose and order the owner's tasks for the given day, respecting constraints.

        Pulls tasks from the owner's pets so the scheduler never holds a stale copy,
        then greedily places each task (highest priority first) into the earliest
        free slot that avoids blocked times and already-placed tasks.
        """
        # Fresh working set: only tasks that still need doing.
        self.tasks = [t for t in owner.list_tasks() if not t.done]
        for t in self.tasks:
            t.scheduled_at = None  # clear any placement from a previous run

        day_start = datetime.combine(day, self.DAY_START)
        day_end = datetime.combine(day, self.DAY_END)
        step = timedelta(minutes=self.SLOT_STEP_MINUTES)

        for task in self.order_by_priority(self.tasks):
            slot = day_start
            while slot + timedelta(minutes=task.duration_minutes) <= day_end:
                if self.fits_in_window(task, slot):
                    task.scheduled_at = slot
                    break
                slot += step
            # If no slot fits, the task stays unscheduled (scheduled_at is None).

        # Return the placed tasks in chronological order.
        placed = [t for t in self.tasks if t.scheduled_at is not None]
        return sorted(placed, key=lambda t: t.scheduled_at)

    # Lower number = higher priority. Unknown values sort last.
    PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

    def order_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted high -> low priority."""
        return sorted(tasks, key=lambda t: self.PRIORITY_RANK.get(t.priority, 99))

    def fits_in_window(self, task: Task, start_time: datetime) -> bool:
        """True if placing task at start_time avoids blocked times AND other scheduled tasks.

        The task's window is [start_time, start_time + duration]. It must not overlap
        any blocked time, nor any other task that already has a scheduled_at slot.
        """
        end_time = start_time + timedelta(minutes=task.duration_minutes)

        # 1. Don't land on a blocked-off time.
        for block in self.blocked_times:
            if self._overlaps(start_time, end_time, block["start"], block["end"]):
                return False

        # 2. Don't collide with another task's scheduled slot.
        for other in self.tasks:
            if other is task or other.scheduled_at is None:
                continue
            other_end = other.scheduled_at + timedelta(minutes=other.duration_minutes)
            if self._overlaps(start_time, end_time, other.scheduled_at, other_end):
                return False

        return True

    @staticmethod
    def _overlaps(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:
        """Two [start, end) intervals overlap iff each begins before the other ends."""
        return start_a < end_b and start_b < end_a

    def explain(self) -> str:
        """Human-readable reasoning for why each task was chosen and when.

        Call after build_schedule(). Lists scheduled tasks in time order, then any
        that could not be placed.
        """
        scheduled = sorted(
            (t for t in self.tasks if t.scheduled_at is not None),
            key=lambda t: t.scheduled_at,
        )
        unscheduled = [t for t in self.tasks if t.scheduled_at is None]

        if not scheduled and not unscheduled:
            return "No tasks to schedule."

        lines = []
        for t in scheduled:
            end = t.scheduled_at + timedelta(minutes=t.duration_minutes)
            lines.append(
                f"{t.scheduled_at:%H:%M}-{end:%H:%M}  {t.title} "
                f"({t.priority} priority, {t.duration_minutes} min)"
            )
        for t in unscheduled:
            lines.append(f"Unscheduled: {t.title} ({t.priority}) — no free slot in the day")
        return "\n".join(lines)


class Owner:
    """The pet owner. Manages pets and sets blocked times via the Scheduler."""

    def __init__(self, name: str, scheduler: Scheduler) -> None:
        """Create an owner with no pets, tied to the given scheduler."""
        self.name = name
        self.pets: list[Pet] = []
        self.scheduler = scheduler

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove this exact pet object (match by identity, not value)."""
        self.pets = [p for p in self.pets if p is not pet]

    def block_time(self, start: datetime, end: datetime, reason: str) -> None:
        """Owner-facing action; forwards the block to the Scheduler."""
        self.scheduler.add_blocked_time(start, end, reason)

    def list_tasks(self) -> list[Task]:
        """All tasks across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]
