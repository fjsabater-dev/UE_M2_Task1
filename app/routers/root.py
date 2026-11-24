from fastapi import APIRouter

# Router for the root endpoint
router = APIRouter()

@router.get("/", include_in_schema=False) # hide it from /docs
def welcome():
    "Welcome to the Twitch Preferences API."
    return {
        "name": "Twitch Preferences API",  # API name
        "version": "0.0.0",                # current version
        "documentation": "/docs",          # link to Swagger UI documentation
    }