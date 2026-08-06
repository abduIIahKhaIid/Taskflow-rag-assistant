"""Tests for typed backend configuration."""

from pathlib import Path

import pytest

from app.core.config import Settings, get_settings

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
def reset_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate settings tests from the host environment and cache."""
    for variable_name in SETTING_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)
    get_settings.cache_clear()


def test_defaults_do_not_require_external_credentials() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "TaskFlow RAG API"
    assert settings.app_environment == "development"
    assert settings.app_version == "0.1.0"
    assert settings.api_v1_prefix == "/api/v1"
    assert settings.frontend_origin == "http://localhost:3000"
    assert settings.log_level == "INFO"
    assert settings.groq_api_key is None
    assert settings.groq_model is None
    assert settings.supabase_url is None
    assert settings.supabase_publishable_key is None
    assert settings.supabase_secret_key is None
    assert settings.database_url is None


def test_backend_dotenv_path_is_configured() -> None:
    configured_path = Settings.model_config["env_file"]

    assert Path(configured_path) == Path(__file__).resolve().parents[1] / ".env"


def test_codespaces_origin_is_derived_from_host_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CODESPACE_NAME", "example-space")
    monkeypatch.setenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")

    settings = Settings(_env_file=None)

    assert settings.frontend_origin == "https://example-space-3000.app.github.dev"


def test_explicit_frontend_origin_overrides_codespaces_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CODESPACE_NAME", "example-space")
    monkeypatch.setenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")
    monkeypatch.setenv("FRONTEND_ORIGIN", "https://frontend.example.test")

    settings = Settings(_env_file=None)

    assert settings.frontend_origin == "https://frontend.example.test"


def test_dotenv_values_load_and_unknown_values_are_ignored(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=Configured TaskFlow API\n"
        "GROQ_API_KEY=test-placeholder-groq-key\n"
        "SUPABASE_URL=https://example.invalid\n"
        "UNKNOWN_SETTING=ignored\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.app_name == "Configured TaskFlow API"
    assert settings.groq_api_key is not None
    assert settings.groq_api_key.get_secret_value() == "test-placeholder-groq-key"
    assert str(settings.supabase_url) == "https://example.invalid/"


def test_empty_external_service_values_are_ignored(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GROQ_API_KEY=\n"
        "GROQ_MODEL=\n"
        "SUPABASE_URL=\n"
        "SUPABASE_PUBLISHABLE_KEY=\n"
        "SUPABASE_SECRET_KEY=\n"
        "DATABASE_URL=\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.groq_api_key is None
    assert settings.groq_model is None
    assert settings.supabase_url is None
    assert settings.supabase_publishable_key is None
    assert settings.supabase_secret_key is None
    assert settings.database_url is None


def test_secret_values_are_masked_in_representations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secret_value = "test-placeholder-secret-value"
    monkeypatch.setenv("SUPABASE_SECRET_KEY", secret_value)

    settings = Settings(_env_file=None)

    assert secret_value not in repr(settings)
    assert secret_value not in settings.model_dump_json()
    assert "**********" in repr(settings)
    assert "**********" in settings.model_dump_json()


def test_get_settings_returns_cached_instance() -> None:
    assert get_settings() is get_settings()
