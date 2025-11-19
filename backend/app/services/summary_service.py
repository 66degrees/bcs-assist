from app.models.schemas import GenesysCustomerData, PrepPackData


async def generate_summary(customer_data: GenesysCustomerData, prep_pack: PrepPackData) -> str:
    """
    Generates a simple summary based on customer and prep pack data.
    """
    key_items_str = '; '.join([content.get('item', 'N/A') for content in prep_pack.contents[:2]])
    summary = (
        f"Summary for {customer_data.customer_name} (Channel: {customer_data.channel}):\n"
        f"- PCIN: {customer_data.pcin or 'N/A'}, BCIN: {customer_data.bcin or 'N/A'}.\n"
        f"- ANI: {customer_data.ani or 'N/A'}.\n"
        f"- The matched agent prep pack is '{prep_pack.pack_name}'.\n"
        f"- Key items from pack: {key_items_str}."
    )
    return summary

