import os
import json
import sys
import requests
from datetime import datetime, timezone
import dotenv

dotenv.load_dotenv()
handle = os.getenv("BSKY_HANDLE")
password = os.getenv("BSKY_APP_PASSWORD")

if len(sys.argv) != 2:
    print("Usage: python create_bsky_post.py <slug>")
    sys.exit(1)

slug = sys.argv[1]

# Load posts data
with open("blog/posts.json") as f:
    posts = json.load(f)

# Find the post with matching slug
post_data = next((post for post in posts if post["slug"] == slug), None)
if not post_data:
    print(f"No post found with slug: {slug}")
    sys.exit(1)

# Create the post text with title and link
post_text = (
    f"{post_data['emoji']} {post_data['title']}\n\nhttps://nilleb.com/blog/post/{slug}"
)

post = {
    "$type": "app.bsky.feed.post",
    "text": post_text,
    "createdAt": datetime.now(timezone.utc).isoformat(),
}

session_resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.server.createSession",
    json={"identifier": handle, "password": password},
)
session_resp.raise_for_status()
session = session_resp.json()

payload = {
    "repo": session["did"],
    "collection": "app.bsky.feed.post",
    "record": post,
}

if False:
    post_resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": f"Bearer {session['accessJwt']}"},
        json=payload,
    )
    post_resp.raise_for_status()
