# Folder: /app
"""
Orchestrator: Single entry workflow engine.

Responsibilities implemented in this scaffold:
- Workflow routing based on `workflow` name
- Context extraction (user, job, org) from payload
- Deterministic step-by-step execution with deterministic state merging
- Basic error handling with `OrchestratorError` and structured step status
"""
from typing import Any, Dict, List, Optional, Callable
import logging
import time
from pathlib import Path
import importlib
import inspect
from types import ModuleType

from .utils.logging import get_logger
from .utils.error_handling import OrchestratorError
from .services.ai_service import AIService
from .services.job_service import JobService
from .services.report_service import ReportService
from .services.media_service import MediaService

logger = get_logger(__name__)


def _deterministic_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Merge nested dicts deterministically by iterating sorted keys.

    This prevents non-deterministic key order from producing inconsistent outputs.
    """
    result = dict(base)
    for key in sorted(update.keys()):
        value = update[key]
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deterministic_merge(result[key], value)
        else:
            result[key] = value
    return result


class Orchestrator:
    """Single entrypoint for workflows. Orchestrates AI reasoning + services.

    This scaffold is intentionally opinionated: it wires a few services, exposes a
    routing function for workflows, and executes a list of steps for each workflow.
    """

    def __init__(self, services: Optional[Dict[str, Any]] = None) -> None:
        services = services or {}
        self.ai_service: AIService = services.get("ai_service") or AIService()
        self.job_service: JobService = services.get("job_service") or JobService()
        self.report_service: ReportService = services.get("report_service") or ReportService()
        self.media_service: MediaService = services.get("media_service") or MediaService()

        # Router maps workflow name -> handler function
        self._router = {
            "mold_inspection": self._workflow_mold_inspection,
            "job_classifier": self._workflow_job_classifier,
        }
        # dynamic step registry maps step name -> callable
        self.step_registry: Dict[str, Callable[[Dict[str, Any], Dict[str, Any]], Any]] = {}
        # default aliases (step_name -> action module)
        self.step_aliases: Dict[str, str] = {
            "vision": "ai_mold_analysis",
            "moisture": "moisture_mapping",
            "protocol": "generate_report",
            "classify": "job_classifier",
        }
        self._load_step_registry()

    async def run_workflow(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow described in `payload`.

        Args:
            payload: Dict containing at minimum a `workflow` key and optional `payload`/context.

        Returns:
            A dict containing a deterministic merged state and per-step status.
        """
        workflow_name = payload.get("workflow")
        if not workflow_name or not isinstance(workflow_name, str):
            raise OrchestratorError("Missing or invalid `workflow` name in payload")

        logger.info("Routing workflow: %s", workflow_name)
        handler = self._router.get(workflow_name)
        if handler is None:
            raise OrchestratorError(f"Unknown workflow: {workflow_name}")

        # Build initial context and state
        context = self._extract_context(payload)
        state: Dict[str, Any] = payload.get("payload", {}) or {}
        state = _deterministic_merge({"_context": context}, state)
        steps_executed: List[Dict[str, Any]] = []
        last_step: Optional[str] = None

        try:
            steps = handler(context, state)
            # support async handlers that return steps
            if inspect.isawaitable(steps):
                steps = await steps
            for step in steps:
                step_name = step.get("name") if isinstance(step, dict) else str(step)
                last_step = step_name
                logger.info("Executing step: %s", step_name)
                start = time.perf_counter()
                step_result = await self._execute_step(step_name, state, context)
                duration_ms = int((time.perf_counter() - start) * 1000)
                # Merge outputs deterministically
                state = _deterministic_merge(state, step_result.get("state_update", {}))
                steps_executed.append(
                    {
                        "name": step_name,
                        "status": step_result.get("status", "ok"),
                        "output": step_result.get("output"),
                        "duration_ms": duration_ms,
                    }
                )

        except Exception as e:
            logger.exception("Workflow '%s' failed on step '%s': %s", workflow_name, last_step, e)
            raise OrchestratorError(f"Workflow execution failed: {e}") from e

        return {
            "workflow": workflow_name,
            "job_id": context.get("job_id"),
            "final_state": state,
            "steps_executed": len(steps_executed),
            "steps": steps_executed,
        }

    def _extract_context(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract execution context from payload.

        Context includes: user_id, job_id, org_id, request_id, etc. Defaults are None.
        """
        ctx = {
            "user_id": payload.get("user_id") or payload.get("user") or None,
            "job_id": payload.get("job_id") or payload.get("payload", {}).get("job_id"),
            "org_id": payload.get("org_id") or None,
        }
        return ctx

    async def _execute_step(self, step_name: str, state: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step and return a result that contains `status`, `output`, and optional `state_update`.

        This function centralizes try / except handling for step execution and returns a consistent structure.
        """
        try:
            # If a dynamic action handler is registered, call it.
            module_key = self.step_aliases.get(step_name, step_name)
            handler = self.step_registry.get(module_key)
            if handler:
                result = handler(state, context)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, dict):
                    # expect action result to be {status, data|output, state_update}
                    status = result.get("status", "ok")
                    output = result.get("data") or result.get("output")
                    state_update = result.get("state_update") or result.get("update") or {}
                    return {"status": status, "output": output, "state_update": state_update}
                else:
                    return {"status": "ok", "output": result, "state_update": {module_key: result}}

            # Fallback behavior (legacy simple implementations):
            if step_name == "vision":
                prompt = state.get("image_prompt") or "analyze image"
                ai_resp = await self.ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
                output = ai_resp.text
                return {"status": "ok", "output": output, "state_update": {"vision": output}}

            if step_name == "moisture":
                prompt = state.get("moisture_prompt") or "detect moisture"
                ai_resp = await self.ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
                output = ai_resp.text
                return {"status": "ok", "output": output, "state_update": {"moisture": output}}

            if step_name == "protocol":
                job_id = context.get("job_id") or state.get("job_id")
                output = await self.report_service.generate_protocol_report(job_id or "", state)
                return {"status": "ok", "output": output, "state_update": {"protocol_report": output}}

            if step_name == "classify":
                prompt = state.get("classify_prompt") or "classify job"
                ai_resp = await self.ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
                output = ai_resp.text
                return {"status": "ok", "output": output, "state_update": {"classification": output}}

            # Default: no-op step
            return {"status": "ok", "output": None, "state_update": {}}

        except Exception as e:\
            logger.exception("Step '%s' failed: %s", step_name, e)
            return {"status": "failed", "output": None, "state_update": {}}

    # Example workflow definitions (simple sequences). Real workflows would be configurable and stored.
    def _workflow_mold_inspection(self, context: Dict[str, Any], state: Dict[str, Any]) -> List[Dict[str, str]]:
        return ["vision", "moisture", "protocol"]

    def _workflow_job_classifier(self, context: Dict[str, Any], state: Dict[str, Any]) -> List[Dict[str, str]]:
        return ["classify"]

    def _load_step_registry(self) -> None:
        """Load action modules from `app.actions` and register their `handle` function.

        The registry will map module filename to the `handle` function. If a module exposes
        a `STEP_NAME` variable, the value is also used as the primary key.
        """
        base_pkg = "app.actions"
        package_dir = Path(__file__).parent / "actions"
        try:
            for file in package_dir.glob("*.py"):
                if file.name.startswith("__"):
                    continue
                module_name = f"{base_pkg}.{file.stem}"
                try:
                    module: ModuleType = importlib.import_module(module_name)
                    func = getattr(module, "handle", None) or getattr(module, "run", None)
                    if func and inspect.isfunction(func):
                        module_key = getattr(module, "STEP_NAME", file.stem)
                        self.step_registry[module_key] = func
                        # also register by file module name
                        self.step_registry[file.stem] = func
                        logger.debug("Registered action handler for %s -> %s", module_key, module_name)
                except Exception:
                    logger.exception("Error importing action module %s", module_name)
        except Exception as e:
            logger.exception("Failed to load step registry: %s", e)

