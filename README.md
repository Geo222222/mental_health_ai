# CalmMind: Privacy-First Mental Health Companion

CalmMind is a prototype conversational wellness platform that runs entirely on local infrastructure using [Ollama](https://ollama.com/) for large language model inference. It targets clinics and coaching practices that need real-time AI assistance without sending sensitive data to third-party clouds.

## Key Ideas
- **Local-first privacy:** All conversations are processed via Ollama-hosted models, keeping PHI on clinician-controlled machines.
- **Risk-aware conversations:** Lightweight sentiment + keyword scoring flags crisis-level language so staff can intervene quickly.
- **Structured journaling:** Guided prompts help clients capture mood, goals, and coping strategies. Entries power analytics dashboards.
- **Resource recommendations:** Matches conversation themes with curated exercises, helplines, and educational material.

## Architecture Overview
```
FastAPI (REST + WebSocket)
   ├── ChatRouter: streams messages between clients and Ollama
   ├── JournalRouter: CRUD for entries, moods, goals
   ├── ResourcesRouter: smart lookup for coping strategies
   └── AdminRouter: clinician alerts, risk dashboards

Services
   ├── OllamaClient: async interface over http://localhost:11434
   ├── RiskScorer: sentiment + crisis keyword detection
   ├── ResourceEngine: keyword graph for recommendations
   └── Persistence: SQLModel (PostgreSQL) + Redis cache
```

## Getting Started
1. Install [Ollama](https://ollama.com/download) and pull a model:
   ```bash
   ollama pull llama3.1
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Demo & Docs
- Interactive CLI demo: `python scripts/demo_cli.py`
- Additional walkthroughs and sample requests: see [`docs/DEMO.md`](docs/DEMO.md)

## Roadmap
- Voice transcription via Whisper + WebRTC streaming
- Clinician dashboard with mood trend visualizations
- Fine-grained risk escalation workflows (SMS, PagerDuty, EHR integration)
- Optional encrypted cloud sync with zero-knowledge storage


