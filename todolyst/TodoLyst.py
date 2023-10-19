from dataclasses import dataclass
from enum import Enum
import datetime

from typing import Dict

import logging
from logging.handlers import TimedRotatingFileHandler

from TodolystExceptions import *


# logger conf:
# 2 timedrotatingfilehandlers: meaning we create 1 file per day and
# rotate through the last 31 files. (31 so that we get a full month,
# even on long months)
# the first prints everything down to debug level
# the second only prints critical and error levels

# debug formatter: precise format, down to the
# filename, function name and line number
debug_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(filename)s.%(funcName)s l.%(lineno)d | %(message)s')
debug_file_handler = TimedRotatingFileHandler(
    filename="debug.log", when='midnight', backupCount=31)
debug_file_handler.setFormatter(debug_formatter)
debug_file_handler.setLevel(logging.DEBUG)

error_file_handler = TimedRotatingFileHandler(
    filename="error.log", when='midnight', backupCount=31)
# error formatter: only the time, module name, logging level and message
error_formatter = logging.Formatter(
    '%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
error_file_handler.setFormatter(error_formatter)
error_file_handler.setLevel(logging.ERROR)

logger = logging.getLogger("TodoLyst")
logger.setLevel(logging.DEBUG)
logger.addHandler(debug_file_handler)
logger.addHandler(error_file_handler)

# The states that can be taken by a task


class TaskState(Enum):
    todo = 0
    in_progress = 1
    complete = 2


# Next Id to be used for a task creation
_max_id: int = 0

Categories = set(["Default", "Work", "Personal"])


def add_category(category: str):
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

    def __init__(self, title: str, description: str = None, category="Default") -> None:
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

        if (category not in Categories):
            raise CategoryNotFoundException("The category you entered is not part of the available categories, here are the current categories : " +
                            str(Categories)+". If you want to add a new category, use the AddCategory method")
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

    
    def __str__(self):
        return "Task : " + str(self.id)+"\n"+"Title : " +self.title+"\n"+"Description : "+self.description+"\n"+"Created on : "+ str(self.creationdate.date())+ " at "  +str(
            self.creationdate.time().hour)+"h"+str(self.creationdate.time().minute)+"\n"+"Category : "+ self.category+"\n"


class TaskList:
    # Container for the
    tasks: Dict[int, _Task] = {}

    def __init__(self) -> None:
        self.tasks = {}

    def add_task(self, title: str, description: str = None, category: str = "Default"):
        """_summary_

        Args:
            title (str): _description_
            description (_type_, optional): _description_. Defaults to None.
        """
        same_tasks = [task for task in self.tasks.values()
                      if task.title == title]
        if (len(same_tasks) > 0):
            raise DuplicateTaskException(
                "Error, can't have two tasks with the same title in a taskList.\n")
        newTask = _Task(title, description=description, category=category)
        self.tasks[newTask.id] = newTask

    def remove_tasks_by_titles(self, *titles: str):
        """_summary_

        Args:
            titles (_type_): _description_
        """
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            self.tasks.pop(task.id)

    def remove_tasks_by_ids(self, *ids: int):
        """_summary_

        Args:
            titles (_type_): _description_
        """
        ids_to_remove = [id for id in self.tasks.keys() if id in ids]
        if (len(ids_to_remove) < len(ids)):
            raise TaskNotFoundException(
                "One or several ids of tasks to be removed do not correspond to ids from this list.")

        for id in ids_to_remove:
            self.tasks.pop(id)

    def begin_task(self, *titles: str):
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.in_progress)

    def complete_task(self, *titles: str):
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.complete)

    # Display taks from the list, can be filtered to display only a certain category
    def display_tasks(self, category: str = None):
        print("Task list contains ", len(self.tasks), " elements.")
        print("--------")

        if (category):
            if (category not in Categories):
                raise CategoryNotFoundException(
                    "Tried to filter using a category that does not exist : "+category)
            tasks = [task for task in self.tasks.values()
                     if task.category == category]
        else:
            tasks = self.tasks.values()
        for task in tasks:
            print(task)
            print("--------")


logger.info("Starting tasklist...")
testlist = TaskList()
testlist.add_task("test", "description1", category="Work")
testlist.add_task("test2", "description1", category="Personal")
add_category("Fun")
testlist.add_task("test3", "description1", category="Fun")
testlist.add_task("test4", "description1", category="Fun")

test_task = _Task("montest","description","Work")
testlist.display_tasks()

# testlist.remove_tasks_by_ids(0)
testlist.complete_task("test")
testlist.begin_task("test3")
logger.info("Tasklist ended.")
logger.error("Done.")
print(test_task)
testlist.display_tasks(category="Work")


task_list_exceptions = TaskList()
initial_length = len(task_list_exceptions.tasks)
task_list_exceptions.add_task("Testtask02")
