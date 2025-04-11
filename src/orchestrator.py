from typing import Dict, Any, List
from .agents.accommodation_agent import AccommodationAgent
from .agents.transportation_agent import TransportationAgent
from .agents.activities_agent import ActivitiesAgent
import google.generativeai as genai

class TripPlannerOrchestrator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.accommodation_agent = AccommodationAgent(api_key)
        self.transportation_agent = TransportationAgent(api_key)
        self.activities_agent = ActivitiesAgent(api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def process_chat_message(self, message: str) -> str:
        """Process a chat message and return a response"""
        prompt = f"""
        You are a helpful and efficient trip planning assistant. The user has sent the following message:
        {message}
        
        Please provide a direct and actionable response in proper markdown format:

        1. Start with a brief acknowledgment
        2. Use markdown headers for day numbers (e.g. ## Day 1: [Theme/Area])
        3. Use proper markdown bullet points and sub-points:
           - Main points with single dash (-)
           - Sub-points indented with 2 spaces and dash
        4. Use markdown bold for all costs (e.g. **$50**)
        5. Use proper line breaks between sections
        6. At the end of each day, show a "Daily Total: **$XX**" line
        7. At the very end, show a "Total Trip Cost: **$XX**" section that breaks down:
           - Daily totals
           - Any additional costs (transport cards, etc.)
           - Final total

        Example format:
        Brief acknowledgment here.

        ## Day 1: [Theme/Area]
        - Morning (**$XX**):
          - Activity 1 description (**$X**)
          - Activity 2 description (**$X**)
        - Afternoon (**$XX**):
          - Activity 1 description (**$X**)
          - Activity 2 description (**$X**)
        - Evening (**$XX**):
          - Activity 1 description (**$X**)
          - Activity 2 description (**$X**)

        Daily Total: **$XX**

        ## Day 2: [Same format as Day 1]

        ## Cost Summary:
        - Day 1 Total: **$XX**
        - Day 2 Total: **$XX**
        - Additional Costs: **$XX**
        - Total Trip Cost: **$XX**

        [Any assumptions or notes at the end]
        """
        
        response = self.model.generate_content(prompt)
        return response.text
        
    async def plan_trip(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate the trip planning process across all agents"""
        try:
            # If it's a chat message, process it directly
            if "message" in request and not request.get("destination"):
                return {
                    "status": "success",
                    "plan": self.process_chat_message(request["message"])
                }
            
            # Get responses from all agents
            accommodation_response = await self.accommodation_agent.process_request(request)
            transportation_response = await self.transportation_agent.process_request(request)
            activities_response = await self.activities_agent.process_request(request)
            
            # Combine all responses into a comprehensive plan
            combined_prompt = f"""
            Create a comprehensive trip plan by combining the following information:
            
            Accommodation:
            {accommodation_response['response']}
            
            Transportation:
            {transportation_response['response']}
            
            Activities:
            {activities_response['response']}
            
            Please provide a well-structured, day-by-day itinerary that:
            1. Optimizes the schedule based on locations and timing
            2. Considers travel time between activities
            3. Includes estimated costs
            4. Provides practical tips and recommendations
            5. Suggests backup options for each day
            """
            
            final_response = self.model.generate_content(combined_prompt)
            
            return {
                "status": "success",
                "plan": final_response.text,
                "details": {
                    "accommodation": accommodation_response,
                    "transportation": transportation_response,
                    "activities": activities_response
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            } 