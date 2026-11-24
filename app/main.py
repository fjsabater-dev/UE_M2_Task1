from fastapi import FastAPI
from app.routers import health, root
# Create the FastAPI application and include the routers
app = FastAPI(
    # Swagger information
    title="Twitch Preferences API",
    description="REST API for managing Twitch user streamers and categories preferences.",
  )

# Include the default router and the health router in the main app
app.include_router(root.router)
app.include_router(health.router)