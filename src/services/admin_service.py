from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.entities import Admin, User
from models.schemas import Admin
from utils.security import get_hashed_password
from services.auth_service import get_user, get_admin

def add_admin(admin_data: Admin, current_admin_email: str, current_admin_degree: str, db: Session) -> Admin:
    if current_admin_degree != 'A':
        raise HTTPException(status_code=403, detail="Only admins with degree A can add other admins")
    
    existing_user = get_user(db, email=admin_data.email)
    existing_admin = get_admin(db, email=admin_data.email)
    if existing_user or existing_admin:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = get_hashed_password(admin_data.password)
    
    new_admin = Admin(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=hashed_password,
        degree=admin_data.degree,
        added_by=current_admin_email
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_admins(degree: str | None, current_admin_degree: str, db: Session) -> list[Admin]:
    if current_admin_degree != 'A':
        raise HTTPException(status_code=403, detail="Only admins with degree A can view other admins")
    try:
        query = db.query(
            Admin.id,
            Admin.username,
            Admin.email,
            Admin.degree,
            Admin.added_by
        )
        if degree is None:
            return query.all()
        else:
            return query.filter(Admin.degree == degree).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get admins: {str(e)}")