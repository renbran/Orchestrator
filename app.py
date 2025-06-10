from fastapi import FastAPI, Request
from services.supabase_service import query_supabase
from services.sheets_service import query_google_sheets
from services.calendar_service import query_google_calendar
from services.serpapi_service import query_serpapi
from utils import format_response
from services.knowledge_base_service import router as knowledge_router

app = FastAPI()

# Include the knowledge base router
app.include_router(knowledge_router)

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_query = data.get("query", "")

    selected_tools = []

    # Basic logic to decide which tools to call
    aggregated_data = ""

    if "calendar" in user_query.lower():
        selected_tools.append("Google Calendar")
        calendar_data = query_google_calendar(user_query)
        aggregated_data += f"📅 Calendar: {calendar_data}\n\n"

    if "sheet" in user_query.lower() or "excel" in user_query.lower():
        selected_tools.append("Google Sheets")
        sheets_data = query_google_sheets(user_query)
        aggregated_data += f"📊 Sheets: {sheets_data}\n\n"

    if "search" in user_query.lower() or "google" in user_query.lower():
        selected_tools.append("SerpAPI")
        serp_data = query_serpapi(user_query)
        aggregated_data += f"🔍 Search: {serp_data}\n\n"

    if "database" in user_query.lower() or "supabase" in user_query.lower():
        selected_tools.append("Supabase")
        supabase_data = query_supabase(user_query)
        aggregated_data += f"🗄️ Supabase: {supabase_data}\n\n"

    # Fallback if no tool matched
    if not aggregated_data:
        aggregated_data = "🤔 Sorry, I could not find relevant data sources for your query."

    # Final polishing
    final_response = format_response(aggregated_data)

    return {
        "aggregatedData": final_response,
        "selectedTools": selected_tools
    }
