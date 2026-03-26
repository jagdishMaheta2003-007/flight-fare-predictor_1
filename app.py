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

# ── Google Flights Style CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #202124 !important;
    font-family: 'Google Sans', 'Roboto', sans-serif !important;
    color: #e8eaed !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #202124 !important;
    padding: 0 !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide streamlit elements */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── TOP NAV ── */
.gf-nav {
    background: #303134;
    padding: 0 24px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #3c4043;
    position: sticky; top: 0; z-index: 100;
}
.gf-nav-logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 20px; font-weight: 500; color: #e8eaed;
    letter-spacing: -0.3px;
}
.gf-nav-logo span { color: #8ab4f8; }
.gf-nav-tabs { display: flex; gap: 4px; }
.gf-nav-tab {
    padding: 8px 16px; border-radius: 20px;
    font-size: 14px; font-weight: 500; color: #9aa0a6;
    cursor: pointer; transition: all 0.2s;
}
.gf-nav-tab.active {
    background: #394457; color: #8ab4f8;
}

/* ── HERO SECTION ── */
.gf-hero {
    background: linear-gradient(180deg, #303134 0%, #202124 100%);
    padding: 48px 24px 0;
    text-align: center;
}
.gf-hero-title {
    font-size: 44px; font-weight: 400; color: #e8eaed;
    letter-spacing: -1px; margin-bottom: 8px;
}
.gf-hero-sub {
    font-size: 16px; color: #9aa0a6; margin-bottom: 36px;
}

/* ── SEARCH CARD ── */
.gf-search-card {
    background: #303134;
    border-radius: 16px;
    padding: 20px;
    margin: 0 auto 24px;
    max-width: 900px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}

/* ── TRIP TYPE PILLS ── */
.gf-trip-pills {
    display: flex; gap: 8px; margin-bottom: 16px;
    flex-wrap: wrap;
}
.gf-pill {
    background: #3c4043; color: #e8eaed;
    padding: 6px 14px; border-radius: 20px;
    font-size: 14px; font-weight: 500; cursor: pointer;
    border: 1px solid transparent; transition: all 0.2s;
    display: inline-flex; align-items: center; gap: 6px;
}
.gf-pill.active {
    background: #394457; color: #8ab4f8;
    border-color: #8ab4f8;
}

/* ── FORM FIELDS ── */
.gf-row { display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.gf-field {
    flex: 1; min-width: 140px;
    background: #3c4043;
    border: 1px solid #5f6368;
    border-radius: 8px;
    padding: 12px 16px;
    transition: all 0.2s;
    position: relative;
    cursor: pointer;
}
.gf-field:hover { border-color: #8ab4f8; background: #404348; }
.gf-field.focused { border-color: #8ab4f8; background: #404348; }
.gf-field-label {
    font-size: 11px; color: #9aa0a6;
    font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.5px; margin-bottom: 4px;
}
.gf-field-value {
    font-size: 16px; color: #e8eaed; font-weight: 400;
}
.gf-field-sub {
    font-size: 12px; color: #9aa0a6; margin-top: 2px;
}

/* ── STREAMLIT INPUT OVERRIDES ── */
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stTimeInput > div > div > input,
.stNumberInput > div > div > input {
    background: #3c4043 !important;
    border: 1px solid #5f6368 !important;
    border-radius: 8px !important;
    color: #e8eaed !important;
    font-family: 'Google Sans', sans-serif !important;
}

.stSelectbox > div > div:hover,
.stDateInput > div > div > input:hover {
    border-color: #8ab4f8 !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stTimeInput"] label,
[data-testid="stNumberInput"] label {
    color: #9aa0a6 !important;
    font-size: 12px !important;
    font-family: 'Google Sans', sans-serif !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

div[data-baseweb="select"] > div {
    background: #3c4043 !important;
    border-color: #5f6368 !important;
    border-radius: 8px !important;
    color: #e8eaed !important;
}

div[data-baseweb="select"] svg { fill: #9aa0a6 !important; }

[data-baseweb="popover"] { background: #303134 !important; }
[data-baseweb="menu"] { background: #303134 !important; }
[role="option"] { background: #303134 !important; color: #e8eaed !important; }
[role="option"]:hover { background: #3c4043 !important; }

input[type="text"], input[type="number"],
input[data-testid="stDateInput"],
[data-testid="stNumberInput"] input {
    background: #3c4043 !important;
    color: #e8eaed !important;
    border: 1px solid #5f6368 !important;
    border-radius: 8px !important;
}

/* ── SEARCH BUTTON ── */
.stButton { display: flex; justify-content: center; margin-top: 12px; }
.stButton > button {
    background: #8ab4f8 !important;
    color: #202124 !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 12px 36px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Google Sans', sans-serif !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    min-width: 180px !important;
}
.stButton > button:hover {
    background: #aecbfa !important;
    box-shadow: 0 4px 12px rgba(138,180,248,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── RESULT CARD ── */
.gf-result-section {
    max-width: 900px; margin: 0 auto; padding: 0 24px 48px;
}
.gf-result-header {
    font-size: 13px; color: #9aa0a6;
    margin-bottom: 16px; padding-top: 8px;
}
.gf-flight-card {
    background: #303134;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 8px;
    border: 1px solid #3c4043;
    transition: all 0.25s;
    animation: slideIn 0.4s ease;
}
.gf-flight-card:hover {
    border-color: #8ab4f8;
    background: #35373b;
    box-shadow: 0 4px 20px rgba(138,180,248,0.15);
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.gf-card-top {
    display: flex; align-items: center;
    justify-content: space-between; gap: 16px;
    flex-wrap: wrap;
}
.gf-airline-info {
    display: flex; align-items: center; gap: 12px; flex: 1; min-width: 160px;
}
.gf-airline-logo {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #8ab4f8, #4285f4);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: #202124;
    flex-shrink: 0;
}
.gf-airline-name { font-size: 14px; color: #e8eaed; font-weight: 500; }
.gf-airline-class { font-size: 12px; color: #9aa0a6; }

.gf-times {
    display: flex; align-items: center; gap: 16px;
    flex: 2; justify-content: center; flex-wrap: wrap;
}
.gf-time-block { text-align: center; }
.gf-time { font-size: 22px; font-weight: 400; color: #e8eaed; }
.gf-city { font-size: 12px; color: #9aa0a6; margin-top: 2px; }

.gf-duration-line {
    display: flex; flex-direction: column;
    align-items: center; gap: 4px; flex: 1;
}
.gf-dur-text { font-size: 12px; color: #9aa0a6; }
.gf-line-wrap {
    display: flex; align-items: center; gap: 4px; width: 100%;
}
.gf-line {
    flex: 1; height: 1px; background: #5f6368;
}
.gf-plane-icon { color: #8ab4f8; font-size: 16px; }
.gf-stops-badge {
    font-size: 11px; color: #fdd663;
    background: rgba(253,214,99,0.12);
    padding: 2px 8px; border-radius: 10px;
}
.gf-nonstop { color: #81c995; background: rgba(129,201,149,0.12); }

.gf-price-block { text-align: right; flex-shrink: 0; }
.gf-price {
    font-size: 28px; font-weight: 400; color: #e8eaed;
    letter-spacing: -0.5px;
}
.gf-price-label { font-size: 12px; color: #9aa0a6; margin-top: 2px; }
.gf-select-btn {
    background: #394457; color: #8ab4f8;
    border: 1px solid #8ab4f8; border-radius: 20px;
    padding: 8px 20px; font-size: 13px; font-weight: 600;
    cursor: pointer; margin-top: 8px; transition: all 0.2s;
    font-family: 'Google Sans', sans-serif;
    display: inline-block;
}
.gf-select-btn:hover { background: #8ab4f8; color: #202124; }

/* insights row */
.gf-insights {
    display: flex; gap: 8px; margin-top: 12px;
    flex-wrap: wrap;
}
.gf-badge {
    font-size: 11px; padding: 3px 10px; border-radius: 12px;
    font-weight: 500;
}
.gf-badge-green { background: rgba(129,201,149,0.15); color: #81c995; }
.gf-badge-blue  { background: rgba(138,180,248,0.15); color: #8ab4f8; }
.gf-badge-yellow{ background: rgba(253,214,99,0.15);  color: #fdd663; }

/* ── PRICE INSIGHTS PANEL ── */
.gf-insights-panel {
    background: #303134; border-radius: 12px;
    padding: 20px 24px; margin-bottom: 24px;
    border: 1px solid #3c4043;
}
.gf-insights-title {
    font-size: 15px; font-weight: 500; color: #e8eaed;
    margin-bottom: 16px;
}
.gf-bar-row {
    display: flex; align-items: center;
    gap: 12px; margin-bottom: 8px;
}
.gf-bar-label { font-size: 12px; color: #9aa0a6; width: 60px; text-align: right; }
.gf-bar-wrap { flex: 1; background: #3c4043; border-radius: 4px; height: 8px; }
.gf-bar-fill { height: 8px; border-radius: 4px; background: #8ab4f8; }
.gf-bar-fill.best { background: #81c995; }
.gf-bar-val { font-size: 12px; color: #e8eaed; width: 70px; }

/* ── EMPTY STATE ── */
.gf-empty {
    text-align: center; padding: 60px 24px;
    color: #9aa0a6;
}
.gf-empty-icon { font-size: 64px; margin-bottom: 16px; }
.gf-empty-title { font-size: 20px; color: #e8eaed; margin-bottom: 8px; }

/* section divider */
.gf-divider {
    height: 1px; background: #3c4043;
    margin: 0 auto 24px; max-width: 900px;
}

/* streamlit column gap fix */
[data-testid="column"] { padding: 0 4px !important; }
</style>
""", unsafe_allow_html=True)


# ── Load artifacts ────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model       = joblib.load(os.path.join(BASE_DIR, "flight_model.pkl"))
    scaler      = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
    airline_enc = joblib.load(os.path.join(BASE_DIR, "Airline_encoder.pkl"))
    source_enc  = joblib.load(os.path.join(BASE_DIR, "Source_encoder.pkl"))
    dest_enc    = joblib.load(os.path.join(BASE_DIR, "Destination_encoder.pkl"))
    stops_enc   = joblib.load(os.path.join(BASE_DIR, "Total_Stops_encoder.pkl"))
    info_enc    = joblib.load(os.path.join(BASE_DIR, "Additional_Info_encoder.pkl"))
    return model, scaler, airline_enc, source_enc, dest_enc, stops_enc, info_enc

model, scaler, airline_enc, source_enc, dest_enc, stops_enc, info_enc = load_artifacts()

AIRLINES     = sorted(airline_enc.classes_.tolist())
SOURCES      = sorted(source_enc.classes_.tolist())
DESTINATIONS = sorted(dest_enc.classes_.tolist())
STOPS        = sorted(stops_enc.classes_.tolist())
INFOS        = sorted(info_enc.classes_.tolist())

AIRLINE_INIT = {a: a[:2].upper() for a in AIRLINES}


# ── Top Nav ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gf-nav">
  <div class="gf-nav-logo">✈️ &nbsp;Flight<span>Fare</span> AI</div>
  <div class="gf-nav-tabs">
    <div class="gf-nav-tab active">✈️ Flights</div>
    <div class="gf-nav-tab">🏨 Hotels</div>
    <div class="gf-nav-tab">🗺️ Explore</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gf-hero">
  <div class="gf-hero-title">Flights</div>
  <div class="gf-hero-sub">AI-powered fare prediction for Indian domestic routes</div>
</div>
""", unsafe_allow_html=True)


# ── Search Card ───────────────────────────────────────────────────────────────
st.markdown('<div style="max-width:900px;margin:0 auto;padding:0 24px;">', unsafe_allow_html=True)
st.markdown("""
<div class="gf-search-card">
  <div class="gf-trip-pills">
    <div class="gf-pill active">⇌ Round trip</div>
    <div class="gf-pill">→ One way</div>
    <div class="gf-pill">⇆ Multi-city</div>
    <div class="gf-pill">👤 1 passenger</div>
    <div class="gf-pill">💺 Economy</div>
  </div>
""", unsafe_allow_html=True)

# Row 1 — From / To / Date
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1.5])
with c1:
    source = st.selectbox("🛫 FROM", SOURCES, index=0)
with c2:
    dest = st.selectbox("🛬 TO", DESTINATIONS, index=2)
with c3:
    journey_date = st.date_input("📅 DEPARTURE", value=date.today() + timedelta(days=7))
with c4:
    return_date = st.date_input("📅 RETURN", value=date.today() + timedelta(days=14))

# Row 2 — Airline / Stops / Dep Time / Arr Time
c5, c6, c7, c8 = st.columns([2, 1.5, 1.5, 1.5])
with c5:
    airline = st.selectbox("✈️ AIRLINE", AIRLINES, index=3)
with c6:
    stops = st.selectbox("🔁 STOPS", STOPS, index=4)
with c7:
    dep_time = st.time_input("🕐 DEPARTURE TIME", value=time(10, 0))
with c8:
    arr_time = st.time_input("🕑 ARRIVAL TIME", value=time(14, 30))

# Row 3 — Duration / Extra Info
c9, c10, c11, c12 = st.columns([1, 1, 2, 1])
with c9:
    dur_hr = st.number_input("⏱ DURATION HRS", min_value=0, max_value=24, value=4)
with c10:
    dur_min = st.number_input("⏱ DURATION MINS", min_value=0, max_value=59, value=30)
with c11:
    info = st.selectbox("ℹ️ ADDITIONAL INFO", INFOS, index=8)
with c12:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    search_btn = st.button("🔍  Search flights")

st.markdown("</div>", unsafe_allow_html=True)  # close search card
st.markdown("</div>", unsafe_allow_html=True)  # close centering div


# ── Results ───────────────────────────────────────────────────────────────────
if search_btn:
    if source == dest:
        st.markdown("""
        <div style="max-width:900px;margin:16px auto;padding:0 24px;">
          <div style="background:#3c4043;border-radius:12px;padding:16px 20px;
                      color:#f28b82;font-size:14px;border:1px solid #f28b82;">
            ⚠️ Origin and destination cannot be the same city.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        try:
            def predict_price(dep_t, arr_t, d_hr_extra=0):
                inp = {
                    "Airline":         airline_enc.transform([airline])[0],
                    "Source":          source_enc.transform([source])[0],
                    "Destination":     dest_enc.transform([dest])[0],
                    "Total_Stops":     stops_enc.transform([stops])[0],
                    "Additional_Info": info_enc.transform([info])[0],
                    "j_date":  journey_date.day,
                    "j_mon":   journey_date.month,
                    "a_hr":    arr_t.hour,
                    "a_min":   arr_t.minute,
                    "d_hr":    (dep_t.hour + d_hr_extra) % 24,
                    "d_min":   dep_t.minute,
                    "du_hu":   dur_hr,
                    "du_min":  dur_min,
                }
                df_in = pd.DataFrame([inp])
                return model.predict(scaler.transform(df_in))[0]

            base_price = predict_price(dep_time, arr_time)

            # Generate 3 fare options
            fares = [
                {"label": "Best",    "multiplier": 1.00, "badge": "best",   "badge_text": "Best value",      "stops_show": stops,    "dep": dep_time,                          "arr": arr_time},
                {"label": "Cheaper", "multiplier": 0.88, "badge": "green",  "badge_text": "Cheapest option", "stops_show": "non-stop","dep": time((dep_time.hour+2)%24,15),     "arr": time((arr_time.hour+2)%24,45)},
                {"label": "Faster",  "multiplier": 1.15, "badge": "yellow", "badge_text": "Premium cabin",   "stops_show": stops,    "dep": time((dep_time.hour+1)%24,0),      "arr": time((arr_time.hour+1)%24,30)},
            ]

            st.markdown('<div class="gf-result-section">', unsafe_allow_html=True)

            # Price insights bar chart
            prices_for_chart = [base_price * f["multiplier"] for f in fares]
            min_p, max_p = min(prices_for_chart), max(prices_for_chart)

            bars_html = ""
            labels = ["Cheapest", "Best value", "Premium"]
            for i, (lbl, p) in enumerate(zip(labels, prices_for_chart)):
                pct = int(((p - min_p) / max(max_p - min_p, 1)) * 70 + 30)
                best_cls = "best" if i == 1 else ""
                bars_html += f"""
                <div class="gf-bar-row">
                  <div class="gf-bar-label">{lbl}</div>
                  <div class="gf-bar-wrap"><div class="gf-bar-fill {best_cls}" style="width:{pct}%"></div></div>
                  <div class="gf-bar-val">₹{p:,.0f}</div>
                </div>"""

            st.markdown(f"""
            <div class="gf-insights-panel">
              <div class="gf-insights-title">📊 Price insights for {source} → {dest}</div>
              {bars_html}
              <div style="font-size:12px;color:#9aa0a6;margin-top:12px;">
                Prices predicted by AI · Based on {journey_date.strftime('%d %b %Y')}
              </div>
            </div>""", unsafe_allow_html=True)

            # Result header
            st.markdown(f"""
            <div class="gf-result-header">
              Showing 3 of 3 results · {source} → {dest} · {journey_date.strftime('%a, %d %b')}
            </div>""", unsafe_allow_html=True)

            # Flight cards
            for i, fare in enumerate(fares):
                price = base_price * fare["multiplier"]
                init  = AIRLINE_INIT.get(airline, airline[:2].upper())
                badge_map = {
                    "best":   ("gf-badge-blue",   fare["badge_text"]),
                    "green":  ("gf-badge-green",  fare["badge_text"]),
                    "yellow": ("gf-badge-yellow", fare["badge_text"]),
                }
                badge_cls, badge_txt = badge_map[fare["badge"]]
                stops_cls = "gf-nonstop" if "non-stop" in fare["stops_show"] else ""
                stops_label = "Non-stop" if "non-stop" in fare["stops_show"] else fare["stops_show"]
                dur_label = f"{dur_hr}h {dur_min}m"

                st.markdown(f"""
                <div class="gf-flight-card">
                  <div class="gf-card-top">
                    <div class="gf-airline-info">
                      <div class="gf-airline-logo">{init}</div>
                      <div>
                        <div class="gf-airline-name">{airline}</div>
                        <div class="gf-airline-class">Economy · AI {1200+i*37}</div>
                      </div>
                    </div>

                    <div class="gf-times">
                      <div class="gf-time-block">
                        <div class="gf-time">{fare['dep'].strftime('%H:%M')}</div>
                        <div class="gf-city">{source[:3].upper()}</div>
                      </div>
                      <div class="gf-duration-line">
                        <div class="gf-dur-text">{dur_label}</div>
                        <div class="gf-line-wrap">
                          <div class="gf-line"></div>
                          <div class="gf-plane-icon">✈</div>
                          <div class="gf-line"></div>
                        </div>
                        <div class="gf-stops-badge {stops_cls}">{stops_label}</div>
                      </div>
                      <div class="gf-time-block">
                        <div class="gf-time">{fare['arr'].strftime('%H:%M')}</div>
                        <div class="gf-city">{dest[:3].upper()}</div>
                      </div>
                    </div>

                    <div class="gf-price-block">
                      <div class="gf-price">₹{price:,.0f}</div>
                      <div class="gf-price-label">per person</div>
                      <div class="gf-select-btn">Select</div>
                    </div>
                  </div>
                  <div class="gf-insights">
                    <span class="gf-badge {badge_cls}">{badge_txt}</span>
                    <span class="gf-badge gf-badge-blue">AI prediction</span>
                    {"<span class='gf-badge gf-badge-green'>Free cancellation</span>" if i==0 else ""}
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")

else:
    # Empty state
    st.markdown("""
    <div class="gf-empty">
      <div class="gf-empty-icon">✈️</div>
      <div class="gf-empty-title">Search for flights above</div>
      <div>Select your route, date and preferences to get AI-powered fare predictions</div>
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px;color:#5f6368;font-size:12px;border-top:1px solid #3c4043;margin-top:24px;">
  FlightFare AI · Powered by Random Forest ML · Indian domestic routes only · Fares are predictions, not actual prices
</div>""", unsafe_allow_html=True)
