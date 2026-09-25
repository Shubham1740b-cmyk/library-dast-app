"""
Database helper.

This is the ONLY file in the project that knows SQLite exists.
If the college switches to MySQL next semester, this is the file you edit.
"""
import sqlite3

import config


def get_connection():
    """Open a connection whose rows behave like dictionaries."""
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row       # lets us write row["title"]
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema():
    """Create the three tables if they do not exist yet."""
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS books (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT    NOT NULL,
            author           TEXT    NOT NULL,
            isbn             TEXT    NOT NULL UNIQUE,
            total_copies     INTEGER NOT NULL DEFAULT 1,
            available_copies INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS members (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            email     TEXT NOT NULL UNIQUE,
            roll_no   TEXT NOT NULL,
            joined_on TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS loans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id     INTEGER NOT NULL REFERENCES books(id),
            member_id   INTEGER NOT NULL REFERENCES members(id),
            issued_on   TEXT NOT NULL,
            due_on      TEXT NOT NULL,
            returned_on TEXT
        );
        """
    )
    conn.commit()
    conn.close()
