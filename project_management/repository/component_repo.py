from fastapi import HTTPException, status
from sqlmodel import select
from ..utils.database import SessionDep
from ..utils import models

def create_component(request: models.ComponentBase, db: SessionDep, current_user: models.User):
    
    existing_component = db.exec(select(models.Component).where(models.Component.code == request.code)).first()
    if existing_component:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Component code already exists")
    
    db_component = models.Component(
        code=request.code,
        brand=request.brand,
        name=request.name,
        amperage_rating=request.amperage_rating,
        voltage=request.voltage,
        watts=request.watts,
        user_id=current_user.id
    )
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


def update_component(id: str, request: models.ComponentUpdate, db: SessionDep):
    db_component = db.get(models.Component, id)
    if not db_component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component not found")
    component_data = request.model_dump(exclude_unset=True)
    db_component.sqlmodel_update(component_data)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


def delete_component(id: str, db: SessionDep):
    db_component = db.get(models.Component, id)
    if not db_component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component not found")
    
    if db_component.project_links:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete a component that is linked to a project")
    
    db.delete(db_component)
    db.commit()
    return {"message": "Component Deleted"}