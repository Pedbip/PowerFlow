from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..utils import JWToken
from datetime import timedelta
from ..utils.database import SessionDep

router = APIRouter(tags=["Login"])

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep) -> JWToken.Token:

    user = JWToken.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)
    
    access_token_expires = timedelta(minutes=JWToken.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWToken.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    
    return JWToken.Token(access_token=access_token, token_type="bearer")