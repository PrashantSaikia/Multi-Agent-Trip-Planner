from .base_agent import BaseAgent
from typing import Dict, Any

class AccommodationAgent(BaseAgent):
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process accommodation-related requests"""
        prompt = f"""
        Based on the following trip details, provide accommodation recommendations:
        - Destination: {request.get('destination', 'Not specified')}
        - Dates: {request.get('dates', 'Not specified')}
        - Budget: {request.get('budget', 'Not specified')}
        - Preferences: {request.get('preferences', 'Not specified')}
        
        Please provide:
        1. 3-5 hotel/lodging options
        2. Price ranges
        3. Key amenities
        4. Location advantages
        5. Booking recommendations
        """
        
        response = self.generate_response(prompt)
        return self.format_response(response) 