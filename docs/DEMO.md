# CalmMind Demo Guide

This guide shows how to exercise the CalmMind backend without building a front-end UI.

## 1. Prerequisites
- Ollama running locally with `llama3.1` (or any compatible model):
  `ollama pull llama3.1`
- Python virtual environment with project dependencies:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
- Start the API:
  `uvicorn app.main:app --reload`

## 2. Interactive CLI
Run the demo script to chat with the backend and view risk analysis:

```powershell
python scripts/demo_cli.py
```

The CLI prints CalmMind's response, risk level, score, and suggested alerts after each user message. Type `quit` to exit.

## 3. Sample REST Calls
### Chat response
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","message":"I am feeling anxious about work."}'
```

### Journal entry
```bash
curl -X POST http://localhost:8000/api/journal \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","title":"Morning reflection","content":"I woke up stressed but practiced breathing.","tags":"morning"}'
```

### Clinician alerts
```bash
curl http://localhost:8000/api/admin/risk-events?minimum_level=moderate
```

## 4. Resetting State
The default configuration stores data in `calmmind.db`. Delete the file to reset the demo:

```powershell
Remove-Item calmmind.db
```

## 5. Next Steps
- Integrate the API with a web or mobile front end.
- Replace SQLite with Postgres for production deployments.
- Feed `risk-events` into dashboards or alerting systems.
