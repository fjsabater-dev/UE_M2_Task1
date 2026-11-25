import os, requests # Read the .env file to get the Twitch API credentials and make HTTP requests to the Twitch API
from fastapi import HTTPException

TOKEN_URL = "https://id.twitch.tv/oauth2/token" # Twitch API endpoint to get an access token
API_URL = "https://api.twitch.tv/helix" # Twitch API endpoint to get user information
TIMEOUT = 10 # seconds

_access_token = None # Store the access token in memory to avoid requesting it multiple times

def get_access_token():
    global _access_token
    if _access_token is not None: # If the access token is already stored in memory, return it
        return _access_token

    # Get the Twitch API credentials from the environment variables
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")

    if not client_id or not client_secret: # If the credentials are not set, raise an error
        raise HTTPException(status_code=503, detail="Twitch API credentials are not configured. Service unavailable")

    try:
        # Request an access token from the Twitch API
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            },
            timeout=TIMEOUT
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Twitch API request timed out")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="Twitch API request failed")
    
    if response.status_code != 200: # If the response is not successful, raise an error
        raise HTTPException(status_code=502, detail="Failed to get access token from Twitch API")

    # Save the access token in memory and return it
    _access_token = response.json().get("access_token")
    return _access_token

def twitch_get(endpoint: str, params: dict, retry: bool = True):
    global _access_token
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Client-Id": os.getenv("TWITCH_CLIENT_ID"),
    }

    try:
        response = requests.get(f"{API_URL}/{endpoint}", headers=headers, params=params, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Twitch API request timed out")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="Twitch API request failed")

    if response.status_code == 401 and retry: # If the access token is invalid, get a new one and retry
        _access_token = None # Clear the stored access token
        return twitch_get(endpoint, params, retry=False) # Retry the request with a new access token

    if response.status_code != 200: # If the response is not successful, raise an error
        raise HTTPException(status_code=502, detail="Unexpected response from Twitch API")
    return response.json()["data"] # Return the JSON response from the Twitch API in a "data" list

def get_streamer(login: str):
    users = twitch_get("users", {"login": login}) # Get user information from the Twitch API
    if not users: # If no user is found, raise an error
        raise HTTPException(status_code=404, detail="Streamer not found")
    user = users[0] # Get the first user from the list

    streams = twitch_get("streams", {"user_id": user["id"]}) # Get stream information from the Twitch API
    stream = None
    if streams: # If the user is currently streaming, get the stream information
        stream = {
            "title": streams[0]["title"],
            "game_name": streams[0]["game_name"],
            "viewer_count": streams[0]["viewer_count"],
        }

    return {
        "login": user["login"],
        "display_name": user["display_name"],
        "is_live": stream is not None,
    }

def get_game(name: str):
    games = twitch_get("games", {"name": name})

    if not games:
         raise HTTPException(status_code=404, detail="Game not found on Twitch")
    game = games[0] # Get the first game from the list

    # Return only the fields we need
    return {
        "id": game["id"],
        "name": game["name"],
    }