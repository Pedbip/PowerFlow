from pydantic import model_validator
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
    name: str = Field(index=True, min_length=1, max_length=100)  # Garantir que o nome não seja vazio e tenha um tamanho máximo
    
class ProjectList(ProjectBase):
    id: int

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime, onupdate=func.now()))
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="project")
    component_links: list[ProjectComponentLink] = Relationship(back_populates="project")

    @property
    def components(self) -> list["ComponentPublic"]:
        return [ComponentPublic(code=link.component.code, brand=link.component.brand, name=link.component.name) for link in self.component_links]  # Retorna os componentes diretamente
    @property
    def total_amperage(self) -> int:
        return sum(link.total_amperage for link in self.component_links)


class ProjectPublic(ProjectBase):
    component_links: list["ComponentPublic"] = Field(default_factory=list)


class ProjectUpdate(ProjectBase):
    name: str | None = Field(default=None)
    

# Component
class ComponentBase(SQLModel):
    code: str = Field(unique=True, nullable=False, index=True, min_length=1, max_length=50)  # Garantir que o código não seja vazio
    brand: str = Field(index=True)
    name: str = Field(index=True)
    amperage_rating: int | None = None
    voltage: int | None = None
    watts: int | None = None

    @model_validator(mode="before")
    @classmethod
    def auto_complete_missing(cls, values):
        amper, volts, watts = values.get("amperage_rating"), values.get("voltage"), values.get("watts")
        filled = [x for x in (amper, volts, watts) if x is not None]

        if len(filled) < 2:
            raise ValueError("Enter at least two attributes between amperage, voltage, and watts.")

        if amper is None:
            values["amperage_rating"] = watts // volts
        elif volts is None:
            values["voltage"] = watts // amper
        elif watts is None:
            values["watts"] = amper * volts

        return values


class Component(ComponentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Chave primária autoincremento
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="component")
    project_links: list[ProjectComponentLink] = Relationship(back_populates="component") 


class ComponentPublic(SQLModel):
    code: str
    brand: str
    name: str


class ComponentUpdate(ComponentBase):
    code: str | None = Field(default=None)
    brand: str | None = Field(default=None)
    name: str | None = Field(default=None)
    amperage_rating: int | None = Field(default=None)
    voltage: int | None = Field(default=None)
    watts: int | None = Field(default=None)


