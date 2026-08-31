import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sentinel HealthOS 6.0",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Sentinel HealthOS 6.0 | Public Health & Climate Intelligence")
st.markdown("Real-time provincial risk monitoring, climate vulnerability, and outbreak surveillance.")

# Sidebar Controls
st.sidebar.header("Navigation & Settings")
api_base_url = st.sidebar.text_input("API Base URL", "http://127.0.0.1:8000")
selected_province = st.sidebar.selectbox("Select Province", ["GP", "KZN", "WC", "EC", "FS", "LP", "MP", "NC", "NW"])

# Fetch Data Functions
def fetch_data(endpoint):
    try:
        res = requests.get(f"{api_base_url}{endpoint}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        return None
    return None

# Top Metrics Row
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌦️ Climate Vulnerability")
    climate_data = fetch_data(f"/api/climate/vulnerability/{selected_province}")
    if climate_data:
        st.metric("Heatwave Risk Score", f"{climate_data.get('heat_wave_risk_score', 0):.2f}")
        st.write(f"**Flood Susceptibility:** {climate_data.get('flood_susceptibility')}")
        st.write(f"**Exposed Population:** {climate_data.get('vulnerable_population_exposure'):,}")
    else:
        st.warning("Connect API to load live climate metrics.")

with col2:
    st.subheader("🦠 Outbreak Surveillance")
    surv_data = fetch_data(f"/api/surveillance/predictions/{selected_province}")
    if surv_data:
        st.metric("Outbreak Risk Score", f"{surv_data.get('outbreak_risk_score', 0):.2f}")
        st.write(f"**Primary Driver:** {surv_data.get('primary_driver')}")
        st.write(f"**Predicted Index:** {surv_data.get('predicted_outbreak_index')}")
    else:
        st.warning("Connect API to load surveillance metrics.")

with col3:
    st.subheader("💨 Air Quality Metrics")
    aqi_data = fetch_data(f"/api/air-quality/metrics/{selected_province}")
    if aqi_data:
        st.metric("Air Quality Index (AQI)", aqi_data.get("aqi_index"))
        st.write(f"**Category:** {aqi_data.get('category')}")
        st.write(f"**PM2.5:** {aqi_data.get('pm2_5_ug_m3')} µg/m³")
    else:
        st.warning("Connect API to load air quality metrics.")

st.divider()

# Interactive Visualization Section
st.subheader("📊 Comparative Risk Breakdown")
chart_data = pd.DataFrame({
    "Metric": ["Heatwave Risk", "Outbreak Risk", "AQI (Scaled 0-1)"],
    "Score": [
        climate_data.get("heat_wave_risk_score", 0.5) if climate_data else 0.5,
        surv_data.get("outbreak_risk_score", 0.4) if surv_data else 0.4,
        (aqi_data.get("aqi_index", 50) / 500) if aqi_data else 0.1,
    ]
})

fig = px.bar(chart_data, x="Metric", y="Score", color="Metric", title=f"Risk Score Breakdown for {selected_province}")
st.plotly_chart(fig, use_container_width=True)
