import time
from Books import Book
from member import Member
from db import Database

class Management:
    db = Database()

    def add_books(self):
        book_title = input("Enter book name: ")
        book_author = input("Enter book author: ")
        book_gener = input("Enter book genre: ")
        book_loc = input("Enter book location: ")
        book_obj = Book(book_title, book_author, book_gener, book_loc)
        self.db.save_book(book_obj)
        print("Book saved.")
        time.sleep(1)

    def update_books(self):
        book_id = input("Enter book id: ")
        if self.db.check_book_id(book_id):
            book_author = input("Enter updated book author: ")
            book_title = input("Enter updated book title: ")
            book_gener = input("Enter updated book genre: ")
            book_loc = input("Enter updated book location: ")
            book_obj = Book(book_title, book_author, book_gener, book_loc, True, book_id)
            self.db.update_book(book_obj)
            print("Book updated.")
        else:
            print("Wrong ID.")
        time.sleep(1)

    def remove_book(self):
        book_id = input("Enter book id to remove: ")
        if self.db.check_book_id(book_id):
            self.db.remove_book(book_id)
            print("Book deleted.")
        else:
            print("Error: Check book id.")
        time.sleep(1)

    def register_member(self):
        member_name = input("Enter member name: ")
        member_number = input("Enter member number: ")
        mem_obj = Member(member_name, member_number)
        self.db.save_member(mem_obj)
        print("Member added.")
        time.sleep(1)

    def view_members(self):
        self.db.view_members()

    def update_member_det(self):
        mem_id = input("Enter member id to update: ")
        if self.db.check_mem_id(mem_id):
            member_name = input("Enter updated member name: ")
            member_number = input("Enter updated member number: ")
            mem_obj = Member(mem_id, member_name, member_number)
            self.db.update_mem(mem_obj)
            print("Member details updated.")
        else:
            print("Wrong ID.")
        time.sleep(1)

    def borrow_book(self):
        member_id = input("Enter your id: ")
        if self.db.check_mem_id(member_id):
            book_id = input("Enter book id: ")
            if self.db.check_book_id(book_id):
                self.db.borrow_book(member_id, book_id)
                print("Done")
            else:
                print("Error: Wrong book ID.")
        else:
            print("Error: Wrong member ID.")
        time.sleep(1)

    def return_book(self):
        member_id = input("Enter your id: ")
        if self.db.check_mem_id(member_id):
            book_id = input("Enter book id: ")
            if self.db.check_book_id(book_id):
                self.db.return_book(member_id, book_id)
        else:
            print("Error: Wrong member ID.")
        time.sleep(1)

    def get_available_books(self):
        self.db.get_all_available_books()

    def history_of_borrowings(self):
        member_id = input("Enter your id: ")
        if self.db.check_mem_id(member_id):
            self.db.history_of_borrowings(member_id)
        else:
            print("Error: Check your id.")
        time.sleep(1)

    def view_records(self):
        self.db.display_records()

    def search_title(self):
        title = input("Enter book title: ")
        if not self.db.search_books(1, title):
            print("Unmatched title.")
        time.sleep(1)

    def search_author(self):
        author = input("Enter book author: ")
        if not self.db.search_books(2, author):
            print("Unmatched author.")
        time.sleep(1)

    def search_gener(self):
        gener = input("Enter book genre: ")
        if not self.db.search_books(3, gener):
            print("Unmatched genre.")
        time.sleep(1)
