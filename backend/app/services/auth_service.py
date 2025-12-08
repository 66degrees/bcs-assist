import time
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


async def get_genesys_auth_token(auth_code: str, code_verifier: str) -> str:
    """
    Simulates the PKCE token exchange with Genesys Cloud.
    In a real application, this function would make a POST request to the
    Genesys token endpoint with the authorization code and code verifier.
    """
    client_id = os.getenv("GENESYS_CLIENT_ID")
    client_secret = os.getenv("GENESYS_CLIENT_SECRET")
    auth_url = os.getenv("GENESYS_AUTH_URL")

    print("--- Simulating Genesys PKCE Token Exchange ---")
    print(f"Auth URL: {auth_url}")
    print(f"Client ID: {client_id}")
    print(f"Received Auth Code: {auth_code}")
    print(f"Received Code Verifier: {code_verifier}")
    print("--> In a real app, we would now send these to Genesys to get a real token.")
    
    # For now, generate a realistic, but fake, JWT for authentication.
    print("--> Generating a mock JWT for demonstration purposes.")
    payload = {
        "sub": "user123",
        "name": "Mock User",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iss": "mock-genesys-auth-service"
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    print("--- Mock Token Exchange Complete ---")
    return token

