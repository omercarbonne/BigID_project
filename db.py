from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, text, Result
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# docker connction
CONNECTION_STRING = 'postgresql+psycopg2://omer:1234@db:5432/mydb'

# local connection
# CONNECTION_STRING = 'postgresql+psycopg2://omer:1234@localhost:5432/mydb'


Base = declarative_base()
engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    articles = relationship("Article", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    body = Column(Text, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='comments')
    article = relationship('Article', back_populates='comments')

def init():
    Base.metadata.create_all(bind=engine)

def add_user(id: int, name: str) -> None:
    """
    Adds a new user to the database.

    :param id: The unique identifier for the user.
    :param name: The name of the user.

    :return: None

    :raises Exception: If an error occurs during the database operation, the session
                        is rolled back, and the exception is raised.
      """

    session = Session()
    try:
        new_user = User(id=id, name=name)
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()

def add_article(id: int, title: str, body: Text, author_id: int) -> None:
    """
    Adds a new article to the database.

    :param id: The unique identifier for the article.
    :param title: The title of the article.
    :param body: The content of the article.
    :param author_id: The unique identifier of the author who wrote the article.

    :return: None

    :raises Exception: If an error occurs during the database operation, the session
                        is rolled back, and the exception is raised.
    """
    session = Session()
    try:
        new_article = Article(id=id, title=title, body=body, author_id=author_id)
        session.add(new_article)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()

def add_comment(id: int, title: str, body: Text, article_id: int, user_id: int) -> None:
    """
    Adds a new comment to the database.

    :param id: The unique identifier for the comment.
    :param title: The title of the comment.
    :param body: The content of the comment.
    :param article_id: The unique identifier of the article to which the comment is associated.
    :param user_id: The unique identifier of the user who made the comment.

    :return: None

    :raises Exception: If an error occurs during the database operation, the session
                        is rolled back, and the exception is raised.
    """
    session = Session()
    try:
        new_comment = Comment(id=id, title=title, body=body, article_id=article_id, user_id=user_id)
        session.add(new_comment)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()

def get_user(id: int) -> Optional[User]:
    """
    Retrieves a user from the database by their unique identifier.

    :param id: The unique identifier of the user to retrieve.
    :return: The User object if found, otherwise None.
    :rtype: Optional[User]

    :raises Exception: If an error occurs during the database operation,
                        it is logged and None is returned.
    """
    session = Session()
    try:
        user = session.query(User).filter(User.id == id).one_or_none()
        return user
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def get_article(id: int) -> Optional[Article]:
    """
    Retrieves an article from the database by its unique identifier.

    :param id: The unique identifier of the article to retrieve.
    :return: The Article object if found, otherwise None.
    :rtype: Optional[Article]

    :raises Exception: If an error occurs during the database operation,
                        it is logged and None is returned.
    """
    session = Session()
    try:
        article = session.query(Article).filter(Article.id == id).one_or_none()
        return article
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def get_comment(id: int) -> Optional[Comment]:
    """
    Retrieves a comment from the database by its unique identifier.

    :param id: The unique identifier of the comment to retrieve.
    :return: The Comment object if found, otherwise None.
    :rtype: Optional[Comment]

    :raises Exception: If an error occurs during the database operation,
                        it is logged and None is returned.
    """
    session = Session()
    try:
        comment = session.query(Comment).filter(Comment.id == id).one_or_none()
        return comment
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def find_string(search_string: str) -> Optional[Result[Any]]:
    """
    Finds the occurrences of a given string within article bodies and returns the
    IDs of the articles along with the exact positions of the string within those articles.

    :param search_string: The string to search for within the articles.
    :return: A list of dictionaries where each dictionary contains an 'article_id'
             and a list of 'offsets' representing the positions of the string within the article.
             If no matches are found, returns None.
    :rtype: Optional[List[dict]]

    :raises Exception: Raises an exception if an error occurs during the database query.

    """
    session = Session()
    query = text("""
            WITH RECURSIVE find_positions AS (
                SELECT
                    id AS article_id,
                    POSITION(:search_string IN body) AS start_pos,
                    body,
                    POSITION(:search_string IN body) AS current_pos
                FROM articles
                WHERE body LIKE '%' || :search_string || '%'

                UNION ALL

                SELECT
                    article_id,
                    POSITION(:search_string IN SUBSTRING(body FROM current_pos + LENGTH(:search_string))) + current_pos AS start_pos,
                    body,
                    POSITION(:search_string IN SUBSTRING(body FROM current_pos + LENGTH(:search_string))) + current_pos AS current_pos
                FROM find_positions
                WHERE POSITION(:search_string IN SUBSTRING(body FROM current_pos + LENGTH(:search_string))) > 0
            )
            SELECT article_id, start_pos - 1 AS position_offset
            FROM find_positions
            WHERE start_pos > 0
            ORDER BY article_id, position_offset;
        """)
    try:
        result = session.execute(query, {'search_string': search_string}).fetchall()

        # Organize results in the right format
        article_matches = {}
        for row in result:
            article_id = row[0]
            offset = row[1]  # Fixed column name
            if article_id not in article_matches:
                article_matches[article_id] = []
            article_matches[article_id].append(offset)

        # Convert to the required output format
        temp = [{'article_id': article_id, 'offsets': offsets} for article_id, offsets in article_matches.items()]
        if temp: # if the dict is not empty - there are results
            return temp
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()
