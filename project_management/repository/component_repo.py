from fastapi import HTTPException, status
from sqlmodel import select
from ..database import SessionDep
from .. import models

def create_component(component: models.ComponentBase, db: SessionDep):
    db_component = models.Component.model_validate(component)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component 

def get_all_components(db: SessionDep):
    components = db.exec(select(models.Component)).all()
    if not components:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return components

def get_component(id: str, db: SessionDep):
    component = db.get(models.Component, id)
    if not component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component not found")
    return component

def update_component(id: str, component: models.ComponentUpdate, db: SessionDep):
    db_component = db.get(models.Component, id)
    if not db_component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component not found")
    component_data = component.model_dump(exclude_unset=True)
    db_component.sqlmodel_update(component_data)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

def delete_component(id: str, db: SessionDep):
    db_component = db.get(models.Component, id)
    if not db_component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component not found")
    db.delete(db_component)
    db.commit()
    return {"message": "Component Deleted"}