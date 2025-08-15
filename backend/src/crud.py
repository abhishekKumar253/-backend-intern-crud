from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src import models, schemas, auth

# users crud operations

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    
    new_user = models.User( 
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password 
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        if "users.username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )
        elif "users.email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )

# posts crud operations

# get all posts
def get_posts(db: Session):
    return db.query(models.Post).all()

# get single post by ID
def get_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


# create a new post
def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(
        title=post.title, 
        content=post.content, 
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# update a post
def update_post(db: Session, post_id: int, post_update: schemas.PostCreate):
    db_post = get_post(db, post_id)
    db_post.title = post_update.title
    db_post.content = post_update.content
    db.commit()
    db.refresh(db_post)
    return db_post

# Delete a post
def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}


# likes crud operations

def like_or_unlike_post(db: Session, post_id: int, user_id: int):
    post = get_post(db, post_id)
    user = get_user(db, user_id)

    if user in post.liked_by:
        post.liked_by.remove(user)
        db.commit()
        return {"post_id": post_id, "liked": False, "message": "Post unliked successfully"}
    else:
        post.liked_by.append(user)
        db.commit()
        return {"post_id": post_id, "liked": True, "message": "Post liked successfully"}
    

# comments crud operations

def get_comments_by_post(db: Session, post_id: int):
    post = get_post(db, post_id)  # ensure post exists
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

def get_comment_by_id(db: Session, comment_id: int): 
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comment

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int, user_id: int):
    get_post(db, post_id) 
    db_comment = models.Comment(
        content=comment.content,
        user_id=user_id,
        post_id=post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment 


def update_comment(db: Session, comment_id: int, updated_comment: schemas.CommentCreate):
    db_comment = get_comment_by_id(db, comment_id) 
    db_comment.content = updated_comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment_by_id(db, comment_id)
    db.delete(db_comment)
    db.commit()
    return {"comment_id": comment_id, "message": "Comment deleted successfully"}