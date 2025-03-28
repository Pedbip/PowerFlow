from fastapi import HTTPException, status
from sqlmodel import select
from ..database import SessionDep
from .. import models
from ..hashing import Hash

def create_user(user: models.UserCreate, db: SessionDep):
    hashed_password = Hash.get_password_hash(user.password)
    user.password = hashed_password
    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: SessionDep):
    users = db.exec(select(models.User)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return users

def get_user(id: int, db: SessionDep):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    return user

def update_user(id: int, user: models.UserUpdate, db: SessionDep):
    db_user = db.get(models.User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    if user.password not in (None, ""):
        hashed_password = Hash.get_password_hash(user.password)
        user.password = hashed_password
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(id: int, db: SessionDep):
    db_user = db.get(models.User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User Deleted"}