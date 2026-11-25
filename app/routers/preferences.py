from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.configuration.connections import get_default_database
from app.schemas.preference import PreferenceCreate
from app.service.twitch_service import get_game, get_streamer

router = APIRouter(tags=["Preferences"]) # no prefix starts in /users/{user_id}

@router.post("/users/{user_id}/preferences", status_code=201)
async def create_preference(user_id: int, preference: PreferenceCreate):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,)) # Check if the user exists
        if cursor.fetchone() is None: # fetchone() returns None if no record is found
            raise HTTPException(status_code=404, detail="User not found")
           
        if preference.type == "streamer":  # Check that the streamer/game really exists on Twitch before saving it
            twitch_data = get_streamer(preference.name)
            name = twitch_data["login"]
        else:
            twitch_data = get_game(preference.name)
            name = twitch_data["name"]

        cursor.execute(
            "INSERT INTO preferences (user_id, type, name) VALUES (%s, %s, %s)", # Placeholders for the values to be inserted
            (user_id, preference.type, name)
        )
        connection.commit() # Save change permanently to the database
        return {"id": cursor.lastrowid, "user_id": user_id, "type": preference.type, "name": name}
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database

@router.get("/users/{user_id}/preferences")
async def get_preferences(user_id: int):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(dictionary=True, buffered=True) # dictionary=True to get results as dictionaries
    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,)) # Check if the user exists
        if cursor.fetchone() is None: # fetchone() returns None if no record is found
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("SELECT id, type, name FROM preferences WHERE user_id = %s", (user_id,)) # Select all preferences for the user
        return cursor.fetchall() # Return all preferences as a list of dictionaries
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database

@router.delete("/users/{user_id}/preferences/{preference_id}")
async def delete_preference(user_id: int, preference_id: int):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM preferences WHERE id = %s AND user_id = %s", (preference_id, user_id)) # Delete the preference for the user
        if cursor.rowcount == 0: # rowcount returns the number of rows affected by the last execute() call
            raise HTTPException(status_code=404, detail="Preference not found")
        connection.commit() # Save change permanently to the database
        return JSONResponse(
            content={"id": preference_id, "message": "Preference deleted successfully"}, status_code=200
        )
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database