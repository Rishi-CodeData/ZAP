import pandas as pd

data = [
    {"cust_id": "C-301", "cust_name": "John Doe", "risk_score": 0.78,
     "report_dt": "2026-06-01", "date_of_birth": "1985-03-12", "address": "123 Main St"},
    {"cust_id": "C-302", "cust_name": "Jane Smith", "risk_score": 0.72,
     "report_dt": "2026-06-02", "date_of_birth": "1990-07-25", "address": "456 Oak Ave"},
    {"cust_id": "C-303", "cust_name": "David Kim", "risk_score": 0.61,
     "report_dt": "2026-06-03", "date_of_birth": "1987-09-14", "address": "12 Cedar Lane"},
    {"cust_id": "C-304", "cust_name": "Fatima Khan", "risk_score": 0.88,
     "report_dt": "2026-06-04", "date_of_birth": "1992-01-30", "address": "77 Rose Street"},
    {"cust_id": "C-305", "cust_name": "Arjun P.", "risk_score": 0.55,
     "report_dt": "2026-06-05", "date_of_birth": "1988-11-09", "address": "789 Pine Rd"},
    {"cust_id": "C-306", "cust_name": "Laura Chen", "risk_score": 0.69,
     "report_dt": "2026-06-06", "date_of_birth": "1995-05-22", "address": "9 Birch Avenue"}
]

df = pd.DataFrame(data)
df.to_parquet("data/bureau3.parquet", engine="pyarrow", index=False)
