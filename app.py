from datetime import date

import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", scheduler=Scheduler())

owner = st.session_state.owner  # the persistent instance, reused across reruns

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
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

# Show the live task list straight from the owner's pets, with a status filter.
status = st.selectbox("Show", ["all", "todo", "done"])
if status == "todo":
    tasks = owner.task_by_status(done=False)
elif status == "done":
    tasks = owner.task_by_status(done=True)
else:
    tasks = owner.list_tasks()
if tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": next(p.name for p in owner.pets if t in p.tasks),
                "title": t.title,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "done": t.done,
            }
            for t in tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    schedule = owner.scheduler.build_schedule(owner, date.today())
    if schedule:
        st.success(f"Planned {len(schedule)} task(s) for today.")
        st.text(owner.scheduler.explain())

        conflicts = owner.scheduler.find_conflicts(schedule)
        if conflicts:
            st.warning(f"{len(conflicts)} time conflict(s) detected:")
            for earlier, later in conflicts:
                st.write(f"• “{earlier.title}” overlaps “{later.title}”")
    else:
        st.info("No tasks to schedule yet. Add some tasks above.")
