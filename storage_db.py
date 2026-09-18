import os
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")

_initialized = False


def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


def init_db():
    global _initialized
    if _initialized:
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    expense_date DATE NOT NULL,
                    amount NUMERIC NOT NULL,
                    category TEXT NOT NULL,
                    note TEXT DEFAULT ''
                )
                """
            )
        conn.commit()
    _initialized = True


def load_expenses():
    init_db()
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT expense_date, amount, category, note FROM expenses ORDER BY id"
            )
            rows = cur.fetchall()
    return [
        {
            "date": row["expense_date"].isoformat(),
            "amount": float(row["amount"]),
            "category": row["category"],
            "note": row["note"] or "",
        }
        for row in rows
    ]


def add_expense(amount, category, note=""):
    init_db()
    entry_date = date.today()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO expenses (expense_date, amount, category, note) VALUES (%s, %s, %s, %s)",
                (entry_date, amount, category, note),
            )
        conn.commit()
    return {
        "date": entry_date.isoformat(),
        "amount": amount,
        "category": category,
        "note": note,
    }


def compute_summary(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals
