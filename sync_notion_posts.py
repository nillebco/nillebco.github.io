import os
import json
from datetime import datetime
import dotenv
from notion_client import Client
from slugify import slugify

dotenv.load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "106023b4857680a19525e8d62436cd60"

notion = Client(auth=NOTION_TOKEN)

def get_existing_posts():
    try:
        with open("blog/posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_notion_posts():
    posts = []
    cursor = None
    existing_posts = {post.get("notion_id"): post for post in get_existing_posts()}
    
    while True:
        if cursor:
            response = notion.databases.query(database_id=DATABASE_ID, start_cursor=cursor)
        else:
            response = notion.databases.query(database_id=DATABASE_ID)
        
        for page in response["results"]:
            notion_id = page["id"].replace("-", "")
            props = page["properties"]
            
            # Check if post is published
            publish_status = (props.get("Published", {}).get("select", {}) or {}).get("name", "")
            if publish_status != "Yes":
                continue
            
            # If post exists and has notion_id, keep it unchanged
            if notion_id in existing_posts:
                posts.append(existing_posts[notion_id])
                continue
                
            # Extract title
            title = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "")
            
            # Extract date from Publish Date property
            date_obj = props.get("Publish Date", {}).get("date", {})
            if date_obj and date_obj.get("start"):
                date = datetime.fromisoformat(date_obj["start"]).strftime("%B %d, %Y")
            else:
                # Skip posts without a publish date
                continue
            
            # Extract tags
            tags = [
                tag.get("name", "")
                for tag in props.get("Tags", {}).get("multi_select", [])
            ]
            
            # Extract emoji from page icon
            emoji = "✍️"  # default emoji
            icon = page.get("icon", {})
            if icon and icon.get("type") == "emoji":
                emoji = icon.get("emoji", "✍️")
            
            # Generate slug from title
            slug = slugify(title)
            
            # Extract BlueSky ID if exists
            bsky_id = props.get("BlueSkyId", {}).get("rich_text", [{}])[0].get("plain_text", "")
            
            post = {
                "title": title,
                "slug": slug,
                "tags": tags,
                "date": date,
                "emoji": emoji,
                "notion_id": notion_id
            }
            
            if bsky_id:
                post["bskyId"] = bsky_id
                
            posts.append(post)
        
        if not response.get("has_more"):
            break
            
        cursor = response.get("next_cursor")
    
    return posts

def update_posts_json(posts):
    # Sort posts by date in descending order
    posts.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y"), reverse=True)
    
    # Write to posts.json
    with open("blog/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    posts = get_notion_posts()
    update_posts_json(posts)
    print(f"Successfully synced {len(posts)} posts from Notion to posts.json")
