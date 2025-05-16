from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class User(UserBase):
    password: str

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class Admin(UserBase):
    password: str
    degree: str

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('degree')
    def degree_valid(cls, v):
        if v not in ['A', 'B']:
            raise ValueError('Degree must be either A, or B')
        return v

class UserDBBase(UserBase):
    id: int
    class Config:
        from_attributes = True

class AdminDBBase(UserBase):
    id: int
    degree: str
    class Config:
        from_attributes = True

class UserDB(UserDBBase):
    hashed_password: str

class AdminDB(AdminDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChatResponse(BaseModel):
    response: str

class ChatRequest(BaseModel):
    query: str

class ProjectBase(BaseModel):
    title: str
    supervisor: str
    description: str
    tools: List[str]
    year: int

    @validator('year')
    def year_valid(cls, v):
        current_year = datetime.datetime.now().year
        if v < 2023 or v > current_year:
            raise ValueError(f'Year must be between 2023 and {current_year}')
        return v

class ProjectResponse(BaseModel):
    id: int
    title: str
    supervisor: str
    description: str
    tools: List[str]
    year: int

    class Config:
        from_attributes = True

class CheckProject(BaseModel):
    title: str
    description: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str
    degree: str
    added_by: str
    class Config:
        from_attributes = True

class ProjectsResponse(BaseModel):
    id: int
    title: str
    supervisor: str
    description: str
    tools: str
    year: int
    class Config:   
        from_attributes = True