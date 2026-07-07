from datetime import date

import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", scheduler=Scheduler())

owner = st.session_state.owner  # the persistent instance, reused across reruns

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    "A pet care planning assistant. Add care tasks for your pets, then build a "
    "time-ordered daily plan that respects priority and flags scheduling conflicts."
)

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
col4, col5 = st.columns(2)
with col4:
    frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])
with col5:
    # Only relevant for weekly tasks; ignored otherwise.
    weekday_name = st.selectbox("On (weekly only)", WEEKDAYS)

if st.button("Add task"):
    # Find the pet by name, or create it and attach it to the owner.
    pet = next((p for p in owner.pets if p.name == pet_name), None)
    if pet is None:
        pet = Pet(pet_name, species)
        owner.add_pet(pet)
    weekday = WEEKDAYS.index(weekday_name) if frequency == "weekly" else None
    pet.add_task(Task(task_title, int(duration), priority, frequency=frequency, weekday=weekday))

# Show the live task list straight from the owner's pets, with filters + sorting
# that reuse the Owner/Scheduler methods rather than re-implementing them here.
st.markdown("### Current tasks")


def _pet_name_for(task: Task) -> str:
    """The name of the pet that owns this task (matched by id, not look-alike)."""
    return next(
        (p.name for p in owner.pets if any(t.id == task.id for t in p.tasks)),
        "—",
    )


fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    pet_choices = ["all"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Pet", pet_choices)
with fcol2:
    status = st.selectbox("Show", ["all", "todo", "done"])
with fcol3:
    sort_by = st.selectbox("Sort by", ["priority", "scheduled time"])

# filter_tasks handles both filters; None means "don't apply this one".
tasks = owner.filter_tasks(
    pet_name=None if pet_filter == "all" else pet_filter,
    done=None if status == "all" else (status == "done"),
)

# Sort with the Scheduler's own methods so the UI matches the backend logic.
if sort_by == "priority":
    tasks = owner.scheduler.order_by_priority(tasks)
else:
    tasks = owner.scheduler.sort_by_time(tasks)

if tasks:
    st.table(
        [
            {
                "pet": _pet_name_for(t),
                "title": t.title,
                "duration (min)": t.duration_minutes,
                "priority": t.priority,
                "repeats": t.frequency,
                "scheduled": f"{t.scheduled_at:%H:%M}" if t.scheduled_at else "—",
                "done": "✓" if t.done else "",
            }
            for t in tasks
        ]
    )
    st.caption(f"{len(tasks)} task(s) shown.")
else:
    st.info("No tasks match these filters. Add one above or widen the filter.")

st.divider()

st.subheader("Build Schedule")
st.caption("Places today's unfinished tasks into the 08:00–20:00 window, highest priority first.")

if st.button("Generate schedule"):
    scheduler = owner.scheduler
    schedule = scheduler.build_schedule(owner, date.today())
    if schedule:
        st.success(f"Planned {len(schedule)} task(s) for today, in time order:")

        # sort_by_time keeps the plan chronological even if build order changes.
        st.table(
            [
                {
                    "time": f"{t.scheduled_at:%H:%M}",
                    "pet": _pet_name_for(t),
                    "task": t.title,
                    "duration (min)": t.duration_minutes,
                    "priority": t.priority,
                }
                for t in scheduler.sort_by_time(schedule)
            ]
        )

        # Conflict warning straight from the Scheduler ("" means none detected).
        warning = scheduler.conflict_warning(schedule)
        if warning:
            st.warning(warning)
        else:
            st.success("No scheduling conflicts detected. ✓")

        with st.expander("Why this plan? (scheduler explanation)"):
            st.text(scheduler.explain())
    else:
        st.info("No tasks to schedule yet. Add some tasks above.")
