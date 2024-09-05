from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import db  # Import your db.py module

app = FastAPI()

def test_insertions():
    a = db.get_user(1)
    db.add_user(1, 'omer')
    db.add_user(2, 'amit')
    db.add_user(3, 'yuval')
    db.add_user(4, 'galit')
    db.add_user(5, 'itai')
    db.add_article(1, 'one', '111 111 1111', 1)
    db.add_article(2, 'two', '22 2222 222 2', 2)
    db.add_article(3, 'three', '333 333 333', 3)
    db.add_article(4, 'four', '444 444 444 4', 4)
    db.add_article(5, 'five', '555 5555 555 555', 5)
    db.add_comment(1, 'o', 'hdhdhd', 1, 1)
    db.add_comment(2, 'o', 'hdhdhd', 1, 1)
    db.add_comment(3, 'y', 'dfbdfb', 1, 2)


class UserCreate(BaseModel):
    id: int
    name: str

class ArticleCreate(BaseModel):
    id: int
    title: str
    body: str
    author_id: int

class CommentCreate(BaseModel):
    id: int
    title: str
    body: str
    article_id: int
    user_id: int


def main():
    db.init()
    # test_insertions()
    # a = db.get_user(4)
    # res = find_string_in_article(" ")


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate):
    """
    Creates a new user in the system with HTTP request

    :param user: A `UserCreate` object containing the user details to be added.
    :type user: UserCreate

    :return: The created `UserCreate` object.
    :rtype: UserCreate

    :raises HTTPException: Raises a 400 error if there is an issue with creating the user,
                           such as invalid data or database errors.
    """
    try:
        db.add_user(user.id, user.name)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@app.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int):
    """
    Retrieves a user by their ID with HTTP request.

    :param user_id: The ID of the user to retrieve.
    :type user_id: int

    :return: The `UserCreate` object representing the user with the specified ID.
    :rtype: UserCreate

    :raises HTTPException: Raises a 404 error if the user with the specified ID is not found.

    """
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/articles/", response_model=ArticleCreate)
def create_article(article: ArticleCreate):
    """
    Creates a new article in the system with HTTP request.

    :param article: The article data to be created, provided as an `ArticleCreate` object.
    :type article: ArticleCreate

    :return: The created `ArticleCreate` object with the provided data.
    :rtype: ArticleCreate

    :raises HTTPException: Raises a 400 error if there is an issue creating the article.

    """
    try:
        db.add_article(article.id, article.title, article.body, article.author_id)
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating article: {str(e)}")

@app.get("/articles/{article_id}", response_model=ArticleCreate)
def read_article(article_id: int):
    """
    Retrieves an article by its ID with HTTP request.

    :param article_id: The ID of the article to be retrieved.
    :type article_id: int

    :return: The article with the specified ID, represented as an `ArticleCreate` object.
    :rtype: ArticleCreate

    :raises HTTPException: Raises a 404 error if the article with the specified ID is not found.
    """
    article = db.get_article(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.post("/comments/", response_model=CommentCreate)
def create_comment(comment: CommentCreate):
    """
    Creates a new comment in the system with HTTP request.

    :param comment: The comment data to be created, represented as a `CommentCreate` object.
    :type comment: CommentCreate

    :return: The created comment, represented as a `CommentCreate` object.
    :rtype: CommentCreate

    :raises HTTPException: Raises a 400 error if there is an error creating the comment.
    """
    try:
        db.add_comment(comment.id, comment.title, comment.body, comment.article_id, comment.user_id)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating comment: {str(e)}")

@app.get("/comments/{comment_id}", response_model=CommentCreate)
def read_comment(comment_id: int):
    """
    Retrieves a comment by its ID with HTTP request.

    :param comment_id: The ID of the comment to be retrieved.
    :type comment_id: int

    :return: The comment details, represented as a `CommentCreate` object, if found.
    :rtype: CommentCreate

    :raises HTTPException: Raises a 404 error if the comment with the given ID is not found.
    """
    comment = db.get_comment(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.get("/find_string/")
def find_string_in_article(search_string: str):
    """
    Finds articles containing a specific string in their body and returns their IDs along with the
    exact locations of the string in the body. HTTP request

    :param search_string: The string to search for within the articles' body.
    :type search_string: str

    :return: A list of dictionaries where each dictionary represents an article with the string found. Each dictionary
             contains the article ID and a list of offsets (positions) where the string appears in the article body.
    :rtype: List[Dict[str, Union[int, List[int]]]]

    :raises HTTPException: Raises a 404 error if no articles contain the string.
    """
    result = db.find_string(search_string)
    if result is None:
        raise HTTPException(status_code=404, detail="String not found in any article")
    return result


if __name__ == "__main__":
    main()