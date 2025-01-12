import json
from datetime import datetime
from feedgen.feed import FeedGenerator
import pytz

def generate_rss():
    # Create feed generator
    fg = FeedGenerator()
    link = 'https://nilleb.com'
    fg.title('Ivo Bellin Salarin Blog')
    fg.author({'name': 'Ivo Bellin Salarin'})
    fg.link(href=link, rel='alternate')
    fg.link(href=link, rel="self")
    fg.subtitle('Consulting in AI, ML, Search Engines, and Integrations')
    fg.language('en')

    # Read posts
    with open('blog/posts.json', 'r') as f:
        posts = json.load(f)

    # Add entries
    for post in posts:
        fe = fg.add_entry()
        fe.title(post['title'])
        fe.link(href=f'https://nilleb.com/blog/post/#{post["slug"]}')
        
        # Convert date string to proper datetime
        try:
            date = datetime.strptime(post['date'], '%B %d, %Y')
            # Make timezone aware
            date = pytz.timezone('Europe/Paris').localize(date)
            fe.published(date)
        except ValueError:
            # Fallback to current time if date parsing fails
            fe.published(datetime.now(pytz.timezone('Europe/Paris')))

        fe.description(f"{post['emoji']} {', '.join(post['tags'])}")
        fe.guid(f"{link}/blog/post/#{post['slug']}", permalink=True)

    # Generate RSS feed
    fg.rss_file('feed.xml')

if __name__ == '__main__':
    generate_rss() 