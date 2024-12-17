import sqlite3
from Books import *
from datetime import datetime
import time
from db_init import *

class Database:
    def __init__(self):
        DatabaseInit.initialize() 
        self.conn = sqlite3.connect('library.db') 
        self.cursor = self.conn.cursor()

    def check_book_id(self, book_id):
        self.cursor.execute('SELECT 1 FROM Books WHERE bookID=?', (book_id,))
        res = self.cursor.fetchone()
        return res is not None

    def save_book(self, book_obj):
        book_data = (book_obj.book_title, book_obj.book_author, book_obj.book_gener, book_obj.book_loc, True)
        self.cursor.execute('''
            INSERT INTO Books (Title, Author, Genre, Location, Available)
            VALUES (?, ?, ?, ?, ?)
        ''', book_data)
        self.conn.commit()

    def update_book(self, book_obj):
        book_data = (book_obj.book_title, book_obj.book_author, book_obj.book_gener, book_obj.book_loc, True, book_obj.book_id)
        self.cursor.execute('''
            UPDATE Books 
            SET Title=?, Author=?, Genre=?, Location=?, Available=?
            WHERE bookID=?
        ''', book_data)
        self.conn.commit()
        return True

    def remove_book(self, book_id):
        self.cursor.execute('SELECT bookID, Title, Author, Genre, Location, Available FROM Books WHERE bookID = ?', (book_id,))
        book_row = self.cursor.fetchone()
        if book_row:
            self.cursor.execute('DELETE FROM Books WHERE bookID = ?', (book_id,))
            self.conn.commit()
        return True

    def view_members(self):
        try:
            self.cursor.execute('SELECT MemberID, Name, Phone FROM Members')
            rows = self.cursor.fetchall()
            for row in rows:
                print("ID:", row[0], "Name:", row[1], "Number:", row[2])
                print('-' * 43)
                time.sleep(1)
        except Exception as e:
            print("Error retrieving members:", e)

    def check_mem_id(self, id):
        self.cursor.execute('SELECT 1 FROM Members WHERE MemberID=?', (id,))
        res = self.cursor.fetchone()
        return res is not None

    def save_member(self, mem_obj):
        member_data = (mem_obj.member_name, mem_obj.member_number)
        self.cursor.execute('''
            INSERT INTO Members (Name, Phone)
            VALUES (?, ?)
        ''', member_data)
        self.conn.commit()

    def update_mem(self, mem_obj):
        member_data = (mem_obj.member_name, mem_obj.member_number, mem_obj.member_id)
        self.cursor.execute('''
            UPDATE Members
            SET Name=?, Phone=?
            WHERE MemberID=?
        ''', member_data)
        self.conn.commit()
        return True

    def borrow_book(self, mem_id, book_id):
        try:
            self.cursor.execute('SELECT Available FROM Books WHERE bookID = ?', (book_id,))
            result = self.cursor.fetchone()

            if not result[0]:
                print("Book is already borrowed.")
                return False

            self.cursor.execute('''
                UPDATE Books 
                SET Available = 0 
                WHERE bookID = ?
            ''', (book_id,))

            self.cursor.execute('''
                INSERT INTO Transactions (BookID, MemberID, BorrowDate)
                VALUES (?, ?, ?)
            ''', (book_id, mem_id, datetime.now()))
            self.conn.commit()
            print("Book borrowed successfully.")
            return True

        except Exception as e:
            print("Error borrowing the book:", e)
            self.conn.rollback()
            return False

    def return_book(self, mem_id, book_id):
        try:
            self.cursor.execute('SELECT Available FROM Books WHERE bookID = ?', (book_id,))
            result = self.cursor.fetchone()

            if result and result[0]:
                print("Book is already available.")
                return False

            self.cursor.execute('SELECT BorrowDate FROM Transactions WHERE BookID = ? AND MemberID = ? AND ReturnDate IS NULL', (book_id, mem_id))
            borrow_result = self.cursor.fetchone()

            if borrow_result is None:
                print("No active borrowing record found for this book and member.")
                return False

            borrow_date = borrow_result[0]
            current_date = datetime.now()
            late_days = (current_date - borrow_date).days
            fine_amount = 0

            if late_days > 10:
                fine_amount = (late_days - 10) * 5

            self.cursor.execute('''
                UPDATE Transactions
                SET ReturnDate = ?, FineAmount = ?
                WHERE BookID = ? AND MemberID = ? AND ReturnDate IS NULL
            ''', (datetime.now(), fine_amount, book_id, mem_id))

            self.cursor.execute('''
                UPDATE Books
                SET Available = 1
                WHERE bookID = ?
            ''', (book_id,))

            self.conn.commit()

            if fine_amount > 0:
                print(f"Book returned with a fine of {fine_amount} units.")
            else:
                print("Book returned successfully with no fine.")
            return True

        except Exception as e:
            print(f"Error returning the book: {e}")
            self.conn.rollback()
            return False

    def get_all_available_books(self):
        try:
            self.cursor.execute('''
                SELECT bookID, Title, Author, Genre, Location 
                FROM Books
                WHERE Available = 1
            ''')
            rows = self.cursor.fetchall()
            if not rows:
                print("No available books")
                return

            print("Available Books:\n")
            for row in rows:
                print(f"Book ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Genre: {row[3]}, Location: {row[4]}")

        except Exception as e:
            print(f"Error retrieving available books: {e}")
            return []

    def history_of_borrowings(self, mem_id):
        self.cursor.execute('''
            SELECT t.BookID, t.BorrowDate, t.ReturnDate, t.FineAmount
            FROM Transactions t
            JOIN Books b ON t.BookID = b.BookID
            WHERE t.MemberID = ?
            ORDER BY t.BorrowDate DESC
        ''', (mem_id,))

        rows = self.cursor.fetchall()

        if rows:
            print(f"Borrowing history for Member ID {mem_id}:")
            for row in rows:
                print(f"Book ID: {row[0]}, Borrowed on: {row[1]}, Returned on: {row[2]}, Fine Amount: {row[3]}")
        else:
            print(f"No borrowing history found for Member ID {mem_id}.")
