from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this!

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def home():
    if "user_id" in session:
        return render_template("journal.html")
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        return "User already exists"
    conn.close()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        session["user_id"] = user[0]
        return redirect("/")
    return "Invalid login"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

@app.route("/save", methods=["POST"])
def save():
    if "user_id" not in session:
        return "Unauthorized", 401
    content = request.json.get("content")
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("INSERT INTO entries (user_id, content) VALUES (?, ?)", (session["user_id"], content))
    conn.commit()
    conn.close()
    return "Saved!"

@app.route("/entries")
def entries():
    if "user_id" not in session:
        return "Unauthorized", 401
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("SELECT content FROM entries WHERE user_id=?", (session["user_id"],))
    data = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
