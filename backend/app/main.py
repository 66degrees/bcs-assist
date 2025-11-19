from fastapi import FastAPI
from app.routers import api_router, health_router

app = FastAPI(
    title="High-Fidelity Mock Genesys Service",
    description="A mock API service that realistically simulates Genesys and backend data lookups.",
    version="1.3.0"
)

# Include routers
app.include_router(health_router)
app.include_router(api_router)

