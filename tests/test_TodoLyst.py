
import contextlib
from io import StringIO
from todolyst import TodoLyst
import re
from todolyst.TodolystExceptions import TaskNotFoundException, DuplicateTaskException
# Tests for TaskList
import pytest


import logging
from logging.handlers import TimedRotatingFileHandler


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
    with pytest.raises(Exception) as einfo:
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

    with pytest.raises(Exception):
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


def test_remove_task_by_title_raise_expt():
    '''Checks that trying to remove a task not in task list raise exception'''
    task_list = TodoLyst.TaskList()
    task_list.add_task("title_01")
    task_list.add_task("title_02")
    task_list.add_task("title_03")

    with pytest.raises(Exception):
        task_list.remove_tasks_by_titles(
            "title_01", "title_02", "title_03", "title_04")


def test_display_task():
    """Checks the tasks are displayed"""
    task_list = TodoLyst.TaskList()
    # Captures output on stdout.
    # Allows testing what is printed to the console.
    # See: https://stackoverflow.com/a/17981937/2112089
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        task_list.display_tasks()
    output = temp_stdout.getvalue().strip()

    assert len(output) >= 1


def test_display_task_raises_exception():
    """Checks the display_task function raises an error 
    when the category supplied in parameter doesn't exist"""
    task_list = TodoLyst.TaskList()

    with pytest.raises(Exception):
        task_list.display_tasks("unexisting_cat")
