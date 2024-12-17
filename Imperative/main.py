import os
import time
from management import *
from db import *
def clear_screen():
    os.system("cls" if(os.name=="nt") else "clear")

def book_mang():
    options = [1, 2, 3, 4]
    print('-------------------------------------------')
    print('|              Book Management            |')
    print('-------------------------------------------')
    print('|          1. Add Book                    |')
    print('|          2. Remove Book                 |')
    print('|          3. Update Book                 |')
    print('|          4. Search                      |')
    print('-------------------------------------------')
    choice = int(input('Enter your option: '))
    book_mang = Management()
    if choice in options:
        match choice:
            case 1: book_mang.add_books()
            case 2: book_mang.remove_book()
            case 3: book_mang.update_books()
            case 4: search()
    else:
        print("Invalid option")
    return 0

def member_mang():
    options = [1, 2, 3]
    print('-------------------------------------------')
    print('|            Member Management            |')
    print('-------------------------------------------')
    print('|           1. Add Member                 |')
    print('|           2. Update Member              |')
    print('|           3. View Members               |')
    print('-------------------------------------------')
    choice = int(input('Enter your option: '))
    mem_mang = Management()
    if choice in options:
        match choice:
            case 1: mem_mang.register_member()
            case 2: mem_mang.update_member_det()
            case 3: mem_mang.view_members()
    else:
        print("Invalid option")
    return 0

def borrow_return():
    options = [1, 2, 3, 4, 5]
    print('-------------------------------------------')
    print('|         Borrow / Return Book            |')
    print('-------------------------------------------')
    print('|           1. Borrow Book                |')
    print('|           2. Return Book                |')
    print('|           3. View Available Books       |')
    print('|           4. View Borrow History       |')
    print('|           5. Exit                      |')
    print('-------------------------------------------')
    choice = int(input('Enter your option: '))
    borrow_mang = Management()
    if choice in options:
        match choice:
            case 1: borrow_mang.borrow_book()
            case 2: borrow_mang.return_book()
            case 3: borrow_mang.get_available_books()
            case 4: borrow_mang.history_of_borrowings()
            case 5: return 0
    else:
        print("Invalid option")
    return 0

def main():
    db = Database()
    db.initialize()
    while True:
        clear_screen()
        print("Library Management System")
        print("---------------------------")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow/Return Book")
        print("4. Exit")
        option = int(input("Choose an option: "))
        
        if option == 1:
            book_mang()
        elif option == 2:
            member_mang()
        elif option == 3:
            borrow_return()
        elif option == 4:
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()