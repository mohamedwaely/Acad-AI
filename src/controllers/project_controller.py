from fastapi import Depends
from sqlalchemy.orm import Session
from models.schemas import ProjectBase, ProjectsResponse
from models.entities import Admin
from services.project_service import upload_project, get_projects
from services.auth_service import get_current_admin
from models.database import get_db

async def upload_projects(data: ProjectBase, cur_admin: Admin, db: Session) -> dict:
    return upload_project(data, cur_admin.username, db)

async def get_projects_controller(title: str | None, db: Session) -> list[ProjectsResponse] | ProjectsResponse:
    return get_projects(title, db)