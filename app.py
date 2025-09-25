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
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()
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
