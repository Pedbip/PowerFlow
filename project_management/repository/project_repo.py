from fastapi import HTTPException, status, Depends
from sqlmodel import select
from ..database import SessionDep
from .. import models
from ..utils import oauth2

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