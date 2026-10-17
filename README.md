# Customer Churn Prediction Web Application

**Student:** Hamza Faisal | **SAP ID:** 70175787 | **Section:** 5-D  
**Course:** Artificial Intelligence — Assignment 2

## Project files
- `app.py` — Flask backend, input validation and prediction route
- `model.joblib` — trained Assignment 1 Logistic Regression pipeline (includes preprocessing)
- `templates/index.html` — customer form and prediction result
- `static/style.css` — responsive styling
- `requirements.txt` — Python dependencies

## Model continuity
The Assignment 1 notebook compared Logistic Regression and Random Forest. Logistic Regression was selected as the final model because its reported test metrics were higher (accuracy 0.8055, precision 0.6572, recall 0.5588, F1-score 0.6040). This project retrains that same model type using the same feature preprocessing approach: numeric median imputation and standard scaling; categorical most-frequent imputation and one-hot encoding. The entire preprocessing + model pipeline is saved in `model.joblib`.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open `http://127.0.0.1:5000`.

## PythonAnywhere deployment
See `PYTHONANYWHERE_DEPLOYMENT.md`. The final public URL must be created from your own PythonAnywhere account; it cannot be activated from this package alone.
