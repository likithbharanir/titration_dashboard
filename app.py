"""
pH Variation During Titration — Interactive Simulation Dashboard
Python PBL Project

Team:
  1. Likith Bharani R        [1RV25CH015]
  2. Yashaswini Pishe        [1RV25CH043]
  3. Yelangi Nithin Kumar    [1RV25CH044]
"""

import io
import datetime

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="pH Titration Simulator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# DARK THEME STYLING (larger fonts throughout)
# ----------------------------------------------------------------------
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-size: 19px !important;
    }
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #131722 100%);
        color: #e8eaed;
    }
    .main-header {
        padding: 1.6rem 2.2rem;
        background: linear-gradient(90deg, #1b2735 0%, #0f1620 100%);
        border-radius: 14px;
        border: 1px solid #2a3441;
        margin-bottom: 1.2rem;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        color: #b0bac8;
        margin: 0.4rem 0 0 0;
        font-size: 1.15rem;
    }
    .team-box {
        font-size: 1.05rem;
        color: #b0bac8;
        line-height: 1.6;
        margin-top: 0.8rem;
        border-top: 1px solid #2a3441;
        padding-top: 0.8rem;
    }
    .result-card {
        background: linear-gradient(135deg, #1a2332 0%, #131b28 100%);
        border: 1px solid #2a3441;
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        text-align: center;
    }
    .result-card .label {
        color: #a3adba;
        font-size: 1.0rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .result-card .value {
        color: #4fd1c5;
        font-size: 2.4rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    .result-card .sub {
        color: #8b95a5;
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #0f1420;
        border-right: 1px solid #2a3441;
        font-size: 1.05rem !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 1.5rem !important;
    }
    label, .stSlider label, .stSelectbox label {
        font-size: 1.05rem !important;
        color: #dfe4ea !important;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 1.15rem !important;
        line-height: 1.6;
    }
    h1 { font-size: 2.3rem !important; }
    h2 { font-size: 1.9rem !important; }
    h3 { font-size: 1.5rem !important; }
    .stChatMessage p {
        font-size: 1.15rem !important;
        line-height: 1.6;
    }
    .stButton button {
        font-size: 1.1rem !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stDownloadButton button {
        font-size: 1.1rem !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.15rem !important;
        padding: 0.8rem 1.4rem !important;
        background-color: #131b28;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a2332 !important;
        color: #4fd1c5 !important;
    }
    .indicator-swatch {
        width: 100%;
        height: 90px;
        border-radius: 12px;
        border: 1px solid #2a3441;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.3rem;
        color: #0e1117;
        text-shadow: 0 1px 2px rgba(255,255,255,0.25);
    }
    .indicator-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0.2rem;
        border-bottom: 1px solid #2a3441;
        font-size: 1.0rem;
    }
    .indicator-row.active {
        background: rgba(79, 209, 197, 0.12);
        border-radius: 8px;
        font-weight: 700;
        color: #4fd1c5;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🧪 pH Variation During Titration — Simulator</h1>
    <p>Interactive acid–base titration curve generator | Python PBL</p>
    <div class="team-box">
        <b>Team:</b> Likith Bharani R (1RV25CH015) &nbsp;|&nbsp;
        Yashaswini Pishe (1RV25CH043) &nbsp;|&nbsp;
        Yelangi Nithin Kumar (1RV25CH044)
    </div>
</div>
""", unsafe_allow_html=True)

Kw = 1.0e-14

# ----------------------------------------------------------------------
# SIDEBAR — TITRATION INPUTS
# ----------------------------------------------------------------------
st.sidebar.header("⚙️ Titration Setup")

mode = st.sidebar.selectbox(
    "Titration Type",
    ["Strong Acid vs Strong Base", "Weak Acid vs Strong Base", "Weak Base vs Strong Acid"],
)

st.sidebar.subheader("Analyte (in flask)")
C0 = st.sidebar.slider("Concentration (mol/L)", 0.01, 1.0, 0.10, 0.01)
V0 = st.sidebar.slider("Volume (mL)", 10.0, 100.0, 25.0, 1.0)

if mode != "Strong Acid vs Strong Base":
    pKlabel = "pKa (weak acid)" if mode == "Weak Acid vs Strong Base" else "pKb (weak base)"
    pK = st.sidebar.slider(pKlabel, 2.0, 10.0, 4.76, 0.01)
    K = 10 ** (-pK)
else:
    pK = None
    K = None

st.sidebar.subheader("Titrant (from burette)")
Ct = st.sidebar.slider("Titrant Concentration (mol/L)", 0.01, 1.0, 0.10, 0.01)

Veq = (C0 * V0) / Ct  # mL of titrant at equivalence
Vmax = st.sidebar.slider("Max Titrant Added (mL)", float(Veq * 1.2), float(Veq * 3), float(Veq * 2))

Vt_current = st.sidebar.slider("Titrant Volume Added Now (mL)", 0.0, float(Vmax), float(Veq / 2), 0.05)

st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Chat Assistant")
api_key = st.sidebar.text_input(
    "Google Gemini API Key (free)",
    type="password",
    help=(
        "Free — no credit card needed. Get one at aistudio.google.com: "
        "sign in with any Google account → 'Get API key' → 'Create API key'. "
        "Paste it here to enable the AI Tutor tab."
    ),
)

# ----------------------------------------------------------------------
# pH CALCULATION ENGINE
# ----------------------------------------------------------------------
def ph_strong_strong(Vb):
    """Strong acid (analyte) titrated with strong base (titrant)."""
    total_V = (V0 + Vb) / 1000.0
    mol_acid = C0 * V0 / 1000.0
    mol_base = Ct * Vb / 1000.0
    net = mol_acid - mol_base
    if abs(net) < 1e-14:
        return 7.0
    if net > 0:
        H = net / total_V
        return -np.log10(H)
    else:
        OH = -net / total_V
        pOH = -np.log10(OH)
        return 14.0 - pOH


def ph_weak_acid_strong_base(Vb, Ka):
    """Weak acid HA (analyte) titrated with strong base (titrant)."""
    total_V = (V0 + Vb) / 1000.0
    mol_HA0 = C0 * V0 / 1000.0
    mol_base = Ct * Vb / 1000.0

    if Vb <= 1e-9:
        C = C0
        a, b, c = 1.0, Ka, -Ka * C
        H = (-b + np.sqrt(b**2 - 4 * a * c)) / (2 * a)
        return -np.log10(H)

    mol_HA = mol_HA0 - mol_base
    mol_A = mol_base

    if mol_HA > 1e-12:
        pKa = -np.log10(Ka)
        return pKa + np.log10(mol_A / mol_HA)
    elif abs(mol_HA) <= 1e-12:
        C_A = mol_A / total_V
        Kb = Kw / Ka
        OH = np.sqrt(Kb * C_A)
        pOH = -np.log10(OH)
        return 14.0 - pOH
    else:
        excess = mol_base - mol_HA0
        OH = excess / total_V
        pOH = -np.log10(OH)
        return 14.0 - pOH


def ph_weak_base_strong_acid(Va, Kb):
    """Weak base B (analyte) titrated with strong acid (titrant)."""
    total_V = (V0 + Va) / 1000.0
    mol_B0 = C0 * V0 / 1000.0
    mol_acid = Ct * Va / 1000.0

    if Va <= 1e-9:
        C = C0
        a, b, c = 1.0, Kb, -Kb * C
        OH = (-b + np.sqrt(b**2 - 4 * a * c)) / (2 * a)
        pOH = -np.log10(OH)
        return 14.0 - pOH

    mol_B = mol_B0 - mol_acid
    mol_BH = mol_acid

    if mol_B > 1e-12:
        pKb = -np.log10(Kb)
        pOH = pKb + np.log10(mol_BH / mol_B)
        return 14.0 - pOH
    elif abs(mol_B) <= 1e-12:
        C_BH = mol_BH / total_V
        Ka = Kw / Kb
        H = np.sqrt(Ka * C_BH)
        return -np.log10(H)
    else:
        excess = mol_acid - mol_B0
        H = excess / total_V
        return -np.log10(H)


def compute_ph(Vb, mode, K):
    try:
        if mode == "Strong Acid vs Strong Base":
            return ph_strong_strong(Vb)
        elif mode == "Weak Acid vs Strong Base":
            return ph_weak_acid_strong_base(Vb, K)
        else:
            return ph_weak_base_strong_acid(Vb, K)
    except (ValueError, ZeroDivisionError):
        return np.nan


# ----------------------------------------------------------------------
# GENERATE CURVE
# ----------------------------------------------------------------------
volumes = np.linspace(0.0001, Vmax, 600)
ph_values = np.array([compute_ph(v, mode, K) for v in volumes])
ph_values = np.clip(ph_values, 0, 14)

current_ph = compute_ph(Vt_current, mode, K)
current_ph = float(np.clip(current_ph, 0, 14))
ph_at_eq = compute_ph(Veq, mode, K)
ph_at_eq = float(np.clip(ph_at_eq, 0, 14))

# First-derivative curve (innovative addition #1) — the classic graphical
# method for locating the equivalence point from experimental titration data.
dph_dv = np.gradient(ph_values, volumes)
deriv_peak_idx = int(np.argmax(np.abs(dph_dv)))
deriv_peak_vol = float(volumes[deriv_peak_idx])
deriv_peak_val = float(dph_dv[deriv_peak_idx])

# ----------------------------------------------------------------------
# UNIVERSAL INDICATOR COLOUR MODEL (innovative addition #2)
# ----------------------------------------------------------------------
_UI_STOPS = [0, 2, 4, 6, 7, 8, 10, 12, 14]
_UI_COLORS = [
    (211, 47, 47),    # 0  red
    (244, 81, 30),    # 2  red-orange
    (255, 160, 0),    # 4  orange
    (251, 224, 60),   # 6  yellow
    (139, 195, 74),   # 7  green
    (38, 166, 154),   # 8  teal
    (30, 136, 229),   # 10 blue
    (94, 53, 177),    # 12 indigo
    (156, 39, 176),   # 14 violet
]


def universal_indicator_color(ph_val):
    ph_val = float(np.clip(ph_val, 0, 14))
    r = np.interp(ph_val, _UI_STOPS, [c[0] for c in _UI_COLORS])
    g = np.interp(ph_val, _UI_STOPS, [c[1] for c in _UI_COLORS])
    b = np.interp(ph_val, _UI_STOPS, [c[2] for c in _UI_COLORS])
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


_UI_COLOR_NAMES = ["Red", "Red-Orange", "Orange", "Yellow", "Green", "Teal", "Blue", "Indigo", "Violet"]


def color_name_for_ph(ph_val):
    """Nearest plain-language colour name for the universal-indicator model at this pH."""
    ph_val = float(np.clip(ph_val, 0, 14))
    idx = min(range(len(_UI_STOPS)), key=lambda i: abs(_UI_STOPS[i] - ph_val))
    return _UI_COLOR_NAMES[idx]


INDICATORS = [
    {"name": "Methyl Orange", "low": 3.1, "high": 4.4, "off_color": "#e53935", "on_color": "#ffee58",
     "color_change_text": "Red -> Yellow"},
    {"name": "Bromothymol Blue", "low": 6.0, "high": 7.6, "off_color": "#ffee58", "on_color": "#1e88e5",
     "color_change_text": "Yellow -> Blue"},
    {"name": "Phenolphthalein", "low": 8.2, "high": 10.0, "off_color": "#f5f5f5", "on_color": "#d81b60",
     "color_change_text": "Colourless -> Pink"},
]


def recommended_indicator(ph_eq):
    best = min(INDICATORS, key=lambda ind: abs((ind["low"] + ind["high"]) / 2 - ph_eq))
    return best["name"]


rec_indicator = recommended_indicator(ph_at_eq)

# ----------------------------------------------------------------------
# TOP-LEVEL NAVIGATION — dedicated full-width sections (no more small popups)
# ----------------------------------------------------------------------
tab_sim, tab_chat, tab_report = st.tabs(
    ["📊 Titration Simulator", "🤖 AI Tutor", "📄 PDF Report"]
)

# ========================================================================
# TAB 1 — SIMULATOR
# ========================================================================
with tab_sim:
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Current pH", f"{current_ph:.2f}", f"at {Vt_current:.2f} mL added"),
        (c2, "Equivalence Volume", f"{Veq:.2f} mL", "titrant required"),
        (c3, "pH at Equivalence", f"{ph_at_eq:.2f}", "theoretical"),
        (c4, "% Titrated", f"{min(Vt_current/Veq*100, 999):.1f}%", "of equivalence"),
    ]
    for col, label, value, sub in cards:
        col.markdown(f"""
        <div class="result-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=volumes, y=ph_values, mode="lines",
        line=dict(color="#4fd1c5", width=3),
        name="pH Curve", hovertemplate="Vol: %{x:.2f} mL<br>pH: %{y:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[Veq], y=[ph_at_eq], mode="markers+text",
        marker=dict(color="#f6ad55", size=13, symbol="diamond"),
        text=["Equivalence Point"], textposition="top center",
        textfont=dict(color="#f6ad55", size=14),
        name="Equivalence Point"
    ))
    fig.add_trace(go.Scatter(
        x=[Vt_current], y=[current_ph], mode="markers",
        marker=dict(color="#fc8181", size=15, line=dict(color="white", width=2)),
        name="Current Point"
    ))
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#131722",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8eaed", size=15),
        xaxis_title="Volume of Titrant Added (mL)",
        yaxis_title="pH",
        yaxis=dict(range=[0, 14], gridcolor="#2a3441"),
        xaxis=dict(gridcolor="#2a3441"),
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=30, t=40, b=50),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📘 Chemistry Notes"):
        if mode == "Strong Acid vs Strong Base":
            st.markdown("""
            - Sharp, symmetric S-curve with equivalence point at **pH 7**.
            - No buffer region — [H⁺] / [OH⁻] determined directly from excess moles.
            """)
        elif mode == "Weak Acid vs Strong Base":
            st.markdown(f"""
            - **Buffer region** (before equivalence) follows Henderson–Hasselbalch:
              pH = pKa + log([A⁻]/[HA]), pKa = {-np.log10(K):.2f}
            - **Equivalence point is basic** (pH > 7) due to hydrolysis of the conjugate base A⁻.
            - Half-equivalence volume ({Veq/2:.2f} mL) gives pH = pKa — useful for Ka determination.
            """)
        else:
            st.markdown(f"""
            - **Buffer region** follows: pOH = pKb + log([BH⁺]/[B]), pKb = {-np.log10(K):.2f}
            - **Equivalence point is acidic** (pH < 7) due to hydrolysis of the conjugate acid BH⁺.
            - Half-equivalence volume ({Veq/2:.2f} mL) gives pOH = pKb.
            """)

    st.caption("Simulation uses standard equilibrium approximations (Henderson–Hasselbalch for buffer regions, "
               "hydrolysis equilibrium at equivalence). Intended for educational demonstration.")

    st.divider()

    # -------- INNOVATIVE ADDITION 1: First-derivative equivalence finder --------
    st.subheader("🔬 Graphical Equivalence-Point Detection (1st Derivative Method)")
    st.caption(
        "A real analytical-chemistry technique: plotting dpH/dV against volume turns the "
        "inflection point of the S-curve into a sharp peak, which is far easier to read "
        "precisely from experimental burette data than eyeballing the inflection itself."
    )
    deriv_fig = go.Figure()
    deriv_fig.add_trace(go.Scatter(
        x=volumes, y=dph_dv, mode="lines",
        line=dict(color="#f6ad55", width=2.5),
        name="dpH/dV", hovertemplate="Vol: %{x:.2f} mL<br>dpH/dV: %{y:.2f}<extra></extra>"
    ))
    deriv_fig.add_trace(go.Scatter(
        x=[deriv_peak_vol], y=[deriv_peak_val], mode="markers+text",
        marker=dict(color="#fc8181", size=13, symbol="star"),
        text=[f"Peak @ {deriv_peak_vol:.2f} mL"], textposition="top center",
        textfont=dict(color="#fc8181", size=13),
        name="Steepest Point"
    ))
    deriv_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#131722",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8eaed", size=14),
        xaxis_title="Volume of Titrant Added (mL)",
        yaxis_title="dpH / dV",
        xaxis=dict(gridcolor="#2a3441"),
        yaxis=dict(gridcolor="#2a3441"),
        height=380,
        margin=dict(l=60, r=30, t=30, b=50),
        showlegend=False,
    )
    st.plotly_chart(deriv_fig, use_container_width=True)
    d1, d2 = st.columns(2)
    d1.info(f"Peak of dpH/dV located at **{deriv_peak_vol:.2f} mL**")
    d2.info(f"Theoretical equivalence volume: **{Veq:.2f} mL** (agreement confirms the model)")

    st.divider()

    # -------- INNOVATIVE ADDITION 2: Live universal-indicator colour guide --------
    st.subheader("🎨 Live Universal Indicator & Indicator Selection Guide")
    st.caption(
        "Colour a chemist would actually observe in the flask at the current pH, plus which "
        "real indicator's colour-change range best brackets this titration's equivalence point."
    )
    ind_col1, ind_col2 = st.columns([1, 2])
    with ind_col1:
        swatch_color = universal_indicator_color(current_ph)
        st.markdown(
            f'<div class="indicator-swatch" style="background:{swatch_color};">'
            f'pH {current_ph:.2f}</div>',
            unsafe_allow_html=True,
        )
        st.caption("Simulated colour of universal indicator solution at the current volume added.")
    with ind_col2:
        st.markdown(f"**Recommended indicator for this titration: `{rec_indicator}`**")
        for ind in INDICATORS:
            active = ind["name"] == rec_indicator
            row_class = "indicator-row active" if active else "indicator-row"
            marker = "✅ " if active else ""
            st.markdown(
                f'<div class="{row_class}">'
                f'<span>{marker}{ind["name"]} &nbsp;({ind["color_change_text"]})</span>'
                f'<span>pH {ind["low"]:.1f} – {ind["high"]:.1f}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.caption(
            f"Equivalence point pH = {ph_at_eq:.2f} → an indicator whose colour-change range "
            f"brackets this value will change colour right at (or very near) the equivalence "
            f"volume, minimising titration error."
        )

# ========================================================================
# TAB 2 — AI TUTOR (full-page, dedicated section)
# ========================================================================
with tab_chat:
    st.subheader("🤖 Titration AI Tutor")
    st.caption(
        "Ask anything about acid–base titration, pH curves, buffers, or indicators. "
        "Answers are saved and included in your downloadable PDF report."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    SYSTEM_PROMPT = (
        "You are a patient chemistry tutor helping an undergraduate Chemical Engineering student "
        "understand acid-base titration and pH curves for a college PBL project. "
        "Explain clearly with correct terminology (Henderson-Hasselbalch, equivalence point, "
        "buffer region, indicators, Ka/Kb, hydrolysis). Keep answers focused and well-structured, "
        "using plain sentences and simple '-' bullet points rather than markdown headers. "
        "When relevant, relate the answer to the current simulation setup the student describes."
    )

    chat_display = st.container(height=520)
    with chat_display:
        if not st.session_state.chat_history:
            st.info("No messages yet — ask your first question below.")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_question = st.chat_input("Type your question here...", key="chat_input_tab")

    if user_question:
        if not api_key:
            st.warning("Enter your free Google Gemini API key in the sidebar first.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)

                context_note = (
                    f"\n\n[Current simulation context: {mode}, analyte {C0} mol/L in {V0} mL, "
                    f"titrant {Ct} mol/L, equivalence volume {Veq:.2f} mL"
                    + (f", pK = {pK:.2f}" if pK is not None else "")
                    + "]"
                )

                gemini_contents = []
                for m in st.session_state.chat_history[:-1]:
                    role = "model" if m["role"] == "assistant" else "user"
                    gemini_contents.append(
                        types.Content(role=role, parts=[types.Part(text=m["content"])])
                    )
                gemini_contents.append(
                    types.Content(role="user", parts=[types.Part(text=user_question + context_note)])
                )

                with st.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=gemini_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            max_output_tokens=1000,
                        ),
                    )
                    answer_text = response.text

                st.session_state.chat_history.append({"role": "assistant", "content": answer_text})
                st.rerun()

            except Exception as e:
                st.error(f"Could not reach the AI assistant: {e}")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear_chat_tab"):
            st.session_state.chat_history = []
            st.rerun()

# ----------------------------------------------------------------------
# PDF REPORT GENERATION
# ----------------------------------------------------------------------
def sanitize_for_pdf(text):
    """Escape XML-special characters and convert simple markdown so ReportLab's
    mini-XML Paragraph parser doesn't choke on raw '<', '>', '&', or markdown
    bullets/bold coming from the AI or from chemistry notation (e.g. 'pH < 7')."""
    import re
    if text is None:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?m)^\s*-\s+", "&bull;&nbsp;", text)
    text = text.replace("\r\n", "\n").replace("\n", "<br/>")
    return text


def build_pdf_figure():
    """A light-themed, print-safe copy of the titration curve for the PDF —
    the dark dashboard theme rendered with near-invisible gridlines/labels on
    a white PDF page, so the report uses higher-contrast colours instead."""
    pfig = go.Figure()
    pfig.add_trace(go.Scatter(
        x=volumes, y=ph_values, mode="lines",
        line=dict(color="#0f6b64", width=3), name="pH Curve"
    ))
    pfig.add_trace(go.Scatter(
        x=[Veq], y=[ph_at_eq], mode="markers+text",
        marker=dict(color="#c05621", size=12, symbol="diamond"),
        text=["Equivalence Point"], textposition="top center",
        textfont=dict(color="#c05621", size=13),
        name="Equivalence Point"
    ))
    pfig.add_trace(go.Scatter(
        x=[Vt_current], y=[current_ph], mode="markers",
        marker=dict(color="#c53030", size=13, line=dict(color="#1a202c", width=1.5)),
        name="Current Point"
    ))
    pfig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#1a202c", size=15),
        xaxis_title="Volume of Titrant Added (mL)",
        yaxis_title="pH",
        yaxis=dict(range=[0, 14], gridcolor="#d0d5dd", zeroline=False),
        xaxis=dict(gridcolor="#d0d5dd", zeroline=False),
        height=480,
        width=850,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=55, r=25, t=35, b=45),
    )
    return pfig


def build_pdf_derivative_figure():
    pfig = go.Figure()
    pfig.add_trace(go.Scatter(
        x=volumes, y=dph_dv, mode="lines",
        line=dict(color="#b7791f", width=2.5), name="dpH/dV"
    ))
    pfig.add_trace(go.Scatter(
        x=[deriv_peak_vol], y=[deriv_peak_val], mode="markers+text",
        marker=dict(color="#c53030", size=11, symbol="star"),
        text=[f"Peak @ {deriv_peak_vol:.2f} mL"], textposition="top center",
        textfont=dict(color="#c53030", size=12),
        name="Steepest Point"
    ))
    pfig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#1a202c", size=14),
        xaxis_title="Volume of Titrant Added (mL)",
        yaxis_title="dpH / dV",
        xaxis=dict(gridcolor="#d0d5dd", zeroline=False),
        yaxis=dict(gridcolor="#d0d5dd", zeroline=False),
        height=340,
        width=850,
        showlegend=False,
        margin=dict(l=55, r=25, t=25, b=45),
    )
    return pfig


def build_pdf_report():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=19, spaceAfter=4)
    heading_style = ParagraphStyle("HeadingStyle", parent=styles["Heading2"], fontSize=14, spaceBefore=10, spaceAfter=5)
    sub_heading_style = ParagraphStyle("SubHeadingStyle", parent=styles["Heading3"], fontSize=12, spaceBefore=7, spaceAfter=3)
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10.5, leading=14.5)
    formula_style = ParagraphStyle(
        "FormulaStyle", parent=styles["Normal"], fontSize=11, leading=15,
        fontName="Helvetica-Bold", textColor=colors.HexColor("#0f6b64"),
        spaceBefore=3, spaceAfter=3, leftIndent=10,
    )
    qa_q_style = ParagraphStyle(
        "QStyle", parent=styles["Normal"], fontSize=10.5, leading=14,
        textColor=colors.HexColor("#1a2332"), spaceBefore=6, fontName="Helvetica-Bold"
    )
    qa_a_style = ParagraphStyle("AStyle", parent=styles["Normal"], fontSize=10.5, leading=14, spaceAfter=4)

    def table_style(header_bg="#1a2332"):
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])

    story = []

    story.append(Paragraph("pH Variation During Titration &mdash; Report", title_style))
    story.append(Paragraph(
        "Team: Likith Bharani R (1RV25CH015) | Yashaswini Pishe (1RV25CH043) | "
        "Yelangi Nithin Kumar (1RV25CH044)", body_style
    ))
    story.append(Paragraph(
        f"Generated: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}", body_style
    ))
    story.append(Spacer(1, 8))

    # ---- Setup table ----
    story.append(Paragraph("Titration Setup", heading_style))
    setup_data = [
        ["Parameter", "Value"],
        ["Titration Type", mode],
        ["Analyte Concentration (C0)", f"{C0} mol/L"],
        ["Analyte Volume (V0)", f"{V0} mL"],
        ["Titrant Concentration (Ct)", f"{Ct} mol/L"],
    ]
    if pK is not None:
        label = "pKa" if mode == "Weak Acid vs Strong Base" else "pKb"
        setup_data.append([label, f"{pK:.2f}  (K = {K:.3e})"])
    setup_table = Table(setup_data, colWidths=[250, 250])
    setup_table.setStyle(table_style())
    story.append(setup_table)
    story.append(Spacer(1, 8))

    # ---- Results table ----
    story.append(Paragraph("Calculated Results", heading_style))
    results_data = [
        ["Quantity", "Value"],
        ["Titrant Volume Added (current)", f"{Vt_current:.2f} mL"],
        ["Current pH", f"{current_ph:.2f}"],
        ["Equivalence Volume (theoretical)", f"{Veq:.2f} mL"],
        ["Equivalence Volume (1st-derivative peak)", f"{deriv_peak_vol:.2f} mL"],
        ["pH at Equivalence Point", f"{ph_at_eq:.2f}"],
        ["% of Equivalence Reached", f"{min(Vt_current/Veq*100, 999):.1f} %"],
        ["Recommended Indicator", rec_indicator],
    ]
    results_table = Table(results_data, colWidths=[300, 200])
    results_table.setStyle(table_style())
    story.append(results_table)
    story.append(Spacer(1, 10))

    # ---- Formulae & Calculations (full worked derivation) ----
    story.append(Paragraph("Formulae &amp; Calculations", heading_style))

    story.append(Paragraph("General relations used throughout:", body_style))
    story.append(Paragraph("pH = -log10[H+]", formula_style))
    story.append(Paragraph("pOH = -log10[OH-]", formula_style))
    story.append(Paragraph("pH + pOH = 14  (at 25&deg;C, since Kw = [H+][OH-] = 1.0 &times; 10^-14)", formula_style))

    story.append(Paragraph("Equivalence volume:", sub_heading_style))
    story.append(Paragraph("Veq = (C0 &times; V0) / Ct", formula_style))
    story.append(Paragraph(
        f"Substituting: Veq = ({C0} mol/L &times; {V0} mL) / {Ct} mol/L = <b>{Veq:.2f} mL</b>",
        body_style
    ))

    if mode == "Strong Acid vs Strong Base":
        story.append(Paragraph("Before equivalence (excess strong acid):", sub_heading_style))
        story.append(Paragraph(
            "[H+] = (mol acid - mol base) / total volume,  pH = -log10[H+]",
            formula_style
        ))
        story.append(Paragraph("After equivalence (excess strong base):", sub_heading_style))
        story.append(Paragraph(
            "[OH-] = (mol base - mol acid) / total volume,  pOH = -log10[OH-],  pH = 14 - pOH",
            formula_style
        ))
        mol_analyte = C0 * V0 / 1000.0
        mol_titrant_now = Ct * Vt_current / 1000.0
        total_V_now = (V0 + Vt_current) / 1000.0
        story.append(Paragraph(
            f"Worked example at {Vt_current:.2f} mL added: mol analyte = {mol_analyte:.5f} mol, "
            f"mol titrant = {mol_titrant_now:.5f} mol, total volume = {total_V_now:.4f} L "
            f"-> calculated pH = <b>{current_ph:.2f}</b> (matches simulator).",
            body_style
        ))

    elif mode == "Weak Acid vs Strong Base":
        pKa_val = -np.log10(K)
        story.append(Paragraph("Before any titrant is added (weak acid equilibrium):", sub_heading_style))
        story.append(Paragraph("Ka = [H+][A-] / [HA]  ->  [H+]^2 + Ka[H+] - Ka&middot;C0 = 0", formula_style))
        story.append(Paragraph("Buffer region (Henderson&ndash;Hasselbalch):", sub_heading_style))
        story.append(Paragraph("pH = pKa + log10([A-] / [HA])", formula_style))
        story.append(Paragraph(
            f"pKa = -log10(Ka) = <b>{pKa_val:.2f}</b>  "
            f"(at the half-equivalence volume, {Veq/2:.2f} mL, [A-] = [HA] so pH = pKa exactly)",
            body_style
        ))
        story.append(Paragraph("At equivalence (solution of conjugate base A-, hydrolysis):", sub_heading_style))
        story.append(Paragraph("Kb = Kw / Ka,   [OH-] = sqrt(Kb &times; C_A),   pOH = -log10[OH-],  pH = 14 - pOH", formula_style))
        story.append(Paragraph(
            f"Worked example: at Veq = {Veq:.2f} mL, C_A = {(C0*V0/1000)/((V0+Veq)/1000):.4f} mol/L "
            f"-> calculated pH at equivalence = <b>{ph_at_eq:.2f}</b> (basic, as expected for a weak acid/strong base titration).",
            body_style
        ))

    else:
        pKb_val = -np.log10(K)
        story.append(Paragraph("Before any titrant is added (weak base equilibrium):", sub_heading_style))
        story.append(Paragraph("Kb = [BH+][OH-] / [B]  ->  [OH-]^2 + Kb[OH-] - Kb&middot;C0 = 0", formula_style))
        story.append(Paragraph("Buffer region:", sub_heading_style))
        story.append(Paragraph("pOH = pKb + log10([BH+] / [B]),  pH = 14 - pOH", formula_style))
        story.append(Paragraph(
            f"pKb = -log10(Kb) = <b>{pKb_val:.2f}</b>  "
            f"(at half-equivalence volume, {Veq/2:.2f} mL, pOH = pKb exactly)",
            body_style
        ))
        story.append(Paragraph("At equivalence (solution of conjugate acid BH+, hydrolysis):", sub_heading_style))
        story.append(Paragraph("Ka = Kw / Kb,   [H+] = sqrt(Ka &times; C_BH),   pH = -log10[H+]", formula_style))
        story.append(Paragraph(
            f"Worked example: at Veq = {Veq:.2f} mL, C_BH = {(C0*V0/1000)/((V0+Veq)/1000):.4f} mol/L "
            f"-> calculated pH at equivalence = <b>{ph_at_eq:.2f}</b> (acidic, as expected for a weak base/strong acid titration).",
            body_style
        ))

    story.append(Paragraph("Graphical (1st-derivative) equivalence-point method:", sub_heading_style))
    story.append(Paragraph(
        f"The equivalence point also corresponds to the maximum of dpH/dV. Numerically, the "
        f"peak occurs at {deriv_peak_vol:.2f} mL, closely matching the stoichiometric value of "
        f"{Veq:.2f} mL &mdash; this is the standard technique for locating equivalence points from "
        f"real (noisy) experimental burette data where the inflection is hard to see by eye.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # ---- Curve image ----
    story.append(Paragraph("Titration Curve", heading_style))
    try:
        img_bytes = build_pdf_figure().to_image(format="png", scale=2)
        story.append(Image(io.BytesIO(img_bytes), width=6.6 * inch, height=3.7 * inch))
    except Exception:
        story.append(Paragraph(
            "(Curve image could not be embedded — install the 'kaleido' package: pip install kaleido)",
            body_style
        ))

    # ---- Derivative curve image ----
    story.append(Paragraph("First-Derivative Curve (Equivalence-Point Detection)", heading_style))
    try:
        img_bytes2 = build_pdf_derivative_figure().to_image(format="png", scale=2)
        story.append(Image(io.BytesIO(img_bytes2), width=6.6 * inch, height=2.65 * inch))
    except Exception:
        story.append(Paragraph("(Derivative curve image could not be embedded.)", body_style))
    story.append(Spacer(1, 6))

    # ---- Indicator guide table (now including the actual colours involved) ----
    story.append(Paragraph("Indicator Selection Guide", heading_style))

    current_color_name = color_name_for_ph(current_ph)
    current_hex = universal_indicator_color(current_ph)

    # Small visual swatch so the report shows the colour, not just names.
    swatch_table = Table(
        [[""]],
        colWidths=[80], rowHeights=[36]
    )
    swatch_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(current_hex)),
        ("BOX", (0, 0), (0, 0), 0.75, colors.HexColor("#333333")),
    ]))
    swatch_row = Table(
        [[swatch_table, Paragraph(
            f"Simulated solution colour at the current volume added "
            f"(pH {current_ph:.2f}): <b>{current_color_name}</b> "
            f"(approx. colour code {current_hex}), based on a universal-indicator colour model.",
            body_style
        )]],
        colWidths=[90, 400]
    )
    swatch_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(swatch_row)
    story.append(Spacer(1, 8))

    ind_data = [["Indicator", "pH Range", "Colour Change", "Suitable?"]]
    for ind in INDICATORS:
        suitable = "Yes — recommended" if ind["name"] == rec_indicator else "No"
        ind_data.append([
            ind["name"],
            f'{ind["low"]:.1f} - {ind["high"]:.1f}',
            ind["color_change_text"],
            suitable,
        ])
    ind_table = Table(ind_data, colWidths=[130, 90, 160, 120])
    ind_table.setStyle(table_style())
    story.append(ind_table)
    story.append(Spacer(1, 10))

    # ---- Chemistry notes (flows naturally — no forced page break) ----
    story.append(Paragraph("Chemistry Notes", heading_style))
    if mode == "Strong Acid vs Strong Base":
        notes = "Sharp, symmetric S-curve with equivalence point at pH 7. No buffer region."
    elif mode == "Weak Acid vs Strong Base":
        notes = (f"Buffer region follows Henderson-Hasselbalch: pH = pKa + log([A-]/[HA]), "
                 f"pKa = {-np.log10(K):.2f}. Equivalence point is basic due to hydrolysis of A-.")
    else:
        notes = (f"Buffer region follows: pOH = pKb + log([BH+]/[B]), pKb = {-np.log10(K):.2f}. "
                 f"Equivalence point is acidic due to hydrolysis of BH+.")
    story.append(Paragraph(sanitize_for_pdf(notes), body_style))
    story.append(Spacer(1, 8))

    # ---- Chat Q&A ----
    if st.session_state.get("chat_history"):
        story.append(Paragraph("AI Tutor &mdash; Questions &amp; Answers", heading_style))
        for m in st.session_state.chat_history:
            safe_content = sanitize_for_pdf(m["content"])
            if m["role"] == "user":
                story.append(Paragraph(f"Q: {safe_content}", qa_q_style))
            else:
                story.append(Paragraph(f"A: {safe_content}", qa_a_style))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


# ========================================================================
# TAB 3 — PDF REPORT
# ========================================================================
with tab_report:
    st.subheader("📄 Download PDF Report")
    st.caption(
        "Bundles your setup, calculated results, full formulae with worked substitutions, "
        "the titration curve, the derivative-method equivalence check, the indicator guide, "
        "and the AI tutor transcript into one compact report."
    )

    if st.button("Generate PDF Report", key="generate_pdf_tab"):
        with st.spinner("Building PDF..."):
            try:
                pdf_bytes = build_pdf_report()
                st.session_state["pdf_bytes"] = pdf_bytes
                st.success("PDF ready — click below to download.")
            except Exception as e:
                st.error(f"Could not build the PDF: {e}")

    if "pdf_bytes" in st.session_state:
        st.download_button(
            label="⬇️ Download PDF",
            data=st.session_state["pdf_bytes"],
            file_name=f"titration_report_{datetime.date.today()}.pdf",
            mime="application/pdf",
            key="download_pdf_tab",
        )