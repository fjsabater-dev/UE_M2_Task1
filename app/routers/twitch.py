from fastapi import APIRouter, HTTPException

from app.configuration.connections import get_default_database
from app.service.twitch_service import get_streamer, get_game

router = APIRouter(tags=["Twitch"]) # no prefix starts in /users/{user_id}

@router.get("/twitch/streamers/{login}")
def read_streamer(login: str):
    return get_streamer(login)

@router.get("/twitch/games/{name}")
def read_game(name: str):
    return get_game(name)

@router.get("/users/{user_id}/streamers")
async def read_user_streamers(user_id: int):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:  # fetchone() returns None if no record is found
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("SELECT name FROM preferences WHERE user_id = %s AND type = 'streamer'",(user_id,),) # Select all preferences for the user
        streamers  = cursor.fetchall() # Return all preferences as a list of dictionaries
    finally:
        cursor.close()
        connection.close()

    result = []
    for streamer in streamers:
        result.append(get_streamer(streamer["name"]))
    return result