import streamlit as st
from api_client import get_prep_pack_data
from components import (
    render_kpi_row, render_network_relationship, render_summary_text, render_ai_insights,
    render_chart, render_transaction_summary,
    render_inhibits, render_journeys, render_complaints, render_ics_results
)

# --- Page Configuration ---
st.set_page_config(
    page_title="BCS Profile Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Card Layout & Header ---
st.markdown("""
    <style>
        .card {
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# --- Header ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://www.logo.wine/a/logo/HSBC/HSBC-Logo.wine.svg", width=150)
with col2:
    st.markdown("<h1 style='text-align: center;'>BCS Profile Assistant</h1>", unsafe_allow_html=True)

st.header("Acme Corporation Summary")
st.caption("HSBC CMB D&A - Customer Pack")
st.divider()

# --- Main Application ---
# Try to get parameters from URL query params (Genesys Widget)
query_params = st.query_params
CONVERSATION_ID = query_params.get("conversationId", "mock-convo-12345")
AUTH_CODE = query_params.get("code", "mock-auth-code")
CODE_VERIFIER = query_params.get("codeVerifier", "mock-code-verifier")

if "conversationId" in query_params:
    st.toast(f"Loaded Context for Conversation: {CONVERSATION_ID}", icon="✅")


@st.cache_data(show_spinner=False)
def load_data(conversation_id, auth_code, code_verifier):
    return get_prep_pack_data(conversation_id, auth_code, code_verifier)

if CONVERSATION_ID:
    with st.spinner("Authenticating with Genesys & Retrieving Customer Profile..."):
        data = load_data(CONVERSATION_ID, AUTH_CODE, CODE_VERIFIER)

    if data:
        prep_pack = data.get('prep_pack_data', {})
    
            # --- Top Row: 3 Columns (No Cards) ---
        col1, col2, col3 = st.columns([1.5, 2, 2], gap="large")
        with col1:
            render_network_relationship(prep_pack.get('network_relationship', {}))
        with col2:
            render_summary_text(prep_pack.get('summary_text', ''))
        with col3:
            render_ai_insights(prep_pack.get('ai_insights', []))

        st.divider()
        
        # --- Middle Rows: KPIs rendered directly on the background ---
        kpis = prep_pack.get('kpis', [])
        
        render_kpi_row(kpis[:5], 5)
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        render_kpi_row(kpis[5:], 5)

        st.divider()

        # --- Bottom Row: 2 Columns (No Cards) ---
        col4, col5 = st.columns([1, 2], gap="large")
        with col4:
            render_inhibits(prep_pack.get('inhibits', []))
            render_journeys(prep_pack.get('journeys', []))
            render_complaints(prep_pack.get('complaints', []))
            render_ics_results(prep_pack.get('ics_results', []))
        with col5:
            st.header("Financial Overview")
            
            # Stack charts for more space
            render_chart(prep_pack.get('monthly_revenue_distribution', {}), chart_type="bar")
            render_chart(prep_pack.get('monthly_revenue_trend', {}), chart_type="line")
            st.divider()

            # Enlarge the transaction summary table
            render_transaction_summary(prep_pack.get('transaction_volume_summary', []))
else:
    st.error("Failed to fetch data from the backend. Please ensure the backend server is running.")

