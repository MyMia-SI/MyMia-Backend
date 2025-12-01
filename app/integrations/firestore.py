# Folder: /app/integrations
"""Firestore integration wrapper. A light abstraction for CRUD operations.
"""
from typing import Any, Dict


class FirestoreClient:
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def get_document(self, path: str) -> Dict[str, Any]:
        return {"path": path, "data": {}}
