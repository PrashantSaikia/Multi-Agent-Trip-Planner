# Multi-Agent Trip Planner

A sophisticated trip planning system powered by Gemini 2.0 Flash, featuring multiple specialized agents for comprehensive travel planning.

## Features

- Accommodation recommendations
- Transportation planning
- Activity and sightseeing suggestions
- Comprehensive itinerary generation
- Budget-aware planning
- Personalized recommendations

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Plan a Trip
- **POST** `/plan-trip`
- Request body:
  ```json
  {
    "destination": "Paris",
    "origin": "New York",
    "dates": "2024-07-01 to 2024-07-07",
    "duration": "7 days",
    "budget": "$2000",
    "preferences": {
      "accommodation": "hotel",
      "transportation": "flight"
    },
    "interests": ["museums", "food", "architecture"]
  }
  ```

### Health Check
- **GET** `/health`
- Returns the status of the service

## Project Structure

```
src/
├── agents/
│   ├── base_agent.py
│   ├── accommodation_agent.py
│   ├── transportation_agent.py
│   └── activities_agent.py
├── orchestrator.py
└── main.py
```

## Contributing

Feel free to submit issues and enhancement requests! 