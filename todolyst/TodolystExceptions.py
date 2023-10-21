

class DuplicateTaskException(Exception):
    
    def __init__(self, message="Error, can't have two tasks with the same title in a taskList.\n"):
        self.message = message
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CategoryNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

