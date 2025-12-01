import asyncio

from app.orchestrator import Orchestrator


async def test_dynamic_step_registry_and_execution():
    orchestrator = Orchestrator()

    # register a simple test step
    async def test_step(state, context):
        return {"status": "ok", "data": "hello", "state_update": {"greet": "hi"}}

    orchestrator.step_registry["test_step"] = test_step
    orchestrator._router["test_workflow"] = lambda ctx, state: ["test_step"]

    payload = {"workflow": "test_workflow", "payload": {"foo": "bar"}}
    result = await orchestrator.run_workflow(payload)

    assert result["workflow"] == "test_workflow"
    assert result["final_state"].get("greet") == "hi"
    assert result["steps_executed"] == 1
