"""Tests for the FastAPI metadata, health, readiness, and CORS behavior."""

from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings, get_settings
from app.main import create_app

SETTING_ENVIRONMENT_VARIABLES = (
    "APP_NAME",
    "APP_ENVIRONMENT",
    "APP_VERSION",
    "API_V1_PREFIX",
    "FRONTEND_ORIGIN",
    "CODESPACE_NAME",
    "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN",
    "LOG_LEVEL",
    "GROQ_API_KEY",
    "GROQ_MODEL",
    "SUPABASE_URL",
    "SUPABASE_PUBLISHABLE_KEY",
    "SUPABASE_SECRET_KEY",
    "DATABASE_URL",
)


@pytest.fixture(autouse=True)
def reset_test_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Prevent developer or CI environment values from changing API contracts."""
    for variable_name in SETTING_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def test_settings(reset_test_environment: None) -> Settings:
    """Provide deterministic settings without reading a backend env file."""
    return Settings(_env_file=None)


@pytest.fixture
async def client(test_settings: Settings) -> AsyncIterator[AsyncClient]:
    """Provide a test client for the configured application."""
    transport = ASGITransport(app=create_app(test_settings))
    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client


async def test_root_returns_public_api_metadata(client: AsyncClient) -> None:
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "TaskFlow RAG API",
        "version": "0.1.0",
        "documentation": "/docs",
    }


async def test_health_returns_public_liveness_data(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "taskflow-rag-api",
        "version": "0.1.0",
        "environment": "development",
    }


async def test_readiness_returns_api_only_check(client: AsyncClient) -> None:
    response = await client.get("/api/v1/readiness")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "phase": "project-foundation",
        "checks": {"api": "ok"},
    }


async def test_cors_permits_configured_frontend_origin(
    client: AsyncClient,
    test_settings: Settings,
) -> None:
    frontend_origin = test_settings.frontend_origin

    response = await client.options(
        "/api/v1/health",
        headers={
            "Origin": frontend_origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == frontend_origin
    assert response.headers["access-control-allow-credentials"] == "true"


def _response_keys(value: Any) -> set[str]:
    """Collect nested JSON object keys for security assertions."""
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested_value in value.values():
            keys.update(_response_keys(nested_value))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for nested_value in value:
            keys.update(_response_keys(nested_value))
        return keys
    return set()


async def test_public_responses_contain_no_secret_like_fields(client: AsyncClient) -> None:
    secret_markers = (
        "secret",
        "password",
        "token",
        "credential",
        "api_key",
        "database_url",
        "groq",
        "supabase",
    )
    response_keys: set[str] = set()

    for path in ("/", "/api/v1/health", "/api/v1/readiness"):
        response_keys.update(_response_keys((await client.get(path)).json()))

    assert all(
        marker not in field_name.lower()
        for field_name in response_keys
        for marker in secret_markers
    )
