# Folder: /app/actions
"""Job classifier action: use AIService to classify job type."""
from typing import Any, Dict
STEP_NAME = "classify"
import asyncio

from app.services.ai_service import AIService
from app.utils.logging import get_logger

logger = get_logger(__name__)
ai_service = AIService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        prompt = payload.get("prompt") or "Classify this job"
            ai_resp = await ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
            result = ai_resp.text
        return {"status": "success", "data": {"classification": result}}
    except Exception as e:
        logger.exception("job_classifier failed: %s", e)
        return {"status": "error", "code": "JOB_CLASSIFIER_FAILED", "message": str(e)}
