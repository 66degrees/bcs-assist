import requests
import os
from typing import Dict, Any

# It's a good practice to have the backend URL configurable
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1_PREFIX = "/api/v1"

def get_prep_pack_data(conversation_id: str, auth_code: str, code_verifier: str) -> Dict[str, Any]:
    """
    Calls the backend to get the prep pack data for the dashboard.
    """
    endpoint = f"{BACKEND_URL}{API_V1_PREFIX}/process"
    
    payload = {
        "conversationId": conversation_id,
        "authorizationCode": auth_code,
        "codeVerifier": code_verifier,
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.RequestException as e:
        # In a real app, you'd want more robust error handling and logging
        print(f"An error occurred while calling the backend: {e}")
        return None
