from flask import Flask, request, jsonify, redirect, send_file
from flask_cors import CORS
import sqlite3
import random
import string
import qrcode
from io import BytesIO
import validators

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return sqlite3.connect(DATABASE)


# ---------------- DATABASE INIT ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS urls(
        short_id TEXT PRIMARY KEY,
        original_url TEXT NOT NULL,
        clicks INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------- GENERATE UNIQUE SHORT CODE ----------------
def generate_short():
    conn = get_db()
    cur = conn.cursor()

    while True:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cur.execute("SELECT short_id FROM urls WHERE short_id=?", (short_id,))
        exists = cur.fetchone()

        if not exists:
            conn.close()
            return short_id


# ---------------- SHORTEN URL ----------------
@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    if not validators.url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_id = generate_short()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO urls(short_id, original_url, clicks) VALUES (?, ?, 0)",
        (short_id, original_url)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "short_url": f"http://192.168.0.6:5000/{short_id}"
    })


# ---------------- REDIRECT + CLICK TRACKING ----------------
@app.route("/<short_id>")
def redirect_url(short_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT original_url FROM urls WHERE short_id=?", (short_id,))
    result = cur.fetchone()

    if result:
        original_url = result[0]

        cur.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_id=?",
            (short_id,)
        )

        conn.commit()
        conn.close()

        return redirect(original_url)

    conn.close()
    return "URL not found", 404


# ---------------- ANALYTICS API ----------------
@app.route("/analytics")
def analytics():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT short_id, original_url, clicks FROM urls")
    rows = cur.fetchall()

    conn.close()
    return jsonify(rows)


# ---------------- DELETE LINK ----------------
@app.route("/delete/<short_id>", methods=["DELETE"])
def delete_link(short_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM urls WHERE short_id=?", (short_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Link deleted"})


# ---------------- QR CODE GENERATOR ----------------
@app.route("/qr/<short_id>")
def generate_qr(short_id):
    url = f"http://192.168.0.6:5000/{short_id}"

    img = qrcode.make(url)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(buf, mimetype="image/png")


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "URL Shortener Backend Running"


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)