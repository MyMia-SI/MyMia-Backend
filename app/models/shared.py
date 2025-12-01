# Folder: /app/models
"""Shared models and types across the application."""
from pydantic import BaseModel
from typing import Optional


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 50
    cursor: Optional[str] = None
