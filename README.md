# kaneo

Python client for the [Kaneo](https://kaneo.app) project management API.

## Installation

```bash
pip install kaneo
```

## Quick Start

```python
from kaneo import KaneoClient

# Token and base URL are read from environment variables by default:
#   KANEO_TOKEN    — required
#   KANEO_BASE_URL — optional (defaults to https://cloud.kaneo.app/api)
client = KaneoClient()

# Or pass them explicitly:
client = KaneoClient(token="your-api-token")

# List projects
projects = client.projects.list(workspace_id="your-workspace-id")
for p in projects:
    print(p.name)

# Create a task
task = client.tasks.create(
    project_id="your-project-id",
    title="Fix the login bug",
    priority="high",
    status="to-do",
)
print(task.id)

# Update task status
client.tasks.update_status(task.id, "in-progress")
```

## Self-hosted Kaneo

```bash
export KANEO_TOKEN=your-token
export KANEO_BASE_URL=https://kaneo.yourdomain.com/api
```

Or explicitly:

```python
client = KaneoClient(
    token="your-token",
    base_url="https://kaneo.yourdomain.com/api",
)
```

## Resources

| Resource | Methods |
|----------|---------|
| `client.projects` | `list(workspace_id)`, `get(project_id, workspace_id)`, `create(...)`, `delete(project_id)` |
| `client.tasks` | `list(project_id)`, `get(id)`, `create(...)`, `delete(id)`, `update_status(id, status)`, `update_priority(id, priority)`, `update_title(id, title)`, `update_description(id, desc)` |
| `client.columns` | `create(project_id, name, ...)`, `delete(column_id)` |
| `client.config` | `get()` |

## MCP Server (for AI agents)

The package includes an MCP server that lets AI tools (Claude Code, Cursor, Windsurf, etc.) manage your Kaneo projects and tasks.

### Install

```bash
pip install kaneo[mcp]
```

### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "kaneo": {
      "command": "kaneo-mcp",
      "env": {
        "KANEO_TOKEN": "your-api-token",
        "KANEO_WORKSPACE_ID": "your-workspace-id"
      }
    }
  }
}
```

For self-hosted Kaneo, add `KANEO_BASE_URL`:

```json
{
  "mcpServers": {
    "kaneo": {
      "command": "kaneo-mcp",
      "env": {
        "KANEO_TOKEN": "your-api-token",
        "KANEO_WORKSPACE_ID": "your-workspace-id",
        "KANEO_BASE_URL": "https://kaneo.yourdomain.com/api"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "kaneo": {
      "command": "kaneo-mcp",
      "env": {
        "KANEO_TOKEN": "your-api-token",
        "KANEO_WORKSPACE_ID": "your-workspace-id"
      }
    }
  }
}
```

### Available Tools

| Tool | Description |
|------|-------------|
| `get_config` | Get Kaneo server configuration |
| `list_projects` | List all projects in workspace |
| `get_project` | Get project details with tasks |
| `create_project` | Create a new project |
| `delete_project` | Delete a project |
| `list_tasks` | List all tasks in a project |
| `get_task` | Get a single task |
| `create_task` | Create a task with title, priority, status, description |
| `delete_task` | Delete a task |
| `update_task_status` | Change task status (backlog/to-do/in-progress/done/cancelled) |
| `update_task_priority` | Change task priority (no-priority/low/medium/high/urgent) |
| `update_task_title` | Change task title |
| `update_task_description` | Change task description |
| `create_column` | Create a board column |
| `delete_column` | Delete a board column |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `KANEO_TOKEN` | Yes | Your Kaneo API token |
| `KANEO_BASE_URL` | No | API URL (default: `https://cloud.kaneo.app/api`) |
| `KANEO_WORKSPACE_ID` | No | Default workspace ID |

## Exceptions

| Exception | Trigger |
|-----------|---------|
| `AuthError` | 401 — invalid or missing token |
| `NotFoundError` | 404 — resource not found |
| `ValidationError` | 400 — bad request / invalid input |
| `ServerError` | 5xx — server-side error |
| `KaneoError` | Base class for all exceptions |

## License

MIT
