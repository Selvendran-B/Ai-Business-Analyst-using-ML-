import streamlit as st

st.set_page_config(page_title="AI Business Analyst", layout="wide")

st.title("📊 Data-Driven Business Decision Support System")

st.markdown("""
This platform helps entrepreneurs and MSME owners understand:
- current MSME ecosystem
- dominant business activities
- market saturation and trends
- data-backed insights using AI
""")

st.markdown("## Choose an option")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 MSME Current Analysing")
    st.write("Analyze current MSME status of a district")
    if st.button("Explore MSME Analysis"):
        st.switch_page("pages/1_MSME_Current_Analysis.py")

with col2:
    st.subheader("📈 Business Profit Analysis")
    st.write("Coming soon")

with col3:
    st.subheader("🤖 AI Business Guidance")
    st.write("Coming soon")

st.markdown("---")
st.caption("AI Business Analyst | Real MSME Data + ML + LLM")
