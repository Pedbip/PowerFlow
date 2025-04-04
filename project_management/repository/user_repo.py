from fastapi import HTTPException, status
from sqlmodel import select
from ..database import SessionDep
from .. import models
from ..utils import hashing

def create_user(user: models.UserCreate, db: SessionDep):
    
    existing_user = db.exec(select(models.User).where(models.User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    existing_email = db.exec(select(models.User).where(models.User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    
    hashed_password = hashing.Hash.get_password_hash(user.password)
    user.password = hashed_password
    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: SessionDep):
    users = db.exec(select(models.User)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users found")
   
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
        hashed_password = hashing.Hash.get_password_hash(user.password)
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

# Projects
def get_all_user_projects(db: SessionDep, current_user: models.User):
    projects = db.exec(select(models.Project).where(models.Project.user_id == current_user.id)).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return projects


# Components
def get_all_user_components(db: SessionDep, current_user: models.User):
    components = db.exec(select(models.Component).where(models.Component.user_id == current_user.id)).all()
    if not components:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return components