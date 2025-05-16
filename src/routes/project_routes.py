from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.project_controller import upload_projects, get_projects_controller
from models.schemas import ProjectBase, ProjectsResponse
from models.database import get_db
from services.auth_service import get_current_admin

router = APIRouter()

@router.post("/upload-projects")
async def upload_projects_route(
    data: ProjectBase,
    db: Session = Depends(get_db),
    cur_admin = Depends(get_current_admin)
):
    return await upload_projects(data, cur_admin, db)

@router.get("/projects/{title}", response_model=ProjectsResponse)
@router.get("/projects", response_model=list[ProjectsResponse])
async def get_projects_route(title: str | None = None, db: Session = Depends(get_db)):
    return await get_projects_controller(title, db)