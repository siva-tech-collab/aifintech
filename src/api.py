from fastapi import FastAPI
import joblib
import numpy as np
import os
from utils import probability_to_credit_score, get_risk_category, loan_policy_decision

app = FastAPI(title="AltCred AI Credit Scoring API")

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model Loaded Successfully")
except:
    print("⚠️ Model not found. Using AI Simulation Mode")
    model = None

@app.get("/")
def home():
    return {"status": "AltCred AI API Running"}

@app.post("/score")
def get_score(data: dict):

    # Required fields
    required = ["age","income","upi_txn_count","bill_payment_score","mobile_recharge_score","ecommerce_spend"]
    for r in required:
        if r not in data:
            return {"error": f"Missing {r}"}

    # Feature vector
    X = np.array([[ 
        data["age"],
        data["income"],
        data["upi_txn_count"],
        data["bill_payment_score"],
        data["mobile_recharge_score"],
        data["ecommerce_spend"]
    ]])

    # If model exists → real ML prediction
    if model:
        prob = model.predict_proba(X)[0][1]
    else:
        # AI Simulation Mode (Realistic fintech logic)
        prob = (
            0.4 
            - data["income"]/300000 
            - data["bill_payment_score"]/500 
            - data["mobile_recharge_score"]/600 
            - data["upi_txn_count"]/5000 
            + data["ecommerce_spend"]/100000
        )
        prob = np.clip(prob, 0.01, 0.95)

    credit_score = probability_to_credit_score(prob)
    risk = get_risk_category(prob)
    decision = loan_policy_decision(credit_score, prob)

    return {
        "credit_score": credit_score,
        "risk_category": risk,
        "loan_decision": decision,
        "probability_of_default": float(prob)
    }
