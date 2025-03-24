from datetime import timedelta, datetime
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SEC_KEY')
ALGORITHM = "HS256"
USER_ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiration time for regular users
ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = 720  # Expiration time for admins (12 hours)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getHashedPassword(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, is_admin: bool = False, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Set expiration time based on user type (admin or regular user)
        expire_minutes = ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES if is_admin else USER_ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


