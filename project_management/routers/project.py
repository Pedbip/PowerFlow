from fastapi import APIRouter, status, Depends
from ..database import SessionDep
from .. import models
from ..repository import project_repo
from ..utils import oauth2

router = APIRouter(tags=["Projects"], prefix="/project", responses={404: {"description": "Not found"}}) 

@router.post("/", response_model=models.ProjectBase, status_code=status.HTTP_201_CREATED)
def create_project(project: models.ProjectBase, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.create_project(project, db, current_user)


@router.get("/", response_model=list[models.Project], status_code=status.HTTP_200_OK)
def get_all_projects(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.get_all_projects(db)


@router.get("/{id}", response_model=models.ProjectBase, status_code=status.HTTP_200_OK)
def get_project(id: str, db: SessionDep):
    return project_repo.get_project(id, db)


@router.patch("/{id}", response_model=models.ProjectBase, status_code=status.HTTP_200_OK)
def update_project(id: str, project: models.ProjectUpdate, db: SessionDep):
    return project_repo.update_project(id, project, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: str, db: SessionDep):
    return project_repo.delete_project(id, db)