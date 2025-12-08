import streamlit as st
import pandas as pd
from typing import List, Dict, Any

HSBC_RED = "#db0011"

def render_kpi_row(kpis: List[Dict[str, Any]], num_columns: int):
    """Renders a row of KPIs with colored sub-lines."""
    cols = st.columns(num_columns)
    for i, kpi in enumerate(kpis):
        with cols[i]:
            st.markdown(f"**{kpi['title']}**")
            st.subheader(kpi['value'])
            
            sub_lines = kpi.get('sub_lines', [])
            if sub_lines:
                delta_val = sub_lines[0]
                color = "#333333" # Default dark grey
                if delta_val.startswith('+'):
                    color = "green"
                elif delta_val.startswith('-'):
                    color = "red"
                
                st.markdown(f"<p style='color: {color}; margin: 0;'>{delta_val}</p>", unsafe_allow_html=True)
                for line in sub_lines[1:]:
                    st.markdown(f"<small>{line}</small>", unsafe_allow_html=True)

def render_network_relationship(data: Dict[str, Any]):
    """Renders the Network Relationship section."""
    st.subheader("Network Relationship")
    st.text(f"CIN: {data['cin']}")
    st.text(f"Parent: {data['parent']}")
    st.text(f"MD Name: {data['md_name']}")
    st.text(f"MD ID: {data['md_id']}")
    st.markdown("**Linked Businesses:**")
    for business in data['linked_businesses']:
        st.markdown(f"`{business}`")

def render_summary_text(text: str):
    """Renders the main summary text block with a heading."""
    st.subheader("Customer Summary")
    st.markdown(text)

def render_ai_insights(insights: List[str]):
    """Renders the AI Generated Insights section."""
    st.subheader("AI Generated Insights")
    for insight in insights:
        st.markdown(f"💡 {insight}")

def render_inhibits(inhibits: List[Dict[str, Any]]):
    """Renders the Inhibits section."""
    st.subheader("Inhibits")
    for item in inhibits:
        st.markdown(f"**{item['title']}** ({item['date']})")
        st.caption(item['description'])
        st.divider()

def render_journeys(journeys: List[Dict[str, Any]]):
    """Renders the Journeys section."""
    st.subheader("Journeys")
    for item in journeys:
        st.markdown(f"**{item['title']}** - `{item['status']}`")
        st.caption(f"{item['subtitle']} ({item['date']})")
        st.divider()

def render_complaints(complaints: List[Dict[str, Any]]):
    """Renders the Complaints section."""
    st.subheader("Complaints")
    for item in complaints:
        st.markdown(f"**{item['description']}** - `{item['status']}`")
        st.caption(f"Date: {item['date']}")
        st.divider()

def render_ics_results(results: List[Dict[str, Any]]):
    """Renders the ICS Results section."""
    st.subheader("ICS Results")
    for item in results:
        st.markdown(f"**Score: {item['score']}** ({item['date']})")
        st.info(f"'{item['quote']}'")
        st.divider()
        
def render_chart(chart_data: Dict[str, Any], chart_type: str = "bar"):
    """Renders a chart (bar or line) with HSBC red."""
    st.subheader(chart_data['title'])
    df = pd.DataFrame(chart_data['data']).set_index('label')
    if chart_type == "bar":
        st.bar_chart(df, color=HSBC_RED)
    elif chart_type == "line":
        st.line_chart(df, color=HSBC_RED)

def render_transaction_summary(transactions: List[Dict[str, Any]]):
    """Renders the transaction summary table with better styling."""
    st.subheader("Transaction Volume Summary (Rolling 12 months)")
    if not transactions:
        st.caption("No transactions to display.")
        return
    df = pd.DataFrame(transactions)
    # Dynamically set height to make the table larger
    height = (len(df) + 1) * 40  # Approx 40px per row
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=height
    )
