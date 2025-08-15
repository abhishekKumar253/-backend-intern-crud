from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import schemas, crud, auth
from src.database import get_db

router = APIRouter(
    prefix="/api/posts",
    tags=["Likes"]
)

@router.post("/{post_id}/like", response_model=dict)
def like_or_unlike_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    return crud.like_or_unlike_post(db, post_id, current_user.id)
    