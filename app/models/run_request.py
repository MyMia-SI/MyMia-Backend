# Folder: /app/models
"""RunRequest model for the /run endpoint.
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class RunRequest(BaseModel):
    workflow: str = Field(..., description="Name of the workflow to execute")
    payload: Optional[Dict[str, Any]] = Field(default_factory=dict)
