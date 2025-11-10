"""Command-line demo for interacting with the CalmMind API."""
from __future__ import annotations

import json
import sys
from typing import Optional

import httpx

API_URL = "http://localhost:8000"


def format_alerts(alerts: list[str]) -> str:
    return "; ".join(alerts) if alerts else "None"


def chat_once(client: httpx.Client, user_id: str, message: str, context: Optional[str]) -> dict:
    payload = {"user_id": user_id, "message": message}
    if context:
        payload["context"] = context
    response = client.post(f"{API_URL}/api/chat", json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def main() -> None:
    user_id = "demo-user"
    context: Optional[str] = None

    print("CalmMind CLI Demo")
    print("Ensure the API is running at http://localhost:8000 before chatting.")
    print("Type 'quit' to exit.\n")

    with httpx.Client() as client:
        while True:
            try:
                message = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if not message:
                continue
            if message.lower() in {"quit", "exit"}:
                print("Goodbye!")
                break

            try:
                result = chat_once(client, user_id, message, context)
            except httpx.HTTPError as exc:
                print(f"[error] Request failed: {exc}")
                continue

            print(f"CalmMind: {result['reply']}\n")
            print(
                f"Risk level: {result['risk_level']} (score={result['risk_score']:.2f}, sentiment={result['sentiment']:.2f})"
            )
            print(f"Alerts: {format_alerts(result.get('alerts', []))}\n")

            transcript = {"user": message, "assistant": result["reply"]}
            context = (context + "\n" if context else "") + json.dumps(transcript)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
