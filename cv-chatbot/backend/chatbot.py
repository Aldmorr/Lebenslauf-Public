import os
from typing import List, Dict, Any, Optional
import anthropic
from backend.prompts import get_system_prompt

class CVChatbot:
    def __init__(self, cv_data: str):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.cv_data = cv_data
        self.model = "claude-3-haiku-20240307"  # Most cost-effective model
        self.max_tokens = 1000
        self.system_prompt = get_system_prompt(cv_data)
        
    def get_response(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Get a response from the chatbot.
        
        Args:
            user_message: The user's question
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Prepare messages for the API
            messages = []
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Limit to last 10 messages
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=messages
            )
            
            return {
                "success": True,
                "response": response.content[0].text,
                "tokens_used": {
                    "input": response.usage.input_tokens,
                    "output": response.usage.output_tokens,
                    "total": response.usage.input_tokens + response.usage.output_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request. Please try again."
            }
    
    def estimate_tokens(self, text: str) -> int:
        """Rough estimation of tokens (approximately 4 characters per token)."""
        return len(text) // 4
    
    def get_conversation_cost(self, total_tokens: int) -> float:
        """
        Calculate approximate cost based on Claude Haiku pricing.
        Input: $0.25 per 1M tokens
        Output: $1.25 per 1M tokens
        This is a rough estimate - actual costs may vary.
        """
        # Rough estimate assuming 70% input, 30% output tokens
        input_tokens = int(total_tokens * 0.7)
        output_tokens = int(total_tokens * 0.3)
        
        input_cost = (input_tokens / 1_000_000) * 0.25
        output_cost = (output_tokens / 1_000_000) * 1.25
        
        return input_cost + output_cost