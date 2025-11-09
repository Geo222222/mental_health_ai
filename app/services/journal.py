"""
Data access helpers for journaling.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.journal import Goal, JournalEntry, MoodLog


async def create_journal_entry(
    session: AsyncSession,
    *,
    user_id: str,
    title: str,
    content: str,
    tags: Optional[str],
    risk_score: float,
) -> JournalEntry:
    entry = JournalEntry(
        user_id=user_id,
        title=title,
        content=content,
        tags=tags,
        risk_score=risk_score,
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def list_journal_entries(session: AsyncSession, user_id: str) -> List[JournalEntry]:
    result = await session.execute(
        select(JournalEntry).where(JournalEntry.user_id == user_id).order_by(JournalEntry.created_at.desc())
    )
    return result.scalars().all()


async def log_mood(
    session: AsyncSession, *, user_id: str, mood: str, intensity: int, notes: Optional[str]
) -> MoodLog:
    record = MoodLog(user_id=user_id, mood=mood, intensity=intensity, notes=notes)
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def list_moods(session: AsyncSession, user_id: str) -> List[MoodLog]:
    result = await session.execute(
        select(MoodLog).where(MoodLog.user_id == user_id).order_by(MoodLog.created_at.desc())
    )
    return result.scalars().all()


async def upsert_goal(
    session: AsyncSession,
    *,
    user_id: str,
    description: str,
    status: str,
    target_date: Optional[datetime],
) -> Goal:
    result = await session.execute(
        select(Goal).where(Goal.user_id == user_id, Goal.description == description)
    )
    goal = result.scalar_one_or_none()
    if goal is None:
        goal = Goal(
            user_id=user_id,
            description=description,
            status=status,
            target_date=target_date,
        )
        session.add(goal)
    else:
        goal.status = status
        goal.target_date = target_date
        goal.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(goal)
    return goal


async def list_goals(session: AsyncSession, user_id: str) -> List[Goal]:
    result = await session.execute(select(Goal).where(Goal.user_id == user_id))
    return result.scalars().all()


async def list_high_risk_entries(
    session: AsyncSession, *, threshold: float = 0.6
) -> List[JournalEntry]:
    result = await session.execute(
        select(JournalEntry)
        .where(JournalEntry.risk_score >= threshold)
        .order_by(JournalEntry.created_at.desc())
    )
    return result.scalars().all()

