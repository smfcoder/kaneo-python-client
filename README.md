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
