import json
import os
from datetime import date

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
