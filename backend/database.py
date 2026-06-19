"""PostgreSQL pripojeni pro serverovy backend."""

from __future__ import annotations

from dataclasses import dataclass

from .config import BackendSettings


@dataclass(frozen=True)
class DatabaseHealth:
    configured: bool
    ok: bool
    detail: str


async def check_database(settings: BackendSettings) -> DatabaseHealth:
    if not settings.database_configured:
        return DatabaseHealth(
            configured=False,
            ok=False,
            detail="DATABASE_URL neni nastaveno.",
        )

    try:
        from sqlalchemy import text
        from sqlalchemy.ext.asyncio import create_async_engine
    except ImportError as exc:
        return DatabaseHealth(
            configured=True,
            ok=False,
            detail=f"Chybi databazova zavislost: {exc.name}.",
        )

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return DatabaseHealth(configured=True, ok=True, detail="PostgreSQL odpovida.")
    except Exception as exc:
        return DatabaseHealth(
            configured=True,
            ok=False,
            detail=f"PostgreSQL kontrola selhala: {exc}",
        )
    finally:
        await engine.dispose()

