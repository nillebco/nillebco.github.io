import matter from 'gray-matter';

const tagColors = {};

function getRandomColor() {
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 70%, 80%)`;
}

function parseMarkdown(markdown) {
  // Use gray-matter to parse frontmatter
  const { data: frontmatter, content } = matter(markdown);
  
  // Extract title from content (first line starting with #)
  const contentLines = content.split('\n');
  const titleLine = contentLines.find(line => line.startsWith('# '));
  const title = titleLine ? titleLine.replace('# ', '') : '';
  
  // Remove the first heading from content to avoid duplication
  const contentWithoutTitle = contentLines
    .filter(line => !line.startsWith('# '))
    .join('\n');
  
  // Parse tags and published date from frontmatter
  const tags = frontmatter.tags ? (Array.isArray(frontmatter.tags) ? frontmatter.tags : frontmatter.tags.split(',').map(tag => tag.trim())) : [];
  const publishedDate = frontmatter.publishedDate || frontmatter.date || '';
  
  return { title, tags, content: contentWithoutTitle, publishedDate };
}

async function loadPost() {
  const slug = window.location.hash.substring(1);
  const response = await fetch(`./${slug}.md`);
  const markdown = await response.text();
  const { title, tags, content, publishedDate } = parseMarkdown(markdown);

  document.getElementById('post-title').innerText = title;
  document.getElementById('post-tags').innerHTML = tags.map(tag => {
    if (!tagColors[tag]) tagColors[tag] = getRandomColor();
    return `<span class="tag" style="background-color: ${tagColors[tag]};">${tag}</span>`;
  }).join(' ');
  document.getElementById('post-content').innerHTML = marked.parse(content);
  document.getElementById('breadcrumb-title').innerText = title;
  document.title = `Blog Post: ${title}`;

  const postsResponse = await fetch('../posts.json', {
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        }
      });
  const posts = await postsResponse.json();
  const post = posts.find(p => p.slug === slug);
  if (post) {
    const pageIcon = document.getElementById('page-icon');
    pageIcon.innerText = post.emoji;
    pageIcon.setAttribute('aria-label', post.emoji);
    if (post.bskyId) {
      const commentsDiv = document.getElementById('bluesky-comments');
      commentsDiv.setAttribute('data-bsky-uri', `at://${window.BLUESKY_DID}/app.bsky.feed.post/${post.bskyId}`);
      commentsDiv.setAttribute('hx-get', '../../components/bluesky-comments.html');
      commentsDiv.setAttribute('hx-trigger', 'load');
      htmx.process(commentsDiv);
    } else {
      console.log('No Bluesky ID found for post:', post);
    }
  }

  hljs.highlightAll();
}

// Make loadPost available globally
window.loadPost = loadPost; 