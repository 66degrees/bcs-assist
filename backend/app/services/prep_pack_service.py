from faker import Faker
from datetime import date, timedelta
import random
import os
from typing import List, Optional
from google.cloud import bigquery

from app.models.schemas import (
    PrepPackData, NetworkRelationship, Kpi, Inhibit, Journey, Complaint,
    ICSResult, Chart, ChartDataPoint, Transaction
)

fake = Faker()

# BigQuery configuration
PROJECT_ID = os.getenv("BQ_PROJECT_ID", "ai-ml-team-sandbox")
DATASET_ID = os.getenv("BQ_DATASET_ID", "HSBC_mock_reuben")

def fetch_complaints_from_bigquery(customer_id: str) -> List[Complaint]:
    """Fetch complaints data from BigQuery"""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        query = f"""
            SELECT complaint_date, description, status
            FROM `{PROJECT_ID}.{DATASET_ID}.complaints`
            WHERE customer_id = @customer_id
            ORDER BY complaint_date DESC
            LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        complaints = []
        for row in results:
            complaints.append(Complaint(
                date=row.complaint_date,
                description=row.description or "No description available",
                status=row.status or "unknown"
            ))
        
        return complaints
    except Exception as e:
        print(f"Error fetching complaints from BigQuery: {e}")
        return []

def fetch_inhibits_from_bigquery(customer_id: str) -> List[Inhibit]:
    """Fetch inhibits data from BigQuery"""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        query = f"""
            SELECT inhibit_name, inhibit_date, inhibit_desc
            FROM `{PROJECT_ID}.{DATASET_ID}.inhibits`
            WHERE customer_id = @customer_id
            ORDER BY inhibit_date DESC
            LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        inhibits = []
        for row in results:
            inhibits.append(Inhibit(
                title=row.inhibit_name or "Unknown Inhibit",
                description=row.inhibit_desc or "No description available",
                date=row.inhibit_date
            ))
        
        return inhibits
    except Exception as e:
        print(f"Error fetching inhibits from BigQuery: {e}")
        return []

def fetch_journeys_from_bigquery(customer_id: str) -> List[Journey]:
    """Fetch journeys data from BigQuery"""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        query = f"""
            SELECT journey_name, journey_desc, journey_date, status
            FROM `{PROJECT_ID}.{DATASET_ID}.journeys`
            WHERE customer_id = @customer_id
            ORDER BY journey_date DESC
            LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        journeys = []
        for row in results:
            journeys.append(Journey(
                title=row.journey_name or "Unknown Journey",
                subtitle=row.journey_desc or "No description available",
                status=row.status or "unknown",
                date=row.journey_date
            ))
        
        return journeys
    except Exception as e:
        print(f"Error fetching journeys from BigQuery: {e}")
        return []

def fetch_ics_results_from_bigquery(customer_id: str) -> List[ICSResult]:
    """Fetch ICS results data from BigQuery"""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        query = f"""
            SELECT ics_score, ics_summary, score_date
            FROM `{PROJECT_ID}.{DATASET_ID}.ics_results`
            WHERE customer_id = @customer_id
            ORDER BY score_date DESC
            LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        ics_results = []
        for row in results:
            ics_results.append(ICSResult(
                date=row.score_date,
                score=row.ics_score or "N/A",
                quote=row.ics_summary or "No feedback available"
            ))
        
        return ics_results
    except Exception as e:
        print(f"Error fetching ICS results from BigQuery: {e}")
        return []

def generate_prep_pack_data(customer_id: str) -> PrepPackData:
    """
    Fetches prep pack data from BigQuery where available, falls back to mock data for others.
    """
    Faker.seed(customer_id)
    
    print(f"🔍 Fetching prep pack data for customer: {customer_id}")
    print(f"   Customer ID format matches BigQuery tables (CUST_XXXXXX)")
    
    # Fetch real data from BigQuery tables
    print("Fetching complaints from BigQuery...")
    complaints = fetch_complaints_from_bigquery(customer_id)
    if not complaints:
        print("No complaints found in BigQuery, using fallback mock data")
        complaints = [
            Complaint(date=date(2024, 3, 22), description="Dispute regarding foreign exchange fees on large international transaction", status="pending"),
            Complaint(date=date(2023, 9, 8), description="Issues with online banking platform accessibility during system upgrade", status="resolved"),
        ]
    else:
        print(f"Found {len(complaints)} complaints in BigQuery")
    
    print("Fetching inhibits from BigQuery...")
    inhibits = fetch_inhibits_from_bigquery(customer_id)
    if not inhibits:
        print("No inhibits found in BigQuery, using fallback mock data")
        inhibits = [
            Inhibit(title="ACH Debit Block", description="All incoming ACH debits", date=date(2024, 1, 15)),
            Inhibit(title="ACH Debit Filter", description="ACH debits from unapproved companies", date=date(2024, 2, 22)),
        ]
    else:
        print(f"Found {len(inhibits)} inhibits in BigQuery")
    
    print("Fetching journeys from BigQuery...")
    journeys = fetch_journeys_from_bigquery(customer_id)
    if not journeys:
        print("No journeys found in BigQuery, using fallback mock data")
        journeys = [
            Journey(title="BIB Registration Request", subtitle="Request for business internet banking registration", status="Completed", date=date(2024, 4, 21)),
            Journey(title="Change of Bank Mandate", subtitle="Request to change mandate", status="Open", date=date(2023, 12, 15)),
        ]
    else:
        print(f"Found {len(journeys)} journeys in BigQuery")
    
    print("Fetching ICS results from BigQuery...")
    ics_results = fetch_ics_results_from_bigquery(customer_id)
    if not ics_results:
        print("No ICS results found in BigQuery, using fallback mock data")
        ics_results = [
            ICSResult(date=date(2024, 3, 5), score="7/10", quote="Overall satisfied with services but would appreciate more tailored solutions for our industry-specific challenges."),
            ICSResult(date=date(2024, 1, 12), score="9/10", quote="Excellent service, very responsive team."),
        ]
    else:
        print(f"Found {len(ics_results)} ICS results in BigQuery")
    
    # Use mock data for metrics not in BigQuery tables
    summary_text = (
        f"Customer {customer_id} is a valued HSBC client with comprehensive banking relationships. "
        "The customer utilizes multiple banking services including commercial accounts, "
        "international payments, and trade finance solutions."
    )

    network_relationship = NetworkRelationship(
        cin="1047382956",
        parent="Acme Corporation PLC",
        md_name="Acme Group", 
        md_id="1025",
        linked_businesses=["Acme Manufacturing Ltd", "Acme Distribution Inc"]
    )

    # Generate AI insights based on real data counts
    complaints_count = len(complaints)
    ai_insights = [
        f"Customer shows stable relationship with {complaints_count} complaint(s) in recent history.",
        f"Customer has {len(inhibits)} active inhibit(s) requiring monitoring.",
        f"Customer journey status shows {len([j for j in journeys if j.status.lower() == 'completed'])} completed and {len([j for j in journeys if j.status.lower() != 'completed'])} pending processes.",
        f"Latest ICS scores indicate {ics_results[0].score if ics_results else 'N/A'} satisfaction rating."
    ]

    # Mock KPIs (these don't have corresponding BigQuery tables)
    kpis = [
        Kpi(title="TOTAL REVENUE", value="£1,256,000", sub_lines=["+0.2%", "from previous quarter"]),
        Kpi(title="ACTIVE PRODUCTS", value="4", sub_lines=["+1", "since last quarter"]),
        Kpi(title="ICS SCORE", value=ics_results[0].score if ics_results else "N/A", sub_lines=["+0.3", "from last assessment"]),
        Kpi(title="AVG. PRODUCT UTILIZATION", value="78.5%", sub_lines=["+3.1%", "from previous quarter"]),
        Kpi(title="SUSTAINABILITY SCORE", value="8.2", sub_lines=["+0.5", "ESG rating improvement"]),
        Kpi(title="CURRENT ACCOUNT TARIFFS", value="£12.50", sub_lines=["month", "standard business plan"]),
        Kpi(title="BIB PAYMENT LIMIT", value="£25,000", sub_lines=["per transaction limit"]),
        Kpi(title="COMPLEX LIMIT", value="£150,000", sub_lines=["approved facility"]),
        Kpi(title="CREDIT LIMIT", value="£75,000", sub_lines=["£22k used", "75% available"]),
        Kpi(title="OUTSTANDING COMPLAINTS", value=str(complaints_count), sub_lines=["active", "requires attention"]),
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
    
    print("Prep pack data compilation complete!")
    
    return PrepPackData(
        summary_text=summary_text,
        network_relationship=network_relationship,
        ai_insights=ai_insights,
        kpis=kpis,
        inhibits=inhibits,  # From BigQuery
        journeys=journeys,  # From BigQuery
        complaints=complaints,  # From BigQuery
        ics_results=ics_results,  # From BigQuery
        monthly_revenue_distribution=monthly_revenue_distribution,  # Mock data
        monthly_revenue_trend=monthly_revenue_trend,  # Mock data
        transaction_volume_summary=transaction_volume_summary  # Mock data
    )


# --- Real Implementation (Commented Out) ---
# def fetch_prep_pack_from_bigquery(customer_id: str) -> PrepPackData:
#     """
#     Fetches prep pack data from BigQuery tables based on the customer_id.
#     """
#     client = bigquery.Client() # Uses GOOGLE_APPLICATION_CREDENTIALS
#     
#     project_id = os.getenv("BQ_PROJECT_ID")
#     dataset_id = os.getenv("BQ_DATASET_ID")
#     # Assuming a main table for summary info and related tables/JSON columns for lists
#     # Update table names as needed
#     table_id = f"{project_id}.{dataset_id}.customer_prep_packs"
# 
#     query = f"""
#         SELECT *
#         FROM `{table_id}`
#         WHERE customer_id = @customer_id
#         LIMIT 1
#     """
#     
#     job_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
#         ]
#     )
# 
#     query_job = client.query(query, job_config=job_config)
#     results = list(query_job.result())
# 
#     if not results:
#         # Fallback or raise error? For now, return a default mock or raise
#         raise ValueError(f"No prep pack data found for customer_id: {customer_id}")
# 
#     row = results[0]
# 
#     # Mapping BigQuery Row to Pydantic Models
#     # This assumes the BQ table has columns matching these names or contains JSON strings
#     
#     # Example mapping (needs to be adjusted based on actual schema):
#     
#     return PrepPackData(
#         summary_text=row.get("summary_text", "No summary available."),
#         
#         # Complex objects might need manual construction or JSON parsing if stored as STRUCT/JSON
#         network_relationship=NetworkRelationship(
#             cin=row.get("cin", ""),
#             parent=row.get("parent_company", ""),
#             md_name=row.get("md_name", ""),
#             md_id=row.get("md_id", ""),
#             linked_businesses=row.get("linked_businesses", []) # Assumes ARRAY<STRING>
#         ),
#         
#         ai_insights=row.get("ai_insights", []), # Assumes ARRAY<STRING>
#         
#         # For lists of objects (KPIs, etc.), you might query joined tables or parse JSON/STRUCT arrays
#         # Here we assume a simplified retrieval or that the row contains the necessary data structure
#         kpis=[
#             Kpi(title=k.get('title'), value=k.get('value'), sub_lines=k.get('sub_lines', [])) 
#             for k in row.get("kpis", [])
#         ],
#         
#         inhibits=[
#             Inhibit(**i) for i in row.get("inhibits", [])
#         ],
#         
#         journeys=[
#             Journey(**j) for j in row.get("journeys", [])
#         ],
#         
#         complaints=[
#             Complaint(**c) for c in row.get("complaints", [])
#         ],
#         
#         ics_results=[
#             ICSResult(**r) for r in row.get("ics_results", [])
#         ],
#         
#         # Charts might need specific construction
#         monthly_revenue_distribution=Chart(
#             title="Monthly Revenue Distribution",
#             data=[ChartDataPoint(**d) for d in row.get("monthly_revenue_distribution", {}).get("data", [])]
#         ),
#         
#         monthly_revenue_trend=Chart(
#             title="Monthly Revenue Trend",
#             data=[ChartDataPoint(**d) for d in row.get("monthly_revenue_trend", {}).get("data", [])]
#         ),
#         
#         transaction_volume_summary=[
#             Transaction(**t) for t in row.get("transaction_volume_summary", [])
#         ]
#     )
