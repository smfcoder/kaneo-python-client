class KaneoError(Exception):
    """Base exception for all kaneo errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthError(KaneoError):
    """401 — invalid or missing token."""


class NotFoundError(KaneoError):
    """404 — resource not found."""


class ValidationError(KaneoError):
    """400 — bad request / invalid input."""


class ServerError(KaneoError):
    """5xx — server-side error."""
