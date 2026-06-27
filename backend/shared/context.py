import contextvars
from typing import Optional

# Request tracking variables
request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("request_id", default=None)
user_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("user_id", default=None)
department_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("department", default=None)
correlation_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("correlation_id", default=None)

def get_request_id() -> Optional[str]:
    return request_id_var.get()

def set_request_id(request_id: str) -> None:
    request_id_var.set(request_id)

def get_user_id() -> Optional[str]:
    return user_id_var.get()

def set_user_id(user_id: str) -> None:
    user_id_var.set(user_id)

def get_department() -> Optional[str]:
    return department_var.get()

def set_department(department: str) -> None:
    department_var.set(department)

def get_correlation_id() -> Optional[str]:
    return correlation_id_var.get()

def set_correlation_id(correlation_id: str) -> None:
    correlation_id_var.set(correlation_id)
