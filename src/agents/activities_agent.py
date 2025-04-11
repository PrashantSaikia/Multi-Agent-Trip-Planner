from .base_agent import BaseAgent
from typing import Dict, Any

class ActivitiesAgent(BaseAgent):
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process activities-related requests"""
        prompt = f"""
        Based on the following trip details, provide activity and sightseeing recommendations:
        - Destination: {request.get('destination', 'Not specified')}
        - Dates: {request.get('dates', 'Not specified')}
        - Duration: {request.get('duration', 'Not specified')}
        - Interests: {request.get('interests', 'Not specified')}
        - Budget: {request.get('budget', 'Not specified')}
        
        Please provide:
        1. Daily itinerary suggestions
        2. Must-see attractions
        3. Local experiences
        4. Activity costs and booking information
        5. Time management tips
        6. Local customs and etiquette
        """
        
        response = self.generate_response(prompt)
        return self.format_response(response) 