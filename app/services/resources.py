"""
Resource recommendation logic.
"""
from __future__ import annotations

from typing import List, Dict


DEFAULT_RESOURCES: Dict[str, List[str]] = {
    "anxiety": [
        "5-minute breathing exercise",
        "Progressive muscle relaxation guide",
        "Headspace: Managing anxiety basics",
    ],
    "depression": [
        "Daily gratitude worksheet",
        "Reach out to a trusted contact",
        "National Suicide Prevention Lifeline: 988",
    ],
    "stress": [
        "Box breathing technique",
        "Take a short mindfulness walk",
        "Pomodoro planning sheet",
    ],
    "sleep": [
        "Sleep hygiene checklist",
        "Guided body scan meditation",
        "Avoid screens 60 minutes before bedtime",
    ],
}


def recommend_resources(text: str) -> List[str]:
    """
    Return a deduplicated list of suggested coping resources.
    """
    lowered = text.lower()
    suggestions: List[str] = []
    for keyword, resources in DEFAULT_RESOURCES.items():
        if keyword in lowered:
            suggestions.extend(resources)

    if "high" in lowered or "overwhelmed" in lowered:
        suggestions.append("Contact a crisis counselor or trusted person immediately.")

    if not suggestions:
        suggestions.extend(
            [
                "Try a 3-minute grounding exercise.",
                "Journal how you feel and what you need right now.",
            ]
        )
    return list(dict.fromkeys(suggestions))


