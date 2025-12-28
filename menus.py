import os
import shutil
import hashlib
import time
import json
from utils import sprint, clear_screen, draw_footer, print_centered, centered_slow_print
from rapidfuzz import fuzz
import time
from session import session


seconds = 0.5

def show_borrowed_books():
    pass
def Extension_request():
    pass
def Return_request():
    pass
def search_menu():
    clear_screen()
    book_name = print_centered("","Please Enter the book name : ", "[0] Back")
    results = []
    with open("books.json", "r") as f:
        books = json.loads(f)
        for book in books:
            score = fuzz.partial_ratio()
            if score >= 70:
                results.append(score, book)
        results.sort(reverse=True, key=lambda x: x[0])
    print_centered(results,"","[0] Back")
    


def show_users():
    with open("users.json", "r") as f:
        users = json.load(f)

    if not users:
        print_centered(["No users found!"])
        time.sleep(1)
        return "MUSERS"

    display_lines = ["=== Users ===", ""]
    header = f"{'Username':<20} | {'Full Name':<20} | {'Role':<10}"
    display_lines.append(header)
    display_lines.append("-" * len(header))

    for u in users:
        line = f"{u['username']:<20} | {u['full_name']:<20} | {u['role']:<10}"
        display_lines.append(line)

    display_lines.append("")
    display_lines.append("")

    print_centered(display_lines, "", "[0] Back")

    return "MUSERS"


def add_user():
    with open("users.json", "r") as f:
        users = json.load(f)
    usernames = {u["username"] for u in users}
    while True:
        username = print_centered("", "username : ", "[0] Back")
        if username == "0":
            return "MUSERS"
        if username in usernames:
            clear_screen()
            print_centered(["Username aleardy is taken"])
            time.sleep(1)
            continue
        while True:
            password = print_centered(
                ["username : " + f"{username}"], "password : ", "[0] Back")
            if password == "0":
                break
            elif len(password) < 5:
                print_centered(["Password must be more than 5 characters."])
                time.sleep(1)
                continue
            while True:
                full_name = print_centered(
                    ["username : " + f"{username}", "password : " + f"{password}"], "full_name : ", "[0] Back")
                if full_name == "0":
                    break
                if not full_name:
                    print_centered(["Enter a Valid name"])
                    time.sleep(1)
                    continue
                while True:
                    role = print_centered(
                        ["username : " + f"{username}", "password : " + f"{password}", "full_name : "+f"{full_name}"], "role : ", "[0] Back").lower()
                    if role == "0":
                        break
                    if not role in ["admin", "librarian", "member"]:
                        print_centered(["Invalid Role!"])
                        time.sleep(1)
                        continue

                    new_user = {
                        "username": username,
                        "password": hashlib.sha256(password.encode()).hexdigest(),
                        "full_name": full_name,
                        "role": role
                    }
                    users.append(new_user)
                    with open("users.json", "w") as fw:
                        json.dump(users, fw, indent=4)
                    print_centered(["User added successfully!"])
                    time.sleep(1)
                    return "ADD_USER"
                continue
            continue
        continue


def de_user():
    return "MUSERS"


def add_book():
    pass
def edit_book():
    pass
def delete_book():
    with open("books.json", "r") as f:
        books = json.load(f)

    while True:
        title = print_centered(
            "",
            "Please enter the title of the book : ",
            "[0] Back"
        )

        if title == "0":
            return "BOOKS"

        matching_titles = [b for b in books if b["title"] == title]

        if not matching_titles:
            print_centered(["Book not found!"])
            time.sleep(1)
            continue

        if len(matching_titles) == 1:
            books.remove(matching_titles[0])
            with open("books.json", "w") as f:
                json.dump(books, f, indent=4)

            print_centered(["Book successfully deleted!"])
            time.sleep(1)
            return "BOOKS"

        while True:
            author = print_centered(
                [f"Title: {title}"],
                "Please enter the author of the book:",
                "[0] Back"
            )

            if author == "0":
                break

            book = next(
                (b for b in matching_titles if b["author"] == author),
                None
            )

            if book:
                books.remove(book)
                with open("books.json", "w") as f:
                    json.dump(books, f, indent=4)

                print_centered(["Book successfully deleted!"])
                time.sleep(1)
                return "BOOKS"
            else:
                print_centered(["Author not found for this title!"])
                time.sleep(1)

def delete_user():
    with open("users.json", "r") as f:
        users = json.load(f)
    usernames = {u["username"] for u in users}
    while True:
        username = print_centered(
            "", "Please enter the username : ", "[0] Back")
        if username == "0":
            return "MUSERS"
        if username in usernames:
            users = [u for u in users if u["username"] != username]
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
            print_centered(["User succesfully deleted!"])
            time.sleep(1)
        else:
            print_centered(["User not found!"])


def manage_books_menu():
    Lines = ["=== Books Management ===", "1. Add New Book", "2. Edit Book",
             "3. Delete Book"]
    choice = print_centered(Lines, ">>", "[0] Back")
    if choice == "0":
        return session.role
    elif choice == "1":
        return "ADDBOOK"
    elif choice == "2":
        return "EDITBOOK"
    elif choice == "3":
        return "DELBOOK"
    else :
        return "BOOKS"
    pass


def manage_users_menu():
    Lines = ["=== User manager menu ===", "1. Show Users", "2. Register New User",
             "3. Deactivate User", "4. Delete User"]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    if choice == "":
        return "MUSERS"
    if choice == "1":
        return "SHOW_USERS"
    if choice == "2":
        return "ADD_USER"
    elif choice == "3":
        return "DE_USER"
    elif choice == "4":
        return "DELETE_USER"
    elif choice == "0":
        return "ADMIN"


def requests_menu():
    clear_screen()
    Lines = ["=== Requests ===", ""]
    f = open("loans.json", "r+")

    print_centered


def main():
    clear_screen()
    Lines = ["=== Library Management System ===",
             "", "", "1. Login", "", "0. Exit", ""]
    choice = print_centered(Lines, "")
    # print("1. Login")
    # print("0. Exit")
    if choice == "4":
        return "ADD_USER"
    if choice == "1":
        return "LOGIN"
    elif choice == "0":
        return choice
    else:
        return "MAIN"


def login():
    login_loop = True

    with open("users.json", "r") as f:
        users = json.load(f)
    while login_loop:
        userfound = False
        clear_screen()
        username = print_centered(
            ["=== Login ===", "", ""], "Please enter the username : ", "[0] Back")
        if username == "0":
            return "MAIN"
        password = print_centered(
            ["=== Login ===", "", "", f"Please enter the username : {username}"], "Please enter the password : ")
        clear_screen()
        for user in users:
            if user["username"] == username:
                userfound = True
                if user["password"] == hashlib.sha256(password.encode()).hexdigest():
                    session.username = username
                    session.role = user["role"].upper()
                    session.logged_in = True
                    time.sleep(seconds)
                    print_centered(["Login successful!"])
                    return user["role"].upper()
                    # user_role = user["role"]
                    # runner = False
                    login_loop = False
                    break
                else:
                    centered_slow_print(
                        ["Username or password is incorrect", ""], "Try again")
                    time.sleep(.25)
        if not userfound:
            centered_slow_print(
                ["Username or password is incorrect", ""], "Try again")
            time.sleep(.25)


def admin():
    clear_screen()
    Lines = [
        "=== Admin panel ===",
        "1. View and manage requests",
        "2. Add / Edit / Delete books",
        "3. Manage users", "", ""
    ]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    if choice == "1":
        return "REQUESTS"
    elif choice == "2":
        return "BOOKS"
    elif choice == "3":
        return "MUSERS"
    elif choice == "0":
        return "MAIN"
    else:
        return "ADMIN"


def librarian():
    clear_screen()
    Lines = [
        "=== Librarian panel ===",
        "1. View and manage requests",
        "2. Add / Edit / Delete books", "",""
    ]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    
    if choice == "0":
        return "MAIN"
    elif choice == "1":
        return "REQUESTS"
    elif choice == "2":
        return "BOOKS"
    else:
        return "LIBRARIAN"




def member():
    clear_screen()
    Lines = [
    "=== Member Panel ===",
    "1. Search books",
    "2. View borrowed books",
    "3. Extension request",
    "4. Return request",
    "0. Return to main menu",
    ]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    
    if choice == "0":
        return "MAIN"
    elif choice == "1":
        return "BOOKSEARCH"
    elif choice == "2":
        return "SHOWB"
    elif choice == "3":
        return "ER"
    elif choice == "4":
        return "RR"
    else:
        return "MEMBER"



'''def admin():
    clear_screen()
    print_centered(["=== Admin panel ==="],["1. View and manage requests"],"2. Add / Edit / Delete books")
    print("=== Admin panel ===")
    print("1. View and manage requests")
    print("2. Add / Edit / Delete books")
    print("3. Manage users")
    print("0. Return to main menu")
    return input("Select an option: ")'''


'''
import os
import shutil
import hashlib
import time
import json
from utils import sprint, clear_screen, draw_footer, print_centered, centered_slow_print
from rapidfuzz import fuzz
from rich.console import Console
from rich.align import Align


seconds = 0.5




def add_user(console):
    f = open("users.json", "r+")
    users = json.load(f)
    while True:
        username = print_centered("", "username : ", "[0] Back")
        if username in {u["username"] for u in users}:
            print("\rUsername aleardy is taken.")
            time.sleep(2)
        elif username == "0":
            return "MUSERS"
        else:
            password = print_centered(
                ["username : " + f"{username}"], "password : ", "[0] Back")
            full_name = print_centered(
                ["username : " + f"{username}", "password : " + f"{password}"], "full_name : ", "[0] Back")
            role = print_centered(
                ["username : " + f"{username}", "password : " + f"{password}", "full_name : "+f"{full_name}"], "role : ", "[0] Back")


def de_user(console):
    pass


def delete_user(console):
    pass


def manage_books_menu(console):
    pass


def manage_users_menu(console):
    Lines = ["=== User manager menu ===", "1. Register New User",
             "2. Deactivate User", "3. Delete User"]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    if choice == "1":
        return "ADD_USER"
    elif choice == "1":
        return "DE_USER"
    elif choice == "3":
        return "DELETE_USER"
    elif choice == "0":
        return "ADMIN"


def requests_menu(console):
    clear_screen()
    Lines = ["=== Requests ===", ""]
    f = open("loans.json", "r+")

    print_centered


def main(console):
    clear_screen()
    Lines = ["=== Library Management System ===",
             "", "", "1. Login", "", "0. Exit", ""]
    choice = print_centered(Lines, "")
    # print("1. Login")
    # print("0. Exit")
    if choice == "4":
        return "ADD_USER"
    if choice == "1":
        return "LOGIN"
    else:
        return choice


def login(console):
    login_loop = True

    f = open("users.json", "r+")
    users = json.loads(f.read())
    while login_loop:
        userfound = False
        clear_screen()
        username = print_centered(
            ["=== Login ===", "", ""], "Please enter the username : ", "[0] Back")
        if username == "0":
            return "MAIN"
        password = print_centered(
            ["=== Login ===", "", "", f"Please enter the username : {username}"], "Please enter the password : ")
        clear_screen()
        for user in users:
            if user["username"] == username:
                userfound = True
                if user["password"] == hashlib.sha256(password.encode()).hexdigest():
                    time.sleep(seconds)
                    print_centered(["Login successful!"])
                    return user["role"].upper()
                    # user_role = user["role"]
                    # runner = False
                    login_loop = False
                    break
                else:
                    centered_slow_print(
                        ["Username or password is incorrect", ""], "Try again")
                    time.sleep(.25)
        if not userfound:
            centered_slow_print(
                ["Username or password is incorrect", ""], "Try again")
            time.sleep(.25)
    f.close()


def admin(console):
    clear_screen()
    Lines = [
        "=== Admin panel ===",
        "1. View and manage requests",
        "2. Add / Edit / Delete books",
        "3. Manage users", "", ""
    ]
    choice = print_centered(Lines, ">>> ", "[0] Back")
    if choice == "1":
        return "REQUESTS"
    elif choice == "2":
        return "BOOKS"
    elif choice == "3":
        return "MUSERS"
    elif choice == "0":
        return "MAIN"


def librarian(console):
    clear_screen()
    print("=== Librarian panel ===")
    print("1. View and manage requests")
    print("2. Add / Edit / Delete books")


def search_menu(console):
    clear_screen()
    book_name = input("Please Enter the book name : ")
    draw_footer("Press 0 to go back | ESC to exit")
    results = []
    with open("books.json", "r") as f:
        books = json.loads(f)
        for book in books:
            score = fuzz.partial_ratio()
            if score >= 70:
                results.append(score, book)
        results.sort(reverse=True, key=lambda x: x[0])

    print(results)


def member(console):
    clear_screen()
    print("=== Member Panel ===")
    print("1. Search books")
    print("2. View borrowed books")
    print("3. Extension request")
    print("4. Return request")
    print("0. Return to main menu")
    choice = input(">>> ")
    if choice == "1":
        search_menu() '''
