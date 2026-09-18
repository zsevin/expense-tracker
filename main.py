import argparse
import sys

from storage import load_expenses, add_expense, compute_summary

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


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
    totals = compute_summary(expenses)
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
        print(f"Hozzáadva: {args.amount} Ft ({args.category})")
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary()


if __name__ == "__main__":
    main()
