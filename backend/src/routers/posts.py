from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src import schemas, crud, auth
from src.database import get_db

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

# get all posts

@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

# get signle post by ID

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id)

# create a new post
@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("user_id")
    return crud.create_post(db, post, user_id)


# update a post
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_update: schemas.PostCreate, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("user_id")
    db_post = crud.get_post(db, post_id)
    if db_post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    return crud.update_post(db, post_id, post_update)

# Delete a post
@router.delete("/{post_id}")
def delete_post(post_id: int, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("user_id")
    db_post = crud.get_post(db, post_id)
    if db_post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    return crud.delete_post(db, post_id)