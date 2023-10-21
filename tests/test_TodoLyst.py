
from todolyst import TodoLyst
from todolyst.TodolystExceptions import TaskNotFoundException,DuplicateTaskException
# Tests for TaskList
import pytest




def test_add_task():
    '''Checks that adding a task increments the length of the task list by 1'''
    task_list = TodoLyst.TaskList()
    initial_length = len(task_list.tasks)
    task_list.add_task("Testtask02")
    assert len(task_list.tasks) == initial_length + 1


def test_add_duplicate_task():
    '''Checks that adding a task of same title raises an exception'''
    task_list_exceptions = TodoLyst.TaskList()
    initial_length = len(task_list_exceptions.tasks)
    task_list_exceptions.add_task("Testtask02")
    with pytest.raises(DuplicateTaskException) as einfo:
        # raise DuplicateTaskException('zefez')
        task_list_exceptions.add_task("Testtask02")


def test_remove_task_by_title():
    '''Checks that removing a task decrements the length of the task list by 1'''
    task_list = TodoLyst.TaskList()

    task_list.add_task("Testtask03")
    initial_length = len(task_list.tasks)

    task_list.remove_tasks_by_titles("Testtask03")
    assert len(task_list.tasks) == initial_length - 1


def test_remove_task_by_id():
    '''Checks that removing a task decrements the length of the task list by 1'''
    task_list = TodoLyst.TaskList()

    task_list.add_task("Testtask04")
    initial_length = len(task_list.tasks)

    task_list.remove_tasks_by_ids(TodoLyst._max_id-1)
    assert len(task_list.tasks) == initial_length - 1


def test_remove_task_by_id_exception():
    '''Checks that removing a task decrements the length of the task list by 1'''
    task_list = TodoLyst.TaskList()

    with pytest.raises(TaskNotFoundException):
        task_list.remove_tasks_by_ids(TodoLyst._max_id-1)


def test_begin_task():
    '''Checks that calling begin_task sets the task's state to in_progress'''
    task_list = TodoLyst.TaskList()
    test_title = "Testtask01"
    task_list.add_task(test_title)

    task = [task for task in task_list.tasks.values()
            if task.title in test_title][0]
    # task = tasks[0]
    assert task.state == TodoLyst.TaskState.todo

    task_list.begin_task(test_title)
    task = [task for task in task_list.tasks.values()
            if task.title in test_title][0]

    assert task.state == TodoLyst.TaskState.in_progress


def test_complete_task():
    '''Checks that calling complete_task sets the task's state to complete'''
    task_list = TodoLyst.TaskList()
    test_title = "Testtask05"
    task_list.add_task(test_title)

    task = [task for task in task_list.tasks.values()
            if task.title in test_title][0]
    assert task.state == TodoLyst.TaskState.todo

    task_list.complete_task(test_title)
    task = [task for task in task_list.tasks.values()
            if task.title in test_title][0]

    assert task.state == TodoLyst.TaskState.complete
