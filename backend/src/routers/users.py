from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import schemas, crud, auth
from src.database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

# User Registration 
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    return crud.create_user(db, user)


# User Login
@router.post("/login", response_model=schemas.LoginResponse)
def login_user(form_data: schemas.TokenRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.identifier)
    if not user:
        user = crud.get_user_by_email(db, email=form_data.identifier)
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"user_id": user.id})
    
    user_response = schemas.UserResponse.model_validate(user)
    
    return {
        "message": "User logged in successfully",
        "user": user_response, 
        "access_token": access_token,
        "token_type": "bearer"
    }


# Get Current User
@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user