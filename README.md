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

# Render-compatible FastAPI Scaffold

This is a minimal, production-ready FastAPI scaffold for Render deployment.

## Features
- `/` health check endpoint
- `/query` POST endpoint (example)
- Modular service structure
- Uses environment variables for config

## Local Development

```powershell
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Render Deployment
1. Push this code to a GitHub repo.
2. Create a new Web Service on Render, connect your repo.
3. Set the Start Command to:
   ```
   uvicorn app:app --host 0.0.0.0 --port 10000
   ```
4. Add any required environment variables in the Render dashboard.

## Example Request
```json
POST /query
{
  "query": "Hello, world!"
}
```

---

Enjoy deploying on Render! 🚀
