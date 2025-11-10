"""
Models for storing risk assessments.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class RiskEvent(SQLModel, table=True):
    """
    Persisted record describing a detected risk signal during chat or journaling.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    source: str = Field(description="Origin of the event, e.g., 'chat' or 'journal'")
    content: str = Field(description="User message or journal excerpt that triggered the event")
    risk_level: str
    risk_score: float
    sentiment: float
    keywords: Optional[str] = Field(default=None, description="Comma-separated keyword hits")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


