import os
import json
import sys
import dotenv
from atproto import client_utils, Client

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

if post_data["bskyId"]:
    print(f"Post already exists with bskyId: {post_data['bskyId']}")
    sys.exit(1)

link = f"https://nilleb.com/blog/post/#{slug}"

text_builder = client_utils.TextBuilder()
post_text = f"{post_data['emoji']} {post_data['title']}\n\n"
text_builder.text(post_text)
text_builder.link(link, link)
text_builder.text("\n\n")
for tag in post_data["tags"]:
    text_builder.tag(f"#{tag} ", tag)

client = Client()
client.login(handle, password)
response = client.send_post(text_builder)
print(response)

bsky_id = response["uri"].split("/")[-1]
post_data["bskyId"] = bsky_id

with open("blog/posts.json", "w") as f:
    json.dump(posts, f, indent=2)
