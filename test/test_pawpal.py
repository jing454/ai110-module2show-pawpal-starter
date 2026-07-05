"""Two simple tests for PawPal+ core behavior.

Run with:  python -m pytest test/     (from the project root)
       or:  python test/test_pawpal.py
"""

import os
import sys

# Allow running this file directly (python test/test_pawpal.py) by putting the
# project root on the import path. pytest handles this on its own via conftest.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Task


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


if __name__ == "__main__":
    test_task_completion()
    test_task_addition()
    print("\nAll tests passed.")
