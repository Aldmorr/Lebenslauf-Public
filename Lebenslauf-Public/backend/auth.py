import os
import hashlib
import time
import bcrypt
import streamlit as st
from typing import Optional

class AuthManager:
    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
        
    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        try:
            # Try to get password hash from Streamlit secrets first
            if hasattr(st, 'secrets') and 'PASSWORD_HASH' in st.secrets:
                stored_hash = st.secrets['PASSWORD_HASH'].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            print(f"Error checking password: {e}")
        
        # Fallback to environment variable (for local dev)
        stored_hash = os.getenv("PASSWORD_HASH", "")
        if stored_hash:
            try:
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            except Exception:
                pass
                
        # Final fallback - plain text comparison (insecure)
        access_password = os.getenv("ACCESS_PASSWORD", "default_password")
        return password == access_password
    
    def generate_session_token(self, password: str) -> Optional[str]:
        """Generate a session token after successful password verification."""
        if self.verify_password(password):
            timestamp = str(int(time.time()))
            token_data = f"{password}_{timestamp}"
            return hashlib.sha256(token_data.encode()).hexdigest()
        return None
    
    def is_session_valid(self, token: str, creation_time: float) -> bool:
        """Check if a session token is still valid."""
        current_time = time.time()
        return (current_time - creation_time) < self.session_timeout
    
    def get_password_from_url(self, query_params: dict) -> Optional[str]:
        """Extract password from URL query parameters."""
        return query_params.get("token")