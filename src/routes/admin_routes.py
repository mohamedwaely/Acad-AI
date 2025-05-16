from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.admin_controller import add_admin_controller, get_admins_controller
from models.schemas import Admin, AdminDBBase, AdminResponse
from models.database import get_db

router = APIRouter()

@router.post("/add-admin", response_model=AdminDBBase)
async def add_admin_route(admin_data: Admin, db: Session = Depends(get_db)):
    return await add_admin_controller(admin_data, db=db)

@router.get("/admins/{degree}", response_model=list[AdminResponse])
@router.get("/admins/", response_model=list[AdminResponse])
async def get_admins_route(degree: str | None = None, db: Session = Depends(get_db)):
    return await get_admins_controller(degree, db=db)