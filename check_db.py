
import sqlite3
import os

database_path = "career_navigator.db"

print("Database path:", os.path.abspath(database_path))

if not os.path.exists(database_path):
    print("ERROR: Database file not found!")
    exit()

print("Database size:", os.path.getsize(database_path), "bytes")

try:
    connection = sqlite3.connect(database_path)

    # Check database integrity
    result = connection.execute(
        "PRAGMA integrity_check"
    ).fetchall()

    print("\nIntegrity Check:", result)

    # Check available tables
    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    print("Available Tables:", tables)

    connection.close()

except sqlite3.DatabaseError as error:
    print("\nDATABASE ERROR:", error)

except Exception as error:
    print("\nOTHER ERROR:", error)
