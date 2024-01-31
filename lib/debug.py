#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.course import Course
from models.assignment import Assignment
import ipdb

Course.drop_table()
Assignment.drop_table()
Course.create_table()
Assignment.create_table()
math_100 = Course.create('Math100', 'Algebra', 4.0, 'Spring 2024')
bio_100 = Course.create('Bio100', 'Intro to Bio', 3.0, 'Fall 2023')
phy_200 = Course.create('Phy200', 'Advanced Physics', 4.0, 'Summer 2024')
math_assign_1 = Assignment.create('math assignment 1', 'math assignment desc 1', '1-1-2024', math_100.id)
math_assign_2 = Assignment.create('math assignment 2', 'math assignment desc 2', '1-5-2024', math_100.id)
math_assign_3 = Assignment.create('math assignment 3', 'math assignment desc 3', '1-10-2024', math_100.id)
bio_assign_1 = Assignment.create('bio assignment 1', 'bio assignment desc 1', '09-01-2023', bio_100.id)
bio_assign_2 = Assignment.create('bio assignment 2', 'bio assignment desc 2', '09-05-2023', bio_100.id)
bio_assign_3 = Assignment.create('bio assignment 3', 'bio assignment desc 3', '09-10-2023', bio_100.id)
phy_assign_1 = Assignment.create('phy assignment 1', 'phy assignment desc 1', '7-01-2024', phy_200.id)
phy_assign_2 = Assignment.create('phy assignment 2', 'phy assignment desc 2', '07-5-2024', phy_200.id)
phy_assign_3 = Assignment.create('phy assignment 3', 'phy assignment desc 3', '07-10-2024', phy_200.id)

ipdb.set_trace()
