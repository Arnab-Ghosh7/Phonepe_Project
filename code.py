import json
import pandas as pd
import os

PULSE_PATH = "C:\\Users\\hp\\Downloads\\pulse-master\\pulse-master\\data"

# ─────────────────────────────────────────
# AGGREGATED TRANSACTIONS
# ─────────────────────────────────────────
def extract_aggregated_transactions(base_path):
    path = os.path.join(base_path, "aggregated/transaction/country/india/state")
    rows = []

    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file)) as f:
                    data = json.load(f)
                txn_data = data["data"]["transactionData"]
                for item in txn_data:
                    rows.append({
                        "state": state,
                        "year": int(year),
                        "quarter": quarter,
                        "payment_type": item["name"],
                        "transaction_count": item["paymentInstruments"][0]["count"],
                        "transaction_amount": item["paymentInstruments"][0]["amount"]
                    })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────
# AGGREGATED USERS
# ─────────────────────────────────────────
def extract_aggregated_users(base_path):
    path = os.path.join(base_path, "aggregated/user/country/india/state")
    rows = []

    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file)) as f:
                    data = json.load(f)
                summary = data["data"]["aggregated"]
                rows.append({
                    "state": state,
                    "year": int(year),
                    "quarter": quarter,
                    "registered_users": summary["registeredUsers"],
                    "app_opens": summary["appOpens"]
                })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────
# AGGREGATED INSURANCE
# ─────────────────────────────────────────
def extract_aggregated_insurance(base_path):
    path = os.path.join(base_path, "aggregated/insurance/country/india/state")
    rows = []

    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file)) as f:
                    data = json.load(f)
                txn = data["data"]["transactionData"]
                for item in txn:
                    rows.append({
                        "state": state,
                        "year": int(year),
                        "quarter": quarter,
                        "insurance_type": item["name"],
                        "insurance_count": item["paymentInstruments"][0]["count"],
                        "insurance_amount": item["paymentInstruments"][0]["amount"]
                    })

    return pd.DataFrame(rows)


# Run all three
df_txn      = extract_aggregated_transactions(PULSE_PATH)
df_users    = extract_aggregated_users(PULSE_PATH)
df_insurance = extract_aggregated_insurance(PULSE_PATH)

print(df_txn.shape, df_users.shape, df_insurance.shape)
print(df_txn.head())