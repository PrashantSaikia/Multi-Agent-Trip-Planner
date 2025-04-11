# Trip Planner Chat

An interactive chat interface for planning trips, powered by Google's Gemini model. The application provides detailed travel itineraries with cost breakdowns and activity suggestions.

## Features

- Interactive chat interface
- Real-time response streaming
- Detailed itinerary generation
- Cost breakdown for activities
- PDF export functionality
- Mobile-responsive design

## Local Development Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies using uv:
   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the Application

Start the FastAPI server:
```bash
uv run uvicorn src.main:app --reload
```

The chat interface will be available at `http://localhost:8000`

## Deployment

### Render Deployment

#### Prerequisites
1. A Render account
2. Set the following environment variables in Render:
   - `GOOGLE_API_KEY`: Your Google API key for Gemini

#### Configuration
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- **Python Version**: 3.11 or higher

## Project Structure

```
src/
├── main.py           # FastAPI application
├── orchestrator.py   # Trip planning orchestration logic
├── templates/
│   └── chat.html    # Chat interface template
└── agents/
    ├── base_agent.py          # Base agent class
    ├── accommodation_agent.py  # Accommodation planning agent
    ├── transportation_agent.py # Transportation planning agent
    └── activities_agent.py     # Activities planning agent
```

## Contributing

Feel free to submit issues and enhancement requests!
