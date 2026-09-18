import os

if os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL"):
    from storage_db import load_expenses, add_expense, compute_summary
else:
    from storage_json import load_expenses, add_expense, compute_summary

__all__ = ["load_expenses", "add_expense", "compute_summary"]
