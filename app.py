import streamlit as st
import os
import time
from dotenv import load_dotenv
from backend.auth import AuthManager
from backend.chatbot import CVChatbot
from backend.prompts import get_welcome_message, get_suggested_questions
from config.settings import load_cv_data, APP_TITLE, APP_ICON

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main container styling - MHP inspired minimal white design */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Override Streamlit's default styling */
    .main .block-container {
        padding-top: 3rem !important;
        padding-bottom: 140px !important;
        max-width: 1000px !important;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        font-size: 16px;
        line-height: 1.6;
    }
    
    .user-message {
        background-color: #f8fafc;
        margin-left: 10%;
        border-left: 3px solid #1612ff;
        color: #262626;
    }
    
    .assistant-message {
        background-color: #ffffff;
        margin-right: 10%;
        border-left: 3px solid #e2e8f0;
        border: 1px solid #d1d5db;
        color: #262626;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom button styling - Enhanced contrast */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        border-radius: 12px;
        border: none;
        padding: 0.875rem 1.75rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
        color: #ffffff !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }
    
    /* Authentication container */
    .auth-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin: 3rem auto;
        max-width: 480px;
        border: 1px solid #d1d5db;
    }
    
    /* Add "Login" text to empty auth container */
    .auth-container:empty::before {
        content: "Login";
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        display: block;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    
    /* Welcome message styling */
    .welcome-message {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 12px;
        border-left: 4px solid #1612ff;
        margin-bottom: 2rem;
        color: #262626;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Typography improvements - FORCE VISIBLE COLORS */
    h1, .stMarkdown h1, [data-testid="stMarkdownContainer"] h1 {
        color: #1e293b !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h2, .stMarkdown h2, [data-testid="stMarkdownContainer"] h2 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    h3, .stMarkdown h3, [data-testid="stMarkdownContainer"] h3 {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Increase font sizes across the app */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        font-size: 18px !important;
        color: #374151;
    }
    
    /* Welcome message text */
    .welcome-message p, .welcome-message li {
        font-size: 18px !important;
    }
    
    /* Button text larger */
    button p, button span {
        font-size: 16px !important;
    }
    
    /* General content text */
    [data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
    }
    
    /* Bullet points */
    ul li, ol li {
        font-size: 18px !important;
    }
    
    /* Fix specific problematic elements with larger text */
    .stMarkdown > div, .stMarkdown p, .stMarkdown span {
        color: #374151 !important;
        font-size: 17px !important;
    }
    
    /* Force larger text on all containers */
    .element-container, .element-container * {
        font-size: 17px !important;
    }
    
    /* TARGET EXACT STREAMLIT BUTTON STRUCTURE */
    
    /* Target the button with exact classes */
    .st-emotion-cache-1rwb540.el4r43z2 {
        background: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #2563eb !important;
        border-radius: 8px !important;
    }
    
    /* Target the markdown container inside button */
    .st-emotion-cache-1rwb540 .st-emotion-cache-bvleps {
        color: #ffffff !important;
    }
    
    /* Target the p tag specifically */
    .st-emotion-cache-1rwb540 .st-emotion-cache-bvleps p {
        color: #ffffff !important;
    }
    
    /* Target by test ID */
    [data-testid="stBaseButton-secondary"] {
        background: #2563eb !important;
        color: #ffffff !important;
    }
    
    [data-testid="stBaseButton-secondary"] p {
        color: #ffffff !important;
    }
    
    /* Target all secondary buttons */
    button[kind="secondary"] {
        background: #2563eb !important;
        color: #ffffff !important;
    }
    
    button[kind="secondary"] p {
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Input styling - Fixed overlapping issue */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        padding: 0.875rem 1rem;
        font-family: 'Inter', sans-serif;
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-size: 16px;
        font-weight: 400;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        width: 100% !important;
    }
    
    /* Hide the dark overlapping helper text */
    .stTextInput > div > div[data-baseweb="base-input"] > div:last-child {
        display: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        background-color: #ffffff !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        font-weight: 400;
    }
    
    /* Fix input container positioning */
    .stTextInput > div {
        position: relative !important;
    }
    
    .stTextInput > div > div {
        width: 100% !important;
        position: relative !important;
    }
    
    /* Enhanced Chat Input - More Visible with Shadow */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border-radius: 20px !important;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.1),
            0 4px 10px rgba(0, 0, 0, 0.06) !important;
        border: 2px solid #e2e8f0 !important;
        margin: 24px auto !important;
        max-width: 900px !important;
        padding: 8px !important;
    }
    
    [data-testid="stChatInput"] > div {
        border: none !important;
        background: transparent !important;
    }
    
    [data-testid="stChatInput"] input {
        background: #ffffff !important;
        color: #1e293b !important;
        font-family: 'Inter', sans-serif !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 18px 24px !important;
        font-size: 17px !important;
        min-height: 48px !important;
    }
    
    
    
    /* MAKE DARK ELEMENTS LIGHT GREY INSTEAD */
    .stCode, [data-testid="stCode"],
    .stCodeBlock, [data-testid="stCodeBlock"],
    pre, code,
    div[style*="background-color: rgb(0, 0, 0)"],
    div[style*="background-color: black"],
    div[style*="background: rgb(0, 0, 0)"],
    div[style*="background: black"] {
        background-color: #f1f5f9 !important;
        background: #f1f5f9 !important;
        color: #374151 !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Target the BLACK bottom container and all chat elements */
    [data-testid="stBottomBlockContainer"],
    .st-emotion-cache-1y34ygi,
    .st-emotion-cache-8fjoqp,
    .st-emotion-cache-1eeryuo,
    .st-emotion-cache-x1bvup,
    .st-emotion-cache-12o5wl7,
    .st-emotion-cache-sey4o0,
    .st-emotion-cache-1d0j37u,
    .st-emotion-cache-vsnu81,
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] *,
    [data-testid="stVerticalBlock"] {
        background-color: #f8fafc !important;
        border-color: #f1f5f9 !important;
        background: #f8fafc !important;
    }
    
    /* Make textarea area bigger and more visible */
    [data-testid="stChatInputTextArea"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
        padding: 18px 24px !important;
        font-size: 17px !important;
        min-height: 48px !important;
        border-radius: 16px !important;
    }
    
    /* Light submit button */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #f1f5f9 !important;
        color: #64748b !important;
    }
    
    /* Fix dark text input helper areas */
    .stTextInput div[style*="background: rgb"],
    div[data-baseweb="base-input"] > div {
        background: #f8fafc !important;
        color: #374151 !important;
    }
    
    /* Keep main app backgrounds white but don't touch chat input */
    
    .stApp {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* AGGRESSIVE TEXT COLOR FIXES */
    .element-container, .stMarkdown, [data-testid="stMarkdownContainer"],
    .block-container, .main, .stApp > div, .css-1d391kg,
    .stForm, .stColumns, .stColumn, .stContainer {
        color: #1e293b !important;
    }
    
    /* Force visible colors on ALL content */
    .element-container * {
        color: #374151 !important;
    }
    
    /* Specifically target white text issues */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp text {
        color: #1e293b !important;
    }
    
    /* Fix markdown container text */
    [data-testid="stMarkdownContainer"] * {
        color: #374151 !important;
    }
    
    /* Enhanced animations */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(20px) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Apply animations to elements */
    .chat-message {
        animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover {
        animation: pulse 0.3s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "session_token" not in st.session_state:
        st.session_state.session_token = None
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "total_tokens_used" not in st.session_state:
        st.session_state.total_tokens_used = 0
    if "chatbot" not in st.session_state:
        cv_data = load_cv_data()
        st.session_state.chatbot = CVChatbot(cv_data)

def check_url_authentication():
    """Check if user is authenticated via URL parameter."""
    auth_manager = AuthManager()
    query_params = st.query_params
    
    if "token" in query_params:
        password = query_params["token"]
        if auth_manager.verify_password(password):
            st.session_state.authenticated = True
            st.session_state.session_token = auth_manager.generate_session_token(password)
            st.session_state.session_start_time = time.time()
            return True
    return False

def show_authentication_form():
    """Display the authentication form."""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.markdown("### Welcome! Please enter the access password to continue.")
    
    password = st.text_input("Access Password", type="password", key="auth_password")
    
    if st.button("Access Chatbot", key="auth_button"):
        auth_manager = AuthManager()
        if auth_manager.verify_password(password):
            st.session_state.authenticated = True
            st.session_state.session_token = auth_manager.generate_session_token(password)
            st.session_state.session_start_time = time.time()
            st.rerun()
        else:
            st.error("❌ Invalid password. Please try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Instructions for URL access
    st.markdown("---")
    st.markdown("**Alternative Access:** You can also access this chatbot directly using a URL with the password parameter:")
    st.code("https://your-app-url.streamlit.app/?token=your_password")

def check_session_validity():
    """Check if the current session is still valid."""
    if st.session_state.authenticated and st.session_state.session_start_time:
        auth_manager = AuthManager()
        if not auth_manager.is_session_valid(
            st.session_state.session_token, 
            st.session_state.session_start_time
        ):
            st.session_state.authenticated = False
            st.session_state.session_token = None
            st.session_state.session_start_time = None
            st.warning("Your session has expired. Please log in again.")
            st.rerun()

def display_chat_interface():
    """Display the main chat interface."""
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    
    # Session info in sidebar
    with st.sidebar:
        st.markdown("### Session Info")
        if st.session_state.session_start_time:
            session_duration = int(time.time() - st.session_state.session_start_time)
            st.markdown(f"**Session Time:** {session_duration // 60}m {session_duration % 60}s")
        
        st.markdown(f"**Total Tokens Used:** {st.session_state.total_tokens_used}")
        
        estimated_cost = st.session_state.chatbot.get_conversation_cost(st.session_state.total_tokens_used)
        st.markdown(f"**Estimated Cost:** ${estimated_cost:.6f}")
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.session_token = None
            st.session_state.session_start_time = None
            st.session_state.messages = []
            st.rerun()
    
    # Display welcome message if no messages yet
    if not st.session_state.messages:
        welcome_msg = get_welcome_message()
        st.markdown(f'<div class="welcome-message">{welcome_msg}</div>', unsafe_allow_html=True)
        
        # Show suggested questions
        st.markdown("### 💡 Suggested Questions:")
        suggested = get_suggested_questions()
        
        cols = st.columns(2)
        for i, question in enumerate(suggested):
            col = cols[i % 2]
            if col.button(question, key=f"suggestion_{i}"):
                st.session_state.messages.append({"role": "user", "content": question})
                handle_user_message(question)
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if user_input := st.chat_input("Ask me anything about my professional background..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        handle_user_message(user_input)
        st.rerun()

def handle_user_message(user_input: str):
    """Handle user message and get chatbot response."""
    with st.spinner("Thinking..."):
        response_data = st.session_state.chatbot.get_response(
            user_input, 
            st.session_state.messages[:-1]  # Exclude the current user message
        )
        
        if response_data["success"]:
            assistant_response = response_data["response"]
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Update token usage
            if "tokens_used" in response_data:
                st.session_state.total_tokens_used += response_data["tokens_used"]["total"]
        else:
            error_message = "I apologize, but I encountered an error. Please try again."
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.error(f"Error: {response_data.get('error', 'Unknown error')}")

def main():
    """Main application function."""
    initialize_session_state()
    
    # Check URL authentication first
    if not st.session_state.authenticated:
        check_url_authentication()
    
    # Check session validity
    if st.session_state.authenticated:
        check_session_validity()
    
    # Show appropriate interface
    if st.session_state.authenticated:
        display_chat_interface()
    else:
        show_authentication_form()

if __name__ == "__main__":
    main()