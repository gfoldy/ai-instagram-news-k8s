import os
import psycopg
from openai import OpenAI

DATABASE_URL = os.environ["DATABASE_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

def get_posts_missing_images():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title
                FROM posts
                WHERE image_b64 IS NULL
                LIMIT 5;
            """)
            return cur.fetchall()

def save_image(post_id, image_b64):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE posts
                SET image_b64 = %s
                WHERE id = %s;
            """, (image_b64, post_id))
        conn.commit()

def generate_image(prompt):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return result.data[0].b64_json

def main():
    print("Image generator started...")
    posts = get_posts_missing_images()

    if not posts:
        print("No posts need images.")
        return

    for post_id, title in posts:
        try:
            print(f"Generating image for post {post_id}")
            prompt = f"Create a modern Instagram-ready tech news image for: {title}"
            image_b64 = generate_image(prompt)
            save_image(post_id, image_b64)
            print(f"Saved image for post {post_id}")
        except Exception as e:
            print(f"Failed for post {post_id}: {e}")

    print("Image generator finished.")

if __name__ == "__main__":
    main()
