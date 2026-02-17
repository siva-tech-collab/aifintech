# utils.py
import numpy as np

# Convert probability → realistic credit score (300–900)
def probability_to_credit_score(prob):
    return int(300 + (1 - prob) * 600)

# Risk category logic
def get_risk_category(prob):
    if prob < 0.25:
        return "Low Risk"
    elif prob < 0.6:
        return "Medium Risk"
    else:
        return "High Risk"

# Soft AI decision policy (NO HARD REJECTION)
def loan_policy_decision(score, prob):
    if score >= 750 and prob < 0.2:
        return "Auto Approved"
    elif score >= 600:
        return "Manual Review Required"
    else:
        return "Conditional Approval (Low Limit / High Interest)"
