from fastapi import APIRouter

# Router for the /health endpoint
router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    "Checks the health of the API."

    # returns a JSON response indicating the API is healthy
    return {"status": "ok"}