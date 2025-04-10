from fastapi import status, APIRouter, Depends
from ..utils.database import SessionDep
from ..repository import user_repo
from ..utils import oauth2, models

router = APIRouter(tags=["Users"], prefix="/user", responses={404: {"description": "Not found"}})

@router.post("/", response_model=models.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(request: models.UserCreate, db: SessionDep):
    return user_repo.create_user(request, db)


@router.get("/", response_model=list[models.UserPublic], status_code=status.HTTP_200_OK)
def get_all_users(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_all_users(db)  


@router.get("/{id:int}", response_model=models.UserPublic, status_code=status.HTTP_200_OK)
def get_user(id: int, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_user(id, db)


@router.patch("/{id:int}", response_model=models.UserPublic, status_code=status.HTTP_200_OK)
def update_user(id: int, request: models.UserUpdate, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.update_user(id, request, db)


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.delete_user(id, db)
    
@router.get("/projects", response_model=list[models.Project], status_code=status.HTTP_200_OK)
def get_all_user_projects(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_all_user_projects(db, current_user)

@router.get("/components", response_model=list[models.Component], status_code=status.HTTP_200_OK)
def get_all_user_components(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return user_repo.get_all_user_components(db, current_user)