import sqlite3

class Author:
    def __init__(self, name):
        # Initialize with a name and insert the author into the database
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author's name must be a non-empty string.")
        
        self._name = name
        self._id = None
        self._create_author()

    def _create_author(self):
        # Insert the author into the database and retrieve the generated id
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO authors (name) 
        VALUES (?)
        ''', (self._name,))

        self._id = cursor.lastrowid  # Get the id of the newly inserted author
        conn.commit()
        conn.close()

    @property
    def id(self):
        # Return the author's id
        return self._id

    @property
    def name(self):
        # Return the author's name
        return self._name

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        # Fetch all articles by this author from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT a.title
        FROM articles a
        WHERE a.author_id = ?
        ''', (self._id,))

        articles = cursor.fetchall()
        conn.close()

        return [article[0] for article in articles]  # Return a list of article titles

    def magazines(self):
        # Fetch all magazines associated with this author from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT m.name
        FROM magazines m
        JOIN articles a ON a.magazine_id = m.id
        WHERE a.author_id = ?
        ''', (self._id,))

        magazines = cursor.fetchall()
        conn.close()

        return [magazine[0] for magazine in magazines]  # Return a list of magazine names

