from fastapi import FastAPI, Depends
from sqlmodel import Session
from .database import create_db_and_tables
from . import models
from .database import SessionDep
from contextlib import asynccontextmanager
from .routers import project, user

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Criando banco de dados e tabelas...")
    create_db_and_tables()
    yield  
    print("API sendo encerrada...")

app = FastAPI(lifespan=lifespan)

app.include_router(project.router) 
app.include_router(user.router)