import sqlite3

conn = sqlite3.connect("comments.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
)
""")

# COMMENTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  comment TEXT NOT NULL,
  is_toxic INTEGER NOT NULL
)
""")

# INSERT ADMIN
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin', 'admin')
""")

conn.commit()
conn.close()

print("✅ Database ready")