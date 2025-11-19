import time
import jwt


async def get_genesys_auth_token(auth_code: str, code_verifier: str) -> str:
    """
    Generates a realistic, but fake, JWT for authentication.
    """
    print(f"Generating mock JWT with auth_code: '{auth_code}' and code_verifier: '{code_verifier}'")
    
    payload = {
        "sub": "user123",
        "name": "Mock User",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iss": "mock-genesys-auth-service"
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    return token

