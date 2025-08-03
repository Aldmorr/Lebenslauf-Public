import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CV_DATA_FILE = DATA_DIR / "cv_data.txt"

# Application settings
APP_TITLE = "Chat with Pauls CV"
APP_ICON = ""
SESSION_TIMEOUT = 3600  # 1 hour

# Anthropic API settings
DEFAULT_MODEL = "claude-3-haiku-20240307"
MAX_TOKENS = 1000
MAX_CONVERSATION_LENGTH = 20  # Maximum number of messages to keep in history

# UI settings
THEME_CONFIG = {
    "primaryColor": "#2b5797",
    "backgroundColor": "#1e3c72",
    "secondaryBackgroundColor": "#2a5298",
    "textColor": "#ffffff"
}

# Rate limiting (optional)
MAX_REQUESTS_PER_HOUR = 50
MAX_TOKENS_PER_DAY = 10000

def load_cv_data() -> str:
    """Load CV data and references from Streamlit secrets or file fallback."""
    cv_content = ""
    references_content = ""
    
    try:
        import streamlit as st
        # Try to load from Streamlit secrets first (for production)
        if hasattr(st, 'secrets'):
            if 'CV_DATA' in st.secrets:
                cv_content = st.secrets['CV_DATA']
            if 'REFERENCES' in st.secrets:
                references_content = st.secrets['REFERENCES']
            
            if cv_content:
                # Combine CV data with references if both exist
                if references_content:
                    return f"{cv_content}\n\n## References\n\n{references_content}"
                return cv_content
    except Exception:
        pass
    
    # Fallback to file (for local development)
    try:
        with open(CV_DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if "placeholder" in content.lower() or "demo content" in content.lower():
                return "CV data not configured. Please add CV_DATA and optionally REFERENCES to Streamlit secrets."
            return content
    except FileNotFoundError:
        return "CV data not found. Please add CV_DATA and optionally REFERENCES to Streamlit secrets or data/cv_data.txt file."
    except Exception as e:
        return f"Error loading CV data: {str(e)}"