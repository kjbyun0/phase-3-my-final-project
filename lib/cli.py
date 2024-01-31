# lib/cli.py

from helpers import (
    exit_program,
    back_to_prev_menu,
    # first level
    disp_course_list,
    # second level
    disp_course_detail,
    create_course,
    #third level
    disp_assignment_detail,
    update_course,
    delete_course,
    create_assignment
)

# Item in the menu_level is a list containing the followings:
# - index: index of current menu at the menu_map
# - function : function executed for current menu
# - choice: user input at the current menu
# - more custome data can be added if needed.
menu_level = []
menu_map = [ \
    [ \
        "Type C or c to see all courses", \
        "C", \
        disp_course_list, \
        [ \
            [ \
                "Select a number for detail course information", \
                "NUM", \
                disp_course_detail, \
                [ \
                    [ \
                        "Select a number for more detail assingment information", \
                        "NUM", \
                        disp_assignment_detail, \
                        [ \
                            [ \
                                "Type B or b to go back to the previous menu", \
                                "B", \
                                back_to_prev_menu, \
                                [] \
                            ], \
                            [ \
                                "Type E or e to exit", \
                                "E", \
                                exit_program, \
                                [] \
                            ] \
                        ] \
                    ], \
                    [ \
                        "Type U or u to update the course", \
                        "U", \
                        update_course, \
                        [] \
                    ], \
                    [ \
                        "Type D or d to delete the course", \
                        "D", \
                        delete_course, \
                        [] \
                    ], \
                    [ \
                        "Type A or a to add a new assignment", \
                        "A", \
                        create_assignment, \
                        [] \
                    ], \
                    [ \
                        "Type B or b to go back to the previous menu", \
                        "B", \
                        back_to_prev_menu, \
                        [] \
                    ], \
                    [ \
                        "Type E or e to exit", \
                        "E", \
                        exit_program, \
                        [] \
                    ] \
                ] \
            ], \
            [ \
                "Type A or a to add a new course", \
                "A", \
                create_course, \
                [] \
            ],
            [ \
                "Type B or b to go back to the previous menu", \
                "B", \
                back_to_prev_menu, \
                [] \
            ], \
            [ \
                "Type E or e to exit", \
                "E", \
                exit_program, \
                [] \
            ] \
        ] \
    ], \
    [ \
        "Type E or e to exit", \
        "E", \
        exit_program, \
        [] \
    ] \
]

def disp_menu(cur_menu):
    print("Please, choose from the following: ")
    for menu_item in cur_menu:
        print(menu_item[0])
    print("")

def execute_choice(choice, cur_menu):
    for index, menu_item in enumerate(cur_menu):
        if menu_item[1] == choice or (menu_item[1] == "NUM" and choice.isdigit()):
            menu_level.append([index, menu_item[2], choice])
            menu_item[2](choice, menu_level)
            return
    print("Invalid input!")

def main():
    while True:
        print("menu_level: ", menu_level)
        
        cur_menu = menu_map
        for idx, *_ in menu_level:
            cur_menu = cur_menu[idx][3]

        print("cur_menu: ", cur_menu[0][0])
        
        disp_menu(cur_menu)
        choice = input("> ").upper()
        execute_choice(choice, cur_menu)

        # if choice == "0":
        #     exit_program()
        # elif choice == "1":
        #     helper_1()
        # else:
        #     print("Invalid choice")

if __name__ == "__main__":
    main()
