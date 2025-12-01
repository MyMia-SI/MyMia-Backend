# Folder: /app/services
"""PropertyService: property data (geocoding, metadata) using MapsClient and Firestore.
"""
from typing import Any, Dict, Optional
import asyncio
from pydantic import BaseModel

from app.integrations.maps_client import MapsClient
from app.integrations.firestore import FirestoreClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class PropertyInfo(BaseModel):
    id: str
    address: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    meta: Optional[Dict[str, Any]]


class PropertyService:
    def __init__(self, maps_client: Optional[MapsClient] = None, firestore_client: Optional[FirestoreClient] = None, api_key: Optional[str] = None, project_id: Optional[str] = None) -> None:
        self.maps = maps_client or MapsClient(api_key or "")
        self.firestore = firestore_client or FirestoreClient(project_id or "")

    async def geocode_address(self, address: str) -> PropertyInfo:
        def _geocode():
            res = self.maps.geocode(address)
            return {"address": address, "lat": res.get("lat"), "lon": res.get("lon"), "id": res.get("address")}

        res = await asyncio.to_thread(_geocode)
        return PropertyInfo(**{"id": str(res.get("id")), "address": res.get("address"), "lat": res.get("lat"), "lon": res.get("lon"), "meta": {}})

    async def get_property_info(self, property_id: str) -> PropertyInfo:
        def _get():
            doc = self.firestore.get_document(f"properties/{property_id}")
            data = doc.get("data", {})
            return {"id": property_id, "address": data.get("address"), "lat": data.get("lat"), "lon": data.get("lon"), "meta": data}

        res = await asyncio.to_thread(_get)
        return PropertyInfo(**res)

    async def get_distance(self, origin: Dict[str, float], destination: Dict[str, float]) -> Dict[str, Any]:
        def _distance():
            # This sample maps client doesn't compute distance; using geocode->distance placeholder
            return {"distance_meters": 0}

        return await asyncio.to_thread(_distance)
