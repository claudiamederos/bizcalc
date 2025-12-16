from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/breakeven", methods=["GET", "POST"])
def break_even():
    result = None
    if request.method == "POST":
        fixed = float(request.form["fixed_costs"])
        price = float(request.form["price"])
        variable = float(request.form["variable_cost"])

        if price > variable:
            result = fixed / (price - variable)

            conn = get_db_connection()
            conn.execute(
                "INSERT INTO calculations (calculator_type, input_data, result) VALUES (?, ?, ?)",
                ("breakeven", json.dumps(request.form), result)
            )
            conn.commit()
            conn.close()

    return render_template("breakeven.html", result=result)

@app.route("/costanalysis", methods=["GET", "POST"])
def cost_benefit():
    result = None

    if request.method == "POST":
        costs = float(request.form["costs"])
        benefits = float(request.form["benefits"])
        result = benefits - costs

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO calculations (calculator_type, input_data, result) VALUES (?, ?, ?)",
            ("costanalysis", json.dumps(dict(request.form)), result)
        )
        conn.commit()
        conn.close()

    return render_template("costanalysis.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

