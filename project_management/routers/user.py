from fastapi import status, APIRouter, Depends
from ..database import SessionDep
from .. import models
from ..repository import user_repo
from ..utils import oauth2

router = APIRouter(tags=["Users"], prefix="/user", responses={404: {"description": "Not found"}})

@router.post("/", response_model=models.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, db: SessionDep):
    return user_repo.create_user(user, db)


@router.get("/", response_model=list[models.UserPublic])
def get_all_users(db: SessionDep):
    return user_repo.get_all_users(db)  


@router.get("/{id:int}", response_model=models.UserPublic)
def get_user(id: int, db: SessionDep):
    return user_repo.get_user(id, db)


@router.patch("/{id:int}", response_model=models.UserPublic)
def update_user(id: int, user: models.UserUpdate, db: SessionDep):
    return user_repo.update_user(id, user, db)


@router.delete("/{id:int}")
def delete_user(id: int, db: SessionDep):
    return user_repo.delete_user(id, db)
    
@router.get("/projects", response_model=list[models.Project])
def get_all_user_projects(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_all_user_projects(db, current_user)

@router.get("/component", response_model=list[models.Component])
def get_all_user_components(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_all_user_components(db, current_user)