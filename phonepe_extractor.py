import json
import pandas as pd
import os

# ✅ Fixed path - using raw string to avoid Windows backslash error
PULSE_PATH = r"C:\Users\hp\Downloads\pulse-master\pulse-master\data"

print("Starting PhonePe data extraction...")
print(f"Reading from: {PULSE_PATH}")
print("-" * 50)

# ─────────────────────────────────────────────────
# 1. AGGREGATED TRANSACTIONS
# ─────────────────────────────────────────────────
def extract_aggregated_transactions(base_path):
    path = os.path.join(base_path, "aggregated", "transaction", "country", "india", "state")
    rows = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("data", {}).get("transactionData", []):
                    inst = item["paymentInstruments"][0]
                    rows.append({
                        "State":              state,
                        "Year":               int(year),
                        "Quarter":            quarter,
                        "Transaction_type":   item["name"],
                        "Transaction_count":  inst["count"],
                        "Transaction_amount": inst["amount"]
                    })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 2. AGGREGATED USERS
# ─────────────────────────────────────────────────
def extract_aggregated_users(base_path):
    path = os.path.join(base_path, "aggregated", "user", "country", "india", "state")
    rows = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                agg = data.get("data", {}).get("aggregated", {})
                rows.append({
                    "State":            state,
                    "Year":             int(year),
                    "Quarter":          quarter,
                    "Registered_users": agg.get("registeredUsers", 0),
                    "App_opens":        agg.get("appOpens", 0)
                })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 3. AGGREGATED INSURANCE
# ─────────────────────────────────────────────────
def extract_aggregated_insurance(base_path):
    path = os.path.join(base_path, "aggregated", "insurance", "country", "india", "state")
    rows = []
    if not os.path.exists(path):
        print("  [SKIP] Insurance aggregated folder not found")
        return pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("data", {}).get("transactionData", []):
                    inst = item["paymentInstruments"][0]
                    rows.append({
                        "State":              state,
                        "Year":               int(year),
                        "Quarter":            quarter,
                        "Insurance_type":     item["name"],
                        "Insurance_count":    inst["count"],
                        "Insurance_amount":   inst["amount"]
                    })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 4. MAP TRANSACTIONS (District level)
# ─────────────────────────────────────────────────
def extract_map_transactions(base_path):
    path = os.path.join(base_path, "map", "transaction", "hover", "country", "india", "state")
    rows = []
    if not os.path.exists(path):
        print("  [SKIP] Map transaction folder not found")
        return pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("data", {}).get("hoverDataList", []):
                    # metric can be a dict OR a list depending on repo version
                    # handle both safely
                    m = item.get("metric", {})
                    if isinstance(m, list):
                        # list format: [{"type": "...", "count": x, "amount": y}]
                        count  = m[0].get("count", 0)  if m else 0
                        amount = m[0].get("amount", 0) if m else 0
                    else:
                        # dict format: {"count": x, "amount": y}
                        count  = m.get("count", 0)
                        amount = m.get("amount", 0)
                    rows.append({
                        "State":              state,
                        "Year":               int(year),
                        "Quarter":            quarter,
                        "District":           item.get("name", ""),
                        "Transaction_count":  count,
                        "Transaction_amount": amount
                    })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 5. MAP USERS (District level)
# ─────────────────────────────────────────────────
def extract_map_users(base_path):
    path = os.path.join(base_path, "map", "user", "hover", "country", "india", "state")
    rows = []
    if not os.path.exists(path):
        print("  [SKIP] Map user folder not found")
        return pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                hover = data.get("data", {}).get("hoverData", {})
                for district, info in hover.items():
                    rows.append({
                        "State":            state,
                        "Year":             int(year),
                        "Quarter":          quarter,
                        "District":         district,
                        "Registered_users": info.get("registeredUsers", 0),
                        "App_opens":        info.get("appOpens", 0)
                    })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 6. MAP INSURANCE (District level)
# ─────────────────────────────────────────────────
def extract_map_insurance(base_path):
    path = os.path.join(base_path, "map", "insurance", "hover", "country", "india", "state")
    rows = []
    if not os.path.exists(path):
        print("  [SKIP] Map insurance folder not found")
        return pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("data", {}).get("hoverDataList", []):
                    m = item.get("metric", {})
                    if isinstance(m, list):
                        count  = m[0].get("count", 0)  if m else 0
                        amount = m[0].get("amount", 0) if m else 0
                    else:
                        count  = m.get("count", 0)
                        amount = m.get("amount", 0)
                    rows.append({
                        "State":              state,
                        "Year":               int(year),
                        "Quarter":            quarter,
                        "District":           item.get("name", ""),
                        "Insurance_count":    count,
                        "Insurance_amount":   amount
                    })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────
# 7. TOP TRANSACTIONS (District + Pincode)
# ─────────────────────────────────────────────────
def extract_top_transactions(base_path):
    path = os.path.join(base_path, "top", "transaction", "country", "india", "state")
    d_rows, p_rows = [], []
    if not os.path.exists(path):
        print("  [SKIP] Top transaction folder not found")
        return pd.DataFrame(), pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                base = {"State": state, "Year": int(year), "Quarter": quarter}
                for d in data.get("data", {}).get("districts", []):
                    m = d["metric"]
                    if isinstance(m, list):
                        count, amount = m[0].get("count", 0), m[0].get("amount", 0)
                    else:
                        count, amount = m.get("count", 0), m.get("amount", 0)
                    d_rows.append({**base,
                        "District":           d["entityName"],
                        "Transaction_count":  count,
                        "Transaction_amount": amount})
                for p in data.get("data", {}).get("pincodes", []):
                    m = p["metric"]
                    if isinstance(m, list):
                        count, amount = m[0].get("count", 0), m[0].get("amount", 0)
                    else:
                        count, amount = m.get("count", 0), m.get("amount", 0)
                    p_rows.append({**base,
                        "Pincode":            p["entityName"],
                        "Transaction_count":  count,
                        "Transaction_amount": amount})
    return pd.DataFrame(d_rows), pd.DataFrame(p_rows)

# ─────────────────────────────────────────────────
# 8. TOP USERS (District + Pincode)
# ─────────────────────────────────────────────────
def extract_top_users(base_path):
    path = os.path.join(base_path, "top", "user", "country", "india", "state")
    d_rows, p_rows = [], []
    if not os.path.exists(path):
        print("  [SKIP] Top user folder not found")
        return pd.DataFrame(), pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                base = {"State": state, "Year": int(year), "Quarter": quarter}
                for d in data.get("data", {}).get("districts", []):
                    d_rows.append({**base,
                        "District":         d["name"],
                        "Registered_users": d["registeredUsers"]})
                for p in data.get("data", {}).get("pincodes", []):
                    p_rows.append({**base,
                        "Pincode":          p["name"],
                        "Registered_users": p["registeredUsers"]})
    return pd.DataFrame(d_rows), pd.DataFrame(p_rows)

# ─────────────────────────────────────────────────
# 9. TOP INSURANCE (District + Pincode)
# ─────────────────────────────────────────────────
def extract_top_insurance(base_path):
    path = os.path.join(base_path, "top", "insurance", "country", "india", "state")
    d_rows, p_rows = [], []
    if not os.path.exists(path):
        print("  [SKIP] Top insurance folder not found")
        return pd.DataFrame(), pd.DataFrame()
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in sorted(os.listdir(year_path)):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(year_path, file), encoding="utf-8") as f:
                    data = json.load(f)
                base = {"State": state, "Year": int(year), "Quarter": quarter}
                for d in data.get("data", {}).get("districts", []):
                    m = d["metric"]
                    if isinstance(m, list):
                        count, amount = m[0].get("count", 0), m[0].get("amount", 0)
                    else:
                        count, amount = m.get("count", 0), m.get("amount", 0)
                    d_rows.append({**base,
                        "District":         d["entityName"],
                        "Insurance_count":  count,
                        "Insurance_amount": amount})
                for p in data.get("data", {}).get("pincodes", []):
                    m = p["metric"]
                    if isinstance(m, list):
                        count, amount = m[0].get("count", 0), m[0].get("amount", 0)
                    else:
                        count, amount = m.get("count", 0), m.get("amount", 0)
                    p_rows.append({**base,
                        "Pincode":          p["entityName"],
                        "Insurance_count":  count,
                        "Insurance_amount": amount})
    return pd.DataFrame(d_rows), pd.DataFrame(p_rows)


# ═══════════════════════════════════════════════════
# RUN ALL EXTRACTIONS
# ═══════════════════════════════════════════════════
print("\n[1/9] Aggregated Transactions...")
df_agg_txn = extract_aggregated_transactions(PULSE_PATH)
print(f"      Done → {df_agg_txn.shape[0]} rows")

print("[2/9] Aggregated Users...")
df_agg_user = extract_aggregated_users(PULSE_PATH)
print(f"      Done → {df_agg_user.shape[0]} rows")

print("[3/9] Aggregated Insurance...")
df_agg_insurance = extract_aggregated_insurance(PULSE_PATH)
print(f"      Done → {df_agg_insurance.shape[0]} rows")

print("[4/9] Map Transactions (district level)...")
df_map_txn = extract_map_transactions(PULSE_PATH)
print(f"      Done → {df_map_txn.shape[0]} rows")

print("[5/9] Map Users (district level)...")
df_map_user = extract_map_users(PULSE_PATH)
print(f"      Done → {df_map_user.shape[0]} rows")

print("[6/9] Map Insurance (district level)...")
df_map_insurance = extract_map_insurance(PULSE_PATH)
print(f"      Done → {df_map_insurance.shape[0]} rows")

print("[7/9] Top Transactions (district + pincode)...")
df_top_txn_district, df_top_txn_pincode = extract_top_transactions(PULSE_PATH)
print(f"      Done → districts: {df_top_txn_district.shape[0]} rows | pincodes: {df_top_txn_pincode.shape[0]} rows")

print("[8/9] Top Users (district + pincode)...")
df_top_user_district, df_top_user_pincode = extract_top_users(PULSE_PATH)
print(f"      Done → districts: {df_top_user_district.shape[0]} rows | pincodes: {df_top_user_pincode.shape[0]} rows")

print("[9/9] Top Insurance (district + pincode)...")
df_top_ins_district, df_top_ins_pincode = extract_top_insurance(PULSE_PATH)
print(f"      Done → districts: {df_top_ins_district.shape[0]} rows | pincodes: {df_top_ins_pincode.shape[0]} rows")


# ═══════════════════════════════════════════════════
# EXPORT ALL TO CSV
# ═══════════════════════════════════════════════════
os.makedirs("phonepe_data", exist_ok=True)

exports = {
    "phonepe_data/Agg_Transaction.csv":      df_agg_txn,
    "phonepe_data/Agg_User.csv":             df_agg_user,
    "phonepe_data/Agg_Insurance.csv":        df_agg_insurance,
    "phonepe_data/Map_Transaction.csv":      df_map_txn,
    "phonepe_data/Map_User.csv":             df_map_user,
    "phonepe_data/Map_Insurance.csv":        df_map_insurance,
    "phonepe_data/Top_Transaction_District.csv": df_top_txn_district,
    "phonepe_data/Top_Transaction_Pincode.csv":  df_top_txn_pincode,
    "phonepe_data/Top_User_District.csv":    df_top_user_district,
    "phonepe_data/Top_User_Pincode.csv":     df_top_user_pincode,
    "phonepe_data/Top_Insurance_District.csv": df_top_ins_district,
    "phonepe_data/Top_Insurance_Pincode.csv":  df_top_ins_pincode,
}

print("\n" + "=" * 50)
print("SAVING CSV FILES")
print("=" * 50)
for filepath, df in exports.items():
    if df is not None and not df.empty:
        df.to_csv(filepath, index=False)
        print(f"  Saved: {filepath}  ({len(df):,} rows)")
    else:
        print(f"  Skipped (empty): {filepath}")

print("\n" + "=" * 50)
print("ALL DONE! Files saved in: phonepe_data/ folder")
print("Upload those CSVs to Google Colab to use in your notebooks.")
print("=" * 50)