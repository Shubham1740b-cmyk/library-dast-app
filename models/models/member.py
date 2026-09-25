"""MODEL: Member — a student who is allowed to borrow books."""
from datetime import date

from models.database import get_connection


class Member:

    def __init__(self, row):
        keys = row.keys()
        self.id = row["id"]
        self.name = row["name"]
        self.email = row["email"]
        self.roll_no = row["roll_no"]
        self.joined_on = row["joined_on"]
        # only present when the query asked for it
        self.books_held = row["books_held"] if "books_held" in keys else 0

    @staticmethod
    def validate(name, email, roll_no):
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if "@" not in email:
            errors.append("A valid email address is required.")
        if not roll_no.strip():
            errors.append("Roll number is required.")
        return errors

    @staticmethod
    def all():
        conn = get_connection()
        rows = conn.execute(
            "SELECT m.*,"
            "       (SELECT COUNT(*) FROM loans l"
            "         WHERE l.member_id = m.id AND l.returned_on IS NULL) AS books_held"
            "  FROM members m ORDER BY m.name"
        ).fetchall()
        conn.close()
        return [Member(r) for r in rows]

    @staticmethod
    def find(member_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
        conn.close()
        return Member(row) if row else None

    @staticmethod
    def create(name, email, roll_no):
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO members (name, email, roll_no, joined_on) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip(), roll_no.strip(), date.today().isoformat()),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def count():
        conn = get_connection()
        row = conn.execute("SELECT COUNT(*) AS c FROM members").fetchone()
        conn.close()
        return row["c"]
