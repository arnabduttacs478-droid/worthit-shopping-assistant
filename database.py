
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "worthit.db"


@contextmanager
def get_connection():
    """Open a database connection and always close it."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    """Create the shortlist table if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shortlist (
                category TEXT NOT NULL,
                product_name TEXT NOT NULL,
                PRIMARY KEY (category, product_name)
            )
            """
        )


def get_shortlist(category):
    """Return saved product names for one category."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT product_name
            FROM shortlist
            WHERE category = ?
            ORDER BY product_name
            """,
            (category,),
        ).fetchall()

    return [row[0] for row in rows]


def save_shortlist(category, product_names):
    """Replace the saved shortlist for one category."""
    unique_names = list(dict.fromkeys(product_names))

    with get_connection() as connection:
        connection.execute(
            "DELETE FROM shortlist WHERE category = ?",
            (category,),
        )

        connection.executemany(
            """
            INSERT INTO shortlist (category, product_name)
            VALUES (?, ?)
            """,
            [(category, name) for name in unique_names],
        )


def clear_shortlist(category):
    """Clear one category without affecting other categories."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM shortlist WHERE category = ?",
            (category,),
        )


initialize_database()
