from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle
import re

app = Flask(__name__)
CORS(app)

# ==================================================
# LOAD ML MODEL
# ==================================================
model = pickle.load(open("toxic_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ==================================================
# DATABASE CONNECTION
# ==================================================
def get_db():
    return sqlite3.connect("comments.db", check_same_thread=False)

# ==================================================
# TEXT NORMALIZATION (ANTI b!tch BYPASS)
# ==================================================
def normalize_text(text):
    text = text.lower()

    replacements = {
        "!": "i",
        "1": "i",
        "@": "a",
        "$": "s",
        "0": "o",
        "*": "",
        "#": "",
        "%": ""
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # remove repeated letters (biiitch → bitch)
    text = re.sub(r'(.)\1+', r'\1', text)

    return text

# ==================================================
# INITIALIZE DATABASE
# ==================================================
conn = get_db()
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    toxic_count INTEGER DEFAULT 0
)
""")

# COMMENTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    comment TEXT NOT NULL,
    is_toxic INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# TOXIC COMMENTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS toxic_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# DEFAULT ADMIN
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin', 'admin')
""")

conn.commit()
conn.close()

# ==================================================
# REGISTER USER
# ==================================================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, 'user')",
            (username, password)
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

# ==================================================
# LOGIN USER
# ==================================================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({"success": True, "role": row[0]})
    else:
        return jsonify({"success": False})

# ==================================================
# ADD COMMENT + TOXIC CHECK
# ==================================================
@app.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.get_json()
    comment = data.get("comment")
    username = data.get("username", "guest")

    conn = get_db()
    cur = conn.cursor()

    # 1️⃣ CHECK TOXIC COUNT
    cur.execute(
        "SELECT toxic_count FROM users WHERE username=?",
        (username,)
    )
    row = cur.fetchone()

    if row and row[0] >= 2:
        conn.close()
        return jsonify({
            "blocked": True,
            "message": "🚫 You are blocked from commenting due to toxic behavior"
        })

    # 2️⃣ NORMALIZE + PREDICT
    clean_comment = normalize_text(comment)
    vec = vectorizer.transform([clean_comment])
    prediction = int(model.predict(vec)[0])  # 1 = toxic

    # 3️⃣ STORE COMMENT
    cur.execute(
        "INSERT INTO comments (username, comment, is_toxic) VALUES (?, ?, ?)",
        (username, comment, prediction)
    )

    # 4️⃣ IF TOXIC → UPDATE COUNT + LOG
    if prediction == 1:
        cur.execute(
            "UPDATE users SET toxic_count = toxic_count + 1 WHERE username=?",
            (username,)
        )
        cur.execute(
            "INSERT INTO toxic_comments (username, comment) VALUES (?, ?)",
            (username, comment)
        )

    conn.commit()
    conn.close()

    return jsonify({
        "toxic": prediction == 1,
        "blocked": False
    })

# ==================================================
# ADMIN: VIEW ALL COMMENTS
# ==================================================
@app.route("/admin/comments", methods=["GET"])
def admin_comments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, comment, is_toxic, created_at
        FROM comments
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

# ==================================================
# ADMIN: VIEW ONLY TOXIC COMMENTS
# ==================================================
@app.route("/admin/toxic_comments", methods=["GET"])
def view_toxic_comments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, comment, created_at
        FROM toxic_comments
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

# ==================================================
# ADMIN: DELETE COMMENT
# ==================================================
@app.route("/admin/delete/<int:cid>", methods=["DELETE"])
def delete_comment(cid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM comments WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": True})

# ==================================================
# RUN SERVER
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)
