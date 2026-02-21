import sqlite3

conn = sqlite3.connect("comments.db")
cur = conn.cursor()

# Drop old tables
cur.execute("DROP TABLE IF EXISTS comments")
cur.execute("DROP TABLE IF EXISTS toxic_comments")

# Main comments table
cur.execute("""
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    comment TEXT NOT NULL,
    is_toxic INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Toxic-only table
cur.execute("""
CREATE TABLE toxic_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ comments & toxic_comments tables created")