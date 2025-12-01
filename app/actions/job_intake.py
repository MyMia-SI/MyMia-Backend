# Folder: /app/actions
"""Job intake action: create or update a job via JobService.
"""
from typing import Any, Dict
import asyncio

from app.services.job_service import JobService
from app.utils.logging import get_logger

logger = get_logger(__name__)

job_service = JobService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = await job_service.create_job(payload)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("job_intake failed: %s", e)
        return {"status": "error", "code": "JOB_INTAKE_FAILED", "message": str(e)}
