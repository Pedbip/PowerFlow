from fastapi import APIRouter, status, Depends, Response
from ..utils.database import SessionDep
from ..repository import project_repo
from ..utils import oauth2, models

router = APIRouter(tags=["Projects"], prefix="/project", responses={404: {"description": "Not found"}}) 


@router.post("/", response_model=models.ProjectPublic, status_code=status.HTTP_201_CREATED)
def create_project(request: models.ProjectBase, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.create_project(request, db, current_user)


@router.get("/", response_model=list[models.ProjectList], status_code=status.HTTP_200_OK)
def get_all_projects(db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.get_all_projects(db)


@router.get("/{id}", response_model=models.ProjectPublic, status_code=status.HTTP_200_OK)
def get_project(id: str, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.get_project(id, db)


@router.patch("/{id}", response_model=models.ProjectPublic, status_code=status.HTTP_200_OK)
def update_project(id: str, request: models.ProjectUpdate, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.update_project(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: str, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.delete_project(id, db)


# Component Functions
@router.patch("/{project_id}/add-component", response_model=models.ProjectPublic)
def add_component_to_project(request: models.ComponentLink, project_id: int, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.add_component_to_project(request, project_id, db)


@router.delete("/{project_id}/delete-component", response_model=models.ProjectPublic)
def remove_component_from_project(request: models.ComponentLink, project_id: int, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.remove_component_from_project(request, project_id, db)


