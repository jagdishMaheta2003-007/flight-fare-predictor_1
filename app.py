import streamlit as st
import numpy as np
import pickle
import os

# Install: pip install tensorflow
from tensorflow.keras.models import load_model

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(page_title="✈️ Flight Fare Predictor (ANN)", page_icon="✈️")

# ── Styling ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 10px;
        padding: 0.6rem 2rem; font-size: 1.1rem; font-weight: 600;
        width: 100%; margin-top: 10px;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 2rem; border-radius: 15px;
        text-align: center; margin-top: 1.5rem;
    }
    .result-box h1 { font-size: 2.8rem; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ── Load Model & Encoders ────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    scaler = pickle.load(open("models/scaler.pkl", "rb"))
    le_airline = pickle.load(open("models/le_airline.pkl", "rb"))
    le_source = pickle.load(open("models/le_source.pkl", "rb"))
    le_destination = pickle.load(open("models/le_destination.pkl", "rb"))
    model = load_model("models/ann_model.h5")
    return scaler, le_airline, le_source, le_destination, model

scaler, le_airline, le_source, le_destination, model = load_artifacts()

# ── Header ───────────────────────────────────────────────────────────────
st.markdown("## ✈️ Flight Fare Predictor (Neural Network)")
st.markdown("Fill in your flight details to get an **instant AI-powered price estimate**.")
st.markdown("---")

# ── Input Form ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("🛫 Airline", le_airline.classes_)
    source = st.selectbox("📍 Source", le_source.classes_)
    destination = st.selectbox("📍 Destination", le_destination.classes_)
    stops = st.selectbox("🔁 Total Stops", [0, 1, 2, 3, 4])

with col2:
    journey_day = st.number_input("📅 Journey Day", 1, 31, 15)
    journey_month = st.number_input("📅 Journey Month", 1, 12, 6)
    duration = st.number_input("⏱ Duration (minutes)", 60, 2000, 180)

st.markdown("#### ⏰ Departure & Arrival Times")
col3, col4 = st.columns(2)

with col3:
    dep_hour = st.number_input("🕐 Departure Hour", 0, 23, 10)
    dep_min = st.number_input("Departure Minute", 0, 59, 0)

with col4:
    arrival_hour = st.number_input("🕑 Arrival Hour", 0, 23, 14)
    arrival_min = st.number_input("Arrival Minute", 0, 59, 30)

# ── Predict ──────────────────────────────────────────────────────────────
if st.button("💰 Predict Fare"):
    if source == destination:
        st.warning("⚠️ Source and Destination cannot be the same!")
    else:
        try:
            # Encode categorical variables
            airline_enc = le_airline.transform([airline])[0]
            source_enc = le_source.transform([source])[0]
            destination_enc = le_destination.transform([destination])[0]
            
            # Prepare input
            input_data = np.array([[airline_enc, journey_day, journey_month,
                                   source_enc, destination_enc, duration,
                                   stops, dep_hour, dep_min,
                                   arrival_hour, arrival_min]])
            
            # Scale and predict
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled, verbose=0)
            
            # Display result
            st.markdown(f"""
            <div class="result-box">
                <p>🤖 AI Predicted Flight Fare</p>
                <h1>₹ {int(prediction[0][0]):,}</h1>
                <p>{airline} · {source} → {destination} · {stops} stop(s)</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")

# ── Footer ───────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🧠 Model: Artificial Neural Network (TensorFlow/Keras) · Deep Learning")
