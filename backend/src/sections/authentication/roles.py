from typing import List, Any, Annotated
from fastapi import Depends, HTTPException, status

# local imports
from src.sections.database.models import User
from src.sections.authentication.dependencies import get_current_user
from src.sections.errors import InsufficientPermission


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
    


role_checker = RoleChecker(["admin", "user"])
getRoleCheckDep = Annotated[bool, Depends(role_checker)]