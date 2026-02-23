import os
import psycopg
import feedparser
from datetime import datetime

DATABASE_URL = os.environ["DATABASE_URL"]

FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/tag/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"),
    ("Ars Technica AI", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
]

def fetch_items(max_per_feed=8):
    items = []
    for source, url in FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries[:max_per_feed]:
            title = (e.get("title") or "").strip()
            link = (e.get("link") or "").strip()
            if not title or not link:
                continue
            items.append({"title": title, "source": source, "url": link})
    return items

def insert_post(post):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO posts (title, source, url, status)
                VALUES (%s, %s, %s, 'PENDING')
                ON CONFLICT (url) DO NOTHING
            """, (post["title"], post["source"], post["url"]))
        conn.commit()

def main():
    items = fetch_items()
    for p in items:
        insert_post(p)
    print(f"Inserted {len(items)} feed items (deduped by URL).")

if __name__ == "__main__":
    main()


