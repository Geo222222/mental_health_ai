"""
Chat endpoints orchestrating Ollama responses with risk assessment.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse
from app.services.ollama import OllamaClient, stream_ollama_reply
from app.services.risk import assess_risk
from app.services.resources import recommend_resources


router = APIRouter(prefix="/chat", tags=["chat"])

SYSTEM_PROMPT = (
    "You are CalmMind, a compassionate mental health companion. "
    "Provide supportive, non-judgmental responses, encourage professional help "
    "when needed, and never make promises you cannot keep."
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Generate a supportive response and return risk signals.
    """
    client = OllamaClient()
    try:
        context = f"{request.context}\nUser: {request.message}" if request.context else request.message
        reply = await client.generate(context, system_prompt=SYSTEM_PROMPT)
    finally:
        await client.close()

    risk = assess_risk(request.message)
    alerts = []
    if risk.keyword_hits:
        alerts.append("Crisis keywords detected.")
    if risk.level == "high":
        alerts.append("Escalate to human support ASAP.")

    return ChatResponse(
        reply=reply.strip(),
        risk_level=risk.level,
        risk_score=risk.score,
        sentiment=risk.sentiment,
        alerts=alerts,
    )


@router.post("/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    """
    Stream an Ollama conversation response token-by-token.
    """
    context = f"{request.context}\nUser: {request.message}" if request.context else request.message
    generator = stream_ollama_reply(context, system_prompt=SYSTEM_PROMPT)
    return StreamingResponse(generator, media_type="text/plain")


@router.post("/resources")
async def recommend(request: ChatRequest) -> dict[str, list[str]]:
    """
    Return resource suggestions based on the user's message.
    """
    suggestions = recommend_resources(request.message)
    return {"resources": suggestions}


