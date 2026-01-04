import os
import shutil
import hashlib
import time
import json
from utils import sprint, clear_screen, draw_footer, print_centered, centered_slow_print
from rapidfuzz import fuzz
import time
from session import session
import uuid
from datetime import datetime, timedelta


seconds = 0.5


def show_borrowed_books():
    with open("loans.json", "r") as f:
        loans = json.load(f)
    with open("books.json", "r") as f:
        books = json.load(f)

    user_loans = [loan for loan in loans if loan['username']
                  == session.username]
    books_dict = {b['id']: b for b in books}

    borrowed_books = []
    for loan in user_loans:
        if loan["status"] == "approved" :
            book = books_dict.get(loan['book_id'])
            if book:
                borrowed_books.append((loan, book))

    if not borrowed_books:
        print_centered(["You have no borrowed books."])
        time.sleep(2)
        return "MEMBER"

    borrowed_books.sort(
        key=lambda x: datetime.fromisoformat(x[0]["approve_date"]))
    while True:
        display_lines = ["=== Borrowed Books ===", ""]
        header = f"{'No':<4} | {'Title':<30} | {'Author':<20} | {'Category':<15} | {'Borrow Date':<12} | {'Due Date':<12}"
        display_lines.append(header)
        display_lines.append("-" * len(header))
        for i, (loan, book) in enumerate(borrowed_books, 1):
            line = f"{i:<4} | {book['title']:<30} | {book['author']:<20} | {book['category']:<15} | {datetime.fromisoformat(loan["approve_date"]).strftime("%Y-%m-%d"):<12} | {datetime.fromisoformat(loan["due_date"]).strftime("%Y-%m-%d"):<12}"
            display_lines.append(line)
        display_lines.append("")
        display_lines.append("")
        display_lines.append("")

        while True:
            choice = print_centered(
                display_lines, "Select a book to renew or return : ", "[0] Back", False)

            if choice == "0":
                return "MEMBER"
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(borrowed_books):
                print_centered(["Invalid choice!"])
                time.sleep(1)
                continue
            loan, book = borrowed_books[int(choice) - 1]
            break

        while True:
            action = print_centered(
                [f"Selected book '{book['title']}'",
                 "1. Renew",
                 "2. Return"],
                ">>> ", "[0] Back"
            ).strip().lower()

            if action == "0":
                break
            elif action == "1":
                loan["status"] = "renew_pending"
                with open("loans.json", "r") as f:
                    loans = json.load(f)
                for l in loans:
                    if l["loan_id"] == loan["loan_id"]:
                        l.update(loan)
                with open("loans.json", "w") as f:
                    json.dump(loans, f, indent=4)
                print_centered(["Your renewal request has been submitted."])
                time.sleep(2)
                return "SHOWB"
            elif action == "2":
                loan["status"] = "returned"
                loan["return_date"] = datetime.now().isoformat()
                book['available_count'] += 1
                with open("loans.json", "r") as f:
                    loans = json.load(f)
                for l in loans:
                    if l["loan_id"] == loan["loan_id"]:
                        l.update(loan)
                with open("loans.json", "w") as f:
                    json.dump(loans, f, indent=4)
                with open("books.json", "r") as f:
                    books = json.load(f)
                for b in books:
                    if b["id"] == book["id"]:
                        b.update(book)
                with open("books.json", "w") as f:
                    json.dump(books, f, indent=4)
                print_centered(
                    [f"You have successfully returned '{book['title']}'"])
                time.sleep(2)
                return "SHOWB"
            else:
                print_centered(["Invalid choice!"])
                time.sleep(1)
                continue


def show_books():
    with open("books.json", "r") as f:
        books = json.load(f)
    if not books:
        print_centered(["No books available."])
        time.sleep(2)
        return session.role

    while True:
        display_lines = ["=== Books ===", ""]
        header = f"{'No':<4} | {'Title':<30} | {'Author':<20} | {'Category':<15} | {'Avail':<6} | {'Total':<5}"
        display_lines.append(header)
        display_lines.append("-" * len(header))

        for i, book in enumerate(books, 1):
            line = f"{i:<4} | {book['title']:<30} | {book['author']:<20} | {book['category']:<15} | {book['available_count']:<6} | "f"{book['total_count']:<5}"
            display_lines.append(line)

        display_lines.append("")

        choice = print_centered(
            display_lines, "Select a book to edit or delete : ", "[0] Back   [A] Add Book").strip().lower()

        if choice == "0":
            return "BOOKS"
        if choice == "a":
            return "ADDBOOK"
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(books):
            print_centered(["Invalid choice!"])
            time.sleep(1)
            continue

        book = books[int(choice) - 1]
        break
    while True:
        action = print_centered(
            [
                f"Selected book '{book['title']}'","",
                "1. Edit",
                "2. Delete"
            ],
            ">>> ", "[0] Back"
        ).strip()
        if action == "0":
            return "SHOWBOOKS"
        if action == "1":
            while True:
                new_author = print_centered(
                    [f"Current author: {book['author']}"], "Enter new author: ", "[0] Back")
                if new_author == "0":
                    break
                if new_author.strip() == "":
                    print_centered(["Enter a valid author"])
                    time.sleep(1)
                    continue
                book["author"] = new_author.strip()

                while True:
                    new_category = print_centered(
                        [f"Current category: {book['category']}"], "Enter new category: ", "[0] Back")
                    if new_category == "0":
                        break
                    if new_category.strip() == "":
                        print_centered(["Enter a valid category"])
                        time.sleep(1)
                        continue
                    book["category"] = new_category.strip()

                    while True:
                        new_total = print_centered(
                            [f"Current total count: {book['total_count']}"], "Enter new total count: ", "[0] Back")
                        if new_total == "0":
                            break
                        if not new_total.isdigit() or int(new_total) <= 0:
                            print_centered(["Enter a valid number greater than 0"])
                            time.sleep(1)
                            continue
                        diff = int(new_total) - book["total_count"]
                        book["total_count"] = int(new_total)
                        book["available_count"] += diff

                        with open("books.json", "w") as f:
                            json.dump(books, f, indent=4)

                        print_centered(["Book updated successfully!"])
                        time.sleep(1)
                        return "SHOWBOOKS"
        if action == "2":
            if book["available_count"] != book["total_count"]:
                print_centered(["Cannot delete book active loans exist."])
                time.sleep(2)
                continue
            books.remove(book)
            with open("books.json", "w") as f:
                json.dump(books, f, indent=4)
            print_centered(["Book deleted successfully."])
            time.sleep(2)
            return "SHOWBOOKS"
        else:
            print_centered(["Invalid choice!"])
            time.sleep(1)


def search_menu():
    with open("books.json", "r") as f:
        books = json.load(f)
    clear_screen()
    while True:
        book_name = print_centered(
            "", "Please Enter the book name : ", "[0] Back")
        if book_name == "0":
            break
        if len(book_name) <= 3:
            book_name = ""
        results = []
        for book in books:
            score = fuzz.partial_ratio(
                book_name.lower(), book['title'].lower())
            if score >= 70:
                results.append((score, book))
        results.sort(reverse=True, key=lambda x: x[0])
        if not results:
            print_centered(["No matching books found."])
            time.sleep(1)
            continue

        while True:
            display_lines = ["=== Matching Books ===", ""]
            header = f"{'No':<4} | {'Title':<30} | {'Author':<20} | {'Category':<15} | {'Total':<5} | {'Available':<10}"
            display_lines.append(header)
            display_lines.append("-" * len(header))
            for i, (score, book) in enumerate(results, 1):
                line = f"{i:<4} | {book['title']:<30} | {book['author']:<20} | {book['category']:<15} | {book['total_count']:<5} | {book['available_count']:<10}"
                display_lines.append(line)
            display_lines.append("")
            display_lines.append("")
            display_lines.append("")

            choice = print_centered(
                display_lines, "chose a book for borrowing : ", "[0] Back", False)

            if choice == "0":
                break
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
                print_centered(["Invalid choice!"])
                time.sleep(1)
                continue
            book = results[int(choice) - 1][1]

            with open("loans.json", "r") as f:
                loans = json.load(f)

            user_loans = [
                loan for loan in loans
                if loan['book_id'] == book['id']
                and loan['username'] == session.username
            ]

            illegal = True
            for loan in user_loans:
                if loan['status'] == "pending":
                    illegal = False
                    print_centered(
                        ["You already have a pending request for this book. Please wait for it to be approved"])
                    time.sleep(2)
                    break

                elif loan['status'] == "approved":
                    illegal = False
                    print_centered([
                        "You have already borrowed this book.",
                        "You must return it before requesting again."
                    ])
                    time.sleep(2)
                    break
            if not illegal:
                continue

            if book['available_count'] <= 0:
                print_centered(
                    [f"Sorry, '{book['title']}' is not available for borrowing."])
                time.sleep(2)
                continue

            confirm = print_centered(
                [f"Do you want to borrow '{book['title']}'?"],
                "Enter Y to confirm, N to cancel: ",
                "[0] Back").strip().lower()

            if confirm == "y":
                new_loan = {
                    "loan_id": str(uuid.uuid4()),
                    "username": session.username,
                    "book_id": book['id'],
                    "status": "pending",
                    "request_date": datetime.now().isoformat(),
                    "approve_date": None,
                    "due_date": None,
                    "return_date": None
                }

                loans.append(new_loan)
                with open("loans.json", "w") as f:
                    json.dump(loans, f, indent=4)

                print_centered(
                    ["Your request has been submitted and is waiting for approval."])
                time.sleep(2)
            else:
                continue
    return "MEMBER"


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

    print_centered(display_lines, ">>> ", "[0] Back")

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
                    return "MUSER"
                continue
            continue
        continue


def de_user():
    return "MUSERS"


def add_book():
    with open("books.json", "r") as f:
        books = json.load(f)

    while True:
        title = print_centered("", "title : ", "[0] Back")
        if title == "0":
            return "BOOKS"
        if not title:
            print_centered(["Enter a valid title"])
            time.sleep(1)
            continue

        while True:
            author = print_centered(
                ["title : " + f"{title}"], "author : ", "[0] Back")
            if author == "0":
                break
            if not author:
                print_centered(["Enter a valid author"])
                time.sleep(1)
                continue

            while True:
                category = print_centered(
                    ["title : " + f"{title}",
                     "author : " + f"{author}"],
                    "category : ",
                    "[0] Back"
                )
                if category == "0":
                    break
                if not category:
                    print_centered(["Enter a valid category"])
                    time.sleep(1)
                    continue

                while True:
                    total_count = print_centered(
                        ["title : " + f"{title}",
                         "author : " + f"{author}",
                         "category : " + f"{category}"],
                        "total count : ",
                        "[0] Back"
                    )
                    if total_count == "0":
                        break
                    if not total_count.isdigit() or int(total_count) <= 0:
                        print_centered(["Enter a valid number (> 0)"])
                        time.sleep(1)
                        continue

                    total_count = int(total_count)

                    new_book = {
                        "title": title,
                        "author": author,
                        "category": category,
                        "total_count": total_count,
                        "available_count": total_count
                    }

                    existing = next(
                        (b for b in books
                         if b["title"] == title
                            and b["author"] == author
                            and b["category"] == category),
                        None
                    )

                    if existing:
                        existing["total_count"] += total_count
                        existing["available_count"] += total_count
                        message = f"Book exists. {total_count} copies added. Total: {existing['total_count']}"
                        s = 3
                    else:
                        new_book = {"id": str(uuid.uuid4()), **new_book}
                        books.append(new_book)
                        message = "Book added successfully!"
                        s = 1.5

                    with open("books.json", "w") as f:
                        json.dump(books, f, indent=4)

                    print_centered([message])
                    time.sleep(s)
                    return "BOOKS"
                continue
            continue
        continue


def edit_book():
    with open("books.json", "r") as f:
        books = json.load(f)

    while True:
        title = print_centered(
            "", "Enter the title of the book to edit: ", "[0] Back")
        if title == "0":
            return "BOOKS"

        matching_books = [b for b in books if b["title"] == title]
        if not matching_books:
            print_centered(["Book not found!"])
            time.sleep(1)
            continue

        while True:
            if len(matching_books) > 1:
                display_lines = ["=== Matching Books ===", ""]
                header = f"{'No.':<4} | {'Title':<20} | {'Author':<20} | {'Category':<15} | {'Total':<5} | {'Available':<5}"
                display_lines.append(header)
                display_lines.append("-" * len(header))
                for i, b in enumerate(matching_books, 1):
                    line = f"{i:<4} | {b['title']:<20} | {b['author']:<20} | {b['category']:<15} | {b['total_count']:<5} | {b['available_count']:<5}"
                    display_lines.append(line)
                display_lines.append("")
                display_lines.append("")
                choice = print_centered(
                    display_lines, "Enter the number of the book to edit: ", "[0] Back")
                if choice == "0":
                    break
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matching_books):
                    print_centered(["Invalid choice!"])
                    time.sleep(1)
                    continue
                book = matching_books[int(choice) - 1]
                break
            else:
                book = matching_books[0]
                break

        while True:
            new_author = print_centered(
                [f"Current author: {book['author']}"], "Enter new author: ", "[0] Back")
            if new_author == "0":
                break
            if new_author.strip() == "":
                print_centered(["Enter a valid author"])
                time.sleep(1)
                continue
            book["author"] = new_author.strip()

            while True:
                new_category = print_centered(
                    [f"Current category: {book['category']}"], "Enter new category: ", "[0] Back")
                if new_category == "0":
                    break
                if new_category.strip() == "":
                    print_centered(["Enter a valid category"])
                    time.sleep(1)
                    continue
                book["category"] = new_category.strip()

                while True:
                    new_total = print_centered(
                        [f"Current total count: {book['total_count']}"], "Enter new total count: ", "[0] Back")
                    if new_total == "0":
                        break
                    if not new_total.isdigit() or int(new_total) <= 0:
                        print_centered(["Enter a valid number greater than 0"])
                        time.sleep(1)
                        continue
                    diff = int(new_total) - book["total_count"]
                    book["total_count"] = int(new_total)
                    book["available_count"] += diff

                    with open("books.json", "w") as f:
                        json.dump(books, f, indent=4)

                    print_centered(["Book updated successfully!"])
                    time.sleep(1)
                    return "BOOKS"


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
            time.sleep(1)


def manage_books_menu():
    Lines = ["=== Books Management ===", "1. Add New Book", "2. Edit Book",
             "3. Delete Book", "4. Show books"]
    choice = print_centered(Lines, ">>", "[0] Back")
    if choice == "0":
        return session.role
    elif choice == "1":
        return "ADDBOOK"
    elif choice == "2":
        return "EDITBOOK"
    elif choice == "3":
        return "DELBOOK"
    elif choice == "4":
        return "SHOWBOOKS"
    else:
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
    with open("loans.json", "r") as f:
        loans = json.load(f)
    with open("books.json", "r") as f:
        books = json.load(f)
    books_dict = {b['id']: b for b in books}
    pending_loans = [loan for loan in loans if loan['status']
                     in ("pending", "renew_pending")]

    while True:
        display_lines = ["=== Pending Requests ===", ""]
        header = f"{'No':<4} | {'Book Title':<30} | {'User':<15} | {'Type':<12} | {'Request Date':<20}"
        display_lines.append(header)
        display_lines.append("-" * len(header))

        for i, loan in enumerate(pending_loans, 1):
            book = books_dict.get(loan['book_id'], {"title": "Unknown"})
            request_type = "Borrow" if loan['status'] == "pending" else "Renew"
            request_date = datetime.fromisoformat(
                loan['request_date']).strftime("%Y-%m-%d")
            line = f"{i:<4} | {book['title']:<30} | {loan['username']:<15} | {request_type:<12} | {request_date:<20}"
            display_lines.append(line)

        display_lines.append("")
        display_lines.append("")

        while True:
            choice = print_centered(
                display_lines, "Select a request to approve/reject: ", "[0] Back")
            if choice == "0":
                return session.role
            elif not choice.isdigit() or int(choice) < 1 or int(choice) > len(pending_loans):
                print_centered(["Invalid choice!"])
                time.sleep(1)
                continue
            selected_loan = pending_loans[int(choice) - 1]
            break

        while True:
            action = print_centered(
                [f"Request for '{books_dict[selected_loan['book_id']]['title']}' by {selected_loan['username']}", "",
                 "1. Approve",
                 "2. Reject", ""],
                ">>> ", "[0] Back"
            ).strip()

            if action == "0":
                break
            elif action == "1":
                if selected_loan['status'] == "pending":
                    selected_loan['status'] = "approved"
                    selected_loan['approve_date'] = datetime.now().isoformat()
                    selected_loan['due_date'] = (
                        datetime.now() + timedelta(days=14)).isoformat()
                    books_dict[selected_loan['book_id']
                               ]['available_count'] -= 1
                elif selected_loan['status'] == "renew_pending":
                    selected_loan['status'] = "approved"
                    selected_loan['approve_date'] = datetime.now().isoformat()
                print_centered(["Request approved."])
                time.sleep(2)
            elif action == "2":
                selected_loan['status'] = "approved"
                print_centered(["Request rejected."])
                time.sleep(1)
            with open("loans.json", "w") as f:
                json.dump(loans, f, indent=4)
            with open("books.json", "w") as f:
                json.dump(list(books_dict.values()), f, indent=4)
            return "REQUESTS"


def main():
    clear_screen()
    Lines = ["=== Library Management System ===",
             "", "", "1. Login", "0. Exit", ""]
    choice = print_centered(Lines, "")
    # print("1. Login")
    # print("0. Exit")
    if choice == "3":
        return "MEMBER"
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
            ["=== Login ===", "", "", " Please enter the username : " + f"{username}"], "Please enter the password : ")
        clear_screen()
        for user in users:
            if user["username"] == username:
                userfound = True
                if user["password"] == hashlib.sha256(password.encode()).hexdigest():
                    session.username = username
                    session.role = user["role"].upper()
                    session.logged_in = True
                    print_centered(["Login successful!"])
                    time.sleep(1)

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
        "=== Admin panel ===", "",
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
        "2. Add / Edit / Delete books", "", ""
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
        "2. View borrowed books"
    ]
    choice = print_centered(Lines, ">>> ", "[0] Back")

    if choice == "0":
        return "MAIN"
    elif choice == "1":
        return "BOOKSEARCH"
    elif choice == "2":
        return "SHOWB"
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
