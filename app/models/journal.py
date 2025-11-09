"""
SQLModel entities for journaling and conversation storage.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class JournalEntry(SQLModel, table=True):
    """
    Free-form journal entry captured from guided prompts.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    content: str
    tags: Optional[str] = Field(default=None, description="Comma-separated topic tags.")
    risk_score: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class MoodLog(SQLModel, table=True):
    """
    Quantitative mood tracking.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    mood: str
    intensity: int = Field(ge=1, le=10)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Goal(SQLModel, table=True):
    """
    Client goals tracked over time.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    description: str
    status: str = Field(default="in_progress")
    target_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


