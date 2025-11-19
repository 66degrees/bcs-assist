from pydantic import BaseModel
from typing import List, Optional, Dict, Any


# --- API Request Models ---
class MockAuthPayload(BaseModel):
    conversationId: str
    authorizationCode: str
    codeVerifier: str


# --- Data Models ---
class GenesysCustomerData(BaseModel):
    pcin: Optional[str] = None
    bcin: Optional[str] = None
    customer_name: str
    channel: str
    ani: Optional[str] = None


class PrepPackData(BaseModel):
    pack_name: str
    contents: List[Dict[str, Any]]


# --- API Response Models ---
class ProcessedConversationResponse(BaseModel):
    customer_data: GenesysCustomerData
    prep_pack: PrepPackData
    summary: str

