import sqlite3

def initialize_database():
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




def create_connection():
    """Create a database connection to SQLite."""
    conn = sqlite3.connect('library.db') 
    return conn

def save_book(book_obj):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO Books (book_title, book_author, book_gener, book_loc, book_status)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (book_obj['book_title'], book_obj['book_author'], book_obj['book_gener'], book_obj['book_loc'], book_obj['book_status']))
    conn.commit()
    conn.close()

def db_update_book(book_id, book_obj):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        UPDATE Books
        SET book_title=?, book_author=?, book_gener=?, book_loc=?, book_status=?
        WHERE book_id=?
    '''
    cursor.execute(query, (book_obj['book_title'], book_obj['book_author'], book_obj['book_gener'], book_obj['book_loc'], book_obj['book_status'], book_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def db_remove_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Books WHERE book_id=?"
    cursor.execute(query, (book_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def check_book_id(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM Books WHERE book_id=?)"
    cursor.execute(query, (book_id,))
    exists = cursor.fetchone()[0] == 1
    conn.close()
    return exists

def save_member(mem_obj):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO Members (member_name, member_number)
        VALUES (?, ?)
    '''
    cursor.execute(query, (mem_obj['member_name'], mem_obj['member_number']))
    conn.commit()
    conn.close()

def db_update_member(mem_id, mem_obj):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        UPDATE Members
        SET member_name=?, member_number=?
        WHERE member_id=?
    '''
    cursor.execute(query, (mem_obj['member_name'], mem_obj['member_number'], mem_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def db_view_members():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Members"
    cursor.execute(query)
    members = cursor.fetchall()
    conn.close()
    for member in members:
        print(f"ID: {member[0]}, Name: {member[1]}, Number: {member[2]}")


def db_borrow_book(member_id, book_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO BorrowRecords (member_id, book_id, borrow_date)
        VALUES (?, ?, DATETIME('now'))
    '''
    cursor.execute(query, (member_id, book_id))
    conn.commit()
    conn.close()

def db_return_book(member_id, book_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
        UPDATE BorrowRecords
        SET return_date=DATETIME('now')
        WHERE member_id=? AND book_id=? AND return_date IS NULL
    '''
    cursor.execute(query, (member_id, book_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def check_mem_id(mem_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM Members WHERE member_id=?)"
    cursor.execute(query, (mem_id,))
    exists = cursor.fetchone()[0] == 1
    conn.close()
    return exists


def get_all_avaliable_books():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Books WHERE book_status=1"
    cursor.execute(query)
    books = cursor.fetchall()
    conn.close()
    return books


def db_history_of_borrowings(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM BorrowRecords WHERE member_id=?"
    cursor.execute(query, (member_id,))
    records = cursor.fetchall()
    conn.close()
    return records


def display_records():
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT BR.record_id, B.book_title, M.member_name, BR.borrow_date, BR.return_date
    FROM BorrowRecords BR
    INNER JOIN Books B ON BR.book_id = B.book_id
    INNER JOIN Members M ON BR.member_id = M.member_id
    """
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        print(f"RecordID: {record[0]}, Book: {record[1]}, Member: {record[2]}, Borrowed: {record[3]}, Returned: {record[4]}")
    conn.close()


def check(type, value):
    conn = create_connection()
    cursor = conn.cursor()
    
    if type == 1:  
        query = "SELECT EXISTS(SELECT 1 FROM Books WHERE book_title=?)"
    elif type == 2:  
        query = "SELECT EXISTS(SELECT 1 FROM Books WHERE book_author=?)"
    elif type == 3:  
        query = "SELECT EXISTS(SELECT 1 FROM Books WHERE book_gener=?)"
    else:
        conn.close()
        return False

    cursor.execute(query, (value,))
    exists = cursor.fetchone()[0] == 1
    conn.close()
    return exists

def search(search_type, search_value):
    conn = create_connection()
    cursor = conn.cursor()
    
    if search_type == 1: 
        query = "SELECT * FROM Books WHERE book_title LIKE ?"
    elif search_type == 2:  
        query = "SELECT * FROM Books WHERE book_author LIKE ?"
    elif search_type == 3:  
        query = "SELECT * FROM Books WHERE book_gener LIKE ?"
    else:
        print("Invalid search type.")
        return
    
    cursor.execute(query, ('%' + search_value + '%',))  
    results = cursor.fetchall()
    
    if results:
        for result in results:
            print(f"Book ID: {result[0]}, Title: {result[1]}, Author: {result[2]}, Genre: {result[3]}, Location: {result[4]}, Status: {result[5]}")
    else:
        print("No results found.")
    
    conn.close()

