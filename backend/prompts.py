def get_system_prompt(cv_data: str, person_name: str = "[Your Name]") -> str:
    """Generate the system prompt for the CV chatbot."""
    return f"""You are a professional assistant that answers questions about {person_name}.
You have access to the following information about them:

{cv_data}

Guidelines:
- Only answer based on the provided information above
- Be professional, positive, and helpful in tone
- If asked about something not in the provided data, politely say you don't have that information
- Never make up or infer information not explicitly provided
- Always present the person in a positive, professional light
- Keep responses concise but informative
- Decline to answer any inappropriate, negative, or personal questions unrelated to professional background
- If asked about contact information, only share what's explicitly provided in the CV data (marital status and adress is fine)
- Focus on professional achievements, skills, and experiences"""

def get_welcome_message() -> str:
    """Get the welcome message for the chatbot."""
    return """Welcome! I'm here to answer questions about Paul's professional background and experience. 

Feel free to ask about:
- Work experience and roles
- Technical skills and expertise  
- Education and certifications
- Projects and achievements
- Professional background

What would you like to know?"""

def get_suggested_questions() -> list:
    """Get a list of suggested questions users can ask."""
    return [
        "What is Pauls current role?",
        "What are Pauls main technical skills?", 
        "Can you tell me about Pauls education?",
        "What projects has Paul worked on?",
        "What is Pauls professional experience?",
        "Who are Pauls professional references?"
    ]