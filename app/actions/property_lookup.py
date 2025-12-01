# Folder: /app/actions
"""Property lookup via PropertyService.
"""
from typing import Any, Dict
import asyncio

from app.services.property_service import PropertyService
from app.utils.logging import get_logger

logger = get_logger(__name__)
property_service = PropertyService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        property_id = payload.get("property_id") or context.get("property_id")
        if not property_id:
            raise ValueError("property_id is required")
        result = await asyncio.to_thread(property_service.get_property, property_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("property_lookup failed: %s", e)
        return {"status": "error", "code": "PROPERTY_LOOKUP_FAILED", "message": str(e)}
