import streamlit as st
import pandas as pd
import plotly.express as px
import time
from pymongo import MongoClient

# --- CONFIGURATION ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "TrafficManagementDB"
COLLECTION_NAME = "RealTimeTraffic"

# Page Config
st.set_page_config(
    page_title="Real-Time Traffic Manager",
    page_icon="🚦",
    layout="wide"
)

# Initialize Connection
@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# --- DASHBOARD LAYOUT ---
st.title("🚦 Real-Time Traffic Management System")

# Create placeholder for real-time updates
placeholder = st.empty()

def get_data():
    """Fetch the most recent 500 records for analysis"""
    data = list(collection.find().sort("timestamp", -1).limit(500))
    if data:
        return pd.DataFrame(data)
    return pd.DataFrame()

# Real-Time Loop
while True:
    df = get_data()

    with placeholder.container():
        if df.empty:
            st.warning("Waiting for data... Run the simulator script!")
            time.sleep(2)
            continue

        # KPI Metrics (Latest Snapshot)
        latest_timestamp = df['timestamp'].max()
        latest_data = df[df['timestamp'] == latest_timestamp]
        
        st.markdown(f"### 🕒 Live Status: {latest_timestamp.strftime('%H:%M:%S')}")
        
        # Create 3 columns for metrics
        kpi1, kpi2, kpi3 = st.columns(3)
        
        avg_speed_now = latest_data['avg_speed'].mean()
        total_cars_now = latest_data['vehicle_count'].sum()
        congestion_rate = len(latest_data[latest_data['congestion_level'] == "High"]) / len(latest_data) * 100

        kpi1.metric(
            label="Avg Network Speed",
            value=f"{avg_speed_now:.1f} km/h",
            delta_color="normal" if avg_speed_now > 40 else "inverse"
        )
        kpi2.metric(
            label="Total Vehicles (Live)",
            value=total_cars_now
        )
        kpi3.metric(
            label="Congestion Rate",
            value=f"{congestion_rate:.0f}%",
            delta_color="inverse"
        )

        st.divider()

        # Charts Row
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Vehicle Flow Over Time")
            # Aggregate data by time to smooth the chart
            chart_df = df.groupby(['timestamp', 'location'])['vehicle_count'].mean().reset_index()
            fig_flow = px.line(chart_df, x='timestamp', y='vehicle_count', color='location', markers=True)
            st.plotly_chart(fig_flow, use_container_width=True)

        with col2:
            st.subheader("Current Congestion Heatmap")
            # Simple bar chart for current speeds by location
            fig_speed = px.bar(
                latest_data, 
                x='location', 
                y='avg_speed', 
                color='congestion_level',
                color_discrete_map={"Low": "green", "Moderate": "orange", "High": "red"},
                title="Live Traffic Speeds by Junction"
            )
            st.plotly_chart(fig_speed, use_container_width=True)

        # Raw Data View
        with st.expander("View Raw Live Data"):
            st.dataframe(latest_data.sort_values(by='location'))
            
        # Refresh interval
        time.sleep(3) 
        # Streamlit will loop this block automatically because of the `while True`