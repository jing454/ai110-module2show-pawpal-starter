# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

A owner should be able to:
1. add a pet
2. edit the task (done or not done) (add and delete task)
4. see if the progress of a task
6. set time constraint (like being able to block off certain time in a day or even certain days)
7. some calender system so it's easy to read the layout of how it's proceed 
8. some kind of time limtation for each task

Class Owner - Designed so that multiple users/owners can use the application. It contains the ability to add pets, remove pets, information of pets names, etc.

Class Pets -  Each pet then has multiple tasks that needs to be completed. They have data on names, tasks to be completed, species, etc.

Class Tasks - Each task then has their own information such as the duration, if tasks are done, the title of the task, the schedule of the task, etc.

Class Schedule - This was created for owner usage. The owner is able to limit some periods off if they're busy and the tasks for each pet will show up for better visualization. It includes task name, their duration, add block time, fits schedule (bool), etc.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

1. The logic of the design was changed during implementation. Schedule.task wasnt connected to the Pet.tasks. This is a problem since we want the creation of tasks within each pets to reflect to the class schedule task so we are able to see the schedule being filled ask we add tasks to each pets. So an implementation was made to the class schedule so that the tasks line up between the 2 classes.

2. fits_in_window(task) is missing it's slot. You are able to add a specific block time in your schedule but pet tasks that you add does not say from what time to what time. Hence, this causes the logic of can i do this pet task to be unanswerable since no time were specified.. A logic was added to fits_in_window(task) so it will end up returning false if any collison was made (for both upon schedule creation and if start time + duration collides with another task or blocked off times) 

3. order_by_priority will sort wrong
the priority is sorted by alphabetically instead of the importance. We can solve this by implementing each number to high, medium, and low to implement importance. Ex: 0 most important, 1 being medium important, 2 being least important

4. delete_task / edit_task have an identity problem
2 tasks with the same title/duration/priority look the same to python. when you want to delete one of them, it may end up removing the incorrect one. So, we implement a unique id for each tasks so we do not get mixed up between multiple tasks. The program now hands out an unique id tag for each tasks.

5. progress() divide-by-zero
progress() (pawpal_system.py:50) is "fraction completed" = done / total. A pet with no tasks gives 0/0. This will causes an issue due to 0/0 which will cause the program to break. Added a logic to it so that if total == 0 then the program will return 0.0 since that would mean no tasks are applied yet. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler func is a "first come, first served" by priority. it places the most important task first in the earliest open time. However, one long task can cause this to hog an early slot and end up blocking the 2 short task that couldve fit there instead. This trade off is resonable since important task should always go first since it's usually something needed to be done rather than something that'll be fine even if it isnt done


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Used to create a system design class for the app. used it for debugging and understanding code whenever needed. The prompt "help me understand the code in 10 seconds" benefitted me since it caused the model to explain the code in simple terms that are easy to understand.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

There was a moment during the system design phase when it was trying to add an element in the class of owner but it should shouldve been in pets instead. I read the system design and made sure that it had all the correct elements and no additional element was added that was unneeded. I also read through the code that the ai provided to ensure that the logic is correct and understandable.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

i tested:
1. add a pet
2. edit the task (done or not done) (add and delete task)
4. see if the progress of a task
6. set time constraint (like being able to block off certain time in a day or even certain days)
7. some calender system so it's easy to read the layout of how it's proceed 
8. some kind of time limtation for each task

These test are important since they should be the core response of the app where it shouldnt break if these cases were to happen or else the program may break or not act correctly when these edge cases arises.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Based on the test, the scheduler should work fine since it passed all the edge cases that was stated above. If i had more time i wouldv'e prob tested the user interface to ensure that the users can understand the program and that it returns the correct prompt. Additionally, i would probably test more edge cases to ensure that everything is perfect.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The system design and how the project turned out

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

The UX is a little weird. I would perhaps change the scheduling so it look easier to understand. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Always look through the code that it provided and make sure there is no issue from system design to code design to testing. Ai is a tool that should be used on anything that takes a long time for efficiency but also check what it gives you. 
