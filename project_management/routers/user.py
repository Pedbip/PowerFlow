from fastapi import status, APIRouter
from ..database import SessionDep
from .. import models
from typing import List
from ..repository import user_repo

router = APIRouter(tags=["Users"], prefix="/user", responses={404: {"description": "Not found"}})

@router.post("/", response_model=models.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, db: SessionDep):
    return user_repo.create_user(user, db)

@router.get("/", response_model=List[models.UserPublic])
def get_all_users(db: SessionDep):
    return user_repo.get_all_users(db)  

@router.get("/{id}", response_model=models.UserPublic)
def get_user(id: int, db: SessionDep):
    return user_repo.get_user(id, db)

@router.patch("/{id}", response_model=models.UserPublic)
def update_user(id: int, user: models.UserUpdate, db: SessionDep):
    return user_repo.update_user(id, user, db)

@router.delete("/{id}")
def delete_user(id: int, db: SessionDep):
    return user_repo.delete_user(id, db)
    