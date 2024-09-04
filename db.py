from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, text, Result
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

CONNECTION_STRING = 'postgresql+psycopg2://omer:1234@db:5432/mydb'
#CONNECTION_STRING = 'postgresql+psycopg2://omer:1234@localhost:5432/mydb'


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

def innit():
    Base.metadata.create_all(bind=engine)

def add_user(id: int, name: str) -> None:
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
