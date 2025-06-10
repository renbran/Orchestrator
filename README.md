
# AI Orchestrator API

This is a simple FastAPI-based orchestrator for your AI Agent.

## Features

- `/query` endpoint accepts free text query
- Decides which tools to call (Supabase, Google Sheets, Google Calendar, SerpAPI)
- Aggregates data
- Returns a clean formatted response ready for Gemini AI

## Running locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Deploy

Deploy this app to Render, and configure n8n HTTP Request node to POST to:

```
https://YOUR_RENDER_URL/query
```

Enjoy! 🚀
