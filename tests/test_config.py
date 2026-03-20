from pytest_httpx import HTTPXMock
from kaneo.models import Config

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


def test_get_config(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://cloud.kaneo.app/api/config", json=CONFIG_RESPONSE)
    cfg = client.config.get()
    assert isinstance(cfg, Config)
    assert cfg.has_smtp is True
    assert cfg.has_github_sign_in is True
    assert cfg.has_google_sign_in is False
