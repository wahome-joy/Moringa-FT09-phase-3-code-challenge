from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Create an Author and a Magazine instance
    author = Author(name=author_name)
    magazine = Magazine(name=magazine_name, category=magazine_category)

    # Create an Article instance
    article = Article(title=article_title, content=article_content, author=author, magazine=magazine)

    # Connect to the database to retrieve data for display (optional)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query the database for inserted records and fetch all authors, magazines, and articles
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine_row in magazines:
        # Create Magazine objects and print their details
        magazine_obj = Magazine(magazine_row[0], magazine_row[1], magazine_row[2])
        print(f"ID: {magazine_obj.id}, Name: {magazine_obj.name}, Category: {magazine_obj.category}")

    print("\nAuthors:")
    for author_row in authors:
        # Create Author objects and print their details
        author_obj = Author(author_row[0], author_row[1])
        print(f"ID: {author_obj.id}, Name: {author_obj.name}")

    print("\nArticles:")
    for article_row in articles:
        # Create Article objects and print their details
        article_obj = Article(article_row[1], article_row[2], Author(author_row[0], author_row[1]), Magazine(magazine_row[0], magazine_row[1], magazine_row[2]))
        print(f"ID: {article_obj.id}, Title: {article_obj.title}, Content: {article_obj.content}, Author: {article_obj.author.name}, Magazine: {article_obj.magazine.name}")

if __name__ == "__main__":
    main()

