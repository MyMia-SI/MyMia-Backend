# Folder: /app/actions
"""Media upload action: store upload via MediaService.
"""
from typing import Any, Dict
import asyncio

from app.services.media_service import MediaService
from app.utils.logging import get_logger

logger = get_logger(__name__)
media_service = MediaService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Expected payload contains `file_path` or `data` placeholder for upload."""
    try:
        file_path = payload.get("file_path")
        if not file_path:
            raise ValueError("file_path required")
        result = await asyncio.to_thread(media_service.upload, file_path)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("media_upload failed: %s", e)
        return {"status": "error", "code": "MEDIA_UPLOAD_FAILED", "message": str(e)}
