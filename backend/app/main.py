from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api_router, health_router

app = FastAPI(
    title="High-Fidelity Mock Genesys Service",
    description="A mock API service that realistically simulates Genesys and backend data lookups.",
    version="1.3.0"
)

# --- CORS Configuration ---
# Allow requests from the frontend (Streamlit) and Genesys Cloud domains
origins = [
    "http://localhost:8501",        # Local Streamlit
    "http://127.0.0.1:8501",        # Local Streamlit IP
    "https://mypurecloud.com",      # Genesys Cloud (Example Region)
    "https://apps.mypurecloud.com", # Genesys Apps
    "*",                            # Allow all for development/iframe simplicity (Lock down in Prod)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(api_router)

