from dataclasses import dataclass
from enum import Enum


class TaskState(Enum):
    todo = 0
    in_progress = 1
    complete = 2


_max_id: int = 0


class _Task:
    id: int
    title: str
    state: TaskState

    def __init__(self, title) -> None:
        global _max_id
        self.title = title
        self.state = TaskState.todo
        self.id = _max_id
        _max_id += 1
    
    def set_state(self, new_state: TaskState):
        self.state = new_state

    def display(self):
        print("Task : ",self.id)
        print("Title : ",self.title)
        print("State : ",self.state.name)



class TaskList:
    tasks: [] = []

    def __init__(self) -> None:
        pass

    def add_task(self,*titles):
        for title in titles:
            same_tasks = [task for task in self.tasks if task.title == title]
            if (len(same_tasks) > 0):
                print("Erreur impossible d'avoir deux tâches de même titre dans une liste.\n")
                continue
            self.tasks.append(_Task(title))

    def remove_task(self,*titles):
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            self.tasks.remove(tasks[0])

        #if(len(tasks) <1):
        #    print("Erreur, impossible de supprimer la tâche ",title,",celle-ci n'existe pas dans la liste actuelle des tâches.\n")
        #    continue


    def begin_task(self,*titles):
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.in_progress)
            #if(len(tasks) <1):
            #    print("Erreur, impossible de supprimer la tâche ",title,",celle-ci n'existe pas dans la liste actuelle des tâches.\n")
            #    continue

    def complete_task(self,*titles):
        tasks = [task for task in self.tasks if task.title in titles]
        for task in tasks:
            task.set_state(TaskState.complete)



    def display_tasks(self):
        print("Task list contains ",len(self.tasks)," elements.")
        print("--------")

        for i in range(len(self.tasks)):
            self.tasks[i].display()
            print("--------")
        


class Test:
    nom: str

    def __init__(self, string) -> None:
        self.nom = string


testlist = TaskList()
testlist.add_task("test","test2","test3")



testlist.display_tasks()

testlist.remove_task("test2","fze")
testlist.complete_task("test")
testlist.begin_task("test3")

testlist.display_tasks()
