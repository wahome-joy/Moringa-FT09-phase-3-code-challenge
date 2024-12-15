import sqlite3
from .author import Author
from .magazine import Magazine

class Article:
    def __init__(self, title, content, author, magazine):
        # Validate the title length
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Article title must be between 5 and 50 characters.")
        
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Article content must be a non-empty string.")

        self._title = title
        self._content = content
        self._author = author  # This is an Author instance
        self._magazine = magazine  # This is a Magazine instance
        self._id = None
        self._create_article()

    def _create_article(self):
        # Insert the article into the database and get the article id
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO articles (title, content, author_id, magazine_id) 
        VALUES (?, ?, ?, ?)
        ''', (self._title, self._content, self._author.id, self._magazine.id))

        self._id = cursor.lastrowid  # Retrieve the id of the newly inserted article
        conn.commit()
        conn.close()

    @property
    def id(self):
        # Return the article's id
        return self._id

    @property
    def title(self):
        # Return the article's title
        return self._title

    @title.setter
    def title(self, value):
        # Title cannot be changed once set, as per the instructions
        raise ValueError("Article title cannot be changed once it is set.")

    @property
    def content(self):
        # Return the article's content
        return self._content

    @property
    def author(self):
        # Fetch and return the author of the article using author_id
        return self._author  # Returning the Author instance

    @property
    def magazine(self):
        # Fetch and return the magazine of the article using magazine_id
        return self._magazine  # Returning the Magazine instance

    def __repr__(self):
        return f'<Article {self.title}>'
