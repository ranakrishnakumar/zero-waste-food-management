from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("zero_waste.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_name TEXT NOT NULL,
                food_name TEXT NOT NULL,
                quantity TEXT NOT NULL,
                location TEXT NOT NULL,
                phone TEXT NOT NULL,
                expiry_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Available',
                requested_by TEXT DEFAULT ''
            )
        """)

@app.route("/")
def index():
    with get_db() as conn:
        donations = conn.execute(
            "SELECT * FROM donations ORDER BY id DESC"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM donations").fetchone()[0]
        available = conn.execute(
            "SELECT COUNT(*) FROM donations WHERE status='Available'"
        ).fetchone()[0]
        collected = conn.execute(
            "SELECT COUNT(*) FROM donations WHERE status='Collected'"
        ).fetchone()[0]
    return render_template("index.html", donations=donations,
                           total=total, available=available, collected=collected)

@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        data = (
            request.form.get("donor_name", "").strip(),
            request.form.get("food_name", "").strip(),
            request.form.get("quantity", "").strip(),
            request.form.get("location", "").strip(),
            request.form.get("phone", "").strip(),
            request.form.get("expiry_time", "").strip()
        )
        if not all(data):
            flash("Please complete all fields.")
            return redirect(url_for("donate"))
        with get_db() as conn:
            conn.execute("""
                INSERT INTO donations
                (donor_name, food_name, quantity, location, phone, expiry_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
        flash("Food donation added successfully.")
        return redirect(url_for("index"))
    return render_template("donate.html")

@app.route("/request/<int:donation_id>", methods=["POST"])
def request_food(donation_id):
    ngo_name = request.form.get("ngo_name", "").strip()
    if not ngo_name:
        flash("Enter the NGO / requester name.")
        return redirect(url_for("index"))
    with get_db() as conn:
        item = conn.execute(
            "SELECT status FROM donations WHERE id=?", (donation_id,)
        ).fetchone()
        if item and item["status"] == "Available":
            conn.execute("""
                UPDATE donations SET status='Requested', requested_by=?
                WHERE id=?
            """, (ngo_name, donation_id))
            flash("Food request submitted.")
        else:
            flash("This food is no longer available.")
    return redirect(url_for("index"))

@app.route("/collect/<int:donation_id>", methods=["POST"])
def collect(donation_id):
    with get_db() as conn:
        conn.execute("""
            UPDATE donations SET status='Collected'
            WHERE id=? AND status='Requested'
        """, (donation_id,))
    flash("Collection status updated.")
    return redirect(url_for("index"))

@app.route("/delete/<int:donation_id>", methods=["POST"])
def delete(donation_id):
    with get_db() as conn:
        conn.execute("DELETE FROM donations WHERE id=?", (donation_id,))
    flash("Donation record deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)