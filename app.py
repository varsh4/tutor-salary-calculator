import math
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Tutor Salary Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PAYMENT RULES
# ============================================================
SESSION_RATE = 375.0
WAIT_RATE_HIGH = 100.0       # Wait % > 85%
WAIT_RATE_LOW = 195.0        # Wait % <= 85%
WAIT_THRESHOLD = 85.0
MAX_SESSION_LENGTH = 60      # minutes

# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 35%, #f5f3ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.2rem;
        color: #111827;
    }
    .subtitle {
        color: #4b5563;
        font-size: 1.05rem;
        margin-bottom: 1.75rem;
        font-weight: 500;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #4f46e5, #8b5cf6);
        color: white;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        color: #111827;
    }
    .small-note {
        color: #6b7280;
        font-size: 0.88rem;
    }
    .calc-box {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 16px;
        background: rgba(255,255,255,0.7);
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.08);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        color: #4b5563;
        font-weight: 600;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 100%);
    }
    .stTabs [role="tablist"] {
        gap: 0.5rem;
    }
    .stTabs [role="tab"] {
        background: rgba(255,255,255,0.7);
        border-radius: 12px 12px 0 0;
        padding: 0.6rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="hero-badge">Live salary estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">💰 Tutor Salary Calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Monthly salary estimate • 85% wait-time target • premium pay dashboard</div>',
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR — PAYMENT RULES
# ============================================================
with st.sidebar:
    st.header("⚙️ Payment Rules")

    st.metric("Session Rate", f"₹{SESSION_RATE:,.0f}/hr")
    st.metric("Wait Rate > 85%", f"₹{WAIT_RATE_HIGH:,.0f}/hr")
    st.metric("Wait Rate ≤ 85%", f"₹{WAIT_RATE_LOW:,.0f}/hr")

    st.divider()

    st.markdown("**Maximum individual session**")
    st.write(f"{MAX_SESSION_LENGTH} minutes")

    st.markdown("**Wait-time formula**")
    st.latex(
        r"\frac{\text{Wait Minutes}}{\text{Wait Minutes}+\text{Session Minutes}}\times100"
    )

    st.divider()
    st.caption("Monthly reports provide aggregate minutes, so the exact number of individual sessions cannot be determined.")

# ============================================================
# 1. MONTHLY REPORT INPUT
# ============================================================
st.markdown('<div class="section-title">1. Monthly Report</div>', unsafe_allow_html=True)

with st.container(border=True):
    input1, input2, input3, input4 = st.columns(4)

    with input1:
        scheduled_hours = st.number_input(
            "Scheduled Hours",
            min_value=0.0,
            value=128.0,
            step=0.01,
        )

    with input2:
        online_hours = st.number_input(
            "Online Hours",
            min_value=0.0,
            value=117.86,
            step=0.01,
        )

    with input3:
        wait_minutes = st.number_input(
            "Minutes Waiting",
            min_value=0.0,
            value=6311.0,
            step=1.0,
        )

    with input4:
        session_minutes = st.number_input(
            "Minutes In Session",
            min_value=0.0,
            value=842.0,
            step=1.0,
        )

# ============================================================
# CALCULATIONS
# ============================================================
total_minutes = wait_minutes + session_minutes

if total_minutes > 0:
    wait_percentage = (wait_minutes / total_minutes) * 100
else:
    wait_percentage = 0.0

wait_rate = WAIT_RATE_HIGH if wait_percentage > WAIT_THRESHOLD else WAIT_RATE_LOW

session_pay = (session_minutes / 60.0) * SESSION_RATE
wait_pay = (wait_minutes / 60.0) * wait_rate
total_pay = session_pay + wait_pay

# ============================================================
# 2. SALARY SUMMARY
# ============================================================
st.markdown('<div class="section-title">2. Salary Summary</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Wait-Time", f"{wait_percentage:.2f}%")

with k2:
    st.metric("Session Pay", f"₹{session_pay:,.2f}")

with k3:
    st.metric("Wait Pay", f"₹{wait_pay:,.2f}")

with k4:
    st.metric("Estimated Total", f"₹{total_pay:,.2f}")

if wait_percentage > WAIT_THRESHOLD:
    st.warning(
        f"⚠️ Wait time is **{wait_percentage:.2f}%**, above the **{WAIT_THRESHOLD:.0f}%** threshold. "
        f"Current wait rate: **₹{WAIT_RATE_HIGH:,.0f}/hour**."
    )
else:
    st.success(
        f"✅ Wait time is **{wait_percentage:.2f}%**, at or below the **{WAIT_THRESHOLD:.0f}%** threshold. "
        f"Current wait rate: **₹{WAIT_RATE_LOW:,.0f}/hour**."
    )

# ============================================================
# 3. 85% TARGET
# ============================================================
st.markdown('<div class="section-title">3. 85% Wait-Time Target</div>', unsafe_allow_html=True)

with st.container(border=True):
    if wait_minutes > 0:
        required_total_session_minutes = (
            wait_minutes * (100.0 - WAIT_THRESHOLD) / WAIT_THRESHOLD
        )

        additional_minutes = max(
            0.0,
            required_total_session_minutes - session_minutes
        )

        additional_minutes_ceil = math.ceil(additional_minutes)

        target_total_session_minutes = session_minutes + additional_minutes_ceil

        resulting_percentage = (
            wait_minutes
            / (wait_minutes + target_total_session_minutes)
            * 100
        )

        if wait_percentage > WAIT_THRESHOLD:
            t1, t2, t3 = st.columns(3)

            with t1:
                st.metric(
                    "Additional Session Time",
                    f"{additional_minutes_ceil // 60}h {additional_minutes_ceil % 60:02d}m",
                )

            with t2:
                st.metric(
                    "Additional Minutes",
                    f"{additional_minutes_ceil:,}",
                )

            with t3:
                st.metric(
                    "Resulting Wait %",
                    f"{resulting_percentage:.2f}%",
                )

            min_sessions = math.ceil(
                additional_minutes_ceil / MAX_SESSION_LENGTH
            )

            st.info(
                f"To reach **85% or lower**, you need **{additional_minutes_ceil:,} additional session minutes**. "
                f"With a maximum session length of {MAX_SESSION_LENGTH} minutes, the minimum possible number "
                f"of additional full-length sessions is **{min_sessions}**. "
                f"The exact session count cannot be determined from aggregate monthly data."
            )
        else:
            st.success(
                f"Your wait percentage is already **{wait_percentage:.2f}%**. "
                "No additional session time is required to stay at or below 85%."
            )
    else:
        st.info("Enter waiting minutes above to calculate the 85% target.")

# ============================================================
# 4. QUICK CALCULATOR — UTILITY POSITION
# ============================================================
st.markdown('<div class="section-title">4. Quick Calculator</div>', unsafe_allow_html=True)
st.caption("A simple utility for checking calculations while reviewing your report.")

with st.container(border=True):
    calc_left, calc_right = st.columns([4, 1])

    with calc_left:
        calculator_expression = st.text_input(
            "Calculation",
            placeholder="Example: 375*4.5  |  6311/(6311+842)*100  |  842/60",
            key="basic_calculator",
            label_visibility="collapsed",
        )

    with calc_right:
        calculate = st.button(
            "🧮 Calculate",
            use_container_width=True,
            type="primary",
        )

    if calculate:
        expression = calculator_expression.strip()
        allowed_chars = set("0123456789+-*/().% ")

        if not expression:
            st.warning("Enter a calculation first.")
        elif any(char not in allowed_chars for char in expression):
            st.error(
                "Use only numbers, +, -, *, /, %, decimal points, parentheses, and spaces."
            )
        else:
            try:
                result = eval(
                    expression,
                    {"__builtins__": {}},
                    {}
                )

                if isinstance(result, (int, float)) and math.isfinite(float(result)):
                    st.success(f"**Result: {result:,.6g}**")
                else:
                    st.error("Please enter a valid calculation.")

            except ZeroDivisionError:
                st.error("Cannot divide by zero.")
            except Exception:
                st.error("I couldn't calculate that. Check the expression.")

# ============================================================
# 5. PAY COMPARISON
# ============================================================
st.markdown('<div class="section-title">5. Wait-Pay Comparison</div>', unsafe_allow_html=True)

comparison1, comparison2, comparison3 = st.columns(3)

wait_pay_at_high = (wait_minutes / 60.0) * WAIT_RATE_HIGH
wait_pay_at_low = (wait_minutes / 60.0) * WAIT_RATE_LOW
difference = wait_pay_at_low - wait_pay_at_high

with comparison1:
    st.metric(
        "If Wait % > 85%",
        f"₹{wait_pay_at_high:,.2f}"
    )

with comparison2:
    st.metric(
        "If Wait % ≤ 85%",
        f"₹{wait_pay_at_low:,.2f}"
    )

with comparison3:
    st.metric(
        "Rate Difference",
        f"₹{difference:,.2f}"
    )

# ============================================================
# 6. REPORT DETAILS
# ============================================================
st.markdown('<div class="section-title">6. Report Details</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)

with d1:
    st.metric("Scheduled Hours", f"{scheduled_hours:,.2f}")

with d2:
    st.metric("Online Hours", f"{online_hours:,.2f}")

with d3:
    st.metric("Total Tracked Minutes", f"{total_minutes:,.0f}")

# ============================================================
# FORMULA REFERENCE
# ============================================================
with st.expander("📘 Formula Reference"):
    st.markdown("**Wait-time percentage**")
    st.latex(
        r"\frac{\text{Wait Minutes}}{\text{Wait Minutes}+\text{Session Minutes}}\times100"
    )

    st.markdown("**Session pay**")
    st.latex(r"\frac{\text{Session Minutes}}{60}\times375")

    st.markdown("**Wait pay**")
    st.latex(r"\frac{\text{Wait Minutes}}{60}\times\text{Applicable Wait Rate}")

    st.markdown("**Additional session minutes to reach 85%**")
    st.latex(
        r"\max\left(0,\ "
        r"\frac{\text{Wait Minutes}\times(100-85)}{85}"
        r"-\text{Current Session Minutes}\right)"
    )

    st.caption(
        "The 85% calculation uses aggregate monthly minutes and does not assume "
        "an average session length."
    )
