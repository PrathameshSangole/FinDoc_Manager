from app.models.role import Role

def create_role(db, name):
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def assign_role(db, user, role_name):
    user.role = role_name
    db.commit()
    db.refresh(user)
    return user