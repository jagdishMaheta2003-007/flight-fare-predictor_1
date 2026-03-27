import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import date, time, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="FlightFare AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #202124 !important;
    font-family: 'Google Sans', 'Roboto', sans-serif !important;
    color: #e8eaed !important;
}
[data-testid="stAppViewContainer"] > .main { background: #202124 !important; }
.main .block-container { padding: 2rem 2rem 2rem 2rem !important; max-width: 1000px !important; }
#MainMenu, footer, header { display: none !important; }

.nav-bar {
    background: #303134; padding: 16px 24px; border-radius: 12px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 24px; border: 1px solid #3c4043;
}
.nav-logo { font-size: 22px; font-weight: 600; color: #e8eaed; }
.nav-logo span { color: #8ab4f8; }

.hero { text-align: center; padding: 20px 0 28px; }
.hero h1 { font-size: 40px; font-weight: 400; color: #e8eaed; margin: 0; letter-spacing: -0.5px; }
.hero p  { color: #9aa0a6; font-size: 15px; margin: 6px 0 0; }

[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stTimeInput"] label,
[data-testid="stNumberInput"] label {
    color: #9aa0a6 !important; font-size: 11px !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: 0.8px !important; font-family: 'Google Sans',sans-serif !important;
}

div[data-baseweb="select"] > div {
    background: #303134 !important; border-color: #5f6368 !important;
    border-radius: 8px !important; color: #e8eaed !important;
}
div[data-baseweb="select"] > div:hover { border-color: #8ab4f8 !important; }
div[data-baseweb="select"] svg { fill: #9aa0a6 !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: #303134 !important; }
[role="option"] { background: #303134 !important; color: #e8eaed !important; }
[role="option"]:hover { background: #3c4043 !important; }
input {
    background: #303134 !important; color: #e8eaed !important;
    border: 1px solid #5f6368 !important; border-radius: 8px !important;
}

.stButton > button {
    background: #8ab4f8 !important; color: #202124 !important;
    border: none !important; border-radius: 24px !important;
    padding: 10px 32px !important; font-size: 15px !important;
    font-weight: 600 !important; width: 100% !important;
    font-family: 'Google Sans',sans-serif !important;
}
.stButton > button:hover {
    background: #aecbfa !important;
    box-shadow: 0 4px 12px rgba(138,180,248,0.35) !important;
}

.section-label {
    font-size: 13px; color: #9aa0a6; margin: 24px 0 12px;
    padding-bottom: 8px; border-bottom: 1px solid #3c4043;
}

.flight-card {
    background: #303134; border: 1px solid #3c4043;
    border-radius: 12px; padding: 20px 24px; margin-bottom: 10px;
    animation: fadeUp 0.35s ease both;
}
.flight-card:hover { border-color: #8ab4f8; box-shadow: 0 4px 20px rgba(138,180,248,0.12); }

@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}

.card-grid {
    display: grid;
    grid-template-columns: 180px 1fr 140px;
    align-items: center; gap: 16px;
}
.airline-block { display: flex; align-items: center; gap: 12px; }
.airline-avatar {
    width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg,#8ab4f8,#4285f4);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px; color: #202124; flex-shrink:0;
}
.airline-name  { font-size: 14px; font-weight: 500; color: #e8eaed; }
.airline-class { font-size: 12px; color: #9aa0a6; margin-top: 2px; }

.route-block { display: flex; align-items: center; gap: 12px; justify-content: center; }
.time-block  { text-align: center; }
.time-big    { font-size: 24px; font-weight: 400; color: #e8eaed; line-height: 1; }
.city-code   { font-size: 12px; color: #9aa0a6; margin-top: 3px; }
.mid-block   { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.dur-text    { font-size: 12px; color: #9aa0a6; }
.route-line  { display: flex; align-items: center; gap: 4px; width: 100%; }
.line-seg    { flex: 1; height: 1px; background: #5f6368; }
.plane-sym   { color: #8ab4f8; font-size: 15px; }
.stops-tag   { font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.tag-green   { background: rgba(129,201,149,.15); color: #81c995; }
.tag-yellow  { background: rgba(253,214,99,.15);  color: #fdd663; }

.price-block { text-align: right; }
.price-big   { font-size: 26px; font-weight: 400; color: #e8eaed; letter-spacing: -.5px; }
.price-sub   { font-size: 12px; color: #9aa0a6; margin-top: 2px; }
.select-btn  {
    display: inline-block; margin-top: 8px;
    background: #394457; color: #8ab4f8;
    border: 1px solid #8ab4f8; border-radius: 20px;
    padding: 6px 18px; font-size: 13px; font-weight: 600;
    cursor: pointer; font-family: 'Google Sans',sans-serif;
}

.badges { display: flex; gap: 6px; margin-top: 12px; flex-wrap: wrap; }
.badge  { font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 500; }
.badge-blue   { background: rgba(138,180,248,.15); color: #8ab4f8; }
.badge-green  { background: rgba(129,201,149,.15); color: #81c995; }
.badge-yellow { background: rgba(253,214,99,.15);  color: #fdd663; }

.insights-card {
    background: #303134; border: 1px solid #3c4043;
    border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;
}
.insights-title { font-size: 15px; font-weight: 500; color: #e8eaed; margin-bottom: 16px; }
.bar-row   { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.bar-lbl   { font-size: 12px; color: #9aa0a6; width: 80px; text-align: right; }
.bar-wrap  { flex: 1; background: #3c4043; border-radius: 4px; height: 8px; }
.bar-fill  { height: 8px; border-radius: 4px; background: #8ab4f8; }
.bar-fill-hi { height: 8px; border-radius: 4px; background: #81c995; }
.bar-val   { font-size: 12px; color: #e8eaed; width: 80px; }

.empty-state { text-align:center; padding: 64px 24px; color: #9aa0a6; }
.empty-icon  { font-size: 60px; margin-bottom: 16px; }
.empty-title { font-size: 20px; color: #e8eaed; margin-bottom: 8px; }

.footer {
    text-align:center; padding: 24px; color: #5f6368;
    font-size: 12px; border-top: 1px solid #3c4043; margin-top: 32px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    m   = joblib.load(os.path.join(BASE_DIR, "flight_model.pkl"))
    sc  = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
    ae  = joblib.load(os.path.join(BASE_DIR, "Airline_encoder.pkl"))
    se  = joblib.load(os.path.join(BASE_DIR, "Source_encoder.pkl"))
    de  = joblib.load(os.path.join(BASE_DIR, "Destination_encoder.pkl"))
    ste = joblib.load(os.path.join(BASE_DIR, "Total_Stops_encoder.pkl"))
    ie  = joblib.load(os.path.join(BASE_DIR, "Additional_Info_encoder.pkl"))
    return m, sc, ae, se, de, ste, ie

model, scaler, airline_enc, source_enc, dest_enc, stops_enc, info_enc = load_artifacts()

AIRLINES = sorted(airline_enc.classes_.tolist())
SOURCES  = sorted(source_enc.classes_.tolist())
DESTS    = sorted(dest_enc.classes_.tolist())
STOPS    = sorted(stops_enc.classes_.tolist())
INFOS    = sorted(info_enc.classes_.tolist())


def predict(airline, source, dest, stops, info, j_date, dep_t, arr_t, d_hr, d_min):
    inp = {
        "Airline":         airline_enc.transform([airline])[0],
        "Source":          source_enc.transform([source])[0],
        "Destination":     dest_enc.transform([dest])[0],
        "Total_Stops":     stops_enc.transform([stops])[0],
        "Additional_Info": info_enc.transform([info])[0],
        "j_date": j_date.day,  "j_mon": j_date.month,
        "a_hr":   arr_t.hour,  "a_min": arr_t.minute,
        "d_hr":   dep_t.hour,  "d_min": dep_t.minute,
        "du_hu":  d_hr,        "du_min": d_min,
    }
    df_in = pd.DataFrame([inp])
    return float(model.predict(scaler.transform(df_in))[0])


# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-logo">&#9992;&#65039; Flight<span>Fare</span> AI</div>
  <div style="color:#9aa0a6;font-size:13px;">Powered by Machine Learning</div>
</div>
<div class="hero">
  <h1>Flights</h1>
  <p>AI-powered fare prediction for Indian domestic routes</p>
</div>
""", unsafe_allow_html=True)


# ── SEARCH FORM ───────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div style="background:#303134;border-radius:14px;padding:24px;border:1px solid #3c4043;margin-bottom:8px;">', unsafe_allow_html=True)

    r1c1, r1c2, r1c3, r1c4 = st.columns([2, 2, 1.5, 1.5])
    with r1c1: source = st.selectbox("🛫 From", SOURCES, index=0)
    with r1c2: dest   = st.selectbox("🛬 To",   DESTS,   index=2)
    with r1c3: j_date = st.date_input("📅 Departure", value=date.today() + timedelta(days=7))
    with r1c4: r_date = st.date_input("📅 Return",    value=date.today() + timedelta(days=14))

    r2c1, r2c2, r2c3, r2c4 = st.columns([2, 1.5, 1.5, 1.5])
    with r2c1: airline  = st.selectbox("✈️ Airline",   AIRLINES, index=3)
    with r2c2: stops    = st.selectbox("🔁 Stops",     STOPS,    index=4)
    with r2c3: dep_time = st.time_input("🕐 Dep Time", value=time(10, 0))
    with r2c4: arr_time = st.time_input("🕑 Arr Time", value=time(14, 30))

    r3c1, r3c2, r3c3, r3c4 = st.columns([1, 1, 2, 1])
    with r3c1: dur_hr  = st.number_input("⏱ Hrs",  min_value=0, max_value=24, value=4)
    with r3c2: dur_min = st.number_input("⏱ Mins", min_value=0, max_value=59, value=30)
    with r3c3: info    = st.selectbox("ℹ️ Additional Info", INFOS, index=8)
    with r3c4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        search = st.button("🔍  Search Flights")

    st.markdown("</div>", unsafe_allow_html=True)


# ── RESULTS ───────────────────────────────────────────────────────────────────
if search:
    if source == dest:
        st.error("⚠️ Origin and destination cannot be the same!")
    else:
        try:
            base = predict(airline, source, dest, stops, info, j_date, dep_time, arr_time, dur_hr, dur_min)

            fares = [
                {
                    "label": "Cheapest", "price": base * 0.88,
                    "dep": time((dep_time.hour + 2) % 24, 15),
                    "arr": time((arr_time.hour + 2) % 24, 45),
                    "stops_lbl": "Non-stop", "stops_cls": "tag-green",
                    "badges": [("Cheapest option","badge-green"), ("AI prediction","badge-blue")],
                },
                {
                    "label": "Best value", "price": base * 1.00,
                    "dep": dep_time, "arr": arr_time,
                    "stops_lbl": stops, "stops_cls": "tag-yellow",
                    "badges": [("Best value","badge-blue"), ("AI prediction","badge-blue"), ("Free cancellation","badge-green")],
                },
                {
                    "label": "Premium", "price": base * 1.15,
                    "dep": time((dep_time.hour + 1) % 24, 0),
                    "arr": time((arr_time.hour + 1) % 24, 30),
                    "stops_lbl": stops, "stops_cls": "tag-yellow",
                    "badges": [("Premium cabin","badge-yellow"), ("AI prediction","badge-blue")],
                },
            ]

            prices = [f["price"] for f in fares]
            mn, mx = min(prices), max(prices)

            # ── Price insights ──
            bars_html = ""
            for lbl, p in zip(["Cheapest","Best value","Premium"], prices):
                w = int(((p - mn) / max(mx - mn, 1)) * 65 + 35)
                fill_cls = "bar-fill-hi" if lbl == "Cheapest" else "bar-fill"
                bars_html += f"""
                <div class="bar-row">
                  <div class="bar-lbl">{lbl}</div>
                  <div class="bar-wrap"><div class="{fill_cls}" style="width:{w}%"></div></div>
                  <div class="bar-val">&#8377;{p:,.0f}</div>
                </div>"""

            st.markdown(f"""
            <div class="insights-card">
              <div class="insights-title">&#128202; Price insights &middot; {source} &rarr; {dest} &middot; {j_date.strftime('%d %b %Y')}</div>
              {bars_html}
              <div style="font-size:12px;color:#5f6368;margin-top:10px;">Fares predicted by AI model &middot; Not actual booking prices</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f'<div class="section-label">Showing 3 results &middot; {source} &rarr; {dest} &middot; {j_date.strftime("%a, %d %b")}</div>', unsafe_allow_html=True)

            # ── Flight cards ──
            init = airline[:2].upper()
            for i, f in enumerate(fares):
                badge_html = "".join([f'<span class="badge {cls}">{txt}</span>' for txt, cls in f["badges"]])
                delay = f"{i * 0.1:.1f}s"

                st.markdown(f"""
                <div class="flight-card" style="animation-delay:{delay}">
                  <div class="card-grid">

                    <div class="airline-block">
                      <div class="airline-avatar">{init}</div>
                      <div>
                        <div class="airline-name">{airline}</div>
                        <div class="airline-class">Economy &middot; AI {1200 + i * 37}</div>
                      </div>
                    </div>

                    <div class="route-block">
                      <div class="time-block">
                        <div class="time-big">{f['dep'].strftime('%H:%M')}</div>
                        <div class="city-code">{source[:3].upper()}</div>
                      </div>
                      <div class="mid-block">
                        <div class="dur-text">{dur_hr}h {dur_min}m</div>
                        <div class="route-line">
                          <div class="line-seg"></div>
                          <div class="plane-sym">&#9992;</div>
                          <div class="line-seg"></div>
                        </div>
                        <div class="stops-tag {f['stops_cls']}">{f['stops_lbl']}</div>
                      </div>
                      <div class="time-block">
                        <div class="time-big">{f['arr'].strftime('%H:%M')}</div>
                        <div class="city-code">{dest[:3].upper()}</div>
                      </div>
                    </div>

                    <div class="price-block">
                      <div class="price-big">&#8377;{f['price']:,.0f}</div>
                      <div class="price-sub">per person</div>
                      <div class="select-btn">Select</div>
                    </div>

                  </div>
                  <div class="badges">{badge_html}</div>
                </div>""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")

else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">&#9992;&#65039;</div>
      <div class="empty-title">Search for flights above</div>
      <div>Select your route, date and preferences to get AI-powered fare predictions</div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  FlightFare AI &middot; Random Forest ML Model &middot; Indian domestic routes &middot; Predictions only, not actual fares
</div>""", unsafe_allow_html=True)
