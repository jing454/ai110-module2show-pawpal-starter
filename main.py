"""Temporary testing ground — verify PawPal+ scheduling logic in the terminal."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Set up the owner and scheduler.
    scheduler = Scheduler()
    owner = Owner("Alex", scheduler)

    # Create at least two pets.
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(rex)
    owner.add_pet(milo)

    # Add at least 3 tasks with different times (durations/priorities).
    rex.add_task(Task("Morning walk", duration_minutes=45, priority="high"))
    rex.add_task(Task("Evening walk", duration_minutes=30, priority="medium"))
    milo.add_task(Task("Feed breakfast", duration_minutes=15, priority="high"))
    milo.add_task(Task("Litter box cleanup", duration_minutes=20, priority="low"))

    # Build and print today's schedule.
    today = date.today()
    schedule = scheduler.build_schedule(owner, today)

    print(f"Today's schedule for {owner.name} ({today:%A, %B %d, %Y}):\n")
    print(scheduler.explain())

    print("\nScheduled tasks (chronological):")
    for task in schedule:
        pet = next(p.name for p in owner.pets if task in p.tasks)
        print(f"  {task.scheduled_at:%H:%M}  {task.title} - {pet} (priority: {task.priority})")


if __name__ == "__main__":
    main()
