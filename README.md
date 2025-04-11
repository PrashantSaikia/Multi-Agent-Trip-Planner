# Trip Planner Chat

An interactive chat interface for planning trips, powered by OpenAI's GPT model. The application provides detailed travel itineraries with cost breakdowns and activity suggestions.

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
4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the FastAPI server:
```bash
uv run uvicorn src.main:app --reload
```

The chat interface will be available at `http://localhost:8000`

## Deployment

The application is set up for automatic deployment to Heroku using GitHub Actions.

### Prerequisites for Deployment

1. A Heroku account
2. The following secrets set in your GitHub repository:
   - `HEROKU_API_KEY`: Your Heroku API key
   - `HEROKU_APP_NAME`: Your Heroku app name
   - `HEROKU_EMAIL`: Your Heroku account email
   - `OPENAI_API_KEY`: Your OpenAI API key

### Deployment Process

1. Push your changes to the main branch
2. GitHub Actions will automatically:
   - Run tests
   - Deploy to Heroku if tests pass
   - Configure environment variables

## Project Structure

```
src/
├── main.py           # FastAPI application
├── templates/
│   └── chat.html    # Chat interface template
└── static/          # Static assets
```

## Contributing

Feel free to submit issues and enhancement requests!
