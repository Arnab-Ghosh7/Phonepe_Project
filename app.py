from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import io
import os

app = Flask(__name__)

# ── Encoders — must match training data exactly ──────────────
STATES = sorted([
    "andhra-pradesh", "assam", "bihar", "chhattisgarh", "delhi",
    "goa", "gujarat", "haryana", "himachal-pradesh", "jharkhand",
    "karnataka", "kerala", "madhya-pradesh", "maharashtra", "manipur",
    "meghalaya", "nagaland", "odisha", "punjab", "rajasthan",
    "tamil-nadu", "telangana", "tripura", "uttar-pradesh", "west-bengal"
])

CATEGORIES = sorted([
    "Financial Services", "Merchant", "Others",
    "Peer-to-Peer", "Recharge & Bill Payments"
])

le_state = LabelEncoder()
le_state.fit(STATES)

le_cat = LabelEncoder()
le_cat.fit(CATEGORIES)

@app.route("/")
def index():
    return render_template("index.html", states=STATES, categories=CATEGORIES)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ── Load models from uploaded files ──────────────────
        rf_file  = request.files.get("rf_model")
        gbc_file = request.files.get("gbc_model")

        # Fall back to local files if already placed in app folder
        if rf_file and rf_file.filename:
            rf_model = joblib.load(io.BytesIO(rf_file.read()))
        elif os.path.exists("phonpe_rf_regressor.pkl"):
            rf_model = joblib.load("phonpe_rf_regressor.pkl")
        else:
            return jsonify({"success": False, "error": "RF model not found. Upload phonpe_rf_regressor.pkl"}), 400

        if gbc_file and gbc_file.filename:
            gbc_model = joblib.load(io.BytesIO(gbc_file.read()))
        elif os.path.exists("phonpe_gbc_classifier.pkl"):
            gbc_model = joblib.load("phonpe_gbc_classifier.pkl")
        else:
            return jsonify({"success": False, "error": "GBC model not found. Upload phonpe_gbc_classifier.pkl"}), 400

        # ── Parse inputs ──────────────────────────────────────
        state     = request.form["state"]
        year      = int(request.form["year"])
        quarter   = int(request.form["quarter"])
        category  = request.form["category"]
        txn_count = float(request.form["txn_count"])
        reg_users = float(request.form["reg_users"])

        # ── Feature engineering (same as training) ────────────
        state_enc    = int(le_state.transform([state])[0])
        category_enc = int(le_cat.transform([category])[0])
        time_idx     = (year - 2019) * 4 + quarter
        log_txn      = np.log1p(txn_count)
        log_users    = np.log1p(reg_users)
        cat_time     = category_enc * time_idx

        features = pd.DataFrame([{
            "time_idx":      time_idx,
            "quarter":       quarter,
            "log_txn_count": log_txn,
            "log_reg_users": log_users,
            "state_enc":     state_enc,
            "category_enc":  category_enc,
            "cat_time":      cat_time
        }])

        # ── Predictions ───────────────────────────────────────
        log_pred    = rf_model.predict(features)[0]
        amount_pred = float(np.expm1(log_pred))

        growth_pred = int(gbc_model.predict(features)[0])
        growth_prob = float(gbc_model.predict_proba(features)[0][1])

        return jsonify({
            "success":     True,
            "amount":      round(amount_pred, 2),
            "amount_cr":   round(amount_pred / 1e7, 2),
            "high_growth": growth_pred,
            "growth_prob": round(growth_prob * 100, 1),
            "state":       state,
            "category":    category,
            "year":        year,
            "quarter":     quarter
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
