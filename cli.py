import asyncio
import os
from dotenv import load_dotenv
from src.orchestrator import TripPlannerOrchestrator

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize orchestrator
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        return
        
    orchestrator = TripPlannerOrchestrator(api_key=api_key)
    
    print("\nWelcome to Trip Planner CLI!")
    print("Type 'quit' or 'exit' to end the session\n")
    
    while True:
        # Get user input
        user_input = input("\nWhat would you like to know about your trip? ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
            
        # Process the request
        request = {
            "message": user_input,
            "destination": "",
            "dates": "",
            "preferences": {}
        }
        
        try:
            response = await orchestrator.plan_trip(request)
            if response["status"] == "success":
                print("\nResponse:")
                print(response["plan"])
            else:
                print(f"\nError: {response.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 