"""
Tests for resource recommendation engine.
"""
from app.services.resources import recommend_resources


def test_recommend_resources_returns_matches():
    suggestions = recommend_resources("I am feeling a lot of anxiety about work.")
    assert any("breathing" in item.lower() for item in suggestions)


def test_recommend_resources_fallback():
    suggestions = recommend_resources("Just checking in, nothing specific.")
    assert len(suggestions) >= 2

