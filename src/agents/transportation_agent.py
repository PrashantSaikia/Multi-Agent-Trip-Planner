from .base_agent import BaseAgent
from typing import Dict, Any

class TransportationAgent(BaseAgent):
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process transportation-related requests"""
        prompt = f"""
        Based on the following trip details, provide transportation recommendations:
        - Origin: {request.get('origin', 'Not specified')}
        - Destination: {request.get('destination', 'Not specified')}
        - Dates: {request.get('dates', 'Not specified')}
        - Budget: {request.get('budget', 'Not specified')}
        - Preferences: {request.get('preferences', 'Not specified')}
        
        Please provide:
        1. Flight options (if applicable)
        2. Local transportation options
        3. Estimated costs
        4. Booking recommendations
        5. Travel tips and considerations
        """
        
        response = self.generate_response(prompt)
        return self.format_response(response) 