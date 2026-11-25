from fastapi import APIRouter
from app.configuration.connections import get_default_database
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", status_code=201)
async def create_user(user: UserCreate):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor()
    try:
        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)", # Placeholders for the values to be inserted
            (user.username, user.email, user.age)
        )
        connection.commit() # Save change permanently to the database
        return {"id": cursor.lastrowid, "username": user.username, "email": user.email, "age": user.age}
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database

@router.get("")
async def get_users():
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(dictionary=True) # dictionary=True to get results as dictionaries
    try:
        cursor.execute("SELECT id, username, email, age FROM users") # Select all users from the database
        return cursor.fetchall() # Return all users as a list of dictionaries
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database