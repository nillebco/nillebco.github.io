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

def format_rich_text(rich_text_list):
    """Convert Notion's rich text array to markdown formatted text."""
    formatted_text = ""
    for text in rich_text_list:
        content = text.get("plain_text", "")
        annotations = text.get("annotations", {})
        
        # Apply formatting based on annotations
        if annotations.get("bold"):
            content = f"**{content}**"
        if annotations.get("italic"):
            content = f"*{content}*"
        if annotations.get("strikethrough"):
            content = f"~~{content}~~"
        if annotations.get("code"):
            content = f"`{content}`"
        if annotations.get("underline"):
            content = f"__{content}__"
        
        formatted_text += content
    
    return formatted_text

def generate_markdown_file(notion_id, post_data=None):
    """Generate a markdown file for a given Notion page ID.
    If post_data is provided, use it instead of fetching from Notion."""
    if not post_data:
        # Fetch the page from Notion
        page = notion.pages.retrieve(page_id=notion_id)
        props = page["properties"]
        
        # Extract title
        title = format_rich_text(props.get("Name", {}).get("title", []))
        
        # Extract date
        date_obj = props.get("Publish Date", {}).get("date", {})
        if date_obj and date_obj.get("start"):
            date = datetime.fromisoformat(date_obj["start"]).strftime("%B %d, %Y")
        else:
            return None
        
        # Extract tags
        tags = [
            tag.get("name", "")
            for tag in props.get("Tags", {}).get("multi_select", [])
        ]
        
        # Get page content
        content_blocks = notion.blocks.children.list(block_id=notion_id)
        
        slug = slugify(title)
    else:
        title = post_data["title"]
        date = post_data["date"]
        tags = post_data["tags"]
        slug = post_data["slug"]
        # For existing posts, we'll need to fetch content
        content_blocks = notion.blocks.children.list(block_id=notion_id.replace("-", ""))
    
    # Create the markdown content
    markdown_content = []
    
    # Add metadata
    markdown_content.append(f"# {title}")
    markdown_content.append("")
    markdown_content.append(f"Tags: {', '.join(tags)}")
    markdown_content.append(f"Publish Date: {date}")
    markdown_content.append("")
    
    # Convert Notion blocks to markdown
    last_block_type = None
    for block in content_blocks["results"]:
        block_type = block["type"]
        
        # Add spacing before new block type (except for list items following list items)
        if last_block_type and last_block_type != block_type and \
           not (last_block_type in ["bulleted_list_item", "numbered_list_item"] and \
                block_type in ["bulleted_list_item", "numbered_list_item"]):
            markdown_content.append("")
        
        if block_type == "paragraph":
            text = format_rich_text(block["paragraph"]["rich_text"])
            if text.strip():  # Only add non-empty paragraphs
                markdown_content.append(text)
                markdown_content.append("")  # Add space after paragraph
        elif block_type == "heading_1":
            text = format_rich_text(block["heading_1"]["rich_text"])
            markdown_content.append(f"# {text}")
            markdown_content.append("")
        elif block_type == "heading_2":
            text = format_rich_text(block["heading_2"]["rich_text"])
            markdown_content.append(f"## {text}")
            markdown_content.append("")
        elif block_type == "heading_3":
            text = format_rich_text(block["heading_3"]["rich_text"])
            markdown_content.append(f"### {text}")
            markdown_content.append("")
        elif block_type == "bulleted_list_item":
            text = format_rich_text(block["bulleted_list_item"]["rich_text"])
            markdown_content.append(f"- {text}")
        elif block_type == "numbered_list_item":
            text = format_rich_text(block["numbered_list_item"]["rich_text"])
            markdown_content.append(f"1. {text}")
        elif block_type == "code":
            code = format_rich_text(block["code"]["rich_text"])
            language = block["code"].get("language", "")
            markdown_content.append(f"```{language}")
            markdown_content.append(code)
            markdown_content.append("```")
            markdown_content.append("")
        elif block_type == "image":
            caption = format_rich_text(block["image"].get("caption", []))
            if block["image"]["type"] == "external":
                url = block["image"]["external"]["url"]
            else:
                url = block["image"]["file"]["url"]
            markdown_content.append(f"![{caption}]({url})")
            markdown_content.append("")
        
        # Update last block type
        last_block_type = block_type
    
    # Add a newline after lists if the last block was a list item
    if last_block_type in ["bulleted_list_item", "numbered_list_item"]:
        markdown_content.append("")
    
    # Remove trailing empty line if exists
    while markdown_content and markdown_content[-1] == "":
        markdown_content.pop()
    
    # Add single newline at the end
    markdown_content.append("")
    
    # Ensure the blog/post directory exists
    os.makedirs("blog/post", exist_ok=True)
    
    # Write the markdown file
    file_path = f"blog/post/{slug}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))
    
    return file_path

def update_posts_json(posts):
    # Sort posts by date in descending order
    posts.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y"), reverse=True)
    
    # Write to posts.json
    with open("blog/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    
    # Generate markdown files for each post
    for post in posts:
        if "notion_id" in post:
            generate_markdown_file(post["notion_id"], post_data=post)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # A slug was provided as argument
        target_slug = sys.argv[1]
        
        # Load existing posts to find the one with matching slug
        existing_posts = get_existing_posts()
        matching_post = next((post for post in existing_posts if post["slug"] == target_slug), None)
        
        if matching_post and "notion_id" in matching_post:
            file_path = generate_markdown_file(matching_post["notion_id"], post_data=matching_post)
            if file_path:
                print(f"Successfully generated markdown file: {file_path}")
            else:
                print(f"Failed to generate markdown for post with slug: {target_slug}")
        else:
            print(f"No post found with slug: {target_slug}")
    else:
        # No arguments, run the full sync
        posts = get_notion_posts()
        update_posts_json(posts)
        print(f"Successfully synced {len(posts)} posts from Notion to posts.json")
