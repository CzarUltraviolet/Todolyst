from dataclasses import dataclass
from enum import Enum
import datetime
from typing import Dict


# The states that can be taken by a task
class TaskState(Enum):
    todo = 0
    in_progress = 1
    complete = 2


# Next Id to be used for a task creation
_max_id: int = 0

Categories = set(["Default","Work","Personal"])

def add_category(category:str):
    Categories.add(category)

class _Task:
    # Id : unique for each task, handled by the global variable _max_id
    id: int
    # Title : must be unique between the tasks of a same list
    title: str
    # State : indicates the progression of the task
    state: TaskState
    # Description : details the task
    description: str
    # Creation date : gives the date of creation for the task
    creationdate: datetime
    # Category : the category of the task
    category: str
    # Create a new task, description can be null and other attributes are not managed by user
    def __init__(self, title:str,description:str=None,category="Default") -> None:
        """_summary_

        Args:
            title (_type_): _description_
            description (_type_, optional): _description_. Defaults to None.
        """
        global _max_id
        global Categories
        self.title = title
        self.state = TaskState.todo
        self.description = description

        if(category not in Categories):
            raise Exception("The category you entered is not part of the available categories, here are the current categories : "+str(Categories)+". If you want to add a new category, use the AddCategory method")
        Categories.add(category)
        self.category = category


        self.id = _max_id
        _max_id += 1
        # Set the creation date the the current time
        self.creationdate = datetime.datetime.today()

    # Set task state
    def set_state(self, new_state: TaskState):
        """_summary_

        Args:
            new_state (TaskState): _description_
        """
        self.state = new_state

    # Display every task attribute
    def display(self):
        """_summary_
        """
        print("Task :", self.id)
        print("Title :", self.title)
        print("State :", self.state.name)
        print("Description :", self.description)
        print("Created on :", self.creationdate.date(),"at", str(self.creationdate.time().hour)+"h"+str(self.creationdate.time().minute))
        print("Category :",self.category)


class TaskList:
    # Container for the
    tasks: Dict[int,_Task] = {}

    def __init__(self) -> None:
        pass

    def add_task(self, title: str,description:str=None,category:str="Default"):
        """_summary_

        Args:
            title (str): _description_
            description (_type_, optional): _description_. Defaults to None.
        """
        same_tasks = [task for task in self.tasks.values() if task.title == title]
        if (len(same_tasks) > 0):
            raise Exception(
                "Error, can't have two tasks with the same title in a taskList.\n")
        newTask = _Task(title,description=description,category=category)
        self.tasks[newTask.id] = newTask

    def remove_tasks_by_titles(self, *titles:str):
        """_summary_

        Args:
            titles (_type_): _description_
        """
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            self.tasks.pop(task.id)

    def remove_tasks_by_ids(self, *ids:int):
        """_summary_

        Args:
            titles (_type_): _description_
        """
        ids_to_remove = [id for id in self.tasks.keys() if id in ids]
        if(len(ids_to_remove) < len(ids)):
            raise Exception("One or several ids of tasks to be removed do not correspond to ids from this list.")
        
        for id in ids_to_remove:
            self.tasks.pop(id)


    def begin_task(self, *titles:str):
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.in_progress)

    def complete_task(self, *titles:str):
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.complete)

    # Display taks from the list, can be filtered to display only a certain category
    def display_tasks(self,category:str=None):
        print("Task list contains ", len(self.tasks), " elements.")
        print("--------")
        
        if(category):
            if(category not in Categories):
                raise Exception("Tried to filter using a category that does not exist : "+category)
            tasks = [task for task in self.tasks.values() if task.category == category]
        else:
            tasks = self.tasks.values()
        for task in tasks:
            task.display()
            print("--------")




testlist = TaskList()
testlist.add_task("test", "description1",category="Work")
testlist.add_task("test2", "description1",category="Personal")
add_category("Fun")
testlist.add_task("test3", "description1",category="Fun")
testlist.add_task("test4", "description1",category="Fun")


testlist.display_tasks()

#testlist.remove_tasks_by_ids(0)
testlist.complete_task("test")
testlist.begin_task("test3")

testlist.display_tasks(category="Work")
