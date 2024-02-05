

# Phase 3 Final Project: CLI for Course & Assignment models

## Project Description
There are two model classes, Course and Assignment for this CLI(Command Line Interface) project. These models has an one-to-many relationship. There are many assignments for a course but an assignment can only belongs to one particular course. ORM(Object-Relational Mapping) is applied. From CLI, you can not only view courses and assignments but also add, update, or delete courses or assignments.

It is developed using python and sqlite3.

## Installation
- Run pipenv install and then pipenv shell
- Creating courses & assignments data: Run 'python lib/debug.py' from the root project directory. Or you can also refer to debug.py to buid your own data.
- Run CLI: Run 'python lib/cli.py' from the root project directory.

## Demo
![](https://github.com/kjbyun0/phase-3-my-final-project/blob/main/ForReadme.gif)