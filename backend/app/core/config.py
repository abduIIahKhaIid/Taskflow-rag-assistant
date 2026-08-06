"""Typed application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import AnyHttpUrl, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Runtime settings for the TaskFlow RAG API foundation."""

    app_name: str = "TaskFlow RAG API"
    app_environment: str = "development"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    frontend_origin: str = "http://localhost:3000"
    log_level: str = "INFO"

    codespace_name: str | None = None
    github_codespaces_port_forwarding_domain: str | None = None

    groq_api_key: SecretStr | None = None
    groq_model: str | None = None

    supabase_url: AnyHttpUrl | None = None
    supabase_publishable_key: SecretStr | None = None
    supabase_secret_key: SecretStr | None = None
    database_url: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=_BACKEND_DIRECTORY / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    @model_validator(mode="after")
    def use_codespaces_frontend_origin(self) -> Self:
        """Use the forwarded frontend origin when Codespaces provides its host metadata."""
        if (
            self.frontend_origin == "http://localhost:3000"
            and self.codespace_name
            and self.github_codespaces_port_forwarding_domain
        ):
            self.frontend_origin = (
                f"https://{self.codespace_name}-3000."
                f"{self.github_codespaces_port_forwarding_domain}"
            )
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
