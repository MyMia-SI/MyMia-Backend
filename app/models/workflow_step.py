# Folder: /app/models
"""Model for a step in a workflow execution history."""
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class WorkflowStep(BaseModel):
    name: str
    status: str = Field(default="pending")
    output: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
