import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from fpdf import FPDF
import io

# ===== LOGO + PAGE CONFIG =====
logo = Image.open("logo.png")
st.set_page_config(
    page_title="AI Triage-SIEM", 
    page_icon=logo, 
    layout="wide"
)
st.sidebar.image(logo, width=200)

# ===== HEADER =====
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo, width=80)
with col2:
    st.title("AI Triage-SIEM")
    st.caption("NexDefend - Intelligent Alert Priorization for Wazuh | AI-Powered SOC Co-Pilot")

st.info("**Supports: CSV, JSON, XLSX | Auto-filters Critical + High threats using AI Scoring**")

# ===== FILE UPLOAD =====
uploaded_file = st.file_uploader(
    "Upload your Wazuh/SIEM alerts file", 
    type=["csv", "json", "xlsx"]
)

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        df = pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    
    st.success(f"File Loaded: {uploaded_file.name} - {len(df)} rows")
    
    # Dummy AI Scoring
    if 'severity' in df.columns:
        df['AI_Score'] = df['severity'].apply(lambda x: 90 if x in ['High', 'Critical'] else 40)
    else:
        df['AI_Score'] = 50
    
    # Filter Critical + High
    high_risk = df[df['AI_Score'] >= 70]
    
    st.subheader(f"Critical + High Alerts: {len(high_risk)}")
    st.dataframe(high_risk, use_container_width=True)
    
    # Chart
    if 'rule' in df.columns:
        fig = px.bar(high_risk['rule'].value_counts().head(10), title="Top 10 Threat Rules")
        st.plotly_chart(fig, use_container_width=True)
    
    # PDF Report Download
    if st.button("Download PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="NexDefend AI Triage Report", ln=True, align='C')
        pdf.output("report.pdf")
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, "NexDefend_Report.pdf")
else:
    st.warning("Please upload a CSV, JSON, or XLSX file to start")
