import sqlite3

conn = sqlite3.connect("comments.db")
cur = conn.cursor()

# Remove old table
cur.execute("DROP TABLE IF EXISTS comments")

# Create new table with timestamp
cur.execute("""
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    comment TEXT NOT NULL,
    is_toxic INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ comments table recreated with timestamp")