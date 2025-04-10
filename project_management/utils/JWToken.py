from datetime import datetime, timedelta, timezone
import jwt
from sqlmodel import select
from fastapi import HTTPException, status
from pydantic import BaseModel
from .database import SessionDep
from . import models
from .hashing import Hash


SECRET_KEY = "d3e24369171598affc0960fb2bdb11641ef2dd0de41df553810c452fec7f8e2b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def authenticate_user(db: SessionDep, username: str, password: str):
    user = db.exec(select(models.User).where(models.User.username == username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password doesn't match")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

