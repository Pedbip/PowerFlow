from ast import Import
from fastapi import HTTPException, status, Depends
from sqlmodel import select
from ..database import SessionDep
from .. import models
from ..utils import oauth2
import pandas as pd
from fastapi.responses import JSONResponse

def create_project(project: models.ProjectBase, db: SessionDep, current_user: models.User):
    db_project = models.Project(name=project.name, user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return models.ProjectPublic(name=db_project.name, component_links=db_project.components)


def get_all_projects(db: SessionDep):
    projects = db.exec(select(models.Project)).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return projects


def get_project(id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == id)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found")
    return models.ProjectPublic(name=project.name, component_links=project.components)


def update_project(id: int, project: models.ProjectUpdate, db: SessionDep):
    db_project = db.get(models.Project, id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found")
    project_data = project.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(id: int, db: SessionDep):
    db_project = db.get(models.Project, id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project Deleted"}
    

def add_component_to_project(project_id: int, component_id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == project_id)).one()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    component = db.exec(select(models.Component).where(models.Component.id == component_id)).one()
    if not component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="component not found")
    project_component_link = models.ProjectComponentLink(project=project, component=component)
    db.add(project_component_link)
    db.commit()
    db.refresh(project)
    return models.ProjectPublic(name=project.name, component_links=project.components)


def remove_component_from_project(project_id: int, component_id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == project_id)).one()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    component = db.exec(select(models.Component).where(models.Component.id == component_id)).one()
    if not component:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="component not found")

    project_component_link = db.exec(select(models.ProjectComponentLink).where(models.ProjectComponentLink.project_id == project.id).filter(models.ProjectComponentLink.component_id == component.id)).one()
    if not project_component_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    db.delete(project_component_link)
    db.commit()
    db.refresh(project)
    return models.ProjectPublic(name=project.name, component_links=project.components)


def export_to_xlsx(project_id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == project_id)).one()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
    
    # Obtenha os componentes associados ao projeto
    project_components = db.exec(
        select(models.Component)
        .join(models.ProjectComponentLink)
        .where(models.ProjectComponentLink.project_id == project_id)
    ).all()
    
    if not project_components:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project has no components")
    
    # Crie o DataFrame com os dados dos componentes
    project_components_df = pd.DataFrame([
        {   
            "id": component.id,
            "code": component.code,
            "brand": component.brand,
            "name": component.name,
            "amperage_rating": component.amperage_rating,
            "volrage": component.voltage,
            "watts": component.watts
        }
        for component in project_components
    ])
    # Criar um dicionário com os totais na última linha
    total_row = {
        "id": "TOTAL",
        "code": "",
        "brand": "",
        "name": "",
        "amperage_rating": "",
        "voltage": "",
        "watts": "",
        "component_quantity": sum(link.component_quantity for link in project.component_links),
        "total_amperage": project.total_amperage
    }

    # Adicionar a linha total ao DataFrame
    project_components_df = pd.concat([project_components_df, pd.DataFrame([total_row])], ignore_index=True)

    # Exporte para um arquivo Excel
    project_components_df.to_excel(f"{project.name}.xlsx", index=False, engine='openpyxl')
    return JSONResponse(content={"message": f"Project {project.name} exported to Excel successfully."}, status_code=status.HTTP_200_OK)