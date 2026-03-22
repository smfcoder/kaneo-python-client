import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

from kaneo import KaneoClient

mcp = FastMCP("kaneo")

# --- Client singleton ---

_client: Optional[KaneoClient] = None


def _get_client() -> KaneoClient:
    global _client
    if _client is None:
        _client = KaneoClient()
    return _client


def _get_workspace_id(workspace_id: Optional[str] = None) -> str:
    ws = workspace_id or os.environ.get("KANEO_WORKSPACE_ID")
    if not ws:
        raise ValueError("workspace_id is required. Pass it explicitly or set KANEO_WORKSPACE_ID.")
    return ws


# --- Config tools ---


@mcp.tool()
def get_config() -> dict:
    """Get Kaneo server configuration (SMTP, SSO providers, registration status)."""
    client = _get_client()
    cfg = client.config.get()
    return {
        "disable_registration": cfg.disable_registration,
        "is_demo_mode": cfg.is_demo_mode,
        "has_smtp": cfg.has_smtp,
        "has_github_sign_in": cfg.has_github_sign_in,
        "has_google_sign_in": cfg.has_google_sign_in,
        "has_discord_sign_in": cfg.has_discord_sign_in,
        "has_custom_oauth": cfg.has_custom_oauth,
        "has_guest_access": cfg.has_guest_access,
    }


# --- Project tools ---


@mcp.tool()
def list_projects(workspace_id: Optional[str] = None) -> list[dict]:
    """List all projects in a workspace.

    Args:
        workspace_id: Workspace ID. Uses KANEO_WORKSPACE_ID env var if not provided.
    """
    client = _get_client()
    ws = _get_workspace_id(workspace_id)
    projects = client.projects.list(workspace_id=ws)
    return [
        {
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "icon": p.icon,
            "is_public": p.is_public,
            "description": p.description,
            "created_at": p.created_at,
        }
        for p in projects
    ]


@mcp.tool()
def get_project(project_id: str, workspace_id: Optional[str] = None) -> dict:
    """Get a project by ID, including its tasks.

    Args:
        project_id: The project ID.
        workspace_id: Workspace ID. Uses KANEO_WORKSPACE_ID env var if not provided.
    """
    client = _get_client()
    ws = _get_workspace_id(workspace_id)
    p = client.projects.get(project_id=project_id, workspace_id=ws)
    return {
        "id": p.id,
        "name": p.name,
        "slug": p.slug,
        "icon": p.icon,
        "is_public": p.is_public,
        "description": p.description,
        "created_at": p.created_at,
        "tasks": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority} for t in p.tasks],
    }


@mcp.tool()
def create_project(
    name: str,
    slug: str,
    icon: str = "Layout",
    workspace_id: Optional[str] = None,
) -> dict:
    """Create a new project in a workspace.

    Args:
        name: Project name.
        slug: Short code (e.g. "KPC").
        icon: Icon name (default "Layout").
        workspace_id: Workspace ID. Uses KANEO_WORKSPACE_ID env var if not provided.
    """
    client = _get_client()
    ws = _get_workspace_id(workspace_id)
    p = client.projects.create(workspace_id=ws, name=name, slug=slug, icon=icon)
    return {"id": p.id, "name": p.name, "slug": p.slug}


@mcp.tool()
def delete_project(project_id: str) -> dict:
    """Delete a project by ID.

    Args:
        project_id: The project ID to delete.
    """
    client = _get_client()
    p = client.projects.delete(project_id=project_id)
    return {"id": p.id, "name": p.name, "deleted": True}


# --- Task tools ---


@mcp.tool()
def list_tasks(project_id: str) -> list[dict]:
    """List all tasks in a project (flattened from all columns).

    Args:
        project_id: The project ID.
    """
    client = _get_client()
    tasks = client.tasks.list(project_id)
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "description": t.description,
            "due_date": t.due_date,
            "created_at": t.created_at,
        }
        for t in tasks
    ]


@mcp.tool()
def get_task(task_id: str) -> dict:
    """Get a single task by ID.

    Args:
        task_id: The task ID.
    """
    client = _get_client()
    t = client.tasks.get(task_id)
    return {
        "id": t.id,
        "title": t.title,
        "status": t.status,
        "priority": t.priority,
        "description": t.description,
        "project_id": t.project_id,
        "due_date": t.due_date,
        "created_at": t.created_at,
    }


@mcp.tool()
def create_task(
    project_id: str,
    title: str,
    priority: str = "no-priority",
    status: str = "to-do",
    description: str = "",
    due_date: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """Create a new task in a project.

    Args:
        project_id: The project ID.
        title: Task title.
        priority: One of: no-priority, low, medium, high, urgent.
        status: One of: backlog, to-do, in-progress, done, cancelled.
        description: Task description (supports markdown).
        due_date: Due date string (e.g. "2026-12-31").
        user_id: Assignee user ID.
    """
    client = _get_client()
    t = client.tasks.create(
        project_id=project_id,
        title=title,
        priority=priority,
        status=status,
        description=description,
        due_date=due_date,
        user_id=user_id,
    )
    return {"id": t.id, "title": t.title, "status": t.status, "priority": t.priority}


@mcp.tool()
def delete_task(task_id: str) -> dict:
    """Delete a task by ID.

    Args:
        task_id: The task ID to delete.
    """
    client = _get_client()
    t = client.tasks.delete(task_id)
    return {"id": t.id, "title": t.title, "deleted": True}


@mcp.tool()
def update_task_status(task_id: str, status: str) -> dict:
    """Update the status of a task.

    Args:
        task_id: The task ID.
        status: New status. One of: backlog, to-do, in-progress, done, cancelled.
    """
    client = _get_client()
    t = client.tasks.update_status(task_id, status)
    return {"id": t.id, "title": t.title, "status": t.status}


@mcp.tool()
def update_task_priority(task_id: str, priority: str) -> dict:
    """Update the priority of a task.

    Args:
        task_id: The task ID.
        priority: New priority. One of: no-priority, low, medium, high, urgent.
    """
    client = _get_client()
    t = client.tasks.update_priority(task_id, priority)
    return {"id": t.id, "title": t.title, "priority": t.priority}


@mcp.tool()
def update_task_title(task_id: str, title: str) -> dict:
    """Update the title of a task.

    Args:
        task_id: The task ID.
        title: New title.
    """
    client = _get_client()
    t = client.tasks.update_title(task_id, title)
    return {"id": t.id, "title": t.title}


@mcp.tool()
def update_task_description(task_id: str, description: str) -> dict:
    """Update the description of a task.

    Args:
        task_id: The task ID.
        description: New description (supports markdown).
    """
    client = _get_client()
    t = client.tasks.update_description(task_id, description)
    return {"id": t.id, "title": t.title, "description": t.description}


# --- Column tools ---


@mcp.tool()
def create_column(
    project_id: str,
    name: str,
    icon: str = "",
    color: str = "",
    is_final: bool = False,
) -> dict:
    """Create a new column in a project.

    Args:
        project_id: The project ID.
        name: Column name (e.g. "In Review").
        icon: Optional icon name.
        color: Optional color hex code.
        is_final: Whether this column represents a "done" state.
    """
    client = _get_client()
    return client.columns.create(project_id=project_id, name=name, icon=icon, color=color, is_final=is_final)


@mcp.tool()
def delete_column(column_id: str) -> dict:
    """Delete a column by ID.

    Args:
        column_id: The column ID to delete.
    """
    client = _get_client()
    client.columns.delete(column_id)
    return {"id": column_id, "deleted": True}


# --- Entry point ---


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
