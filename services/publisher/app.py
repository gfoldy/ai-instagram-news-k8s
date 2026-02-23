import os
import psycopg
from flask import Flask, request, redirect, url_for, render_template_string

DATABASE_URL = os.environ["DATABASE_URL"]

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Publisher (Safe Mode)</title>
  <style>
    body { font-family: -apple-system, system-ui, Arial; margin: 24px; }
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
    .meta { color:#666; font-size: 14px; margin-bottom: 8px; }
    .title { font-size: 18px; font-weight: 700; margin: 6px 0; }
    textarea { width: 100%; height: 140px; border-radius: 10px; padding: 10px; border: 1px solid #ccc; }
    .btn { display:inline-block; padding:10px 12px; border-radius:10px; border:1px solid #333; background:#111; color:#fff; text-decoration:none; cursor:pointer; margin-right:8px; }
    .btn2 { border:1px solid #333; background:#fff; color:#111; }
    .row { margin-top: 10px; }
    code { background:#f6f6f6; padding:2px 6px; border-radius:6px; }
    .status { font-weight:700; }
  </style>
</head>
<body>
  <h1>Publisher (Safe Mode)</h1>

  <div style="margin-bottom:20px;">
    <a class="btn btn2" href="/?status=ENRICHED">ENRICHED</a>
    <a class="btn btn2" href="/?status=APPROVED">APPROVED</a>
  </div>

  <p>Shows <code>ENRICHED</code> posts. You approve + manually post to Instagram.</p>

  {% for p in posts %}
    <div class="card">
      <div class="meta">
        <span class="status">{{ p.status }}</span> • ID {{ p.id }} • {{ p.source }} • {{ p.created_at }}
      </div>

      <div class="title">{{ p.title }}</div>

      <div class="row">
        <a class="btn btn2" href="{{ p.url }}" target="_blank">Open Article</a>
        <a class="btn btn2" href="https://www.instagram.com/" target="_blank">Open Instagram</a>
      </div>

      <div class="row">
        <label><b>Caption (copy/paste into IG)</b></label>
        <textarea readonly id="cap-{{p.id}}">{{ p.caption }}</textarea>
      </div>

      <div class="row">
        <button class="btn btn2" onclick="copyText('cap-{{p.id}}')">Copy Caption</button>

        <form style="display:inline" method="post" action="/approve">
          <input type="hidden" name="id" value="{{p.id}}">
          <button class="btn" type="submit">Approve</button>
        </form>

        <form style="display:inline" method="post" action="/reject">
          <input type="hidden" name="id" value="{{p.id}}">
          <button class="btn btn2" type="submit">Reject</button>
        </form>

        <form style="display:inline" method="post" action="/posted">
          <input type="hidden" name="id" value="{{p.id}}">
          <button class="btn btn2" type="submit">Mark Posted</button>
        </form>
      </div>

      <div class="row">
        <small>Tip: Approve = ready queue. Mark Posted after you publish in IG.</small>
      </div>
    </div>
  {% endfor %}

  <script>
    function copyText(id){
      const el = document.getElementById(id);
      el.select();
      el.setSelectionRange(0, 999999);
      navigator.clipboard.writeText(el.value);
      alert("Caption copied!");
    }
  </script>
</body>
</html>
"""

def fetch_by_status(status: str, limit=20):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, source, url, caption, status, created_at
                FROM posts
                WHERE status = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (status, limit))
            rows = cur.fetchall()

    posts = []
    for r in rows:
        posts.append({
            "id": r[0],
            "title": r[1],
            "source": r[2],
            "url": r[3],
            "caption": r[4] or "",
            "status": r[5],
            "created_at": r[6],
        })
    return posts

def set_status(post_id: int, status: str, ts_col: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE posts SET status=%s, {ts_col}=NOW() WHERE id=%s",
                (status, post_id),
            )
        conn.commit()

@app.get("/")
def home():
    status = request.args.get("status", "ENRICHED")
    posts = fetch_by_status(status)
    return render_template_string(HTML, posts=posts, current=status)

@app.post("/approve")
def approve():
    post_id = int(request.form["id"])
    set_status(post_id, "APPROVED", "approved_at")
    return redirect(url_for("home"))

@app.post("/posted")
def posted():
    post_id = int(request.form["id"])
    set_status(post_id, "POSTED", "posted_at")
    return redirect(url_for("home"))

@app.post("/reject")
def reject():
    post_id = int(request.form["id"])
    set_status(post_id, "REJECTED", "approved_at")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
