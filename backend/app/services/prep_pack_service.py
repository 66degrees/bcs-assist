from faker import Faker
from datetime import date, timedelta
import random

from app.models.schemas import (
    PrepPackData, NetworkRelationship, Kpi, Inhibit, Journey, Complaint,
    ICSResult, Chart, ChartDataPoint, Transaction, ProductRevenue
)

fake = Faker()

def generate_prep_pack_data(customer_id: str) -> PrepPackData:
    """
    Generates a complete, realistic mock dataset for the prep pack dashboard.
    """
    Faker.seed(customer_id)
    
    summary_text = (
        "Acme Corporation is a mid-sized manufacturing company with a strong focus on sustainable practices. "
        "They have been an HSBC customer since 2019 and utilize multiple banking services including commercial accounts, "
        "international payments, and trade finance solutions."
    )

    network_relationship = NetworkRelationship(
        cin="1047382956",
        parent="Acme Corporation PLC",
        md_name="Acme Group",
        md_id="1025",
        linked_businesses=["Acme Manufacturing Ltd", "Acme Distribution Inc"]
    )

    ai_insights = [
        "Acme Corporation shows a positive revenue trend, with Jun revenue increasing by 18% compared to Apr.",
        "Customer is currently using 4 active products, with Retail Payments being the highest revenue generator at £456,000.",
        "Customer has 95% score recommendation for the Global Wallet Product.",
        "There is 1 pending customer complaint that requires immediate attention."
    ]

    kpis = [
        Kpi(title="TOTAL REVENUE", value="£1,256,000", sub_lines=["+0.2%", "from previous quarter"]),
        Kpi(title="ACTIVE PRODUCTS", value="4", sub_lines=["+1", "since last quarter"]),
        Kpi(title="ICS SCORE", value="8.5", sub_lines=["+0.3", "from last assessment"]),
        Kpi(title="AVG. PRODUCT UTILIZATION", value="78.5%", sub_lines=["+3.1%", "from previous quarter"]),
        Kpi(title="SUSTAINABILITY SCORE", value="8.2", sub_lines=["+0.5", "ESG rating improvement"]),
        Kpi(title="CURRENT ACCOUNT TARIFFS", value="£12.50", sub_lines=["month", "standard business plan"]),
        Kpi(title="BIB PAYMENT LIMIT", value="£25,000", sub_lines=["per transaction limit"]),
        Kpi(title="COMPLEX LIMIT", value="£150,000", sub_lines=["approved facility"]),
        Kpi(title="CREDIT LIMIT", value="£75,000", sub_lines=["£22k used", "75% available"]),
        Kpi(title="OUTSTANDING FOLDER NOTES", value="3", sub_lines=["pending", "requires attention"]),
    ]

    inhibits = [
        Inhibit(title="ACH Debit Block", description="All incoming ACH debits", date=date(2024, 1, 15)),
        Inhibit(title="ACH Debit Filter", description="ACH debits from unapproved companies", date=date(2024, 2, 22)),
    ]

    journeys = [
        Journey(title="BIB Registration Request", subtitle="Request for business internet banking registration", status="Completed", date=date(2024, 4, 21)),
        Journey(title="Change of Bank Mandate", subtitle="Request to change mandate", status="Open", date=date(2023, 12, 15)),
    ]

    complaints = [
        Complaint(date=date(2024, 3, 22), description="Dispute regarding foreign exchange fees on large international transaction", status="pending"),
        Complaint(date=date(2023, 9, 8), description="Issues with online banking platform accessibility during system upgrade", status="resolved"),
    ]

    ics_results = [
        ICSResult(date=date(2024, 3, 5), score="7/10", quote="Overall satisfied with services but would appreciate more tailored solutions for our industry-specific challenges."),
        ICSResult(date=date(2024, 1, 12), score="9/10", quote="Excellent service, very responsive team."),
    ]
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_revenue_distribution = Chart(
        title="Monthly Revenue Distribution",
        data=[ChartDataPoint(label=month, value=random.uniform(2000, 5000)) for month in months]
    )

    monthly_revenue_trend = Chart(
        title="Monthly Revenue Trend",
        data=[ChartDataPoint(label=month, value=random.uniform(80, 120)) for month in months]
    )
    
    transaction_volume_summary = [
        Transaction(date=date(2023, 11, 4), product="Retail Payments", amount="£68,400", status="completed"),
        Transaction(date=date(2023, 11, 2), product="Commercial Cards", amount="£23,400", status="completed"),
        Transaction(date=date(2023, 10, 25), product="Retail Payments", amount="£54,720", status="completed"),
        Transaction(date=date(2023, 10, 22), product="Trade Finance", amount="£27,600", status="completed"),
    ]
    
    return PrepPackData(
        summary_text=summary_text,
        network_relationship=network_relationship,
        ai_insights=ai_insights,
        kpis=kpis,
        inhibits=inhibits,
        journeys=journeys,
        complaints=complaints,
        ics_results=ics_results,
        monthly_revenue_distribution=monthly_revenue_distribution,
        monthly_revenue_trend=monthly_revenue_trend,
        transaction_volume_summary=transaction_volume_summary
    )
