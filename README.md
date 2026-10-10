# Bookmark Manager API
A REST API for saving and organizing web bookmarks. Built with FastAPI as part of my AI Engineering journey (Phase 1).

## Run locally
1. Activate the virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Service health check |
| POST | `/bookmarks` | *(Coming soon)* |
| GET | `/bookmarks` | *(Coming soon)* |
| GET | `/bookmarks/{id}` | *(Coming soon)* |
| DELETE | `/bookmarks/{id}` | *(Coming soon)* |