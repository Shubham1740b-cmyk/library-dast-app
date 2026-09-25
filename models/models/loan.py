"""
MODEL: Loan — one book issued to one member.

This is where the most interesting rules of the whole system live:
  * a book may not be issued when no copy is free
  * a member may not hold more than MAX_BOOKS_PER_MEMBER books
  * a late return is fined FINE_PER_DAY rupees per day

Put these in the controller and every new screen has to remember them.
Put them here and they are enforced once, for everybody.
"""
from datetime import date, datetime, timedelta

import config
from models.database import get_connection


class Loan:

    def __init__(self, row):
        self.id = row["id"]
        self.book_id = row["book_id"]
        self.member_id = row["member_id"]
        self.issued_on = row["issued_on"]
        self.due_on = row["due_on"]
        self.returned_on = row["returned_on"]
        # joined-in display fields
        keys = row.keys()
        self.book_title = row["book_title"] if "book_title" in keys else ""
        self.member_name = row["member_name"] if "member_name" in keys else ""
        self.roll_no = row["roll_no"] if "roll_no" in keys else ""

    # ---------- business rules ----------

    @property
    def is_returned(self):
        return self.returned_on is not None

    @property
    def days_overdue(self):
        """How many days late this loan is, counted up to today (or the return date)."""
        end = date.fromisoformat(self.returned_on) if self.is_returned else date.today()
        due = date.fromisoformat(self.due_on)
        return max(0, (end - due).days)

    @property
    def fine(self):
        """Rupees owed. Zero until the due date passes."""
        return self.days_overdue * config.FINE_PER_DAY

    @property
    def status(self):
        if self.is_returned:
            return "Returned"
        return "Overdue" if self.days_overdue > 0 else "On loan"

    # ---------- the two operations that change the world ----------

    @staticmethod
    def issue(book_id, member_id):
        """Try to issue a book. Returns (success, message).

        The controller does not decide any of this; it only reports the answer.
        """
        from models.book import Book          # imported here to avoid a cycle

        book = Book.find(book_id)
        if book is None:
            return False, "That book does not exist."
        if not book.is_available:
            return False, f"'{book.title}' has no free copy right now."

        conn = get_connection()
        held = conn.execute(
            "SELECT COUNT(*) AS c FROM loans"
            " WHERE member_id = ? AND returned_on IS NULL",
            (member_id,),
        ).fetchone()["c"]

        if held >= config.MAX_BOOKS_PER_MEMBER:
            conn.close()
            return False, (
                f"This member already holds {held} books "
                f"(limit is {config.MAX_BOOKS_PER_MEMBER})."
            )

        issued_on = date.today()
        due_on = issued_on + timedelta(days=config.LOAN_PERIOD_DAYS)
        conn.execute(
            "INSERT INTO loans (book_id, member_id, issued_on, due_on)"
            " VALUES (?, ?, ?, ?)",
            (book_id, member_id, issued_on.isoformat(), due_on.isoformat()),
        )
        conn.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
            (book_id,),
        )
        conn.commit()
        conn.close()
        return True, f"'{book.title}' issued. Due on {due_on.strftime('%d %b %Y')}."

    @staticmethod
    def return_book(loan_id):
        """Mark a loan returned and report the fine, if any."""
        loan = Loan.find(loan_id)
        if loan is None:
            return False, "That loan record does not exist."
        if loan.is_returned:
            return False, "That book has already been returned."

        fine = loan.fine                       # computed BEFORE we set returned_on
        conn = get_connection()
        conn.execute(
            "UPDATE loans SET returned_on = ? WHERE id = ?",
            (date.today().isoformat(), loan_id),
        )
        conn.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
            (loan.book_id,),
        )
        conn.commit()
        conn.close()

        if fine:
            return True, (
                f"Returned {loan.days_overdue} day(s) late. Fine due: Rs {fine}."
            )
        return True, "Returned on time. No fine."

    # ---------- data access ----------

    @staticmethod
    def _select(where="", params=()):
        conn = get_connection()
        rows = conn.execute(
            "SELECT l.*, b.title AS book_title, m.name AS member_name, m.roll_no"
            "  FROM loans l"
            "  JOIN books b   ON b.id = l.book_id"
            "  JOIN members m ON m.id = l.member_id "
            + where
            + " ORDER BY l.returned_on IS NOT NULL, l.due_on",
            params,
        ).fetchall()
        conn.close()
        return [Loan(r) for r in rows]

    @staticmethod
    def all():
        return Loan._select()

    @staticmethod
    def active():
        return Loan._select("WHERE l.returned_on IS NULL")

    @staticmethod
    def find(loan_id):
        rows = Loan._select("WHERE l.id = ?", (loan_id,))
        return rows[0] if rows else None

    @staticmethod
    def stats():
        active = Loan.active()
        overdue = [l for l in active if l.days_overdue > 0]
        return {
            "on_loan": len(active),
            "overdue": len(overdue),
            "fines_due": sum(l.fine for l in overdue),
        }
