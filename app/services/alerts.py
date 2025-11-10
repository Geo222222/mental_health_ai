"""
Utilities for persisting and querying risk assessment events.
"""

from __future__ import annotations

from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.risk import RiskEvent
from app.services.risk import RiskAssessment


async def log_risk_event(
    session: AsyncSession,
    *,
    user_id: str,
    source: str,
    content: str,
    assessment: RiskAssessment,
) -> RiskEvent:
    """Persist the latest risk evaluation for auditing and dashboards."""

    keywords = ",".join(assessment.keyword_hits) if assessment.keyword_hits else None
    event = RiskEvent(
        user_id=user_id,
        source=source,
        content=content,
        risk_level=assessment.level,
        risk_score=assessment.score,
        sentiment=assessment.sentiment,
        keywords=keywords,
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def list_risk_events(
    session: AsyncSession,
    *,
    minimum_level: Optional[str] = None,
    limit: int = 50,
) -> List[RiskEvent]:
    """Return recent risk events filtered by minimum risk level if provided."""

    query = select(RiskEvent).order_by(RiskEvent.created_at.desc()).limit(limit)
    if minimum_level:
        order = ["low", "moderate", "high"]
        level = minimum_level.lower()
        if level in order:
            threshold_index = order.index(level)
            allowed = set(order[threshold_index:])
            query = query.where(RiskEvent.risk_level.in_(allowed))
    result = await session.execute(query)
    return result.scalars().all()
