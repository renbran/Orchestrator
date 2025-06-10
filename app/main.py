from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.github_orchestrator import list_repo_issues
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For n8n, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/github/issues")
async def github_issues(request: Request):
    data = await request.json()
    owner = data.get("owner")
    repo = data.get("repo")
    if not owner or not repo:
        raise HTTPException(status_code=400, detail="owner and repo required")
    issues = list_repo_issues(owner, repo)
    return {"issues": issues}

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    query_text = data.get("query", "")
    # Add orchestration logic here
    return {"result": f"Received: {query_text}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))