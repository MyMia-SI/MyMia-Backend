# Folder: /app/services
"""ReportService: Generates PDFs / structured summaries and stores them in Storage.
"""
from typing import Any, Dict, Optional
import asyncio
from pydantic import BaseModel

from app.integrations.storage import StorageClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class ReportOutput(BaseModel):
    report_id: str
    url: Optional[str] = None


class ReportService:
    def __init__(self, storage_client: Optional[StorageClient] = None, bucket: Optional[str] = None) -> None:
        self.storage = storage_client or StorageClient(bucket or "")

    async def generate_protocol_report(self, job_id: str, data: Dict[str, Any]) -> ReportOutput:
        def _generate():
            # Placeholder: generate PDF, store it, return storage path
            path = f"reports/{job_id}/protocol.pdf"
            # save to storage (placeholder)
            self.storage.upload_blob(path, b"PDF-BYTES")
            return {"report_id": path, "url": f"gs://{path}"}

        res = await asyncio.to_thread(_generate)
        return ReportOutput(**res)

    async def generate_inspection_summary(self, job_id: str, data: Dict[str, Any]) -> ReportOutput:
        def _generate():
            # same as protocol but different naming
            path = f"reports/{job_id}/summary.pdf"
            self.storage.upload_blob(path, b"PDF-BYTES")
            return {"report_id": path, "url": f"gs://{path}"}

        res = await asyncio.to_thread(_generate)
        return ReportOutput(**res)
