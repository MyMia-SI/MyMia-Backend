# Folder: /app/integrations
"""Weather client integration wrapper.
"""
from typing import Any, Dict


class WeatherClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        return {"forecast": "not implemented"}
