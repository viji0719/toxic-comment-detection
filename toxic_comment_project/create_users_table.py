import sqlite3

conn = sqlite3.connect("comments.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password TEXT,
  role TEXT
)
""")

# Create default admin
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin', 'admin')
""")

conn.commit()
conn.close()

print("Users table created, admin added")