# data_generator.py
import pandas as pd
import numpy as np

np.random.seed(42)
n = 10000
data = []

for _ in range(n):
    age = np.random.randint(18, 60)
    income = np.random.randint(8000, 200000)
    upi = np.random.randint(0, 500)
    bill = np.random.uniform(0, 100)
    mobile = np.random.uniform(0, 100)
    ecom = np.random.randint(0, 50000)

    # TRUE AI-like default logic
    risk = 0
    if income < 20000: risk += 3
    if ecom > income: risk += 2
    if bill < 30: risk += 1
    if upi < 10: risk += 1
    if age < 21: risk += 1

    # Convert risk → probability-like default
    prob_default = min(risk / 8, 1)
    loan_default = np.random.rand() < prob_default  # stochastic realism

    data.append([age,income,upi,bill,mobile,ecom,int(loan_default)])

df = pd.DataFrame(data, columns=[
    "age","income","upi_txn_count","bill_payment_score",
    "mobile_recharge_score","ecommerce_spend","loan_default"
])

df.to_csv("../data/synthetic_credit_data.csv", index=False)
print("REALISTIC dataset generated!")
