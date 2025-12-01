# Folder: /app
"""
FastAPI application entrypoint.
This is intentionally minimal for scaffolding; the real application logic belongs in orchestrator and services.
"""
from typing import Any
from time import perf_counter
import uuid

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except Exception:  # Keep import lightweight in case dependencies aren't installed in the scaffold
    FastAPI = Any  # type: ignore
    Request = Any  # type: ignore
    JSONResponse = dict  # type: ignore

from .orchestrator import Orchestrator
from .models.run_request import RunRequest
from .utils.logging import get_logger
from .utils.error_handling import OrchestratorError
from .services.auth_service import AuthService

logger = get_logger(__name__)

app = FastAPI(title="MyMia Backend - Orchestrator")


@app.on_event("startup")
async def create_orchestrator_on_startup() -> None:
    """Create the Orchestrator instance once on app startup and attach it to app.state.

    This ensures the orchestrator is reused across requests and avoids re-creating it per request.
    """
    # Create an orchestrator and auxiliary services once on startup
    app.state.auth_service = AuthService()
    app.state.orchestrator = Orchestrator()


@app.get("/")
async def root() -> dict:
    """Health check root endpoint."""
    return {"status": "ok", "service": "MyMia Backend Orchestrator"}


@app.post("/run")
async def run_workflow(payload: RunRequest, request: Request) -> dict:
    """Run a workflow via the orchestrator using a validated RunRequest.

    Returns a structured JSON response with consistent shape for both success and error cases.
    """
    start = perf_counter()
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    try:
        orchestrator = getattr(app.state, "orchestrator", None)
        if orchestrator is None:
            # This should not happen as orchestrator is created on startup - guard and create temporary instance.
            logger.warning("Orchestrator not initialized; creating temporary Orchestrator instance for request.")
            orchestrator = Orchestrator()
            app.state.orchestrator = orchestrator
        # If Authorization header present, validate token and attach user context
        auth_header = request.headers.get("Authorization")
        if auth_header and isinstance(auth_header, str) and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            try:
                auth_service: AuthService = getattr(app.state, "auth_service")
                user_info = await auth_service.get_user_info(token)
                # inject user_id / org_id into payload if not present
                payload_dict = payload.dict()
                payload_dict.setdefault("user_id", user_info.uid)
                if user_info.org_id:
                    payload_dict.setdefault("org_id", user_info.org_id)
            except Exception as e:
                logger.exception("Auth token validation failed: %s", e)
                content = {
                    "status": "error",
                    "code": "AUTH_INVALID",
                    "message": "Invalid or expired token",
                    "metadata": {"request_id": request_id, "duration_ms": 0},
                }
                return JSONResponse(status_code=401, content=content)
        else:
            payload_dict = payload.dict()

        result = await orchestrator.run_workflow(payload_dict)
        duration_ms = int((perf_counter() - start) * 1000)
        response = {
            "status": "success",
            "workflow": payload.workflow,
            "data": result,
            "metadata": {"request_id": request_id, "duration_ms": duration_ms},
        }
        return JSONResponse(status_code=200, content=response)

    except OrchestratorError as e:
        duration_ms = int((perf_counter() - start) * 1000)
        logger.exception("Workflow orchestration failed: %s", e)
        content = {
            "status": "error",
            "code": "WORKFLOW_EXECUTION_FAILURE",
            "message": str(e),
            "metadata": {"request_id": request_id, "duration_ms": duration_ms},
        }
        return JSONResponse(status_code=500, content=content)

    except Exception as e:
        duration_ms = int((perf_counter() - start) * 1000)
        logger.exception("Unexpected error running workflow: %s", e)
        content = {
            "status": "error",
            "code": "UNEXPECTED_ERROR",
            "message": "Unexpected server error",
            "metadata": {"request_id": request_id, "duration_ms": duration_ms},
        }
        return JSONResponse(status_code=500, content=content)
