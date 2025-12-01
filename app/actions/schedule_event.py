# Folder: /app/actions
"""Event scheduling via SchedulingService.
"""
from typing import Any, Dict
import asyncio

from app.services.scheduling_service import SchedulingService
from app.utils.logging import get_logger

logger = get_logger(__name__)

scheduling_service = SchedulingService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        job_id = payload.get("job_id") or context.get("job_id")
        time_iso = payload.get("time") or payload.get("time_iso")
        if not job_id or not time_iso:
            raise ValueError("job_id and time are required")
        result = await asyncio.to_thread(scheduling_service.schedule_visit, job_id, time_iso)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("schedule_event failed: %s", e)
        return {"status": "error", "code": "SCHEDULE_EVENT_FAILED", "message": str(e)}
