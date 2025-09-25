from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key"  # change to something secure!

# ---------------------------
# Database Setup
# ---------------------------
def init_db():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Trades table
    c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            pair TEXT,
            direction TEXT,
            entry REAL,
            exit REAL,
            sl REAL,
            tp REAL,
            lots REAL,
            rr TEXT,
            duration TEXT,
            pl_pips REAL,
            balance_before REAL,
            balance_after REAL,
            technical TEXT,
            fundamental TEXT,
            conditions TEXT,
            reason TEXT,
            before TEXT,
            during TEXT,
            exit_reason TEXT,
            outcome TEXT,
            lessons TEXT,
            adjustments TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("journal.html")  # your trade entry template

# -------- Auth --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("journal.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("journal.db")
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect(url_for("home"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------- Trade Saving --------
@app.route("/save_trade", methods=["POST"])
def save_trade():
    if "user_id" not in session:
        return "Unauthorized", 401

    data = {key: request.form.get(key) for key in request.form.keys()}

    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("""INSERT INTO trades (
        user_id, date, pair, direction, entry, exit, sl, tp, lots, rr, duration, pl_pips,
        balance_before, balance_after, technical, fundamental, conditions,
        reason, before, during, exit_reason, outcome, lessons, adjustments
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
        session["user_id"], data["date"], data["pair"], data["direction"], data["entry"], data["exit"],
        data["sl"], data["tp"], data["lots"], data["rr"], data["duration"], data["pl_pips"],
        data["balance_before"], data["balance_after"], data["technical"], data["fundamental"], data["conditions"],
        data["reason"], data["before"], data["during"], data["exit_reason"], data["outcome"], data["lessons"], data["adjustments"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
