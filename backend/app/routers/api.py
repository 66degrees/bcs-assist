from fastapi import APIRouter
from app.models.schemas import MockAuthPayload, ProcessedConversationResponse
from app.controllers.conversation_controller import ConversationController

router = APIRouter(prefix="/api/v1", tags=["api"])

conversation_controller = ConversationController()


@router.post("/process", response_model=ProcessedConversationResponse)
async def process_conversation(payload: MockAuthPayload):
    """
    Orchestrates the realistic mock flow, now aligned with production data structures.
    """
    return await conversation_controller.process_conversation(payload)

