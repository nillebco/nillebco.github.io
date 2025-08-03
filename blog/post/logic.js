const tagColors = {};

function getRandomColor() {
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 70%, 80%)`;
}

function parseMarkdown(markdown) {
  // Check if the markdown has frontmatter (starts with ---)
  if (markdown.startsWith('---')) {
    // Find the end of frontmatter (second ---)
    const frontmatterEnd = markdown.indexOf('---', 3);
    if (frontmatterEnd !== -1) {
      // Extract frontmatter content
      const frontmatter = markdown.substring(3, frontmatterEnd).trim();
      // Extract content (everything after the second ---)
      const content = markdown.substring(frontmatterEnd + 3).trim();
      
      // Parse frontmatter (simple YAML parsing)
      const metadata = {};
      const frontmatterLines = frontmatter.split('\n');
      
      for (const line of frontmatterLines) {
        const colonIndex = line.indexOf(':');
        if (colonIndex !== -1) {
          const key = line.substring(0, colonIndex).trim();
          let value = line.substring(colonIndex + 1).trim();
          
          // Remove quotes if present
          if ((value.startsWith('"') && value.endsWith('"')) || 
              (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
          }
          
          metadata[key] = value;
        }
      }
      
      // Extract title from content (first line starting with #)
      const contentLines = content.split('\n');
      const titleLine = contentLines.find(line => line.startsWith('# '));
      const title = titleLine ? titleLine.replace('# ', '') : '';
      
      // Parse tags and published date from metadata
      const tags = metadata.tags ? metadata.tags.split(',').map(tag => tag.trim()) : [];
      const publishedDate = metadata.publishedDate || metadata.date || '';
      
      return { title, tags, content, publishedDate };
    }
  }
  
  // Fallback to original parsing for backward compatibility
  const lines = markdown.split('\n');
  const titleLine = lines.shift();
  const title = titleLine?.startsWith('#') ? titleLine.replace('# ', '') : '';
  const tagsLine = lines.find(line => line.startsWith('Tags: '));
  const tags = tagsLine ? tagsLine.replace('Tags: ', '').split(',').map(tag => tag.trim()) : [];
  const publishedDateLine = lines.find(line => line.startsWith('Publish Date: '));
  const publishedDate = publishedDateLine ? publishedDateLine.replace('Publish Date: ', '') : '';
  const contentLines = lines.filter(line => !line.startsWith('Tags: ') && !line.startsWith('Publish Date: ') && !line.startsWith('Published: '));
  const content = contentLines.join('\n');
  return { title, tags, content, publishedDate };
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