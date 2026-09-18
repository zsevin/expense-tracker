import json
import os
import tempfile
from datetime import date

# Vercel serverless functions have a read-only filesystem except /tmp,
# and /tmp is not shared or persisted across invocations. Until we add
# a real database (step 5), fall back to /tmp there so the demo doesn't
# crash on write — data just won't persist between requests in prod.
if os.environ.get("VERCEL"):
    DATA_FILE = os.path.join(tempfile.gettempdir(), "expenses.json")
else:
    DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)


def add_expense(amount, category, note=""):
    expenses = load_expenses()
    entry = {
        "date": date.today().isoformat(),
        "amount": amount,
        "category": category,
        "note": note,
    }
    expenses.append(entry)
    save_expenses(expenses)
    return entry


def compute_summary(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals
