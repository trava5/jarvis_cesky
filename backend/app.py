"""FastAPI aplikace pro JARVIS backend."""

from __future__ import annotations

from fastapi import FastAPI

from .api import create_api_router
from .config import load_settings


def create_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Serverovy backend pro viceklientskou architekturu JARVIS.",
    )
    app.include_router(create_api_router(settings))
    return app


app = create_app()

