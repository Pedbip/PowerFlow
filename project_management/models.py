from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import Optional, List

# User
class UserBase(SQLModel): # Modelo de entrada
    username: str = Field(index=True)
    email: str = Field(index=True)
    

class User(UserBase, table=True): # Modelo do banco
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field()

class UserCreate(UserBase): 
    password: str = Field()

class UserPublic(UserBase): # Modelo de saída
    id: int # Não precisa de Field(), pois não é gerenciado pelo BD

class UserUpdate(UserBase): 
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)


class ProjectComponentLink(SQLModel):
    project_id: int | None = Field(default=None, foreign_key="component.id", primary_key=True)
    component_id: int | None = Field(default=None, foreign_key="project.id", primary_key=True)
    component_quantity: int | None

# Project
class ProjectBase(SQLModel):
    name: str = Field(index=True)
    

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, onupdate=func.now()))

    components: list["Component"] = Relationship(back_populates="projects", link_model=ProjectComponentLink) # N:N

class ProjectUpdate(ProjectBase):
    name: str | None = Field(default=None)
    

# Component
class ComponentBase(SQLModel):
    code: str = Field(unique=True, nullable=False, index=True)  # Garante que seja único
    brand: str = Field(index=True)
    name: str = Field(index=True)
    amperage_rating: int = Field()
    voltage: int = Field()
    watts: int = Field()

class Component(ComponentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Chave primária autoincremento

    projects: list[Project] = Relationship(back_populates="components", link_model=ProjectComponentLink) # N:N

class ComponentUpdate(ComponentBase):
    code: str | None = Field(default=None)
    brand: str | None = Field(default=None)
    name: str | None = Field(default=None)
    amperage_rating: int | None = Field(default=None)
    voltage: int | None = Field(default=None)
    watts: int | None = Field(default=None)


