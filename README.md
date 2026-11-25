# Twitch Preferences API

REST API to manage users and their Twitch preferences, built with FastAPI and MySQL.
Favorite streamers and games will be enriched with data from the Twitch API.

> Work in progress: this README grows with every feature branch.

## Tech stack

- Python and FastAPI
- MySQL
- Twitch API (planned)

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

### 4. Run the API

From the project root:

```bash
fastapi dev app/main.py
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are at `/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | API status |
| POST | `/users` | Create a user |
| GET | `/users` | List users |
| GET | `/users/{user_id}` | Get a user by ID |
| PUT | `/users/{user_id}` | Update a user by ID |
| DELETE | `/users/{user_id}` | Delete a user by ID |

## Project structure

```
app/
├── main.py              # app creation and router registration
├── configuration/       # database connection
├── routers/             # endpoints
└── schemas/             # input validation
sql/                     # database scripts
```

## Documentation

Not yet