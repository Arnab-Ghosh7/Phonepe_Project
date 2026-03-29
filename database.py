import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

engine = create_engine(
    "mysql+mysqlconnector://",
    connect_args={
        "host":     "localhost",
        "user":     "root",
        "password": "",   
        "database": "phonepe_db"
    }
)

# First create the database if it doesn't exist
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_db")
conn.close()
print("Database ready.")

# Now load all CSVs
import os

tables = {
    "agg_transaction":          "Agg_Transaction.csv",
    "agg_user":                 "Agg_User.csv",
    "agg_insurance":            "Agg_Insurance.csv",
    "map_transaction":          "Map_Transaction.csv",
    "map_user":                 "Map_User.csv",
    "map_insurance":            "Map_Insurance.csv",
    "top_transaction_district": "Top_Transaction_District.csv",
    "top_transaction_pincode":  "Top_Transaction_Pincode.csv",
    "top_user_district":        "Top_User_District.csv",
    "top_user_pincode":         "Top_User_Pincode.csv",
    "top_insurance_district":   "Top_Insurance_District.csv",
    "top_insurance_pincode":    "Top_Insurance_Pincode.csv",
}

for table_name, csv_file in tables.items():
    csv_path = os.path.join("phonepe_data", csv_file)
    if not os.path.exists(csv_path):
        print(f"  Skipped (file not found): {csv_file}")
        continue
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"  Loaded → {table_name}  ({len(df):,} rows)")

print("\nAll tables loaded into MySQL successfully.")