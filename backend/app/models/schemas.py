from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# --- API Request Models ---
class MockAuthPayload(BaseModel):
    conversationId: str
    authorizationCode: str
    codeVerifier: str


# --- Internal Data Models ---
class GenesysCustomerData(BaseModel):
    customer_id: str
    pcin: Optional[str] = None
    bcin: Optional[str] = None
    customer_name: str
    channel: str
    ani: Optional[str] = None


# --- Dashboard Component Models ---

class NetworkRelationship(BaseModel):
    cin: str
    parent: str
    md_name: str
    md_id: str
    linked_businesses: List[str]

class Kpi(BaseModel):
    title: str
    value: str
    sub_lines: List[str]

class Inhibit(BaseModel):
    title: str
    description: str
    date: date

class Journey(BaseModel):
    title: str
    subtitle: str
    status: str
    date: date

class Complaint(BaseModel):
    date: date
    description: str
    status: str

class ICSResult(BaseModel):
    date: date
    score: str
    quote: str

class ChartDataPoint(BaseModel):
    label: str
    value: float

class Chart(BaseModel):
    title: str
    data: List[ChartDataPoint]

class Transaction(BaseModel):
    date: date
    product: str
    amount: str
    status: str


# --- Main Prep Pack Model ---
    
class PrepPackData(BaseModel):
    summary_text: str
    network_relationship: NetworkRelationship
    ai_insights: List[str]
    kpis: List[Kpi]
    inhibits: List[Inhibit]
    journeys: List[Journey]
    complaints: List[Complaint]
    ics_results: List[ICSResult]
    monthly_revenue_distribution: Chart
    monthly_revenue_trend: Chart
    transaction_volume_summary: List[Transaction]


# --- API Response Model ---

class ProcessedConversationResponse(BaseModel):
    prep_pack_data: PrepPackData

