from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.role import RoleCreate
from app.services.role_service import create_role, assign_role
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role.name)

@router.post("/assign")
def assign_user_role(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return assign_role(db, user, role_name)

@router.get("/user/{user_id}")
def get_user_role(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user_id": user.id, "role": user.role}

from app.utils.permissions import get_permissions

@router.get("/permissions/{user_id}")
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    permissions = get_permissions(user.role)
    return {"user_id": user.id, "role": user.role, "permissions": permissions}