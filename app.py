from fastapi import FastAPI, Request
import os
from services.example_service import example_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Render-compatible FastAPI app!"}

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    # Example: call a service function
    result = example_query(user_query)
    return {"result": result}
