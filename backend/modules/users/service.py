from exceptions.base import SystemException
from typing import List, Optional
from .models import UserEntity
from logging import getLogger

logger = getLogger("UsersService")

class EmployeeDirectoryService:
    """Service for searching and managing employee profiles."""
    
    async def get_employee_by_id(self, user_id: str) -> Optional[UserEntity]:
        raise SystemException("Not Implemented: get_employee_by_id")

    async def search_employees(self, query: str) -> List[UserEntity]:
        raise SystemException("Not Implemented: search_employees")

class ManagerService:
    """Service for managing direct reports and manager delegations."""
    
    async def get_direct_reports(self, manager_id: str) -> List[UserEntity]:
        raise SystemException("Not Implemented: get_direct_reports")

    async def get_manager_chain(self, employee_id: str) -> List[UserEntity]:
        """Returns the chain of command up to the root level."""
        raise SystemException("Not Implemented: get_manager_chain")

class ValidationService:
    """Service for validating HR rules across the user domain."""
    
    async def validate_employee_status(self, user_id: str) -> bool:
        raise SystemException("Not Implemented: validate_employee_status")
