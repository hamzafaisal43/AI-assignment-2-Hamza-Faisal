from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

CATEGORIES = {
    "gender": ["Female", "Male"],
    "Partner": ["Yes", "No"],
    "Dependents": ["Yes", "No"],
    "PhoneService": ["Yes", "No"],
    "MultipleLines": ["No phone service", "No", "Yes"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "OnlineSecurity": ["No", "Yes", "No internet service"],
    "OnlineBackup": ["No", "Yes", "No internet service"],
    "DeviceProtection": ["No", "Yes", "No internet service"],
    "TechSupport": ["No", "Yes", "No internet service"],
    "StreamingTV": ["No", "Yes", "No internet service"],
    "StreamingMovies": ["No", "Yes", "No internet service"],
    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": ["Yes", "No"],
    "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
}

DEFAULTS = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
    "tenure": 1, "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check", "MonthlyCharges": 70.0, "TotalCharges": 70.0
}

def build_customer(form):
    customer = {}
    for field, options in CATEGORIES.items():
        value = form.get(field, DEFAULTS[field])
        if value not in options:
            raise ValueError("Please select a valid value for " + field + ".")
        customer[field] = value
    customer["SeniorCitizen"] = int(form.get("SeniorCitizen", DEFAULTS["SeniorCitizen"]))
    customer["tenure"] = int(form.get("tenure", DEFAULTS["tenure"]))
    customer["MonthlyCharges"] = float(form.get("MonthlyCharges", DEFAULTS["MonthlyCharges"]))
    customer["TotalCharges"] = float(form.get("TotalCharges", DEFAULTS["TotalCharges"]))
    if customer["SeniorCitizen"] not in (0, 1):
        raise ValueError("Senior citizen must be Yes or No.")
    if not 0 <= customer["tenure"] <= 72:
        raise ValueError("Tenure must be between 0 and 72 months.")
    if customer["MonthlyCharges"] < 0 or customer["TotalCharges"] < 0:
        raise ValueError("Charges cannot be negative.")
    return pd.DataFrame([customer])

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    probability = None
    submitted = {}
    if request.method == "POST":
        submitted = request.form.to_dict()
        try:
            customer = build_customer(request.form)
            result = int(model.predict(customer)[0])
            prediction = "Churn" if result == 1 else "No Churn"
            if hasattr(model, "predict_proba"):
                probability = round(float(model.predict_proba(customer)[0][1]) * 100, 1)
        except (ValueError, TypeError) as exc:
            error = str(exc) or "Please check your input values and try again."
        except Exception:
            error = "The prediction could not be completed. Please check all fields and try again."
    return render_template("index.html", categories=CATEGORIES, defaults=DEFAULTS,
                           prediction=prediction, error=error, probability=probability,
                           submitted=submitted)

@app.route("/health")
def health():
    return {"status": "ok", "model": "Logistic Regression pipeline"}

if __name__ == "__main__":
    app.run(debug=True)
