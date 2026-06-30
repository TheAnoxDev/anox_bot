import sqlite3

conn = sqlite3.connect("anox.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service TEXT,
    status TEXT
)
""")

conn.commit()

def add_user(user_id, username):
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?)", (user_id, username))
    conn.commit()

def add_order(user_id, service):
    c.execute("INSERT INTO orders (user_id, service, status) VALUES (?,?,?)",
              (user_id, service, "pending"))
    conn.commit()