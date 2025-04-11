from fastapi import HTTPException, status
from sqlmodel import select
from ..utils.database import SessionDep
from ..utils import models
import pandas as pd
from fastapi.responses import JSONResponse
from sqlalchemy import or_

def create_project(request: models.ProjectBase, db: SessionDep, current_user: models.User):

    existing_project = db.exec(select(models.Project).where(models.Project.name == request.name).where(models.Project.user_id == current_user.id)).first()
    
    if existing_project:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="a project with this name already exists for the current user")
    
    db_project = models.Project(name=request.name, user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return models.ProjectPublic(name=db_project.name, component_links=db_project.components, latest_modification=db_project.updated_at if db_project.updated_at else db_project.created_at)


def get_all_projects(db: SessionDep):
    projects = db.exec(select(models.Project)).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return projects


def get_project(id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == id)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project not found")
    return models.ProjectPublic(name=project.name, component_links=project.components, latest_modification=project.updated_at if project.updated_at else project.created_at)


def update_project(id: int, request: models.ProjectUpdate, db: SessionDep):
    db_project = db.get(models.Project, id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project not found")
    project_data = request.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return models.ProjectPublic(name=db_project.name, component_links=db_project.components, latest_modification=db_project.updated_at if db_project.updated_at else db_project.created_at)


def delete_project(id: int, db: SessionDep):
    db_project = db.get(models.Project, id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project not found")
    db.delete(db_project)
    db.commit()
    return JSONResponse(content={"message": "Project deleted."})
    

def add_component_to_project(request: models.ComponentLink, project_id: int, db: SessionDep):
    project = db.exec(select(models.Project)
                      .where(models.Project.id == project_id)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    component = db.exec(select(models.Component)
                        .where(or_(models.Component.id == request.id, models.Component.code == request.code))).first()
    if not component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="component not found")

    existing_link = db.exec(select(models.ProjectComponentLink).where(models.ProjectComponentLink.project_id == project_id)
        .where(models.ProjectComponentLink.component_id == component.id)).first()
    
    if existing_link:
        if request.quantity <= 0:  
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be greater than 0")
        existing_link.component_quantity += request.quantity
        db.add(existing_link)
        db.commit()
        db.refresh(existing_link)
        db.refresh(project)
    else:
        project_component_link = models.ProjectComponentLink(project=project, component=component, component_quantity=request.quantity)
        db.add(project_component_link)
        db.commit()
        db.refresh(project_component_link)
        db.refresh(project)

    return models.ProjectPublic(name=project.name, component_links=project.components, latest_modification=project.updated_at if project.updated_at else project.created_at)


def remove_component_from_project(request: models.ComponentLink, project_id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == project_id)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    
    component = db.exec(select(models.Component).where(or_(models.Component.code == request.code, models.Component.id == request.id))).first()
    if not component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="component not found")

    project_component_link = db.exec(select(models.ProjectComponentLink).where(models.ProjectComponentLink.project_id == project.id).filter(models.ProjectComponentLink.component_id == component.id)).one()
    if not project_component_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    
    if request.quantity > project_component_link.component_quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity is greater than the current quantity")
    
    if request.quantity == project_component_link.component_quantity:
        db.delete(project_component_link)
    else:
        project_component_link.component_quantity -= request.quantity
        db.add(project_component_link)

    db.commit()
    db.refresh(project)
    
    return models.ProjectPublic(name=project.name, component_links=project.components, latest_modification=project.updated_at if project.updated_at else project.created_at)


def export_to_xlsx(project_id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == project_id)).one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


    project_component_links = db.exec(select(models.ProjectComponentLink).join(models.Component).where(models.ProjectComponentLink.project_id == project_id)).all()

    if not project_component_links:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project has no components")


    project_components_df = pd.DataFrame([
        {
            "id": link.component.id,
            "code": link.component.code,
            "brand": link.component.brand,
            "name": link.component.name,
            "amperage rating": link.component.amperage_rating,
            "voltage": link.component.voltage,
            "watts": link.component.watts,
            "quantity": link.component_quantity
        }
        for link in project_component_links
    ])


    total_row = {
        "id": "TOTAL",
        "code": "",
        "brand": "",
        "name": "",
        "amperage rating": "",
        "voltage": "",
        "watts": "",
        "quantity": sum(link.component_quantity for link in project_component_links),  
        "total amperage": project.total_amperage
    }

    project_components_df = pd.concat([project_components_df, pd.DataFrame([total_row])], ignore_index=True)

    project_components_df.to_excel(f"{project.name}.xlsx", index=False, engine='openpyxl')
    return JSONResponse(content={"message": f"Project {project.name} exported to Excel successfully."}, status_code=status.HTTP_200_OK)