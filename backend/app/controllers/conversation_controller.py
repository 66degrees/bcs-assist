from app.models.schemas import MockAuthPayload, ProcessedConversationResponse
from app.services import (
    get_genesys_auth_token,
    get_genesys_customer_data,
    get_prep_pack_data,
    generate_summary
)


class ConversationController:
    """
    Controller for handling conversation processing logic.
    """

    @staticmethod
    async def process_conversation(payload: MockAuthPayload) -> ProcessedConversationResponse:
        """
        Orchestrates the realistic mock flow, now aligned with production data structures.
        """
        # Authenticate with Genesys
        access_token = await get_genesys_auth_token(
            auth_code=payload.authorizationCode,
            code_verifier=payload.codeVerifier
        )
        
        # Get customer data
        customer_data = await get_genesys_customer_data(payload.conversationId)
        
        # Get prep pack data
        prep_pack = await get_prep_pack_data(customer_data)
        
        # Generate summary
        summary = await generate_summary(customer_data, prep_pack)
        
        return ProcessedConversationResponse(
            customer_data=customer_data,
            prep_pack=prep_pack,
            summary=summary
        )

