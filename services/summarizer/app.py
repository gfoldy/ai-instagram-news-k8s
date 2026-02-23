import os
import json
import psycopg
from openai import OpenAI

DATABASE_URL = os.environ["DATABASE_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You write high-retention Instagram tech news content.

Return JSON only:
{
  "summary": "...",
  "caption": "...",
  "hashtags": "...",
  "score": 0-100
}

- summary: 1-2 short sentences
- caption: strong hook + 3 bullets + CTA
- hashtags: 8-15 relevant hashtags
- score: integer 0-100
"""

def fetch_pending(limit=5):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, source, url
                FROM posts
                WHERE status = 'PENDING'
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

def mark_enriched(post_id, summary, caption, hashtags, score):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE posts
                SET summary=%s,
                    caption=%s,
                    hashtags=%s,
                    score=%s,
                    status='ENRICHED'
                WHERE id=%s
            """, (summary, caption, hashtags, score, post_id))
        conn.commit()

def enrich_post(title, source, url):
    user_prompt = f"""
Title: {title}
Source: {source}
URL: {url}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
    )

    text = response.output_text.strip()
    return json.loads(text)

def main():
    print("Summarizer starting...")

    posts = fetch_pending()
    print(f"Fetched {len(posts)} posts")

    if not posts:
        print("No PENDING posts.")
        return

    for post_id, title, source, url in posts:
        try:
            result = enrich_post(title, source, url)

            mark_enriched(
                post_id,
                result.get("summary", ""),
                result.get("caption", ""),
                result.get("hashtags", ""),
                int(result.get("score", 0))
            )

            print("ENRICHED:", post_id)

        except Exception as e:
            print("FAILED:", post_id, e)

if __name__ == "__main__":
    main()
