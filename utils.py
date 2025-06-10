
def format_response(data: str) -> str:
    formatted_data = data.strip()
    sections = formatted_data.split('\n\n')
    formatted_sections = [f"• {section.strip()}" for section in sections]
    formatted_content = '\n\n'.join(formatted_sections)
    return f"✨ Here is the information I gathered for you:\n\n{formatted_content}\n🌟"
