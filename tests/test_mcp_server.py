import pytest
from pytest_httpx import HTTPXMock
from kaneo import KaneoClient

from kaneo.mcp.server import (
    _get_workspace_id,
    get_config,
    list_projects,
    get_project,
    create_project,
    delete_project,
    list_tasks,
    get_task,
    create_task,
    delete_task,
    update_task_status,
    update_task_priority,
    update_task_title,
    update_task_description,
    create_column,
    delete_column,
)
import kaneo.mcp.server as server_module

BASE_URL = "https://cloud.kaneo.app/api"
TOKEN = "test-token"
WORKSPACE_ID = "ws-123"

CONFIG_RESPONSE = {
    "disableRegistration": False,
    "isDemoMode": False,
    "hasSmtp": True,
    "hasGithubSignIn": True,
    "hasGoogleSignIn": False,
    "hasDiscordSignIn": False,
    "hasCustomOAuth": False,
    "hasGuestAccess": True,
}

PROJECT_DATA = {
    "id": "proj-abc",
    "workspaceId": WORKSPACE_ID,
    "name": "My Project",
    "slug": "MP",
    "icon": "Layout",
    "isPublic": False,
    "description": None,
    "createdAt": "2026-01-01T00:00:00.000Z",
    "tasks": [],
}

TASK_DATA = {
    "id": "task-xyz",
    "projectId": "proj-abc",
    "title": "Fix the bug",
    "description": "Details here",
    "status": "to-do",
    "priority": "high",
    "position": 1,
    "number": 1,
    "columnId": None,
    "userId": None,
    "dueDate": None,
    "createdAt": "2026-01-01T00:00:00.000Z",
}


@pytest.fixture(autouse=True)
def reset_client():
    """Reset singleton client before each test."""
    server_module._client = None
    yield
    server_module._client = None


@pytest.fixture
def mock_client(httpx_mock: HTTPXMock):
    """Provide a real KaneoClient with mocked HTTP."""
    client = KaneoClient(token=TOKEN, base_url=BASE_URL)
    server_module._client = client
    return httpx_mock


# --- Workspace ID resolution ---


def test_workspace_id_from_arg():
    assert _get_workspace_id("ws-explicit") == "ws-explicit"


def test_workspace_id_from_env(monkeypatch):
    monkeypatch.setenv("KANEO_WORKSPACE_ID", "ws-env")
    assert _get_workspace_id() == "ws-env"


def test_workspace_id_missing_raises(monkeypatch):
    monkeypatch.delenv("KANEO_WORKSPACE_ID", raising=False)
    with pytest.raises(ValueError, match="KANEO_WORKSPACE_ID"):
        _get_workspace_id()


# --- Config ---


def test_get_config(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/config", json=CONFIG_RESPONSE)
    result = get_config()
    assert result["has_smtp"] is True
    assert result["has_google_sign_in"] is False


# --- Projects ---


def test_list_projects(mock_client, monkeypatch):
    monkeypatch.setenv("KANEO_WORKSPACE_ID", WORKSPACE_ID)
    mock_client.add_response(
        url=f"{BASE_URL}/project?workspaceId={WORKSPACE_ID}", json=[PROJECT_DATA]
    )
    result = list_projects()
    assert len(result) == 1
    assert result[0]["name"] == "My Project"


def test_get_project(mock_client, monkeypatch):
    monkeypatch.setenv("KANEO_WORKSPACE_ID", WORKSPACE_ID)
    mock_client.add_response(
        url=f"{BASE_URL}/project/proj-abc?workspaceId={WORKSPACE_ID}",
        json=PROJECT_DATA,
    )
    result = get_project("proj-abc")
    assert result["id"] == "proj-abc"
    assert result["name"] == "My Project"


def test_create_project(mock_client, monkeypatch):
    monkeypatch.setenv("KANEO_WORKSPACE_ID", WORKSPACE_ID)
    mock_client.add_response(url=f"{BASE_URL}/project", json=PROJECT_DATA)
    result = create_project(name="My Project", slug="MP")
    assert result["id"] == "proj-abc"


def test_delete_project(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/project/proj-abc", json=PROJECT_DATA)
    result = delete_project("proj-abc")
    assert result["deleted"] is True


# --- Tasks ---


def test_list_tasks(mock_client):
    mock_client.add_response(
        url=f"{BASE_URL}/task/tasks/proj-abc",
        json={
            "columns": [
                {"id": "to-do", "name": "To Do", "tasks": [TASK_DATA]},
                {"id": "done", "name": "Done", "tasks": []},
            ]
        },
    )
    result = list_tasks("proj-abc")
    assert len(result) == 1
    assert result[0]["title"] == "Fix the bug"


def test_get_task(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=TASK_DATA)
    result = get_task("task-xyz")
    assert result["id"] == "task-xyz"
    assert result["priority"] == "high"


def test_create_task(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/task/proj-abc", json=TASK_DATA)
    result = create_task(project_id="proj-abc", title="Fix the bug", priority="high")
    assert result["id"] == "task-xyz"


def test_delete_task(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=TASK_DATA)
    result = delete_task("task-xyz")
    assert result["deleted"] is True


def test_update_task_status(mock_client):
    updated = {**TASK_DATA, "status": "in-progress"}
    mock_client.add_response(url=f"{BASE_URL}/task/status/task-xyz", json=TASK_DATA)
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=updated)
    result = update_task_status("task-xyz", "in-progress")
    assert result["status"] == "in-progress"


def test_update_task_priority(mock_client):
    updated = {**TASK_DATA, "priority": "urgent"}
    mock_client.add_response(url=f"{BASE_URL}/task/priority/task-xyz", json=TASK_DATA)
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=updated)
    result = update_task_priority("task-xyz", "urgent")
    assert result["priority"] == "urgent"


def test_update_task_title(mock_client):
    updated = {**TASK_DATA, "title": "New title"}
    mock_client.add_response(url=f"{BASE_URL}/task/title/task-xyz", json=TASK_DATA)
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=updated)
    result = update_task_title("task-xyz", "New title")
    assert result["title"] == "New title"


def test_update_task_description(mock_client):
    updated = {**TASK_DATA, "description": "New desc"}
    mock_client.add_response(
        url=f"{BASE_URL}/task/description/task-xyz", json=TASK_DATA
    )
    mock_client.add_response(url=f"{BASE_URL}/task/task-xyz", json=updated)
    result = update_task_description("task-xyz", "New desc")
    assert result["description"] == "New desc"


# --- Columns ---


def test_create_column(mock_client):
    mock_client.add_response(
        url=f"{BASE_URL}/column/proj-abc",
        json={"id": "col-new", "name": "Review"},
    )
    result = create_column(project_id="proj-abc", name="Review")
    assert result["name"] == "Review"


def test_delete_column(mock_client):
    mock_client.add_response(url=f"{BASE_URL}/column/col-123", json={})
    result = delete_column("col-123")
    assert result["deleted"] is True
