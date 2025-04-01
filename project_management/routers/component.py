from fastapi import APIRouter, status, Depends
from ..database import SessionDep
from .. import models
from ..repository import component_repo
from ..utils import oauth2

router = APIRouter(tags=["Components"], prefix="/component", responses={404: {"description": "Not found"}})

@router.post("/", response_model=models.ComponentBase, status_code=status.HTTP_201_CREATED)
def create_component(component: models.ComponentBase, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return component_repo.create_component(component, db, current_user)


@router.get("/", response_model=list[models.Component], status_code=status.HTTP_200_OK)
def get_all_components(db: SessionDep):
    return component_repo.get_all_components(db)


@router.get("/{id}", response_model=models.ComponentBase, status_code=status.HTTP_200_OK)   
def get_component(id: str, db: SessionDep):
    return component_repo.get_component(id, db)


@router.patch("/{id}", response_model=models.ComponentBase, status_code=status.HTTP_200_OK)
def update_component(id: str, component: models.ComponentUpdate, db: SessionDep):
    return component_repo.update_component(id, component, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(id: str, db: SessionDep):
    return component_repo.delete_component(id, db)

