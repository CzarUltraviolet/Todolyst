

class DuplicateTaskException(Exception):
    
    def __init__(self, message):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CategoryNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

