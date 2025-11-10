"""
Database configuration using SQLModel with async support.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .config import get_settings

# Import models so metadata is populated when create_all is executed
from app.models import journal as _journal_models  # noqa: F401
from app.models import risk as _risk_models  # noqa: F401


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, future=True)


async def init_db() -> None:
    """
    Initialize database tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that yields an async session.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


