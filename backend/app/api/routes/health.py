"""Health and readiness routes for the TaskFlow API foundation."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse, ReadinessChecks, ReadinessResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API health",
)
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Return public liveness metadata without exposing configuration secrets."""
    return HealthResponse(
        status="ok",
        service="taskflow-rag-api",
        version=settings.app_version,
        environment=settings.app_environment,
    )


@router.get(
    "/readiness",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API readiness",
)
async def readiness() -> ReadinessResponse:
    """Report Phase 2 readiness without checking future external services."""
    return ReadinessResponse(
        status="ready",
        phase="project-foundation",
        checks=ReadinessChecks(api="ok"),
    )
