import streamlit as st
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CS-RFM",
    page_icon="🌩️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0f0f13;
    color: #e8e8f0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Title block */
.title-block {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
}
.title-block h1 {
    font-size: 2rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 0;
}
.title-block p {
    color: #6b6b80;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    font-weight: 300;
}

/* Input card */
.input-card {
    background: #17171f;
    border: 1px solid #2a2a38;
    border-radius: 16px;
    padding: 2rem 2.2rem 1.6rem 2.2rem;
    margin-bottom: 1.5rem;
}
.input-card h3 {
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a4a60;
    margin: 0 0 1.5rem 0;
}

/* Streamlit number input tweaks */
.stNumberInput label {
    font-size: 0.85rem !important;
    color: #9090a8 !important;
    font-weight: 400 !important;
}
.stNumberInput input {
    background: #0f0f13 !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.1rem !important;
}
.stNumberInput input:focus {
    border-color: #5566ff !important;
    box-shadow: 0 0 0 3px rgba(85,102,255,0.15) !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: #5566ff;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    background: #4455ee;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* Result card */
.result-card {
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 0.5rem;
    border: 1px solid;
    animation: fadeUp 0.4s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    opacity: 0.6;
}
.result-segment {
    font-size: 1.8rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 0.6rem;
}
.result-desc {
    font-size: 0.9rem;
    font-weight: 300;
    line-height: 1.6;
    opacity: 0.75;
}
.result-action {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 0.82rem;
    font-weight: 400;
    opacity: 0.55;
    font-family: 'DM Mono', monospace;
}

/* RFM badge strip */
.badge-strip {
    display: flex;
    gap: 0.6rem;
    margin-top: 1rem;
}
.badge {
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.35rem 0.7rem;
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
}

/* Divider */
hr.subtle {
    border: none;
    border-top: 1px solid #1e1e28;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Segmentation logic ─────────────────────────────────────────────────────────
SEGMENTS = {
    "VIP": {
        "emoji": "🏆",
        "color_bg":     "#0d1f0d",
        "color_border": "#1a4020",
        "color_text":   "#4ade80",
        "desc": "Bought recently, orders frequently, and spends the most. Your absolute best customers.",
        "action": "→ Reward with loyalty perks & early product access",
    },
    "Loyal Customer": {
        "emoji": "💙",
        "color_bg":     "#0d1220",
        "color_border": "#1a2a50",
        "color_text":   "#60a5fa",
        "desc": "Purchase regularly with solid spend. Highly dependable segment with upsell potential.",
        "action": "→ Introduce premium tiers & referral incentives",
    },
    "Promising / New": {
        "emoji": "🌱",
        "color_bg":     "#0f1a12",
        "color_border": "#1e3a24",
        "color_text":   "#86efac",
        "desc": "Bought recently but haven't ordered many times yet. High potential if nurtured early.",
        "action": "→ Onboarding campaigns & first-order discounts",
    },
    "At Risk": {
        "emoji": "⚠️",
        "color_bg":     "#1a1200",
        "color_border": "#3a2800",
        "color_text":   "#fbbf24",
        "desc": "Used to purchase frequently but haven't been seen recently. Slipping away.",
        "action": "→ Win-back emails with personalized offers",
    },
    "Dormant": {
        "emoji": "💤",
        "color_bg":     "#180f0f",
        "color_border": "#341818",
        "color_text":   "#f87171",
        "desc": "Last purchase was a long time ago with low engagement overall. Hard to reactivate.",
        "action": "→ Aggressive reactivation campaign or sunset",
    },
}

# Median thresholds derived from the Online Retail dataset
R_MED = 50    # days
F_MED = 4     # orders
M_MED = 600   # £

def classify(recency, frequency, monetary):
    R, F, M = recency, frequency, monetary
    if R <= R_MED and F >= F_MED and M >= M_MED:
        return "VIP"
    elif R <= R_MED and F >= F_MED:
        return "Loyal Customers"
    elif R <= R_MED and F < F_MED:
        return "Promising Customers (New)"
    elif R > R_MED and F >= F_MED:
        return "At Risk "
    else:
        return "Dormant Customers"


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h3>🛒 Customer Segmentation</h3>
    <p>Enter RFM values to classify a customer into one of 5 segments</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card"><h3>RFM Inputs</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    recency = st.number_input(
        "Recency (days)", min_value=0, max_value=1000, value=30,
        help="Days since the customer's last purchase"
    )
with col2:
    frequency = st.number_input(
        "Frequency (orders)", min_value=0, max_value=500, value=5,
        help="Total number of distinct orders placed"
    )
with col3:
    monetary = st.number_input(
        "Monetary (£)", min_value=0, max_value=100000, value=800,
        help="Total amount spent by the customer"
    )

st.markdown('</div>', unsafe_allow_html=True)

classify_btn = st.button("Classify Now!")

if classify_btn:
    segment = classify(recency, frequency, monetary)
    s = SEGMENTS[segment]

    st.markdown(f"""
    <div class="result-card" style="
        background: {s['color_bg']};
        border-color: {s['color_border']};
    ">
        <div class="result-label">Segment</div>
        <div class="result-segment" style="color: {s['color_text']};">
            {s['emoji']} {segment}
        </div>
        <div class="result-desc">{s['desc']}</div>
        <div class="badge-strip">
            <span class="badge">R = {recency}d</span>
            <span class="badge">F = {frequency} orders</span>
            <span class="badge">M = £{monetary:,}</span>
        </div>
        <div class="result-action">{s['action']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Segment reference ──────────────────────────────────────────────────────────
with st.expander("View all 5 segments"):
    for name, s in SEGMENTS.items():
        st.markdown(f"""
        <div style="
            display:flex; align-items:flex-start; gap:1rem;
            padding: 0.9rem 1rem;
            background:#17171f;
            border-radius:12px;
            border-left: 3px solid {s['color_border']};
            margin-bottom: 0.6rem;
        ">
            <div style="font-size:1.4rem; margin-top:2px;">{s['emoji']}</div>
            <div>
                <div style="font-weight:500; color:{s['color_text']}; font-size:0.95rem;">{name}</div>
                <div style="font-size:0.82rem; color:#6b6b80; margin-top:2px;">{s['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
