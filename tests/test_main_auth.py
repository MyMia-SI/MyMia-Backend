from fastapi.testclient import TestClient
from app.main import app


class DummyUser:
    def __init__(self, uid, org_id=None):
        self.uid = uid
        self.org_id = org_id


def test_run_workflow_with_auth(monkeypatch):
    client = TestClient(app)

    # Replace auth_service.get_user_info to return a dummy user
    class FakeAuthService:
        async def get_user_info(self, token):
            return DummyUser(uid="user-123", org_id="org-xyz")

    # replace existing auth service on app state
    app.state.auth_service = FakeAuthService()

    # make sure orchestrator runs a simple step that doesn't call external APIs
    orchestrator = app.state.orchestrator

    async def test_step(state, context):
        return {"status": "ok", "data": "ok", "state_update": {"hello": "world"}}

    orchestrator.step_registry["test_step"] = test_step
    orchestrator._router["test_auth_workflow"] = lambda ctx, state: ["test_step"]

    payload = {"workflow": "test_auth_workflow", "payload": {}}
    headers = {"Authorization": "Bearer faketoken"}
    response = client.post("/run", json=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["workflow"] == "test_auth_workflow"
    assert body["data"]["workflow"] == "test_auth_workflow"
    assert body["data"]["final_state"]["hello"] == "world"
