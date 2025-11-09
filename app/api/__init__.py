"""
API router aggregation.
"""
from __future__ import annotations

from fastapi import APIRouter

from .routes_admin import router as admin_router
from .routes_chat import router as chat_router
from .routes_journal import router as journal_router


api_router = APIRouter()
api_router.include_router(chat_router)
api_router.include_router(journal_router)
api_router.include_router(admin_router)


