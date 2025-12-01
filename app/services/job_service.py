# Folder: /app/services
"""JobService: deterministic business logic for job CRUD via Firestore integration.

Services must not access external APIs directly; Firestore integration handles persistence.
"""
from typing import Any, Dict, List, Optional
import asyncio
from pydantic import BaseModel

from app.integrations.firestore import FirestoreClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class JobCreateRequest(BaseModel):
    tenant_id: str
    description: Optional[str] = None


class JobModel(BaseModel):
    id: str
    tenant_id: str
    status: str
    description: Optional[str] = None


class JobService:
    def __init__(self, client: Optional[FirestoreClient] = None, project_id: Optional[str] = None) -> None:
        self.client = client or FirestoreClient(project_id or "")

    async def create_job(self, payload: Dict[str, Any]) -> JobModel:
        data = JobCreateRequest(**payload)

        def _create():
            doc_ref = f"jobs/{data.tenant_id}/{id(payload)}"
            # Persist minimal fields; real implementation would use a uuid or Firestore generated ID.
            self.client.get_document(doc_ref)  # touch, placeholder
            return {"id": doc_ref, "tenant_id": data.tenant_id, "status": "created", "description": data.description}

        result = await asyncio.to_thread(_create)
        return JobModel(**result)

    async def update_job(self, job_id: str, update: Dict[str, Any]) -> JobModel:
        def _update():
            # Placeholder: update doc in Firestore
            doc = self.client.get_document(job_id)
            merged = {**doc.get("data", {}), **update}
            return {"id": job_id, **merged}

        result = await asyncio.to_thread(_update)
        return JobModel(**{"id": result.get("id"), "tenant_id": result.get("tenant_id", ""), "status": result.get("status", ""), "description": result.get("description", None)})

    async def get_job(self, job_id: str) -> JobModel:
        def _get():
            doc = self.client.get_document(job_id)
            return {"id": job_id, **doc.get("data", {})}

        result = await asyncio.to_thread(_get)
        return JobModel(**{"id": result.get("id"), "tenant_id": result.get("tenant_id", ""), "status": result.get("status", ""), "description": result.get("description", None)})

    async def list_jobs(self, tenant_id: str, page: int = 1, per_page: int = 50) -> List[JobModel]:
        def _list():
            # Placeholder: list docs with a basic filter
            return []

        results = await asyncio.to_thread(_list)
        return [JobModel(**r) for r in results]
