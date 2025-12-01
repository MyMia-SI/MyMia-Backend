# Folder: /app/models
"""User models (basic user profile and metadata)."""
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    tenant_id: Optional[str] = None
