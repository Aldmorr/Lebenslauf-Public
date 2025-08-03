# Claude Code Project Context

## Project Overview
This is a professional CV chatbot application built with Streamlit and Anthropic's Claude AI. The application provides an interactive way for recruiters and potential employers to learn about Paul Schiel's professional background through natural conversation.

## Key Features
- **Password-protected access** with session management
- **Modern white theme** with professional blue accents
- **Floating chat interface** with smooth animations
- **Privacy-first design** - CV data stored in Streamlit secrets
- **Real-time AI conversations** about professional experience
- **Suggested questions** for easy interaction
- **Token usage tracking** and cost estimation

## Architecture

### Core Components
- `app.py` - Main Streamlit application with UI and routing
- `backend/chatbot.py` - Claude AI integration and conversation logic
- `backend/auth.py` - Authentication and session management
- `backend/prompts.py` - Welcome messages and suggested questions
- `config/settings.py` - Application configuration and CV data loading

### Authentication Flow
1. User enters password or uses URL parameter `?token=password`
2. Password verified against `PASSWORD_HASH` in secrets
3. Session token generated and stored with timeout
4. Protected chat interface displayed

### Data Privacy
- **CV data never stored in repository** - loaded from `st.secrets['CV_DATA']`
- **Password hashed** using bcrypt for security
- **Session management** with automatic timeout
- **Environment variables** for API keys

## Technology Stack
- **Frontend**: Streamlit with custom CSS for modern UI
- **AI**: Anthropic Claude API (claude-3-haiku-20240307)
- **Authentication**: bcrypt password hashing
- **Deployment**: Streamlit Cloud
- **Styling**: Custom CSS with Inter font family

## Current UI Design
- **Clean white background** with professional appearance
- **Blue gradient buttons** (#2563eb) with white text
- **Floating chat input** at bottom with shadows and rounded corners
- **Enhanced typography** with 18px font sizes for readability
- **Smooth animations** for user interactions
- **Responsive design** optimized for desktop and mobile

## Recent Major Changes
1. **Complete UI redesign** from dark blue theme to clean white professional theme
2. **Privacy enhancement** - moved CV data to Streamlit secrets
3. **Typography improvements** - increased font sizes and improved contrast
4. **Button styling fixes** - ensured white text on blue backgrounds
5. **Chat input redesign** - floating modern design with proper shadows

## Development Notes
- Uses `st.chat_input()` for modern chat interface
- Custom CSS targets specific Streamlit classes for styling
- Error handling for missing secrets and API failures
- Conversation history maintained in session state
- Token usage tracking for cost monitoring

## Deployment Configuration
### Required Streamlit Secrets:
```toml
[secrets]
ANTHROPIC_API_KEY = "your_anthropic_api_key"
PASSWORD_HASH = "bcrypt_hash_of_password" 
CV_DATA = "Complete CV content as string"
```

### Environment Setup:
- Python 3.8+
- Dependencies in `requirements.txt`
- Local development uses `.env` file for API key

## Common Development Tasks
- **Styling**: Modify CSS in `app.py` around line 20-400
- **Questions**: Update `backend/prompts.py` 
- **Authentication**: Modify `backend/auth.py`
- **AI Logic**: Update `backend/chatbot.py`
- **Settings**: Configure in `config/settings.py`

## Known Issues & Considerations
- Font size changes require aggressive CSS with `!important`
- Streamlit auto-generates CSS classes that may change between versions
- Chat input styling uses specific `data-testid` selectors
- Session timeout requires manual refresh

## Future Enhancements
- Multi-language support
- CV data sections (experience, education, skills)
- Download CV functionality
- Analytics dashboard
- Mobile app version