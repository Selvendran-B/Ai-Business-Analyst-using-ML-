import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="MSME Current Analysis", layout="wide")

st.title("📍 MSME Current Analysis")

st.markdown("""
Understand the **current MSME ecosystem** of a district using
**real government MSME data** and **AI-driven insights**.
""")

# ---------------------------
# USER INPUT
# ---------------------------
city = st.selectbox(
    "Select District",
    ["Tiruppur", "Coimbatore"]
)

if st.button("Analyze MSME Status"):

    # ---------------------------
    # API CALLS
    # ---------------------------
    with st.spinner("Fetching MSME data..."):

        count_res = requests.get(f"{BACKEND_URL}/real/msme-count/{city}")
        activities_res = requests.get(f"{BACKEND_URL}/real/top-activities/{city}")
        trend_res = requests.get(f"{BACKEND_URL}/real/registration-trend/{city}")

    # ---------------------------
    # MSME COUNT
    # ---------------------------
    st.markdown("## 📊 MSME Overview")

    if count_res.status_code == 200:
        msme_count = count_res.json()["msme_count"]
        st.metric(label=f"Total MSMEs in {city}", value=msme_count)

    # ---------------------------
    # TOP ACTIVITIES (CHART)
    # ---------------------------
    st.markdown("## 🏭 Major MSME Activities")

    activities = activities_res.json()

    import ast

    def clean_activity_name(name):
        try:
            # Convert string to actual Python object
            parsed = ast.literal_eval(name)

            # If it is a list, extract first element
            if isinstance(parsed, list) and len(parsed) > 0:
                description = parsed[0].get("Description", "")
            else:
                description = str(name)

        except:
            description = str(name)

        return description


    df_act = pd.DataFrame(
        [(clean_activity_name(k), v) for k, v in activities.items()],
        columns=["Activity", "Count"]
    )

    df_act = df_act[df_act["Activity"] != ""]  # remove empty
    df_act = df_act.sort_values("Count", ascending=False).head(8)

    fig = px.bar(
        df_act,
        y="Activity",
        x="Count",
        orientation="h",
        color="Count",
        text="Count",
        title=f"Top MSME Activities in {city}"
    )

    fig.update_layout(
        yaxis_title="MSME Activity Type",
        xaxis_title="Number of MSMEs",
        height=550,
        showlegend=False
    )

    fig.update_traces(textposition="outside")
    fig.update_xaxes(tickmode='array')

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # REGISTRATION TREND
    # ---------------------------
    st.markdown("## 📈 MSME Registration Trend")

    trend = trend_res.json()
    df_trend = pd.DataFrame(
        trend.items(),
        columns=["Year", "Registrations"]
    ).sort_values("Year")

    fig2 = px.line(
        df_trend,
        x="Year",
        y="Registrations",
        markers=True,
        title=f"MSME Registration Trend in {city}"
    )

    fig2.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "y": 0.95
        },
        xaxis_title="Year",
        yaxis_title="Number of MSME Registrations",
        margin=dict(l=40, r=40, t=80, b=60),
        height=400
    )

    st.plotly_chart(fig2, use_container_width=True)


    # ---------------------------
    # LLM BUSINESS EXPLANATION
    # ---------------------------
    st.markdown("### 📌 Business Analyst Interpretation")
    st.markdown(
        "Below is an AI-generated business-level explanation based on current MSME data and market patterns."
    )

    summary_prompt = f"""
    You are a senior MSME Business Analyst.

    Analyze the current MSME ecosystem of {city} using the data below.

    DATA:
    - Total MSMEs: {msme_count}
    - Top MSME activities: {list(activities.keys())[:5]}
    - MSME registration trend by year: {trend}

    TASK:
    1. Explain the dominant business sectors in simple language.
    2. Explain what this means for a NEW entrepreneur.
    3. Mention opportunities and risks clearly.
    4. Give 2–3 practical recommendations.

    Write in a clear, structured, professional tone.
    Avoid technical jargon.
    """


    with st.spinner("Generating business insights..."):
        explain_res = requests.get(
            f"{BACKEND_URL}/ask",
            params={"q": summary_prompt}
        )

    response_data = explain_res.json()

    if isinstance(response_data, dict) and "answer" in response_data:
        st.markdown(response_data["answer"])
    else:
        st.markdown(str(response_data))


st.markdown("---")
st.caption("MSME Current Analysis | Powered by Real MSME Data + AI")
