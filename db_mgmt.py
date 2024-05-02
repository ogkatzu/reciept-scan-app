import sqlite3


def connect_to_db() -> None:
    """
    Connects to the database and creates a scores table if it does not exist.
    """
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_file_path(file_path: str, name: str) -> None:
    """
    Adds a file path to the database.
    """
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO file_paths (name, path) VALUES (?, ?)', (name, file_path,))
    conn.commit()

    conn.close()


def get_file_paths() -> list:
    """
    Returns a list of file paths from the database.
    """
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM file_paths')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_path_by_name(name) -> str:
    # Connect to SQLite database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # Retrieve path from the database based on the name
    cursor.execute('SELECT path FROM file_paths WHERE name = ?', (name,))
    row = cursor.fetchone()

    # Close database connection
    conn.close()

    # Return the path if found, otherwise return None
    return row[0] if row else None

def check_if_name_exists(name) -> bool:
    # Connect to SQLite database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # Check if name exists in the database
    cursor.execute('SELECT * FROM file_paths WHERE name = ?', (name,))
    row = cursor.fetchone()

    # Close database connection
    conn.close()

    # Return True if name exists, otherwise return False
    return row is not None