from fastapi import APIRouter, status, Response, Depends
from ..utils.database import SessionDep
from ..repository import project_repo
from ..utils import oauth2, models


router = APIRouter(tags=["Export"], prefix="/export", responses={404: {"description": "Not found"}})


@router.get("/export/{project_id}", response_class=Response, status_code=status.HTTP_200_OK)
def export_projects_to_xlsx(project_id: int, db: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    return project_repo.export_to_xlsx(project_id, db)