import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

# ================= CONFIG ==================
st.set_page_config(page_title="AltCred AI Dashboard", layout="wide")
st.title("🏦 AltCred AI - Alternate Credit Scoring Dashboard")

API_URL = "http://127.0.0.1:9000/score"

# ================= MODE SELECTION ==================
mode = st.radio("Select Input Mode", ["Manual", "Automatic Sample User"])

# ================= SAMPLE USERS ==================
sample_users = {
    "User A (Young Professional)": {
        "age": 25, "income": 50000, "upi_txn_count": 120,
        "bill_payment_score": 85, "mobile_recharge_score": 90, "ecommerce_spend": 12000
    },
    "User B (High Income Customer)": {
        "age": 35, "income": 80000, "upi_txn_count": 300,
        "bill_payment_score": 95, "mobile_recharge_score": 80, "ecommerce_spend": 25000
    },
    "User C (Risky Profile)": {
        "age": 20, "income": 15000, "upi_txn_count": 5,
        "bill_payment_score": 20, "mobile_recharge_score": 30, "ecommerce_spend": 50000
    }
}

# ================= INPUT UI ==================
payload = {}

if mode == "Manual":
    st.subheader("🧑 Manual Input Mode")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 60, 30)
        income = st.number_input("Monthly Income (₹)", 10000, 200000, 50000)

    with col2:
        upi = st.slider("UPI Transactions / Month", 0, 500, 100)
        bill = st.slider("Bill Payment Score (0-100)", 0, 100, 80)

    with col3:
        mobile = st.slider("Mobile Recharge Score (0-100)", 0, 100, 70)
        ecom = st.number_input("E-commerce Spend (₹)", 0, 50000, 10000)

    payload = {
        "age": age,
        "income": income,
        "upi_txn_count": upi,
        "bill_payment_score": bill,
        "mobile_recharge_score": mobile,
        "ecommerce_spend": ecom
    }

else:
    st.subheader("🤖 Automatic Sample User Mode")
    selected_user = st.selectbox("Select Sample User", list(sample_users.keys()))
    payload = sample_users[selected_user]

    st.write("### Sample User Data")
    st.table(pd.DataFrame([payload]))

# ================= BUTTON ==================
if st.button("🚀 Get AI Credit Score"):
    try:
        response = requests.post(API_URL, json=payload)
        res = response.json()

        # Check API error
        if "error" in res:
            st.error(f"API Error: {res['error']}")
            st.stop()

        # ================= DASHBOARD ==================
        st.markdown("---")
        st.markdown("## 📊 AI Credit Assessment Result")

        # -------- Credit Score Gauge --------
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res["credit_score"],
            number={"font": {"size": 48}},
            title={"text": "AI Credit Score (300 - 900)", "font": {"size": 22}},
            gauge={
                "axis": {"range": [300, 900]},
                "bar": {"color": "black"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",

                "steps": [
                    {"range": [300, 500], "color": "#ff4d4d"},   # Poor
                    {"range": [500, 650], "color": "#ff944d"},   # Fair
                    {"range": [650, 750], "color": "#ffd11a"},   # Good
                    {"range": [750, 850], "color": "#66cc66"},   # Very Good
                    {"range": [850, 900], "color": "#009933"}    # Excellent
                ],

                "threshold": {
                    "line": {"color": "blue", "width": 6},
                    "thickness": 0.75,
                    "value": res["credit_score"]
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        # -------- Credit Rating Text --------
        score = res["credit_score"]
        if score < 500:
            rating = "Poor"
        elif score < 650:
            rating = "Fair"
        elif score < 750:
            rating = "Good"
        elif score < 850:
            rating = "Very Good"
        else:
            rating = "Excellent"

        st.markdown(f"### 🏷️ Credit Rating: **{rating}**")

        # -------- Risk Category --------
        risk = res["risk_category"]
        risk_color = "green" if "Low" in risk else "orange" if "Medium" in risk else "red"
        st.markdown(f"<h3 style='color:{risk_color}'>Risk Category: {risk}</h3>", unsafe_allow_html=True)

        # -------- Loan Decision --------
        decision = res["loan_decision"]
        decision_color = "green" if "Auto" in decision else "orange"
        st.markdown(f"<h3 style='color:{decision_color}'>Loan Decision: {decision}</h3>", unsafe_allow_html=True)

        # -------- Probability --------
        st.metric("Probability of Default", f"{res['probability_of_default']*100:.2f}%")

        # ================= AI Explainability ==================
        st.markdown("## 🧠 AI Feature Impact Explanation")

        features = list(payload.keys())
        values = list(payload.values())

        total = sum(values) + 1
        importance = [v / total for v in values]

        df_imp = pd.DataFrame({
            "Feature": features,
            "Impact Score": importance
        }).sort_values(by="Impact Score", ascending=False)

        fig2 = go.Figure(go.Bar(
            x=df_imp["Impact Score"],
            y=df_imp["Feature"],
            orientation="h"
        ))
        fig2.update_layout(title="Feature Contribution to Credit Score (AI Simulated)")
        st.plotly_chart(fig2, use_container_width=True)

        # ================= AI TEXT EXPLANATION ==================
        st.markdown("### 📌 AI Explanation")
        explanation = f"""
        • Higher income and consistent UPI usage improved creditworthiness  
        • Strong bill payment and recharge behavior reduced default risk  
        • E-commerce spending compared to income was evaluated  
        • Overall AI detected **{risk} financial behavior**  
        """
        st.info(explanation)

    except Exception as e:
        st.error(f"API request failed: {e}")
