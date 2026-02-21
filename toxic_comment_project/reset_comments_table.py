import sqlite3

conn = sqlite3.connect("comments.db")
cur = conn.cursor()

# Delete old table if exists
cur.execute("DROP TABLE IF EXISTS comments")

# Create fresh table
cur.execute("""
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  comment TEXT NOT NULL,
  is_toxic INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ comments table reset successfully")