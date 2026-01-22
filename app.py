import streamlit as st
import plotly.graph_objects as go
import time

# 1. UI HEADER
st.set_page_config(page_title="AI Ventilator Design Tool", layout="wide")
st.title("🫁 Generative Medical Device Design Tool")
st.subheader("Project: Smart Ventilator Digital Twin")

# 2. SIDEBAR - DESIGN PARAMETERS
st.sidebar.header("Design Requirements")
target_pip = st.sidebar.slider("Target PIP (Max Pressure)", 20, 50, 40)
target_peep = st.sidebar.slider("Target PEEP (Min Pressure)", 0, 15, 5)

# 3. AI DESIGN OUTPUT (Simulated from your previous step)
col1, col2 = st.columns(2)

with col1:
    st.info("### AI Agent Output")
    st.write(f"**Selected Sensor:** MPX5010DP")
    st.write(f"**Compliance Check:** ISO 80601-2-12 Validated")
    if target_pip > 40:
        st.error("⚠️ RISK: High pressure detected. Lung barotrauma risk!")
    else:
        st.success("✅ Design within safe clinical limits.")

# 4. DIGITAL TWIN SIMULATION (Visualized)
with col2:
    st.info("### Live Digital Twin Simulation")
    
    # Create breathing data for a graph
    times = [0, 2, 5, 7, 10, 12, 15]
    pressures = [target_peep, target_pip, target_peep, target_pip, target_peep, target_pip, target_peep]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=pressures, mode='lines+markers', name='Airway Pressure'))
    fig.update_layout(xaxis_title="Time (seconds)", yaxis_title="Pressure (cmH2O)", height=300)
    st.plotly_chart(fig, width='stretch')

# 5. DRILL-DOWN VIEW (Components)
st.divider()
st.write("### System Architecture - Drill Down")
tab1, tab2 = st.tabs(["Pneumatic Subsystem", "Electronic Subsystem"])

with tab1:
    st.table({
        "Component": ["Solenoid Valve", "Oxygen Mixer", "HEPA Filter"],
        "Status": ["Active", "Active", "Verified"],
        "Value": ["10Hz PWM", "FiO2 40%", "99.9% Efficiency"]
    })

with tab2:
    st.json({
        "sensor_id": "MPX5010DP",
        "voltage": "5V",
        "resolution": "0.03%",
        "simulated_error_rate": "0.001%"
    })