"""
Unit tests for risk assessment utilities.
"""
from app.services.risk import assess_risk


def test_assess_risk_detects_keywords():
    message = "I feel like I might hurt myself and can't go on."
    assessment = assess_risk(message)
    assert assessment.level == "high"
    assert assessment.keyword_hits


def test_assess_risk_handles_positive_text():
    message = "I had a good day and enjoyed talking with friends."
    assessment = assess_risk(message)
    assert assessment.level == "low"
    assert assessment.score < 0.4

