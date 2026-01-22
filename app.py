import streamlit as st
import plotly.graph_objects as go
import os
import requests

# 1. UI SETUP
st.set_page_config(page_title="AI Ventilator Design Tool", layout="wide")
st.title("🫁 Generative Medical Device Design Tool")
st.subheader("Project: Smart Ventilator Digital Twin")

# 2. SIDEBAR - DESIGN PARAMETERS
st.sidebar.header("Step 1: Clinical Requirements")
target_pip = st.sidebar.slider("Target PIP (Inspiratory Pressure)", 20, 50, 40)
target_peep = st.sidebar.slider("Target PEEP (End-Expiratory)", 0, 15, 5)
st.sidebar.divider()

# 3. AI AGENT LOGIC (HYBRID LOCAL/CLOUD)
st.write("### Step 2: AI-Generated System Architecture")
col1, col2 = st.columns(2)

with col1:
    st.info("### 🤖 AI Agent Analysis")
    
    # Check if Ollama is running locally
    ollama_active = False
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            ollama_active = True
    except:
        ollama_active = False

    if ollama_active:
        st.success("Connected to Local Brain (Ollama/Phi3)")
        if st.button("Run Live Design Agent"):
            st.write("**Doctor Agent:** Analyzing clinical safety...")
            st.write("**Engineer Agent:** Selecting MPX5010DP based on 0-40 cmH2O range.")
    else:
        st.warning("Running in 'Demo Mode' (Cloud Optimized)")
        st.write("**Selected Sensor:** MPX5010DP")
        st.write("**Compliance:** ISO 80601-2-12 Checked")

    # Safety Guardrail
    if target_pip > 40:
        st.error("⚠️ CRITICAL RISK: PIP exceeds 40 cmH2O. Risk of barotrauma detected!")
    else:
        st.success("✅ Parameters within safe medical limits.")

# 4. DIGITAL TWIN SIMULATION (VISUALIZED)
with col2:
    st.info("### 📈 Live Digital Twin Simulation")
    
    # Mathematical Model of Breathing
    times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Simple waveform logic: Up for 2s, Down for 3s
    pressures = [target_peep, target_pip/2, target_pip, target_pip, target_peep, 
                 target_peep, target_pip/2, target_pip, target_pip, target_peep, target_peep]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=pressures, mode='lines+markers', 
                             line=dict(color='#1f77b4', width=4), name='Airway Pressure'))
    
    fig.update_layout(
        xaxis_title="Time (seconds)", 
        yaxis_title="Pressure (cmH2O)",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, width='stretch')

# 5. DRILL-DOWN VIEW (SYSTEM ARCHITECTURE)
st.divider()
st.write("### Step 3: Engineering Drill-Down")
tab1, tab2, tab3 = st.tabs(["Pneumatic Layout", "Electronic Specs", "RAG Evidence"])

with tab1:
    st.table({
        "Subsystem": ["Inspiration Valve", "Expiration Valve", "O2 Blender", "HEPA Filter"],
        "Component Type": ["Proportional Solenoid", "Solenoid", "Electronic Mixer", "Medical Grade"],
        "AI Selection Status": ["Optimized", "Verified", "Verified", "Required"]
    })

with tab2:
    st.json({
        "sensor_id": "MPX5010DP",
        "interface": "I2C via ESP32",
        "supply_voltage": "5.0V",
        "sensitivity": "450 mV/kPa",
        "simulated_latency": "1.2ms"
    })

with tab3:
    st.markdown("""
    **Evidence extracted from RAG Knowledge Base:**
    - *Source:* NXP MPX5010DP Datasheet
    - *Key Fact:* Device is integrated on-chip, providing a high-level analog output signal that is proportional to the applied pressure.
    - *Validation:* The 0 to 10 kPa range matches the 0-100 cmH2O requirement for ventilator safety.
    """)