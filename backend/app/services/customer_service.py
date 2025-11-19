import random
from faker import Faker
from app.models.schemas import GenesysCustomerData


fake = Faker()


async def get_genesys_customer_data(conversation_id: str) -> GenesysCustomerData:
    """
    Generates realistic, synthetic customer data that mirrors the production service's logic.
    """
    Faker.seed(conversation_id)
    print(f"Generating synthetic data for conversation ID: {conversation_id}")
    
    # Randomly assign a channel to simulate different interaction types
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

    return GenesysCustomerData(
        pcin=pcin,
        bcin=bcin,
        customer_name=customer_name,
        channel=channel,
        ani=ani
    )

