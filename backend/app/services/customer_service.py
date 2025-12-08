import random
import os
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
    
    customer_id = f"customer_{fake.uuid4()}"
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

