"""
Pydantic models used in API responses/requests.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Client identifier or session token.")
    message: str
    context: Optional[str] = Field(default=None, description="Optional conversation context/history.")


class ChatResponse(BaseModel):
    reply: str
    risk_level: str
    risk_score: float
    sentiment: float
    alerts: List[str] = []


class JournalEntryCreate(BaseModel):
    user_id: str
    title: str
    content: str
    tags: Optional[str] = None


class JournalEntryRead(BaseModel):
    id: int
    user_id: str
    title: str
    content: str
    tags: Optional[str]
    risk_score: float
    created_at: datetime


class MoodLogCreate(BaseModel):
    user_id: str
    mood: str
    intensity: int
    notes: Optional[str] = None


class MoodLogRead(BaseModel):
    id: int
    user_id: str
    mood: str
    intensity: int
    notes: Optional[str]
    created_at: datetime


class GoalUpsert(BaseModel):
    user_id: str
    description: str
    status: str = "in_progress"
    target_date: Optional[datetime] = None


class GoalRead(BaseModel):
    id: int
    user_id: str
    description: str
    status: str
    target_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


