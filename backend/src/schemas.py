from pydantic import BaseModel, EmailStr, field_validator
from typing import  Optional
from datetime import datetime


# user schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    
class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class TokenRequest(BaseModel):
    identifier: str 
    password: str
    
class LoginResponse(BaseModel):
    message: str
    user: UserResponse 
    access_token: str
    token_type: str
        
class Token(BaseModel):
    access_token: str
    token_type: str
        

# post schemas
        
class PostBase(BaseModel):
    title: str
    content: str
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: UserResponse
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        orm_mode = True

# comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user: UserResponse
    created_at: datetime
    
    class Config:
        orm_mode = True
        
# like schemas

class LikeResponse(BaseModel):
    user_id: int
    post_id: int
    
    class Config:
        orm_mode = True