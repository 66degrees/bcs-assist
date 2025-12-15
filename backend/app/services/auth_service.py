import time
import jwt
import os
import requests
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


# --- Real Implementation (Commented Out) ---
# async def get_real_genesys_auth_token(auth_code: str, code_verifier: str) -> str:
#     """
#     Exchanges the auth code and code verifier for an access token from Genesys Cloud.
#     """
#     client_id = os.getenv("GENESYS_CLIENT_ID")
#     client_secret = os.getenv("GENESYS_CLIENT_SECRET")
#     redirect_uri = os.getenv("GENESYS_REDIRECT_URI")
#     
#     # Determine region from env or default to mypurecloud.com
#     region = os.getenv("GENESYS_REGION", "mypurecloud.com")
#     token_url = f"https://login.{region}/oauth/token"
# 
#     payload = {
#         "grant_type": "authorization_code",
#         "code": auth_code,
#         "redirect_uri": redirect_uri,
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "code_verifier": code_verifier
#     }
# 
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
# 
#     try:
#         print(f"--- POSTing to Genesys Token Endpoint: {token_url} ---")
#         response = requests.post(token_url, data=payload, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         
#         access_token = data.get("access_token")
#         print("--- Successfully retrieved Access Token ---")
#         return access_token
#         
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching Genesys token: {e}")
#         if e.response:
#             print(f"Response Body: {e.response.text}")
#         raise
