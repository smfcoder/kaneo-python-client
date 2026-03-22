from pytest_httpx import HTTPXMock

from kaneo.models import Project

WORKSPACE_ID = "ws-123"

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
    "statistics": {"completionPercentage": 0, "totalTasks": 0, "dueDate": None},
    "archivedTasks": [],
    "plannedTasks": [],
    "columns": [],
}


def test_list_projects(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.kaneo.app/api/project?workspaceId={WORKSPACE_ID}",
        json=[PROJECT_DATA],
    )
    projects = client.projects.list(workspace_id=WORKSPACE_ID)
    assert len(projects) == 1
    assert isinstance(projects[0], Project)
    assert projects[0].name == "My Project"
    assert projects[0].slug == "MP"


def test_get_project(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.kaneo.app/api/project/proj-abc?workspaceId={WORKSPACE_ID}",
        json=PROJECT_DATA,
    )
    project = client.projects.get(project_id="proj-abc", workspace_id=WORKSPACE_ID)
    assert isinstance(project, Project)
    assert project.id == "proj-abc"


def test_create_project(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.kaneo.app/api/project", json=PROJECT_DATA
    )
    project = client.projects.create(
        workspace_id=WORKSPACE_ID, name="My Project", slug="MP", icon="Layout"
    )
    assert isinstance(project, Project)
    assert project.name == "My Project"


def test_delete_project(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.kaneo.app/api/project/proj-abc", json=PROJECT_DATA
    )
    deleted = client.projects.delete(project_id="proj-abc")
    assert deleted.id == "proj-abc"
