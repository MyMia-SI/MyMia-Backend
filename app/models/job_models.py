# Folder: /app/models
"""Job related models (e.g., job data, summaries, statuses)."""
from pydantic import BaseModel, Field
from typing import Optional


class Job(BaseModel):
    id: str
    tenant_id: str
    status: str = Field(default="created")
    description: Optional[str] = None
