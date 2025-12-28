import json
import hashlib
import time
import getpass
import menus
from menus import admin, main, login, librarian, member,requests_menu,manage_books_menu,manage_users_menu,add_user,de_user,delete_user,show_users,search_menu
from utils import sprint, clear_screen,print_centered


login_loop = True
is_runnig = True
user_role = None
seconds = 0.5

STATES = {
    "MAIN": main,
    "LOGIN": login,
    "ADMIN": admin,
    "LIBRARIAN": librarian,
    "MEMBER": member,
    "REQUESTS" : requests_menu,
    "BOOKS" : manage_books_menu,
    "SHOW_USERS" : show_users,
    "BOOKSEARCH" : search_menu,
    "ADDBOOK" : menus.add_book,
    "EDITBOOK" : menus.edit_book,
    "DELBOOK" : menus.delete_book,
    "SHOWB" : menus.show_borrowed_books,
    "RR" : menus.Return_request,
    "ER" : menus.Extension_request,
    "MUSERS" : manage_users_menu,
    "ADD_USER" : add_user,
    "DE_USER" : de_user,
    "DELETE_USER" : delete_user
    
}
FILES = {
    "users": ("users.json", [
        {
            "id": 1,
            "username": "admin",
            "password": "4b1b8aa3608a26da451ae0630d75b60ab1bc2dd229c41a80838fc7993e835c46",
            "full_name": "admin",
            "role": "admin"
        }
    ]),
    "books": ("books.json", [{}]),
    "loans": ("loans.json", [{}])
}


def first_run_creation(filename, content):
    try:
        with open(filename, "x") as f:
            json.dump(content, f)
    except FileExistsError:
        pass


# create data files
for filename, content in FILES.values():
    first_run_creation(filename, content)

clear_screen()
#print("\nWelcome to Library Management System")

runner = True
State = "MAIN"
while runner:
    func = STATES.get(State)
    if func:
        State = func()
    else :
        clear_screen()
        time.sleep(0.5)
        print_centered(["Good bye!"])
        time.sleep(0.5)
        runner = False
        break



