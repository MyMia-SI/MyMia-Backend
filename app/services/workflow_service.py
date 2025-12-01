# Folder: /app/services
"""WorkflowService: helper utilities for workflow validation, merging, and step execution.

Keep deterministic merging rules here to centralize how state changes across steps are merged.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.utils.logging import get_logger

logger = get_logger(__name__)


class WorkflowDefinition(BaseModel):
    name: str
    version: str
    steps: List[str]


class WorkflowService:
    def __init__(self) -> None:
        # In a real system this would load workflow definitions from storage or config
        self._definitions: Dict[str, WorkflowDefinition] = {}

    def validate_workflow(self, name: str) -> bool:
        # Placeholder validation: check if a definition exists.
        return name in self._definitions

    def register_workflow(self, definition: WorkflowDefinition) -> None:
        self._definitions[definition.name] = definition

    def get_workflow(self, name: str) -> Optional[WorkflowDefinition]:
        return self._definitions.get(name)

    def merge_state(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        # Deterministic merge: simple shallow merge here, can be replaced with more complex rules
        merged = dict(base)
        for k in sorted(update.keys()):
            merged[k] = update[k]
        return merged

