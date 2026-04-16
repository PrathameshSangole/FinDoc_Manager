from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.schemas.role import RoleCreate
from app.utils.permissions import get_permissions

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/roles/create")
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.name == role.name).first()

    if existing_role:
        return {"message": "Role already exists", "role": role.name}

    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role

@router.post("/users/assign-role")
def assign_user_role(user_id: int, role_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_name
    db.commit()
    db.refresh(user)

    return {"message": "Role assigned", "role": user.role}

@router.get("/users/{user_id}/roles")
def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user_id": user.id, "role": user.role}

@router.get("/users/{user_id}/permissions")
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "role": user.role,
        "permissions": get_permissions(user.role)
    }