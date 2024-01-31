# lib/helpers.py
from models.course import Course
from models.assignment import Assignment

#bkj -  global variables
# courses = []
# assignments = []

def exit_program(choice, menu_level):
    print("exit_program!")
    exit()

def back_to_prev_menu(choice, menu_level):
    # print('prev_menu!')
    # print('in prev_menu, 1. menu_level: ', menu_level)
    menu_level.pop()
    menu_level.pop()
    print('in prev_menu, 2. menu_level: ', menu_level)
    if len(menu_level) > 0:
        menu_level[-1][1](menu_level[-1][2], menu_level)

def disp_prev_menu(choice, menu_level):
    menu_level.pop()
    menu_level[-1][1](menu_level[-1][2], menu_level)

def disp_course_list(choice, menu_level):
    # print("disp_course_list!")
    # print("choice: ", choice, ", menu_level: ", menu_level)
    try:
        # global courses
        courses = Course.get_all()
        print("- Courses")
        print("****************************************")
        for index, course in enumerate(courses):
            print(f'{index+1}. {course.name}')
        print("****************************************")
        # adding course list for next level menu
        menu_level[-1].append(courses)
    except Exception as exc:
        print("Error displaying courses: ", exc)
        disp_prev_menu(choice, menu_level)

def disp_course_detail(choice, menu_level):
    # print("disp_course_detail!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    courses = menu_level[-2][3]
    c_idx = int(choice) - 1
    if c_idx < 0 or c_idx >= len(courses):
        print(f"Invalid input - {choice} isn't in the list!")
        disp_prev_menu(choice, menu_level)
        return
    
    print(f"- Name: {courses[c_idx].name}")
    print(f"- Description: {courses[c_idx].desc}")
    print(f"- Credit: {courses[c_idx].credit}")
    print(f"- Semester: {courses[c_idx].semester}")

    try:
        assignments = courses[c_idx].assignments()
        print("****************************************")
        for a_idx, assignment in enumerate(assignments):
            print(f"{a_idx + 1}. {assignment.name}")
        print("****************************************")
        # adding course and its assignment list for next level menu
        menu_level[-1].append(courses[c_idx])
        menu_level[-1].append(assignments)
    except Exception as exc:
        print("Error displaying the course's detail information: ", exc)
        disp_prev_menu(choice, menu_level)

# def disp_course_detail(choice, menu_level):
#     print("disp_course_detail!")
#     print("choice: ", choice, "menu_level: ", menu_level)

#     #bkj - the following routine is already in disp_course_list(). 
#     #      is there a way to use the result got from disp_course_list()???
#     idx = int(choice) - 1
#     if idx < 0 or idx >= len(courses):
#         print("Invalid Input - Number isn't in the course list.")
#         disp_prev_menu(choice, menu_level)
#         return

#     print(f"- Name: {courses[idx].name}")
#     print(f"- Description: {courses[idx].desc}")
#     print(f"- Credit: {courses[idx].credit}")
#     print(f"- Semester: {courses[idx].semester}")
#     try:
#         global assignments
#         assignments = courses[idx].assignments()
#         print("****************************************")
#         for index, assignment in enumerate(assignments):
#             print(f"{index+1}. {assignment.name}")
#         print("****************************************")
#     except Exception as exc:
#         print("Error displaying the course's assignments: ", exc)
#         disp_prev_menu(choice, menu_level)
        
def create_course(choice, menu_level):
    # print("create_course!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    try:
        name = input("Enter the course name: ")
        desc = input("Enter the course description: ")
        credit = float(input("Enter the course's credit: "))
        semester = input("Enter the course's semester: ")
        Course.create(name, desc, credit, semester)
        print(f"{name} course is added!")
    except Exception as exc:
        print("Error creating a course: ", exc)

    disp_prev_menu(choice, menu_level)
    
def disp_assignment_detail(choice, menu_level):
    # print("disp_assignment_detail!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    course = menu_level[-2][3]
    assignments = menu_level[-2][4]
    a_idx = int(choice) - 1
    if a_idx < 0 or a_idx >= len(assignments):
        print(f"Invalid input - {choice} isn't in the list!")
        disp_prev_menu(choice, menu_level)
        return

    print(f"- Name: {assignments[a_idx].name}")
    print(f"- Description: {assignments[a_idx].desc}")
    print(f"- Due Date: {assignments[a_idx].due_date}")
    print(f"- Course Name: {course.name}")

    # adding the assignment for next level menu
    menu_level[-1].append(assignments[a_idx])

# def disp_assignment_detail(choice, menu_level):
#     print("disp_assignment_detail!")
#     print("choice: ", choice, "menu_level: ", menu_level)

#     idx = int(choice) - 1
#     if 0 <= idx < len(assignments):
#         print(f"- Name: {assignments[idx].name}")
#         print(f"- Description: {assignments[idx].desc}")
#         print(f"- Due Date: {assignments[idx].due_date}")
#         for course in courses:
#             if course.id == assignments[idx].course_id:
#                 print(f"-Course Name: {course.name}")
#                 break
#     else:
#         print("Invalid Input - Number isn't in the assignment list.")
#         disp_prev_menu(choice, menu_level)

def update_course(choice, menu_level):
    # print("update_course!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    course = menu_level[-2][3]
    try:
        name = input(f"Enter name for {course.name}'s to change or hit <enter> to leave it as is: ")
        if name != '':
           course.name = name
        desc = input(f"Enter a new description or hit <enter> to leave it as is: ")
        if desc != '':
            course.desc = desc
        credit = input(f"Enter credit for {course.credit}'s to change or hit <enter> to leave it as is: ")
        if credit != '':
            course.credit = float(credit)
        semester = input(f"Enter credit for {course.semester}'s to change or hit <enter> to leave it as is: ")
        if semester != '':
            course.semester = semester
        course.update()
        print(f"{course.name} is updated!")
    except Exception as exc:
        print("Error updating the course: ", exc)
    
    disp_prev_menu(choice, menu_level)
    
def delete_course(choice, menu_level):
    # print("delete_course!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    course = menu_level[-2][3]
    name = course.name
    try:
        course.delete()
        print(f"{name} is deleted!")
        back_to_prev_menu(choice, menu_level)
    except Exception as exc:
        print("Error deleting the course: ", exc)
        disp_prev_menu(choice, menu_level)

def create_assignment(choice, menu_level):
    # print("create_assignment!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    course = menu_level[-2][3]
    try:
        name = input("Enter an assignment name: ")
        desc = input("Enter its assignment description: ")
        due_date = input("Enter its due_date in mm-dd_yyyy format: ")
        assignment = Assignment.create(name, desc, due_date, course.id)
        print(f"{name} assignment is added!")
    except Exception as exc:
        print("Error creating an assignment: ", exc)
    
    disp_prev_menu(choice, menu_level)

def update_assignment(choice, menu_level):
    # print("update_assignment!")
    # print("choice: ", choice, "menu_level: ", menu_level)

    assignment = menu_level[-2][3]
    try:
        name = input(f"Enter name for {assignment.name}'s to change or hit <enter> to leave it as is: ")
        if name != '':
            assignment.name = name
        desc = input(f"Enter a new description or hit <enter> to leave it as is: ")
        if desc != '':
            assignment.desc = desc
        due_date = input(f"Enter due date for {assignment.due_date}'s to change or hit <enter> to leave it as is: ")
        if due_date != '':
            assignment.due_date = due_date
        assignment.update()
        print(f"{assignment.name} is updated!")
    except Exception as exc:
        print("Error updating an assignment: ", exc)

    disp_prev_menu(choice, menu_level)

def delete_assignment(choice, menu_level):
    # print("delete_assignment!")
    # print("choice: ", choice, "menu_level: ", menu_level)
    
    assignment = menu_level[-2][3]
    name = assignment.name
    try:
        assignment.delete()
        print(f"{name} is deleted!")
        back_to_prev_menu(choice, menu_level)
    except Exception as exc:
        print("Error deleting the assignment: ", exc)
        disp_prev_menu(choice, menu_level)
