"""Fill the database with sample data so the screens have something to show."""
import os
from datetime import date, timedelta

import config
from models.database import get_connection, init_schema

if os.path.exists(config.DATABASE):
    os.remove(config.DATABASE)
init_schema()

conn = get_connection()

books = [
    ("Introduction to Algorithms", "Cormen, Leiserson, Rivest", "9780262046305", 4),
    ("Clean Code", "Robert C. Martin", "9780132350884", 3),
    ("Design Patterns", "Gamma, Helm, Johnson, Vlissides", "9780201633610", 2),
    ("The Pragmatic Programmer", "Hunt & Thomas", "9780135957059", 3),
    ("Operating System Concepts", "Silberschatz & Galvin", "9781118063330", 2),
    ("Database System Concepts", "Silberschatz, Korth, Sudarshan", "9780078022159", 3),
    ("Computer Networks", "Andrew S. Tanenbaum", "9780132126953", 2),
]
for title, author, isbn, copies in books:
    conn.execute(
        "INSERT INTO books (title, author, isbn, total_copies, available_copies)"
        " VALUES (?,?,?,?,?)", (title, author, isbn, copies, copies))

members = [
    ("Aarav Sharma", "aarav.sharma@ccl.edu.in", "CS21-014", 320),
    ("Priya Nair", "priya.nair@ccl.edu.in", "CS21-027", 300),
    ("Rohan Verma", "rohan.verma@ccl.edu.in", "IT22-008", 210),
    ("Simran Kaur", "simran.kaur@ccl.edu.in", "CS22-041", 180),
    ("Devansh Gupta", "devansh.gupta@ccl.edu.in", "EC22-019", 95),
]
for name, email, roll, days_ago in members:
    joined = (date.today() - timedelta(days=days_ago)).isoformat()
    conn.execute(
        "INSERT INTO members (name, email, roll_no, joined_on) VALUES (?,?,?,?)",
        (name, email, roll, joined))
conn.commit()

# (book_id, member_id, issued days ago)  -- one of these is deliberately overdue
loans = [(1, 1, 20), (2, 1, 6), (3, 2, 3), (6, 3, 25), (4, 1, 2)]
for book_id, member_id, days_ago in loans:
    issued = date.today() - timedelta(days=days_ago)
    due = issued + timedelta(days=config.LOAN_PERIOD_DAYS)
    conn.execute(
        "INSERT INTO loans (book_id, member_id, issued_on, due_on) VALUES (?,?,?,?)",
        (book_id, member_id, issued.isoformat(), due.isoformat()))
    conn.execute(
        "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
        (book_id,))

conn.commit()
conn.close()
print("Sample data loaded: 7 books, 5 members, 5 loans (2 overdue).")
