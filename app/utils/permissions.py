ROLE_PERMISSIONS = {
    "Admin": ["full_access"],
    "Analyst": ["upload", "edit"],
    "Auditor": ["review"],
    "Client": ["view"]
}

def get_permissions(role: str):
    return ROLE_PERMISSIONS.get(role, [])