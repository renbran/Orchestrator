# query_orchestrator.py
"""
AI-driven orchestrator using Gemini for classification and dynamic tool selection.
"""
import os
from services.supabase_service import query_supabase
from services.sheets_service import query_google_sheets
from services.calendar_service import query_google_calendar
from services.serpapi_service import query_serpapi
from services.property_finder_service import query_property_finder
from services.prosearch_service import query_prosearch
from services.bayut_service import query_bayut
from utils import format_response
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

# Map tool names to functions
TOOL_FUNCTIONS = {
    "Google Calendar": query_google_calendar,
    "Google Sheets": query_google_sheets,
    "SerpAPI": query_serpapi,
    "Supabase": query_supabase,
    "Property Finder": query_property_finder,
    "Prosearch": query_prosearch,
    "Bayut": query_bayut,
}

TOOL_DESCRIPTIONS = {
    "Google Calendar": "calendar, events, schedule, meeting, appointment",
    "Google Sheets": "sheet, excel, spreadsheet, table, data",
    "SerpAPI": "search, google, web, internet, lookup",
    "Supabase": "database, db, supabase, sql, records",
    "Property Finder": "property, real estate, apartment, house, rent, buy, finder",
    "Prosearch": "property, real estate, prosearch, listings, homes, apartments",
    "Bayut": "property, real estate, bayut, listings, homes, apartments",
}

def classify_tools_with_gemini(user_query):
    """Use Gemini to classify which tools to use for the query."""
    prompt = (
        "You are an AI orchestrator. Given a user query, select the most relevant tools from the following list: "
        f"{list(TOOL_FUNCTIONS.keys())}.\n"
        "For each tool, return only the tool name if it is relevant.\n"
        f"User query: {user_query}\n"
        "Respond with a comma-separated list of tool names."
    )
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Parse comma-separated tool names
        selected = [tool.strip() for tool in text.split(",") if tool.strip() in TOOL_FUNCTIONS]
        return selected
    except Exception as e:
        # Fallback: use all tools if Gemini fails
        return list(TOOL_FUNCTIONS.keys())

def orchestrate_query(user_query):
    selected_tools = classify_tools_with_gemini(user_query)
    aggregated_data = ""
    for tool in selected_tools:
        func = TOOL_FUNCTIONS[tool]
        try:
            tool_data = func(user_query)
            emoji = ""
            if tool == "Google Calendar": emoji = "📅"
            if tool == "Google Sheets": emoji = "📊"
            if tool == "SerpAPI": emoji = "🔍"
            if tool == "Supabase": emoji = "🗄️"
            if tool == "Property Finder": emoji = "🏠"
            if tool == "Propsearch": emoji = "🏢"
            if tool == "Bayut": emoji = "🏡"
            aggregated_data += f"{emoji} {tool}: {tool_data}\n\n"
        except Exception as e:
            aggregated_data += f"{tool}: Error - {str(e)}\n\n"
    if not aggregated_data:
        aggregated_data = "🤔 Sorry, I could not find relevant data sources for your query."
    final_response = format_response(aggregated_data)
    return {
        "aggregatedData": final_response,
        "selectedTools": selected_tools
    }
