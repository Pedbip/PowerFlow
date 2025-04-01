from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy import DateTime, func
from datetime import datetime

# User
class UserBase(SQLModel): # Modelo de entrada
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    

class User(UserBase, table=True): # Modelo do banco
    id: int | None = Field(default=None, primary_key=True)
    password: str

    component: list["Component"] = Relationship(back_populates="user")
    project: list["Project"] = Relationship(back_populates="user")


class UserCreate(UserBase): 
    password: str


class UserPublic(UserBase): # Modelo de saída
    id: int # Não precisa de Field(), pois UserPublic é um DTO e não interage diretamente com o banco de dados


class UserUpdate(UserBase): 
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)


# Link tables
class ProjectComponentLink(SQLModel, table=True):
    project_id: int | None = Field(default=None, foreign_key="project.id", primary_key=True)
    component_id: int | None = Field(default=None, foreign_key="component.id", primary_key=True)
    component_quantity: int = Field(default=1)

    project: "Project" = Relationship(back_populates="component_links")
    component: "Component" = Relationship(back_populates="project_links")

    @property
    def total_amperage(self) -> int:
        return self.component.amperage_rating * self.component_quantity


# Project
class ProjectBase(SQLModel):
    name: str = Field(index=True)
    

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime, onupdate=func.now()))
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="project")
    component_links: list[ProjectComponentLink] = Relationship(back_populates="project")

    @property
    def total_amperage(self) -> int:
        return sum(link.total_amperage for link in self.component_links)


class ProjectUpdate(ProjectBase):
    name: str | None = Field(default=None)
    

# Component
class ComponentBase(SQLModel):
    code: str = Field(unique=True, nullable=False, index=True)  # Garante que seja único
    brand: str = Field(index=True)
    name: str = Field(index=True)
    amperage_rating: int
    voltage: int
    watts: int


class Component(ComponentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Chave primária autoincremento
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="component")
    project_links: list[ProjectComponentLink] = Relationship(back_populates="component") 


class ComponentUpdate(ComponentBase):
    code: str | None = Field(default=None)
    brand: str | None = Field(default=None)
    name: str | None = Field(default=None)
    amperage_rating: int | None = Field(default=None)
    voltage: int | None = Field(default=None)
    watts: int | None = Field(default=None)


