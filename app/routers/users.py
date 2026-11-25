from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.configuration.connections import get_default_database
from app.schemas.user import UserCreate, UserUpdate

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

@router.get("/{user_id}")
async def get_user(user_id: int):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(dictionary=True) # dictionary=True to get results as dictionaries
    try:
        cursor.execute("SELECT id, username, email, age FROM users WHERE id = %s", (user_id,)) # Select user by ID
        user = cursor.fetchone() # Fetch the user from the database
        if user is None: # If no user is found, raise an HTTP 404 error
            raise HTTPException(status_code=404, detail="User not found")
        return user # Return the user as a dictionary
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    db = get_default_database()
    connection = await db.get_db_connection() # "await" because the method is async
    cursor = connection.cursor(buffered=True) # buffered=True to allow multiple queries on the same connection to avoid "Unread result found" error
    try:
        update_fields = []
        update_values = []
        if user.username is not None:
            update_fields.append("username = %s")
            update_values.append(user.username)
        if user.email is not None:
            update_fields.append("email = %s")
            update_values.append(user.email)
        if user.age is not None:
            update_fields.append("age = %s")
            update_values.append(user.age)
        
        if not update_fields: # If no fields are provided for update, raise an HTTP 400 error
            raise HTTPException(status_code=400, detail="No fields provided for update")

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,)) # Check if the user exists in the database
        if cursor.fetchone() is None: # fetchone() returns None if no record is found
            raise HTTPException(status_code=404, detail="User not found")

        update_values.append(user_id) # Add user_id to the end of the values list
        cursor.execute(f"UPDATE `users` SET {', '.join(update_fields)} WHERE id= %s;", tuple(update_values)) # Execute the update query
        connection.commit() # Save change permanently to the database

        return JSONResponse(
            content={"id": user_id, "message": "User updated successfully"}, status_code=200
            ) # Only return the user ID and a success message, not the updated user info that can be empty or null if the user didn't provide any fields to update
    finally:
        cursor.close() # Close the cursor to free up resources
        connection.close() # Close the connection to the database