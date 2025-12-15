import random
import os
import requests
from faker import Faker
from app.models.schemas import GenesysCustomerData
from dotenv import load_dotenv

load_dotenv()
fake = Faker()


async def get_genesys_customer_data(conversation_id: str, access_token: str) -> GenesysCustomerData:
    """
    Simulates fetching customer data from the Genesys Cloud API.
    In a real application, this function would use the access token to make an
    authenticated API request to a Genesys endpoint.
    """
    genesys_api_url = os.getenv("GENESYS_API_URL")
    
    print("--- Simulating Genesys Customer Data Fetch ---")
    print(f"Genesys API URL: {genesys_api_url}")
    print(f"Using Access Token: {access_token[:15]}...")
    print(f"Fetching data for Conversation ID: {conversation_id}")
    print("--> In a real app, we would make a GET request to a Genesys API endpoint.")

    # Generate realistic, synthetic customer data
    Faker.seed(conversation_id)
    print("--> Generating synthetic data for demonstration.")
    
    # Map to BigQuery customer ID format (CUST_000001 to CUST_000500)
    # Use hash of conversation_id to get consistent customer mapping
    import hashlib
    hash_obj = hashlib.md5(conversation_id.encode())
    hash_int = int(hash_obj.hexdigest()[:8], 16)
    customer_num = (hash_int % 500) + 1  # 1 to 500
    customer_id = f"CUST_{customer_num:06d}"
    print(f"--> Mapped conversation to BigQuery customer: {customer_id}")
    channel = random.choice(['voice', 'message', 'email'])
    customer_name = fake.name()
    ani = fake.phone_number() if channel == 'voice' else None
    pcin = None
    bcin = None

    # Simulate channel-specific attributes
    if channel == 'voice':
        if random.random() > 0.5:  # Simulate authenticated caller
            pcin = f"pcin_{fake.uuid4()}"
            bcin = f"bcin_{fake.uuid4()}"
        # else: Anonymous caller, no PCIN/BCIN
    elif channel == 'message':
        pcin = f"subclaim_{fake.uuid4()}"

    print("--- Mock Customer Data Fetch Complete ---")
    return GenesysCustomerData(
        customer_id=customer_id,
        pcin=pcin,
        bcin=bcin,
        customer_name=customer_name,
        channel=channel,
        ani=ani
    )


# --- Real Implementation (Commented Out) ---
# async def get_real_genesys_customer_data(conversation_id: str, access_token: str) -> GenesysCustomerData:
#     """
#     Fetches conversation details from Genesys Cloud API to identify the customer.
#     """
#     region = os.getenv("GENESYS_REGION", "mypurecloud.com")
#     api_url = f"https://api.{region}/api/v2/conversations/{conversation_id}"
#     
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
# 
#     try:
#         print(f"--- Fetching Conversation Details from: {api_url} ---")
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         
#         # Parse the conversation data to find the customer/external participant
#         participants = data.get("participants", [])
#         
#         # Placeholder logic: Find the first participant with 'purpose' == 'customer' or 'external'
#         # Adjust logic based on actual Genesys interaction data structure
#         customer_participant = next(
#             (p for p in participants if p.get("purpose") in ["customer", "external"]), 
#             None
#         )
#         
#         if not customer_participant:
#             raise ValueError("No customer participant found in conversation.")
# 
#         # Extract attributes - keys depend on your specific IVR/Flow setup
#         attributes = customer_participant.get("attributes", {})
#         
#         customer_id = customer_participant.get("id")
#         pcin = attributes.get("pcin") or attributes.get("PCIN")
#         bcin = attributes.get("bcin") or attributes.get("BCIN")
#         customer_name = customer_participant.get("name", "Unknown Customer")
#         ani = customer_participant.get("ani")
#         
#         # Determine channel (simplified)
#         # In reality, might need to check media types present on the participant
#         channel = "voice" # Default or derive from 'calls', 'chats', etc. keys
#         
#         print(f"--- Customer Identified: {customer_name} (ID: {customer_id}) ---")
#         
#         return GenesysCustomerData(
#             customer_id=customer_id,
#             pcin=pcin,
#             bcin=bcin,
#             customer_name=customer_name,
#             channel=channel,
#             ani=ani
#         )
#         
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching Genesys customer data: {e}")
#         raise
