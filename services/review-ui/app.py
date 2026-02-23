import os
import psycopg
from flask import Flask, jsonify, request

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

app = Flask(__name__)

@app.route("/")
def health():
    return {"status": "review-ui running"}

@app.route("/posts")
def posts():
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            "SELECT id, title, source, status, created_at FROM posts ORDER BY created_at DESC"
        ).fetchall()

    return jsonify([
        {
            "id": r[0],
            "title": r[1],
            "source": r[2],
            "status": r[3],
            "created_at": r[4].isoformat()
        }
        for r in rows
    ])

@app.route("/posts/<int:post_id>", methods=["PATCH"])
def update_status(post_id):
    data = request.get_json()
    new_status = data.get("status")

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE posts SET status = %s WHERE id = %s",
                (new_status, post_id),
            )
        conn.commit()

    return jsonify({"message": "updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

