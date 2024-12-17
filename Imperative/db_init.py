import sqlite3

class DatabaseInit:
    @staticmethod
    def initialize():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL,
                book_author TEXT NOT NULL,
                book_gener TEXT NOT NULL,
                book_loc TEXT NOT NULL,
                book_status BOOLEAN NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_name TEXT NOT NULL,
                member_number TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BorrowRecords (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (member_id) REFERENCES Members(member_id),
                FOREIGN KEY (book_id) REFERENCES Books(book_id)
            )
        ''')

        conn.commit()
        conn.close()
