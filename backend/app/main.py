"""FastAPI application entry point for the TaskFlow backend."""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.schemas.health import RootResponse


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a FastAPI application from explicit or environment-backed settings."""
    app_settings = settings or get_settings()
    application = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[app_settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    if settings is not None:

        async def provide_settings() -> Settings:
            return app_settings

        application.dependency_overrides[get_settings] = provide_settings

    application.include_router(api_router, prefix=app_settings.api_v1_prefix)

    @application.get(
        "/",
        response_model=RootResponse,
        status_code=status.HTTP_200_OK,
        tags=["Metadata"],
        summary="Get API metadata",
    )
    async def root() -> RootResponse:
        """Return public API metadata and the interactive documentation path."""
        return RootResponse(
            name=app_settings.app_name,
            version=app_settings.app_version,
            documentation="/docs",
        )

    return application


app = create_app()
