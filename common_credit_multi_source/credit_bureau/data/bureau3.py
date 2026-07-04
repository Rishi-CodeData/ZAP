import pandas as pd

data = [
    {"cust_id": "C-301", "cust_name": "John Doe", "risk_score": 0.78, "report_dt": "2026-06-01"},
    {"cust_id": "C-302", "cust_name": "Jane Smith", "risk_score": 0.72, "report_dt": "2026-06-02"},
    {"cust_id": "C-303", "cust_name": "Arjun Patel", "risk_score": 0.55, "report_dt": "2026-06-03"},
    {"cust_id": "C-304", "cust_name": "Maria Lopez", "risk_score": 0.92, "report_dt": "2026-06-04"},
]

df = pd.DataFrame(data)
df.to_parquet("data/bureau3.parquet", engine="pyarrow", index=False)
