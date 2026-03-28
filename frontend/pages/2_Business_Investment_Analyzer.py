import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

st.title("💼 Business Investment & Opportunity Analyzer")
st.markdown("Analyze profitability and success potential before starting your business.")

# -----------------------------
# INPUT SECTION
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    city = st.selectbox(
        "Select City",
        ["Tiruppur", "Coimbatore"]
    )

with col2:
    sector = st.text_input(
        "Enter Business Type",
        placeholder="Example: tea shop, textile unit, mobile repair..."
    )

with col3:
    investment = st.number_input(
        "Investment (Lakhs)",
        min_value=1,
        max_value=500,
        value=10
    )

# -----------------------------
# ANALYSIS BUTTON
# -----------------------------

if st.button("Analyze Investment"):

    if sector == "":
        st.warning("Please enter a business type.")
        st.stop()

    with st.spinner("Analyzing Business Opportunity..."):

        response = requests.post(
            f"{BACKEND_URL}/analyze-business",
            json={
                "city": city,
                "sector": sector,
                "investment": investment
            }
        )

    if response.status_code != 200:
        st.error("Backend error.")
        st.stop()

    data = response.json()

    # Save context for chatbot
    st.session_state["analysis_data"] = data

    # -----------------------------
    # RESULT DISPLAY
    # -----------------------------

    st.markdown("## 📊 Business Analysis Results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Predicted Monthly Profit (Lakhs)",
        data["predicted_monthly_profit_lakhs"]
    )

    c2.metric(
        "Success Probability (%)",
        data["success_probability_percent"]
    )

    c3.metric(
        "Break-even Period",
        f"{data['break_even_months']} months"
    )

    risk = data["risk_level"]

    if risk == "High":
        risk_display = f"🔴 {risk}"
    elif risk == "Moderate":
        risk_display = f"🟠 {risk}"
    else:
        risk_display = f"🟢 {risk}"

    c4.metric("Risk Level", risk_display)

    c5, c6 = st.columns(2)

    c5.metric(
        "Competition Index (%)",
        data["competition_index"]
    )

    c6.metric(
        "Sector Growth (%)",
        data["growth_rate_percent"]
    )

    # -----------------------------
    # AI REPORT
    # -----------------------------

    st.markdown("## 🧠 AI Business Consultant Report")

    prompt = f"""
BUSINESS ANALYSIS DATA

City: {data['city']}
Business Type: {sector}
Investment: {data['investment_lakhs']} lakhs

Predicted Monthly Profit: {data['predicted_monthly_profit_lakhs']} lakhs
Success Probability: {data['success_probability_percent']} 
Break-even Period: {data['break_even_months']} months
Competition Level: {data['competition_index']} 
Sector Growth Rate: {data['growth_rate_percent']} 
Risk Level: {data['risk_level']}

Write a short professional business analysis.

Explain:

1. Market opportunity in {data['city']}
2. Whether the investment is attractive
3. Why the risk level is {data['risk_level']}
4. One practical recommendation for entrepreneurs

Important:
Use ONLY the numbers provided above.
Do not invent statistics.
"""

    explain = requests.get(
        f"{BACKEND_URL}/ask",
        params={"q": prompt}
    )

    st.info(explain.json()["answer"])


# --------------------------------
# CHATBOT
# --------------------------------

st.markdown("---")
st.markdown("## 💬 Business AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask anything about your business idea")

if st.button("Ask AI"):

    context = ""

    if "analysis_data" in st.session_state:

        d = st.session_state["analysis_data"]

        context = f"""
Current Business Analysis Context:

City: {d['city']}
Sector: {d['sector']}
Investment: {d['investment_lakhs']} lakhs
Predicted Profit: {d['predicted_monthly_profit_lakhs']} lakhs
Success Probability: {d['success_probability_percent']} %
Break-even: {d['break_even_months']} months
Competition: {d['competition_index']} %
Growth Rate: {d['growth_rate_percent']} %
Risk Level: {d['risk_level']}
"""

    full_query = f"""
{context}

User Question:
{user_input}

Answer based on the analysis data above.
"""

    response = requests.get(
        f"{BACKEND_URL}/ask",
        params={"q": full_query}
    )

    answer = response.json()["answer"]

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("ai", answer))

for role, msg in st.session_state.messages:

    if role == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")