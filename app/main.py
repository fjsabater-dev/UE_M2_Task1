from fastapi import FastAPI
from app.routers import health, root, users, preferences, twitch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI application and include the routers
app = FastAPI(
    # Swagger information
    title="Twitch Preferences API",
    description="REST API for managing Twitch user streamers and categories preferences.",
  )

# Include the default router, the health router, the users router, the preferences router and the twitch router in the main app
app.include_router(root.router)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(preferences.router)
app.include_router(twitch.router)