"""
Risk scoring utilities for mental health conversations.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from textblob import TextBlob

from app.core.config import get_settings


@dataclass
class RiskAssessment:
    sentiment: float
    keyword_hits: List[str]
    score: float
    level: str


NEGATIVE_SENTIMENT_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4


def assess_risk(message: str) -> RiskAssessment:
    """
    Compute a simple risk score combining sentiment and keyword hits.
    """
    settings = get_settings()
    blob = TextBlob(message)
    sentiment = blob.sentiment.polarity
    keywords = [
        keyword for keyword in settings.risk_keywords if keyword.lower() in message.lower()
    ]

    normalized_sentiment = max(0.0, min(1.0, -sentiment))  # 0 (positive) -> 1 (very negative)
    keyword_score = min(1.0, len(keywords) / max(1, len(settings.risk_keywords) // 2))

    combined = (normalized_sentiment * NEGATIVE_SENTIMENT_WEIGHT) + (
        keyword_score * KEYWORD_WEIGHT
    )

    level = "low"
    if combined > 0.7 or keywords:
        level = "high"
    elif combined > 0.4:
        level = "moderate"

    return RiskAssessment(
        sentiment=sentiment,
        keyword_hits=keywords,
        score=combined,
        level=level,
    )


