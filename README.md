# Evaluation project for BGDIA700

This project is part of the evaluation for the BDGIA700 - Kit Data Science module for the IA and Big Data Mastères spécialisés.
Its goal is to show how Python code should be produced in production, showcasing good practices such as:
 - code structure
 - Python environment managed (with Poetry)
 - Object-oriented programming
 - type hinting
 - log management
 - PEP8
 - exception management
 - security
 - unit tests... (with Pytest) and code coverage
 - documentation (with Sphinx)
 - a simple CI/CD pipeline (with Github Actions)

A complete description of the assignement (in French) can be found at: https://ecampus.paris-saclay.fr/pluginfile.php/2624407/mod_resource/content/0/Projet%20_coder%20en%20Python%20pour%20la%20production.pdf

## Quickstart

This package follows a simple structure, you manipulate lists (TaskList) of tasks (_Task).
First clone the package in a folder of your choice : `git clone git@github.com:CzarUltraviolet/Todolyst.git`
Then ensure you are currently using python 3.11 or higher.
Install the package locally usuing `pip install Todolyst`, or `pip install .` while at the root of the project.
You can then use the packge simply with 
```py
from todolyst.TodoLyst import *

```
for example.


### Create a new list
```py
mylist = TaskList()
```

### Add tasks
```py
mylist.add_task("first task","description for first task")
# You can add a task in a particular category
mylist.add_task("first task","description for first task",category="Work")
```

### Change task state
```py
mylist.begin_task("first task")
mylist.complete("first_task")
# You can change the state of several tasks at once
mylist.complete("third_task","fourth_task")
```

### Display tasks
```py
mylist.display_tasks()
# Display by categories
mylist.display_tasks(category="Work")
```

### Add custom  category
Default available categories are Default", "Work", "Personal". You can add a custom category using the following function.
```py
add_category("mycategory")
```



## Running tests

### Prerequisite
In order to run tests, coverage and pytest are needed:
`pip install pytest`
`pip install coverage`

To run tests, from the root of the project, run:
`python3 -m coverage run -m pytest tests`

To see the code coverage of the tests, run:
`python3 -m coverage report`

(See .coveragerc for the exact config of coverage)
