from fastapi import FastAPI, Request
from services.example_service import example_query
from services.knowledge_base_service import router as kb_router

app = FastAPI()

# Mount the knowledge base router
app.include_router(kb_router)

@app.get("/")
def root():
    return {"message": "Hello from Local FastAPI app!"}

@app.post("/query")
async def query(request: Request):
    # Try to parse JSON, fallback to form-data
    user_query = None
    # Try JSON
    try:
        data = await request.json()
        user_query = data.get("query")
    except Exception:
        pass
    # Try form-data if JSON failed or query is missing
    if not user_query:
        try:
            form = await request.form()
            user_query = form.get("query")
        except Exception:
            pass
    if not user_query:
        return {"error": "Missing 'query' parameter in request body (JSON or form-data)"}
    result = example_query(user_query)
    return {"result": result}
