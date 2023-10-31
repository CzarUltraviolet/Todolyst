"""Exceptions used by the TodoList module"""


class DuplicateTaskException(Exception):
    """Exception raised when 2 Tasks have the same title."""

    def __init__(self, message="Error, can't have two tasks with the same title in a taskList.\n"):
        self.message = message
        super().__init__(message)


class TaskNotFoundException(Exception):
    """Exception raised when trying to remove a Task that does not exist."""

    def __init__(self, message):
        super().__init__(message)


class CategoryNotFoundException(Exception):
    """Exception raised when trying to add a Task to a Category that does not exist."""

    def __init__(self, message):
        super().__init__(message)
