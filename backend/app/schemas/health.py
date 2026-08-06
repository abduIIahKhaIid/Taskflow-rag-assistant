"""Response schemas for API metadata and service health endpoints."""

from typing import Literal

from pydantic import BaseModel


class RootResponse(BaseModel):
    """Public metadata returned by the API root endpoint."""

    name: str
    version: str
    documentation: str


class HealthResponse(BaseModel):
    """Public liveness information for the API service."""

    status: Literal["ok"]
    service: Literal["taskflow-rag-api"]
    version: str
    environment: str


class ReadinessChecks(BaseModel):
    """Phase 2 readiness checks that do not require external services."""

    api: Literal["ok"]


class ReadinessResponse(BaseModel):
    """Public readiness information for the API service."""

    status: Literal["ready"]
    phase: Literal["project-foundation"]
    checks: ReadinessChecks
