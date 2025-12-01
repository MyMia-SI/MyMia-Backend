# Folder: /app/actions
"""Weather risk assessment using WeatherService and AI for risk scoring.
"""
from typing import Any, Dict
import asyncio

from app.services.weather_service import WeatherService
from app.utils.logging import get_logger

logger = get_logger(__name__)
weather_service = WeatherService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        lat = payload.get("lat")
        lon = payload.get("lon")
        if lat is None or lon is None:
            raise ValueError("lat and lon are required")
        forecast = await asyncio.to_thread(weather_service.forecast, lat, lon)
        # placeholder risk assessment
        risk_score = "low"
        return {"status": "success", "data": {"forecast": forecast, "risk_score": risk_score}}
    except Exception as e:
        logger.exception("weather_risk_assessment failed: %s", e)
        return {"status": "error", "code": "WEATHER_RISK_FAILED", "message": str(e)}
