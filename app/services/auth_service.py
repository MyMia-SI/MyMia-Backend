# Folder: /app/services
"""AuthService: wrapper for Firebase Auth integration.

This service validates tokens and resolves user / org identities.
"""
from typing import Any, Dict, Optional
import asyncio
from pydantic import BaseModel

from app.integrations.firebase_auth import FirebaseAuthClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class UserInfo(BaseModel):
    uid: str
    email: Optional[str]
    name: Optional[str]
    org_id: Optional[str]


class AuthService:
    def __init__(self, client: Optional[FirebaseAuthClient] = None, project_id: Optional[str] = None) -> None:
        self.client = client or FirebaseAuthClient(project_id or "")

    async def verify_token(self, token: str) -> Dict[str, Any]:
        def _verify():
            return self.client.verify_token(token)

        return await asyncio.to_thread(_verify)

    async def get_user_info(self, token: str) -> UserInfo:
        raw = await self.verify_token(token)
        return UserInfo(uid=raw.get("uid"), email=raw.get("email"), name=raw.get("name"), org_id=raw.get("org_id"))

    async def get_org_id(self, token: str) -> Optional[str]:
        user = await self.get_user_info(token)
        return user.org_id

