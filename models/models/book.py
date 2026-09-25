"""
MODEL: Book

Owns book data AND the rules that belong to book data.
Notice what is missing: no Flask import, no HTML, no request object.
This class can be used from a script, a unit test, or a mobile API.
"""
from models.database import get_connection


class Book:

    def __init__(self, row):
        self.id = row["id"]
        self.title = row["title"]
        self.author = row["author"]
        self.isbn = row["isbn"]
        self.total_copies = row["total_copies"]
        self.available_copies = row["available_copies"]

    # ---------- business rules ----------

    @property
    def is_available(self):
        """A book can be issued only while a free copy exists."""
        return self.available_copies > 0

    @property
    def issued_count(self):
        return self.total_copies - self.available_copies

    # ---------- validation ----------

    @staticmethod
    def validate(title, author, isbn, copies):
        """Return a list of error messages; an empty list means the data is legal.

        These rules live here, NOT in the HTML form and NOT in the controller,
        so every route that creates a book gets exactly the same checks.
        """
        errors = []
        if not title.strip():
            errors.append("Title is required.")
        if not author.strip():
            errors.append("Author is required.")
        if not isbn.strip():
            errors.append("ISBN is required.")
        elif len(isbn.strip()) < 10:
            errors.append("ISBN must be at least 10 characters long.")
        if copies < 1:
            errors.append("A book must have at least 1 copy.")
        return errors

    # ---------- data access ----------

    @staticmethod
    def all(search=None):
        conn = get_connection()
        if search:
            like = f"%{search}%"
            rows = conn.execute(
                "SELECT * FROM books"
                " WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?"
                " ORDER BY title",
                (like, like, like),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
        conn.close()
        return [Book(r) for r in rows]

    @staticmethod
    def find(book_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        conn.close()
        return Book(row) if row else None

    @staticmethod
    def create(title, author, isbn, copies):
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO books (title, author, isbn, total_copies, available_copies)"
            " VALUES (?, ?, ?, ?, ?)",
            (title.strip(), author.strip(), isbn.strip(), copies, copies),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def delete(book_id):
        conn = get_connection()
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def stats():
        conn = get_connection()
        row = conn.execute(
            "SELECT COUNT(*) AS titles,"
            "       IFNULL(SUM(total_copies), 0) AS copies,"
            "       IFNULL(SUM(available_copies), 0) AS available"
            " FROM books"
        ).fetchone()
        conn.close()
        return {"titles": row["titles"], "copies": row["copies"],
                "available": row["available"]}
