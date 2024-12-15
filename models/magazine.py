import sqlite3
from .article import Article
from .author import Author

class Magazine:
    def __init__(self, name, category):
        # Initialize with a name and category and insert the magazine into the database
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Magazine name must be between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Magazine category must be a non-empty string.")

        self._name = name
        self._category = category
        self._id = None
        self._create_magazine()

    def _create_magazine(self):
        # Insert the magazine into the database and retrieve the generated id
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO magazines (name, category) 
        VALUES (?, ?)
        ''', (self._name, self._category))

        self._id = cursor.lastrowid  # Get the id of the newly inserted magazine
        conn.commit()
        conn.close()

    @property
    def id(self):
        # Return the magazine's id
        return self._id

    @property
    def name(self):
        # Return the magazine's name
        return self._name

    @name.setter
    def name(self, value):
        # Set the magazine's name (allowed to change)
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
            self._update_magazine()
        else:
            raise ValueError("Magazine name must be between 2 and 16 characters.")

    @property
    def category(self):
        # Return the magazine's category
        return self._category

    @category.setter
    def category(self, value):
        # Set the magazine's category (allowed to change)
        if isinstance(value, str) and len(value) > 0:
            self._category = value
            self._update_magazine()
        else:
            raise ValueError("Magazine category must be a non-empty string.")

    def _update_magazine(self):
        # Update the magazine's details in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE magazines
        SET name = ?, category = ?
        WHERE id = ?
        ''', (self._name, self._category, self._id))

        conn.commit()
        conn.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        # Fetch all articles associated with this magazine from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT a.title
        FROM articles a
        WHERE a.magazine_id = ?
        ''', (self._id,))

        articles = cursor.fetchall()
        conn.close()

        return [article[0] for article in articles]  # Return a list of article titles

    def contributors(self):
        # Fetch all authors associated with this magazine from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT DISTINCT a.name
        FROM authors a
        JOIN articles ar ON ar.author_id = a.id
        WHERE ar.magazine_id = ?
        ''', (self._id,))

        authors = cursor.fetchall()
        conn.close()

        return [author[0] for author in authors]  # Return a list of author names

    def article_titles(self):
        # Fetch all article titles for this magazine
        return self.articles()  # Reuse the articles method to return titles

    def contributing_authors(self):
        # Return authors who have written more than 2 articles for this magazine
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT a.name
        FROM authors a
        JOIN articles ar ON ar.author_id = a.id
        WHERE ar.magazine_id = ?
        GROUP BY a.id
        HAVING COUNT(ar.id) > 2
        ''', (self._id,))

        authors = cursor.fetchall()
        conn.close()

        return [author[0] for author in authors] if authors else None  # Return authors or None

