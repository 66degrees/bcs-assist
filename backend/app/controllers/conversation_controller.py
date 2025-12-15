from app.models.schemas import MockAuthPayload, ProcessedConversationResponse
from app.services.auth_service import get_genesys_auth_token
from app.services.customer_service import get_genesys_customer_data
from app.services.prep_pack_service import generate_prep_pack_data


class ConversationController:
    """
    Controller for handling conversation processing logic.
    """

    @staticmethod
    async def process_conversation(payload: MockAuthPayload) -> ProcessedConversationResponse:
        """
        Orchestrates the flow of authenticating, fetching customer data,
        and generating the full prep pack data for the dashboard.
        """
        #  Authenticate with Genesys to get an access token
        access_token = await get_genesys_auth_token(
            auth_code=payload.authorizationCode,
            code_verifier=payload.codeVerifier
        )
        
        #  Get customer data from Genesys using the conversation ID
        customer_data = await get_genesys_customer_data(
            conversation_id=payload.conversationId,
            access_token=access_token
        )
        
        #  Generate the full prep pack data for the dashboard
        prep_pack_data = generate_prep_pack_data(
            customer_id=customer_data.customer_id
        )
        
        # Return the consolidated response
        return ProcessedConversationResponse(
            prep_pack_data=prep_pack_data
        )

