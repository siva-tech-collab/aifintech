import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

data = pd.read_csv("../data/synthetic_credit_data.csv")

X = data.drop("loan_default", axis=1)
y = data["loan_default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(
    n_estimators=400,
    class_weight="balanced",
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "model.pkl")
print("AI MODEL TRAINED")
