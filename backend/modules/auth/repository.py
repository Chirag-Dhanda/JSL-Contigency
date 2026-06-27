from abc import ABC, abstractmethod
from typing import Optional
from .models import User

class IAuthRepository(ABC):
    """Interface for Authentication Repository."""
    
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def log_failed_attempt(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def reset_failed_attempts(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def update_last_login(self, user_id: str) -> None:
        pass

class MockAuthRepository(IAuthRepository):
    """Placeholder implementation of AuthRepository until database integration."""
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        return None

    async def log_failed_attempt(self, user_id: str) -> None:
        pass

    async def reset_failed_attempts(self, user_id: str) -> None:
        pass

    async def update_last_login(self, user_id: str) -> None:
        pass
