# Fund Ledger Reconciliation & Exception Tracker

Compares two synthetic ledger extracts by transaction ID and amount, classifies breaks, and reports exception ageing.

## Run
```bash
python -m pip install -r requirements.txt
python src/reconcile.py
```
Outputs `reports/reconciliation.csv` and `reports/summary.json`. This is an educational demo, not a financial control system.
