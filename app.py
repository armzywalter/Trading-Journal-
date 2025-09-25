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
