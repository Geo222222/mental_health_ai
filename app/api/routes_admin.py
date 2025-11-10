"""
Clinician/admin oriented endpoints.
"""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_async_session
from app.models.schemas import JournalEntryRead, RiskEventRead
from app.services.alerts import list_risk_events
from app.services.journal import list_high_risk_entries


router = APIRouter(prefix="/admin", tags=["admin"])


# Provide clinicians with the latest high-risk journal entries for manual follow-up.
@router.get("/alerts", response_model=List[JournalEntryRead])
async def high_risk_alerts(
    threshold: float = 0.6, session: AsyncSession = Depends(get_async_session)
) -> List[JournalEntryRead]:
    """
    Return journal entries that exceed the configured risk threshold.
    """
    entries = await list_high_risk_entries(session, threshold=threshold)
    return [JournalEntryRead.model_validate(entry.model_dump()) for entry in entries]


# List recent risk assessments captured across chat and journaling.
@router.get("/risk-events", response_model=List[RiskEventRead])
async def get_risk_events(
    minimum_level: Optional[str] = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_async_session),
) -> List[RiskEventRead]:
    events = await list_risk_events(
        session,
        minimum_level=minimum_level,
        limit=limit,
    )
    return [RiskEventRead.model_validate(event.model_dump()) for event in events]


