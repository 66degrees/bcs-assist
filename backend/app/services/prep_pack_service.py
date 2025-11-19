import random
from app.models.schemas import PrepPackData, GenesysCustomerData


# --- Mock Database for Prep Packs (Aligned with Production Model) ---
PREP_PACK_DB = {
    "CA": PrepPackData(
        pack_name="California Welcome Pack",
        contents=[
            {"item": "Info on local regulations"},
            {"item": "Special West Coast offers"},
            {"item": "Contact info for CA support team"}
        ]
    ),
    "NY": PrepPackData(
        pack_name="New York Welcome Pack",
        contents=[
            {"item": "Info on NY-specific services"},
            {"item": "Details on East Coast shipping times"},
            {"item": "Contact info for NY support team"}
        ]
    ),
    "DEFAULT": PrepPackData(
        pack_name="Standard Welcome Pack",
        contents=[
            {"item": "General company information"},
            {"item": "Standard offers"},
            {"item": "National support line"}
        ]
    ),
}


async def get_prep_pack_data(customer_data: GenesysCustomerData) -> PrepPackData:
    """
    Matches customer data to a prep pack from the mock database based on a simulated location.
    """
    # We don't have a state in the new model, so let's simulate a lookup
    # In a real scenario, you might derive location from ANI or another attribute.
    # For the mock, we'll just assign a random one for variety.
    mock_state = random.choice(["CA", "NY", "FL"])  # FL will cause a fallback to DEFAULT
    print(f"Matching prep pack for customer using mock state: {mock_state}")
    return PREP_PACK_DB.get(mock_state, PREP_PACK_DB["DEFAULT"])

