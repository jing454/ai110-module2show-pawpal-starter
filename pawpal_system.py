"""PawPal+ — pet care planning assistant.

Class skeleton generated from diagrams/uml.mmd. Method bodies are stubs;
implement the scheduling logic and wire these into app.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Task:
    """A single pet care task (e.g. a morning walk)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    done: bool = False
    scheduled_at: datetime | None = None
    deadline: datetime | None = None

    def mark_done(self) -> None:
        raise NotImplementedError

    def mark_undone(self) -> None:
        raise NotImplementedError

    def is_overdue(self) -> bool:
        raise NotImplementedError


@dataclass
class Pet:
    """A pet owned by an Owner, with its own list of care tasks."""

    name: str
    species: str  # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def delete_task(self, task: Task) -> None:
        raise NotImplementedError

    def edit_task(self, task: Task) -> None:
        raise NotImplementedError

    def progress(self) -> float:
        """Fraction of tasks completed, 0.0–1.0."""
        raise NotImplementedError


class Scheduler:
    """Builds a day's plan and holds owner-set blocked times (the calendar)."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self.blocked_times: list[dict] = []  # {"start": datetime, "end": datetime, "reason": str}

    def add_blocked_time(self, start: datetime, end: datetime, reason: str) -> None:
        raise NotImplementedError

    def build_schedule(self, day: date) -> list[Task]:
        """Choose and order tasks for the given day, respecting constraints."""
        raise NotImplementedError

    def order_by_priority(self) -> list[Task]:
        raise NotImplementedError

    def fits_in_window(self, task: Task) -> bool:
        """True if the task can be placed without overlapping a blocked time."""
        raise NotImplementedError

    def explain(self) -> str:
        """Human-readable reasoning for why each task was chosen and when."""
        raise NotImplementedError


class Owner:
    """The pet owner. Manages pets and sets blocked times via the Scheduler."""

    def __init__(self, name: str, scheduler: Scheduler) -> None:
        self.name = name
        self.pets: list[Pet] = []
        self.scheduler = scheduler

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def remove_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def block_time(self, start: datetime, end: datetime, reason: str) -> None:
        """Owner-facing action; forwards the block to the Scheduler."""
        raise NotImplementedError

    def list_tasks(self) -> list[Task]:
        """All tasks across all of this owner's pets."""
        raise NotImplementedError
