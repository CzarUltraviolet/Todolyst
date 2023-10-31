from dataclasses import dataclass
from enum import Enum
import datetime

from typing import Dict

import logging
from logging.handlers import TimedRotatingFileHandler

from todolyst.TodolystExceptions import *

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


class TaskState(Enum):
    """The states that can be taken by a task.
    0: To do
    1: in progress
    2: complete"""
    todo = 0
    in_progress = 1
    complete = 2


# Next Id to be used for a task creation
_max_id: int = 0

Categories = set(["Default", "Work", "Personal"])


def add_category(category: str):
    """Adds a category to the set of Categories"""
    Categories.add(category)


class _Task:
    """Internal class to keep track of tasks"""
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
        """Creates a new Task

        Args:
            title (str): title of the task
            description (str, optional): description of the task Defaults to None.
            category (str, optional): category of the task. Defaults to "Default".

        Raises:
            TodolystExceptions.CategoryNotFoundException: raised if input category doesn't exist
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
        """set the state of the task

        Args:
            new_state (TaskState): new state
        """
        self.state = new_state

    def __str__(self):
        """Show what the task should be displayed like

        Returns:
            str: str detailing all characteristics of the task
        """
        return "Task : " + str(self.id)+"\n"+"Title : " + self.title+"\n"+"Description : "+self.description+"\n"+"Created on : " + str(self.creationdate.date()) + " at " + str(
            self.creationdate.time().hour)+"h"+str(self.creationdate.time().minute)+"\n"+"Category : " + self.category+"\n"


class TaskList:
    """Managers the tasks."""
    tasks: Dict[int, _Task] = {}

    def __init__(self) -> None:
        self.tasks = {}

    def add_task(self, title: str, description: str = None, category: str = "Default"):
        """Creates a new Task and adds it to the list

        Args:
            title (str): title of the new task
            description (str, optional): description of the new task. Defaults to None.
            category (str, optional): category of the new task. Defaults to "Default".

        Raises:
            TodolystExceptions.DuplicateTaskException: raised if a similar task already exists
        """
        same_tasks = [task for task in self.tasks.values()
                      if task.title == title]
        if (len(same_tasks) > 0):
            raise DuplicateTaskException()
        newTask = _Task(title, description=description, category=category)
        self.tasks[newTask.id] = newTask

    def remove_tasks_by_titles(self, *titles: str):
        """removes all tasks by title

        Args:
            titles (string[]): titles of the tasks to be removed
        """
        tasks = [task for task in self.tasks.values() if task.title in titles]

        if (len(tasks) < len(titles)):
            raise TodolystExceptions.TaskNotFoundException(
                "One or several ids of tasks to be removed do not correspond to ids from this list.")

        for task in tasks:
            self.tasks.pop(task.id)

    def remove_tasks_by_ids(self, *ids: int):
        """removes all tasks by id

        Raises:
            TodolystExceptions.TaskNotFoundException: raised if a task can't be found in the current list
        """
        ids_to_remove = [id for id in self.tasks.keys() if id in ids]
        if (len(ids_to_remove) < len(ids)):
            raise TaskNotFoundException(
                "One or several ids of tasks to be removed do not correspond to ids from this list.")

        for id in ids_to_remove:
            self.tasks.pop(id)

    def begin_task(self, *titles: str):
        """Sets the state of the tasks to TaskState.in_progress
        """
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.in_progress)

    def complete_task(self, *titles: str):
        """Sets the state of the tasks to TaskState.complete
        """
        tasks = [task for task in self.tasks.values() if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.complete)

    # Display taks from the list, can be filtered to display only a certain category
    def display_tasks(self, category: str = None):
        """Displays all tasks in current list with the possibility to filter by category

        Args:
            category (str, optional): If category is set, only tasks of this particular category will be shown. Defaults to None.

        Raises:
            TodolystExceptions.CategoryNotFoundException: Is raised if a category is set but does not exist
        """
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


'''
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
'''
