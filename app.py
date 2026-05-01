from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT,
            reps INTEGER,
            sets INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_workout():
    data = request.get_json()
    exercise = data["exercise"]
    reps = data["reps"]
    sets = data["sets"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO workouts (exercise, reps, sets) VALUES (?, ?, ?)",
              (exercise, reps, sets))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/stats")
def stats():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT exercise, reps, sets, date FROM workouts ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
