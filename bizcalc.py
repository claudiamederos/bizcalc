from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calculator_type TEXT,
            input_data TEXT,
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/breakeven", methods=["GET", "POST"])
def breakeven():
    result = None
    error = None
    inputs = {}

    if request.method == "POST":
        inputs = request.form
        try:
            fixed = float(request.form["fixed_costs"])
            price = float(request.form["price"])
            variable = float(request.form["variable_cost"])
            if price <= variable:
                error = "Price must be greater than variable cost."
            else:
                result = fixed / (price - variable)
                conn = get_db_connection()
                conn.execute(
                    "INSERT INTO calculations (calculator_type, input_data, result) VALUES (?, ?, ?)",
                    ("breakeven", json.dumps(dict(request.form)), str(result))
                )
                conn.commit()
                conn.close()
        except Exception as e:
            error = f"Invalid input: {e}"
    return render_template("breakeven.html", result=result, error=error, inputs=inputs)

@app.route("/costanalysis", methods=["GET", "POST"])
def costanalysis():
    result = None
    error = None
    inputs = {}
    if request.method == "POST":
        inputs = request.form
        try:
            costs = float(request.form["costs"])
            benefits = float(request.form["benefits"])
            net_benefit = benefits - costs
            result = f"{net_benefit:.2f}"
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO calculations (calculator_type, input_data, result) VALUES (?, ?, ?)",
                ("costanalysis", json.dumps(dict(request.form)), result)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            error = f"Invalid input: {e}"
    return render_template("costanalysis.html", result=result, error=error, inputs=inputs)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/history")
def history():
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM calculations ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("history.html", logs=logs)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)