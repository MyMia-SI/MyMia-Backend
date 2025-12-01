# Folder: /app/services
"""WeatherService: fetch weather and compute mold risk index using WeatherClient.
"""
from typing import Any, Dict, Optional
import asyncio
from pydantic import BaseModel

from app.integrations.weather_client import WeatherClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class WeatherData(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    raw: Optional[Dict[str, Any]]


class WeatherService:
    def __init__(self, client: Optional[WeatherClient] = None, api_key: Optional[str] = None) -> None:
        self.client = client or WeatherClient(api_key or "")

    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        def _get():
            return self.client.forecast(lat, lon)

        raw = await asyncio.to_thread(_get)
        # Placeholder mapping
        return WeatherData(temperature=raw.get("temp"), humidity=raw.get("humidity"), raw=raw)

    async def get_mold_risk(self, lat: float, lon: float) -> Dict[str, Any]:
        weather = await self.get_weather(lat, lon)
        # Simple heuristic for mold risk, deterministic
        humidity = (weather.humidity or 0)
        temp = (weather.temperature or 0)
        risk_score = "low"
        if humidity > 70 and temp > 18:
            risk_score = "high"
        elif humidity > 55:
            risk_score = "moderate"
        return {"risk": risk_score, "humidity": humidity, "temperature": temp}
