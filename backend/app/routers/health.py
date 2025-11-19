from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "High-Fidelity Mock Genesys Service is running."}

