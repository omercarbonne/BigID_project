from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, text, Result
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.row import Row
from typing import List, Optional, Any

CONNECTION_STRING = 'postgresql+psycopg2://omer:1234@localhost:5432/mydb'

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
    # Create all tables in the database (this is typically done only once)
    Base.metadata.create_all(bind=engine)


def add_user(id: int, name: String) -> None:
    session = Session()
    try:
        new_user = User(id=id, name=name)
        session.add(new_user)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def add_article(id: int, title: str, body: Text, author_id: int) -> None:
    session = Session()
    try:
        new_article = Article(id=id, title=title, body=body, author_id=author_id)
        session.add(new_article)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def add_comment(id: int, title: str, body: Text, article_id: int, user_id: int) -> None:
    session = Session()
    try:
        new_comment = Comment(id=id, title=title, body=body, article_id=article_id, user_id=user_id)
        session.add(new_comment)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def get_user(id: int) -> Optional[User]:
    session = Session()
    try:
        user = session.query(User).filter(User.id == id).one_or_none()
        if user:
            return user
        else:
            print(f"No user found with ID: {id}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()


def get_article(id: int) -> Optional[Article]:
    session = Session()
    try:
        article = session.query(Article).filter(Article.id == id).one_or_none()
        if article:
            return article
        else:
            print(f"No article found with ID: {id}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()


def get_comment(id: int) -> Optional[Comment]:
    session = Session()
    try:
        comment = session.query(Comment).filter(Comment.id == id).one_or_none()
        if comment:
            return comment
        else:
            print(f"No comment found with ID: {id}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()


def find_string(search_string: str) -> Optional[Result[Any]]:
    session = Session()
    query = text("""
            SELECT articleID, POSITION(:search_string IN body) AS position
            FROM Articles
            WHERE body LIKE '%' || :search_string || '%'
        """)
    try:
        result = session.execute(query, {'search_string': search_string})
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()










