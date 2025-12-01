# Folder: /app/actions
"""Generate a protocol report using ReportService.
"""
from typing import Any, Dict
STEP_NAME = "protocol"
import asyncio

from app.services.report_service import ReportService
from app.utils.logging import get_logger

logger = get_logger(__name__)
report_service = ReportService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        job_id = context.get("job_id") or payload.get("job_id")
        if not job_id:
            raise ValueError("job_id required to generate_report")
        # ReportService returns a ReportOutput pydantic model
        result = await report_service.generate_protocol_report(job_id, payload.get("data", {}))
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("generate_report failed: %s", e)
        return {"status": "error", "code": "GENERATE_REPORT_FAILED", "message": str(e)}
