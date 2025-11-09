"""
Reusable FastAPI dependencies.
"""
from __future__ import annotations

from app.core.database import get_session

get_async_session = get_session


