from .connection import get_db_connection

def create_tables():
    # Establish a database connection using the helper function
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign key constraints (important for SQLite)
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create authors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create magazines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # Create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

