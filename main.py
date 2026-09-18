import argparse
import json
import os
import sys
from datetime import date

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)


def add_expense(amount, category, note):
    expenses = load_expenses()
    expenses.append({
        "date": date.today().isoformat(),
        "amount": amount,
        "category": category,
        "note": note,
    })
    save_expenses(expenses)
    print(f"Hozzáadva: {amount} Ft ({category})")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("Még nincs egy rögzített kiadás sem.")
        return
    for e in expenses:
        note = f" - {e['note']}" if e["note"] else ""
        print(f"{e['date']}  {e['amount']:>8.2f} Ft  [{e['category']}]{note}")


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("Még nincs egy rögzített kiadás sem.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    print("Összesítés kategóriánként:")
    for category, total in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"  {category:<15} {total:>10.2f} Ft")
    print(f"\nÖsszesen: {sum(totals.values()):.2f} Ft")


def main():
    parser = argparse.ArgumentParser(description="Egyszerű személyes kiadáskövető")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Új kiadás rögzítése")
    add_parser.add_argument("amount", type=float, help="Összeg (Ft)")
    add_parser.add_argument("category", help="Kategória, pl. étel, közlekedés")
    add_parser.add_argument("--note", default="", help="Megjegyzés (opcionális)")

    subparsers.add_parser("list", help="Összes kiadás listázása")
    subparsers.add_parser("summary", help="Összesítés kategóriánként")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.note)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary()


if __name__ == "__main__":
    main()
