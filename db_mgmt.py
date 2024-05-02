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
        name TEXT NOT NULL,
        date TEXT,
        price TEXT
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


def get_path_by_name(name) -> list:
    # Connect to SQLite database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # Retrieve path from the database based on the name
    cursor.execute('SELECT id, path FROM file_paths WHERE name = ?', (name,))
    row = cursor.fetchone()

    # Close database connection
    conn.close()

    # Return the path if found, otherwise return None
    return row if row else None


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


def get_table_data() -> list:
    # Connect to the SQLite database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # Query all rows from your table
    cursor.execute('SELECT * FROM file_paths')
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass the rows to the template and render it
    return rows


def add_date_and_price(date, price, id) -> None:
    # Connect to the SQLite database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    # Query all rows from your table
    cursor.execute('UPDATE file_paths SET date = ?, price = ? WHERE id = ?', (date, price, id))
    conn.commit()

    # Close the database connection
    conn.close()