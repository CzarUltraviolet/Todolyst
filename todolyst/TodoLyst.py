from dataclasses import dataclass
from enum import Enum
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

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

    # Create a new task, description can be null and other attributes are not managed by user
    def __init__(self, title: str, description: str = None) -> None:
        """_summary_

        Args:
            title (_type_): _description_
            description (_type_, optional): _description_. Defaults to None.
        """
        global _max_id
        self.title = title
        self.state = TaskState.todo
        self.description = description

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
        print("Task : ", self.id)
        print("Title : ", self.title)
        print("State : ", self.state.name)
        print("Description : ", self.description)
        print("Created on : ", self.creationdate.date(), "at", str(
            self.creationdate.time().hour)+"h"+str(self.creationdate.time().minute))


class TaskList:
    # Container for the
    tasks: [] = []

    def __init__(self) -> None:
        pass

    def add_task(self, title: str, description: str = None):
        """_summary_

        Args:
            title (str): _description_
            description (_type_, optional): _description_. Defaults to None.
        """
        same_tasks = [task for task in self.tasks if task.title == title]
        if (len(same_tasks) > 0):
            print(
                "Erreur impossible d'avoir deux tâches de même titre dans une liste.\n")
        self.tasks.append(_Task(title, description=description))

    def remove_task(self, *titles: str):
        """_summary_

        Args:
            titles (_type_): _description_
        """
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            self.tasks.remove(task)

    def begin_task(self, *titles: str):
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.in_progress)

    def complete_task(self, *titles: str):
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.complete)

    def display_tasks(self):
        print("Task list contains ", len(self.tasks), " elements.")
        print("--------")

        for i in range(len(self.tasks)):
            self.tasks[i].display()
            print("--------")


logger.info("Starting tasklist...")
testlist = TaskList()
testlist.add_task("test", "description1")
testlist.add_task("test2", "description1")
testlist.add_task("test3", "description1")


testlist.display_tasks()

testlist.remove_task("test2", "test3")
testlist.complete_task("test")
testlist.begin_task("test3")
logger.info("Tasklist ended.")
logger.error("Done.")

testlist.display_tasks()
