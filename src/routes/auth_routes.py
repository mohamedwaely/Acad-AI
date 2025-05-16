from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.auth_controller import register, login
from models.schemas import User, UserDBBase, Token, LoginRequest
from models.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserDBBase)
async def register_route(user: User, db: Session = Depends(get_db)):
    return await register(user, db)

@router.post("/token", response_model=Token)
async def login_route(login_data: LoginRequest, db: Session = Depends(get_db)):
    return await login(login_data, db)