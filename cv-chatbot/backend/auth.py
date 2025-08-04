import os
import hashlib
import time
from typing import Optional

class AuthManager:
    def __init__(self):
        self.access_password = os.getenv("ACCESS_PASSWORD", "default_password")
        self.session_timeout = 3600  # 1 hour in seconds
        
    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the access password."""
        return password == self.access_password
    
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