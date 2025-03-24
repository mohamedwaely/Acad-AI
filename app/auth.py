from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models, schemas, security
from app.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getUser(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def getAdmin(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

async def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")  # Use email as the subject (sub) in JWT
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # First, check if the user is an admin
    admin = getAdmin(db, email=token_data.email)
    if admin:
        return admin
    
    # If not an admin, check if the user is a regular user
    user = getUser(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def getCurrentAdmin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")  # Use email as the subject (sub) in JWT
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Check if the user is an admin
    admin = getAdmin(db, email=token_data.email)
    if not admin:
        raise HTTPException(status_code=403, detail="Only admins can perform this action")
    return admin


