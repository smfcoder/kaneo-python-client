from pytest_httpx import HTTPXMock

PROJECT_ID = "proj-abc"


def test_create_column(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"https://cloud.kaneo.app/api/column/{PROJECT_ID}", json={})
    result = client.columns.create(project_id=PROJECT_ID, name="In Review")
    assert result == {}


def test_delete_column(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://cloud.kaneo.app/api/column/col-123", json={})
    result = client.columns.delete(column_id="col-123")
    assert result == {}
