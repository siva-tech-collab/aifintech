import shap
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load data and model
data = pd.read_csv("../data/synthetic_credit_data.csv")
model = joblib.load("model.pkl")

# Use exact training columns
X = data[model.feature_names_in_]  # ensures feature order matches model
y = data["loan_default"]

# Create SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Global feature importance
shap.summary_plot(shap_values[1], X, plot_type="bar", show=True)
shap.summary_plot(shap_values[1], X, plot_type="dot", show=True)
