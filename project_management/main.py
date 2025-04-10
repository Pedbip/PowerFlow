from fastapi import FastAPI
from .utils.database import create_db_and_tables
from contextlib import asynccontextmanager
from .routers import project, user, component, authentication, export

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Criando banco de dados e tabelas...")
    create_db_and_tables()
    yield  
    print("API sendo encerrada...")

app = FastAPI(lifespan=lifespan)

app.include_router(project.router) 
app.include_router(user.router)
app.include_router(component.router)
app.include_router(authentication.router)
app.include_router(export.router)