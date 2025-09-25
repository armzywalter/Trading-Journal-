from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------- DB SETUP ----------------
def init_db():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS trades (
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
        locked INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM trades WHERE user_id=?", (session["user_id"],))
    trades = c.fetchall()
    conn.close()
    return render_template("index.html", trades=trades)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("journal.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("journal.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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
    return redirect("/")

@app.route("/lock_trade/<int:trade_id>")
def lock_trade(trade_id):
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("UPDATE trades SET locked=1 WHERE id=?", (trade_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/unlock_trade/<int:trade_id>")
def unlock_trade(trade_id):
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("UPDATE trades SET locked=0 WHERE id=?", (trade_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete_trade/<int:trade_id>")
def delete_trade(trade_id):
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("DELETE FROM trades WHERE id=?", (trade_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/next_page")
def next_page():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("INSERT INTO trades (user_id) VALUES (?)", (session["user_id"],))
    conn.commit()
    conn.close()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
