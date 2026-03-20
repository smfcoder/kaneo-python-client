from __future__ import annotations

from kaneo.models.config import Config


class ConfigResource:
    def __init__(self, client):
        self._client = client

    def get(self) -> Config:
        """Get application configuration."""
        data = self._client._get("/config")
        return Config.from_dict(data)
