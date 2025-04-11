from abc import ABC, abstractmethod
import google.generativeai as genai
from typing import Dict, Any, List

class BaseAgent(ABC):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process the request and return a response"""
        pass
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response using the Gemini model"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def format_response(self, response: str) -> Dict[str, Any]:
        """Format the response into a structured format"""
        return {
            "status": "success",
            "response": response
        } 