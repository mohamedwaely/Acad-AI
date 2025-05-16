from fastapi import Depends
from sqlalchemy.orm import Session
from models.schemas import Admin, AdminDBBase, AdminResponse
from services.admin_service import add_admin, get_admins
from services.auth_service import get_current_admin
from models.database import get_db

async def add_admin_controller(
    admin_data: Admin,
    db: Session = Depends(get_db),
    cur_admin = Depends(get_current_admin)
) -> AdminDBBase:
    return add_admin(admin_data, cur_admin.email, cur_admin.degree, db)

async def get_admins_controller(
    degree: str | None = None,
    db: Session = Depends(get_db),
    cur_admin = Depends(get_current_admin)
) -> list[AdminResponse]:
    return get_admins(degree, cur_admin.degree, db)