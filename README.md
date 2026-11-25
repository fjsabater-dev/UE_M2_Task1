# Twitch Preferences API

REST API to manage users and their Twitch preferences, built with FastAPI and MySQL.
Favorite streamers and games will be enriched with data from the Twitch API.

> Work in progress: this README grows with every feature branch.

## Tech stack

- Python and FastAPI
- MySQL
- Twitch API

## Getting started

### 1. Set up the database

Create a database called `twitch_api` and a MySQL user with access to it (using `root` is not recommended). Then run `sql/twitch_table.sql` to create the tables, from MySQL Workbench or the `mysql` client.

### 2. Set up the environment

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
source .venv/Scripts/activate   # Windows (Git Bash)

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the credentials

Copy `.env.template` to `.env` and fill in your values. `.env` is ignored for git.

| Variable | Description |
|----------|-------------|
| `DB_HOST` | MySQL host (usually `localhost`) |
| `DB_USER` | MySQL user |
| `DB_PASSWORD` | Password of that user |
| `DB_NAME` | Database name (`twitch_api`) |
| `TWITCH_CLIENT_ID`     | Client ID of your Twitch app (dev.twitch.tv/console) |
| `TWITCH_CLIENT_SECRET` | Client Secret of your Twitch app |

Without the Twitch variables the API still runs, but the Twitch endpoints answer `503`.

### 4. Run the API

From the project root:

```bash
fastapi dev app/main.py
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are at `/docs`.

## Endpoints

| Method | Path                                         | Description                     |
|--------|----------------------------------------------|---------------------------------|
| GET    | `/health`                                    | Health check                    |
| POST   | `/users`                                     | Create a user                   |
| GET    | `/users`                                     | List users                      |
| GET    | `/users/{user_id}`                           | Get a user                      |
| PUT    | `/users/{user_id}`                           | Update a user (partial fields)  |
| DELETE | `/users/{user_id}`                           | Delete a user (and preferences) |
| POST   | `/users/{user_id}/preferences`               | Add a streamer/game preference  |
| GET    | `/users/{user_id}/preferences`               | List a user's preferences       |
| DELETE | `/users/{user_id}/preferences/{preference_id}` | Delete a preference           |
| GET    | `/users/{user_id}/streamers`                 | Live status of the user's favorite streamers |
| GET    | `/twitch/streamers/{login}`                  | Streamer info and live status   |
| GET    | `/twitch/games/{name}`                       | Game info                       |

### Error codes

| Code | Meaning |
|------|---------|
| 404  | User, preference, streamer or game not found |
| 422  | Invalid request body or parameters |
| 502  | Twitch failed or rejected our credentials |
| 503  | Twitch credentials not configured |
| 504  | Twitch did not answer in time |

## Project structure

```
app/
├── main.py              # app creation and router registration
├── configuration/       # database connection
├── routers/             # endpoints
├── service/             # Twitch API client (token + requests)
└── schemas/             # Pydantic models (Input validation)
sql/                     # database scripts
```

## Documentation

Not yet