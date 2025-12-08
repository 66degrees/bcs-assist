from fastapi import APIRouter
from app.models.schemas import MockAuthPayload, ProcessedConversationResponse
from app.controllers.conversation_controller import ConversationController

router = APIRouter(prefix="/api/v1", tags=["api"])

conversation_controller = ConversationController()


@router.post("/process", response_model=ProcessedConversationResponse)
async def process_conversation(payload: MockAuthPayload):
    """
    Accepts a conversation ID and authentication details, and returns
    a comprehensive prep pack data object for the customer dashboard.
    """
    return await conversation_controller.process_conversation(payload)

