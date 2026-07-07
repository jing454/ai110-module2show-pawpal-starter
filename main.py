"""Temporary testing ground — verify PawPal+ sorting and filtering in the terminal."""

from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Set up the owner and scheduler.
    scheduler = Scheduler()
    owner = Owner("Alex", scheduler)

    # Create two pets.
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(rex)
    owner.add_pet(milo)

    # Add tasks OUT OF ORDER on purpose — not sorted by time or priority — so the
    # sorting methods have something real to reorder.
    rex.add_task(Task("Evening walk", duration_minutes=30, priority="medium"))
    milo.add_task(Task("Litter box cleanup", duration_minutes=20, priority="low"))
    rex.add_task(Task("Morning walk", duration_minutes=45, priority="high"))
    milo.add_task(Task("Feed breakfast", duration_minutes=15, priority="high"))
    rex.add_task(Task("Midday play", duration_minutes=25, priority="medium"))

    # Mark one task done so the completion-status filter has both sides to show.
    milo.tasks[0].mark_done()  # "Litter box cleanup" is now complete

    # Build today's schedule (this assigns each task a scheduled_at time).
    today = date.today()
    schedule = scheduler.build_schedule(owner, today)

    print(f"PawPal+ demo for {owner.name} ({today:%A, %B %d, %Y})")

    # --- SORTING -----------------------------------------------------------
    # Reverse the schedule first to prove sort_by_time actually reorders it.
    shuffled = list(reversed(schedule))
    print("\n[sort] schedule in scrambled order:")
    for t in shuffled:
        print(f"  {t.scheduled_at:%H:%M}  {t.title}")

    print("\n[sort] after scheduler.sort_by_time():")
    for t in scheduler.sort_by_time(shuffled):
        print(f"  {t.scheduled_at:%H:%M}  {t.title}")

    # --- FILTERING ---------------------------------------------------------
    print("\n[filter] not-yet-done tasks (filter_tasks(done=False)):")
    for t in owner.filter_tasks(done=False):
        print(f"  {t.title}")

    print("\n[filter] completed tasks (filter_tasks(done=True)):")
    for t in owner.filter_tasks(done=True):
        print(f"  {t.title}")

    print("\n[filter] Rex's tasks (filter_tasks(pet_name='Rex')):")
    for t in owner.filter_tasks(pet_name="Rex"):
        print(f"  {t.title}")

    print("\n[filter] Rex's unfinished tasks (both filters combined):")
    for t in owner.filter_tasks(pet_name="Rex", done=False):
        print(f"  {t.title}")

    # --- CONFLICT DETECTION ------------------------------------------------
    # The scheduler normally avoids overlaps, so force two tasks to the SAME
    # time (one Rex, one Milo) to prove the detector catches it.
    clash = datetime.combine(today, time(hour=8))
    rex_walk = Task("Extra walk", duration_minutes=30, priority="medium")
    milo_meal = Task("Extra feeding", duration_minutes=30, priority="high")
    rex_walk.scheduled_at = clash
    milo_meal.scheduled_at = clash  # exact same start time as rex_walk

    print("\n[conflict] two tasks placed at 08:00 (different pets):")
    warning = scheduler.conflict_warning([rex_walk, milo_meal])
    print(warning if warning else "  No conflicts detected.")

    print("\n[conflict] a non-overlapping pair (sanity check):")
    milo_meal.scheduled_at = datetime.combine(today, time(hour=9))
    ok = scheduler.conflict_warning([rex_walk, milo_meal])
    print(ok if ok else "  No conflicts detected.")


if __name__ == "__main__":
    main()
