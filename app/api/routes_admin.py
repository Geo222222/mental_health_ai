"""
Clinician/admin oriented endpoints.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_async_session
from app.models.schemas import JournalEntryRead
from app.services.journal import list_high_risk_entries


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/alerts", response_model=List[JournalEntryRead])
async def high_risk_alerts(
    threshold: float = 0.6, session: AsyncSession = Depends(get_async_session)
) -> List[JournalEntryRead]:
    """
    Return journal entries that exceed the configured risk threshold.
    """
    entries = await list_high_risk_entries(session, threshold=threshold)
    return [JournalEntryRead.model_validate(entry.model_dump()) for entry in entries]


