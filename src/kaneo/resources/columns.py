from __future__ import annotations


class ColumnsResource:
    def __init__(self, client):
        self._client = client

    def create(
        self,
        project_id: str,
        name: str,
        icon: str = "",
        color: str = "",
        is_final: bool = False,
    ) -> dict:
        """Create a new column in a project."""
        body: dict = {"name": name}
        if icon:
            body["icon"] = icon
        if color:
            body["color"] = color
        if is_final:
            body["isFinal"] = is_final
        return self._client._post(f"/column/{project_id}", body)

    def delete(self, column_id: str) -> dict:
        """Delete a column by ID."""
        return self._client._delete(f"/column/{column_id}")
