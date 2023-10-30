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

## Running tests

### Prerequisite
In order to run tests, coverage and pytest are needed:

`pip install pytest`

`pip install coverage`

### Run
To run tests, from the root of the project, run:

`python3 -m coverage run -m pytest tests`

To see the code coverage of the tests, run:

`python3 -m coverage report`

(See .coveragerc for the exact config of coverage)

## Running the project

To run from the todolyst folder:

`python3 TodoLyst.py`
