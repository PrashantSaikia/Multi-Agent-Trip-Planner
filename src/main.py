from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from .orchestrator import TripPlannerOrchestrator
import os
from dotenv import load_dotenv
import json
import asyncio
from pathlib import Path

# Load environment variables
load_dotenv()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Multi-Agent Trip Planner")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates and static files
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "src" / "static")), name="static")

# Initialize the orchestrator with API key
orchestrator = TripPlannerOrchestrator(api_key=os.getenv("GEMINI_API_KEY"))

# Keep track of active connections
active_connections: List[WebSocket] = []

class TripRequest(BaseModel):
    destination: str
    origin: Optional[str] = None
    dates: str
    duration: Optional[str] = None
    budget: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    interests: Optional[Dict[str, Any]] = None

@app.get("/")
async def chat_interface(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"New WebSocket connection attempt")
    try:
        await websocket.accept()
        print("WebSocket connection accepted")
        active_connections.append(websocket)
        print(f"Total active connections: {len(active_connections)}")
        
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received raw data: {data}")
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                print(f"Processed message: {user_message}")
                
                # Process the message using the orchestrator
                try:
                    # Convert the chat message into a trip request format
                    trip_request = {
                        "message": user_message,
                        "destination": "",
                        "dates": "",
                        "preferences": {}
                    }
                    
                    # Get response from the orchestrator
                    response = await orchestrator.plan_trip(trip_request)
                    print(f"Got response from orchestrator: {response['status']}")
                    
                    if response["status"] == "error":
                        await websocket.send_json({
                            "message": f"I encountered an error: {response.get('message', 'Unknown error')}"
                        })
                    else:
                        await websocket.send_json({"type": "start"})
                        
                        response_text = response.get("plan", "I'm sorry, I couldn't process your request.")
                        
                        # Stream the response with proper accumulation
                        accumulated_text = ""
                        # Split into sentences for smoother streaming
                        sentences = response_text.replace('\n', '\n ').split('. ')
                        
                        for i, sentence in enumerate(sentences):
                            if websocket not in active_connections:
                                break
                                
                            # Add period back except for last sentence
                            if i < len(sentences) - 1:
                                sentence += '.'
                                
                            accumulated_text += sentence + ' '
                            
                            await websocket.send_json({
                                "type": "stream",
                                "message": accumulated_text
                            })
                            await asyncio.sleep(0.1)  # Slightly longer delay for readability
                        
                        if websocket in active_connections:
                            await websocket.send_json({"type": "end"})
                    
                except Exception as e:
                    print(f"Error in message processing: {str(e)}")
                    if websocket in active_connections:
                        await websocket.send_json({
                            "message": f"I encountered an error: {str(e)}"
                        })
                    
            except WebSocketDisconnect:
                print("Client disconnected")
                break
            except Exception as e:
                print(f"Error in message loop: {str(e)}")
                break
                
    except Exception as e:
        print(f"Error in connection setup: {str(e)}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()

@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    try:
        # Convert Pydantic model to dict
        request_dict = request.dict()
        
        # Get the trip plan
        result = await orchestrator.plan_trip(request_dict)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 