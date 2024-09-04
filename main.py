from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import db  # Import your db.py module


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



app = FastAPI()


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
    #db.innit()
    # test_insertions()
    # a = db.get_user(4)
    res = find_string_in_article(" ")




@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate):
    try:
        db.add_user(user.id, user.name)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@app.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int):
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/articles/", response_model=ArticleCreate)
def create_article(article: ArticleCreate):
    try:
        db.add_article(article.id, article.title, article.body, article.author_id)
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating article: {str(e)}")

@app.get("/articles/{article_id}", response_model=ArticleCreate)
def read_article(article_id: int):
    article = db.get_article(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.post("/comments/", response_model=CommentCreate)
def create_comment(comment: CommentCreate):
    try:
        db.add_comment(comment.id, comment.title, comment.body, comment.article_id, comment.user_id)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating comment: {str(e)}")

@app.get("/comments/{comment_id}", response_model=CommentCreate)
def read_comment(comment_id: int):
    comment = db.get_comment(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.get("/find_string/")
def find_string_in_article(search_string: str):
    result = db.find_string(search_string)
    if result is None:
        raise HTTPException(status_code=404, detail="String not found in any article")
    return result


if __name__ == "__main__":
    main()