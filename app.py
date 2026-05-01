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

    recommendation = coach_recommendation(reps, sets)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO workouts (exercise, reps, sets) VALUES (?, ?, ?)",
        (exercise, reps, sets)
    )
    conn.commit()
    conn.close()

    return jsonify(recommendation)

@app.route("/stats")
def stats():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT exercise, reps, sets, date FROM workouts ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)

def get_next_progress(exercise, reps):
    try:
        reps = int(reps)
    except:
        return reps

    # logique simple de progression
    if reps >= 15:
        return reps + 2
    elif reps >= 8:
        return reps + 1
    else:
        return reps

def coach_recommendation(reps, sets):
    reps = int(reps)
    sets = int(sets)

    # logique simple mais efficace
    if reps >= 15:
        return {
            "message": "🔥 Niveau facile détecté → on augmente l'intensité",
            "next_reps": reps + 2,
            "advice": "Ajoute du tempo lent ou plus de difficulté"
        }

    elif reps >= 8:
        return {
            "message": "💪 Bon niveau → progression stable",
            "next_reps": reps + 1,
            "advice": "Continue comme ça, focus exécution propre"
        }

    else:
        return {
            "message": "⚠️ Niveau difficile → stabilisation",
            "next_reps": reps,
            "advice": "Reste sur ce volume et améliore la technique"
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
