"""
Endpoints for journaling, mood logging, and goals.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_async_session
from app.models.schemas import (
    GoalRead,
    GoalUpsert,
    JournalEntryCreate,
    JournalEntryRead,
    MoodLogCreate,
    MoodLogRead,
)
from app.services.journal import (
    create_journal_entry,
    list_goals,
    list_journal_entries,
    list_moods,
    log_mood,
    upsert_goal,
)
from app.services.risk import assess_risk


router = APIRouter(prefix="/journal", tags=["journal"])


@router.post("", response_model=JournalEntryRead)
async def create_entry(
    payload: JournalEntryCreate, session: AsyncSession = Depends(get_async_session)
) -> JournalEntryRead:
    risk = assess_risk(payload.content)
    entry = await create_journal_entry(
        session,
        user_id=payload.user_id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        risk_score=risk.score,
    )
    return JournalEntryRead.model_validate(entry.model_dump())


@router.get("/{user_id}", response_model=List[JournalEntryRead])
async def list_entries(
    user_id: str, session: AsyncSession = Depends(get_async_session)
) -> List[JournalEntryRead]:
    entries = await list_journal_entries(session, user_id)
    return [JournalEntryRead.model_validate(entry.model_dump()) for entry in entries]


@router.post("/mood", response_model=MoodLogRead)
async def log_mood_endpoint(
    payload: MoodLogCreate, session: AsyncSession = Depends(get_async_session)
) -> MoodLogRead:
    record = await log_mood(
        session,
        user_id=payload.user_id,
        mood=payload.mood,
        intensity=payload.intensity,
        notes=payload.notes,
    )
    return MoodLogRead.model_validate(record.model_dump())


@router.get("/mood/{user_id}", response_model=List[MoodLogRead])
async def list_mood_endpoint(
    user_id: str, session: AsyncSession = Depends(get_async_session)
) -> List[MoodLogRead]:
    records = await list_moods(session, user_id)
    return [MoodLogRead.model_validate(record.model_dump()) for record in records]


@router.post("/goals", response_model=GoalRead)
async def upsert_goal_endpoint(
    payload: GoalUpsert, session: AsyncSession = Depends(get_async_session)
) -> GoalRead:
    goal = await upsert_goal(
        session,
        user_id=payload.user_id,
        description=payload.description,
        status=payload.status,
        target_date=payload.target_date,
    )
    return GoalRead.model_validate(goal.model_dump())


@router.get("/goals/{user_id}", response_model=List[GoalRead])
async def list_goals_endpoint(
    user_id: str, session: AsyncSession = Depends(get_async_session)
) -> List[GoalRead]:
    goals = await list_goals(session, user_id)
    return [GoalRead.model_validate(goal.model_dump()) for goal in goals]


