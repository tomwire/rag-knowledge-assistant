"""Role-based access control service."""


ALLOWED_ROLES = {"admin", "editor", "viewer"}


def check_role(user_role: str, required: str) -> bool:
    if required == "admin":
        return user_role == "admin"
    if required == "editor":
        return user_role in ("admin", "editor")
    return user_role in ALLOWED_ROLES
