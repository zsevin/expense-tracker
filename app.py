from flask import Flask, jsonify, request, send_from_directory

from storage import load_expenses, add_expense, compute_summary

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    return jsonify(load_expenses())


@app.route("/api/expenses", methods=["POST"])
def create_expense():
    data = request.get_json(force=True)
    amount = float(data["amount"])
    category = data["category"]
    note = data.get("note", "")
    entry = add_expense(amount, category, note)
    return jsonify(entry), 201


@app.route("/api/summary", methods=["GET"])
def get_summary():
    expenses = load_expenses()
    totals = compute_summary(expenses)
    return jsonify(totals)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
