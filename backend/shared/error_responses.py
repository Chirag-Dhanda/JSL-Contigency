from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class ValidationErrorDetail(BaseModel):
    loc: List[str] = Field(description="The location of the field that failed validation.")
    msg: str = Field(description="The validation error message.")
    type: str = Field(description="The type of the validation error.")

class ErrorResponse(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status_code: int
    error_code: str
    title: str
    user_message: str
    developer_message: Optional[str] = None
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    path: str
    validation_errors: Optional[List[ValidationErrorDetail]] = None
    documentation_ref: Optional[str] = None
