# UE_M2_Task1
REST API with FastAPI/Flask and Twitch Integration


> Work in progress: this README grows with every feature branch.

## Tech stack

- Python and FastAPI
- MySQL (planned)
- Twitch API (planned)

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
source .venv/Scripts/activate   # Windows (Git Bash)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
fastapi dev app/main.py
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are at `/docs`.

## Project structure

```
app/
├── main.py       # app creation and router registration
└── routers/      # endpoints (HTTP layer)
```

## Documentation

Not yet