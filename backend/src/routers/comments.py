from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src import schemas, crud, auth
from src.database import get_db

router = APIRouter(
    prefix="/api/posts",
    tags=["Comments"]
)

@router.post("/{post_id}/comments", response_model=schemas.CommentResponse)
def create_comment_for_post_route(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    db_comment = crud.create_comment(db, comment, post_id, current_user.id)
    return db_comment

@router.get("/{post_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments_for_post_route(
    post_id: int,
    db: Session = Depends(get_db)
):

    comments = crud.get_comments_by_post(db, post_id)
    return comments

@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment_route(
    comment_id: int,
    updated_comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user) 
):
    comment = crud.get_comment_by_id(db, comment_id) 
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    updated_db_comment = crud.update_comment(db, comment_id, updated_comment) 
    return updated_db_comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_route(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    comment = crud.get_comment_by_id(db, comment_id) 
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
        
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    crud.delete_comment(db, comment_id) 
    return

