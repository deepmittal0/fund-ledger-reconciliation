from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
a = pd.read_csv(ROOT/"data"/"ledger_a.csv")
b = pd.read_csv(ROOT/"data"/"ledger_b.csv")
m = a.merge(b, on="transaction_id", how="outer", suffixes=("_a","_b"), indicator=True)
def classify(r):
    if r["_merge"] == "left_only": return "MISSING_IN_B"
    if r["_merge"] == "right_only": return "MISSING_IN_A"
    if round(r["amount_a"],2) != round(r["amount_b"],2): return "AMOUNT_MISMATCH"
    return "MATCH"
m["status"] = m.apply(classify, axis=1)
m["age_days"] = (pd.Timestamp("today") - pd.to_datetime(m["date_a"].fillna(m["date_b"]))).dt.days
out = ROOT/"reports"
out.mkdir(exist_ok=True)
m.to_csv(out/"reconciliation.csv", index=False)
summary = {"records":len(m),"matched":int((m.status=="MATCH").sum()),
           "exceptions":int((m.status!="MATCH").sum())}
(out/"summary.json").write_text(json.dumps(summary, indent=2))
print(summary)
