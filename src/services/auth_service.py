from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Union
from models.entities import User, Admin
from models.schemas import TokenData
from utils.security import SECRET_KEY, ALGORITHM
from models.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/token")

def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_admin(db: Session, email: str) -> Admin:
    return db.query(Admin).filter(Admin.email == email).first()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Union[User, Admin]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    admin = get_admin(db, email=token_data.email)
    if admin:
        return admin
        
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    admin = get_admin(db, email=token_data.email)
    if not admin:
        raise HTTPException(status_code=403, detail="Only admins can perform this action")
    return admin