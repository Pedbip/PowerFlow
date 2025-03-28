from fastapi import HTTPException, status
from sqlmodel import select
from ..database import SessionDep
from .. import models

def create_project(project: models.ProjectBase, db: SessionDep):
    db_project = models.Project.model_validate(project)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_all_projects(db: SessionDep):
    projects = db.exec(select(models.Project)).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty list, please add an item")
    return projects

def get_project(id: int, db: SessionDep):
    project = db.exec(select(models.Project).where(models.Project.id == id)).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found")
    return project

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