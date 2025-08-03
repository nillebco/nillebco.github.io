import { Buffer } from 'buffer';
import matter from 'gray-matter';

// Make Buffer available globally for gray-matter
window.Buffer = Buffer;

const tagColors = {};

function getRandomColor() {
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 70%, 80%)`;
}

function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')     // Replace spaces with -
    .replace(/&/g, '-and-')   // Replace & with 'and'
    .replace(/[^\w\-]+/g, '') // Remove all non-word chars
    .replace(/\-\-+/g, '-');  // Replace multiple - with single -
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
  
  // Process the content, converting tag lines into HTML and adding anchors to headings
  const processedContentLines = contentWithoutTitle.split('\n').map(line => {
    if (line.startsWith('Tags: ')) {
      const tags = line.replace('Tags: ', '')
        .split('#')
        .filter(Boolean)
        .map(tag => {
          const tagText = '#' + tag.trim();
          if (!tagColors[tagText]) tagColors[tagText] = getRandomColor();
          return `<span class="tag" style="background-color: ${tagColors[tagText]};">${tagText}</span>`;
        })
        .join(' ');
      return `<div class="tags">${tags}</div>`;
    }
    return line;
  });

  const processedContent = processedContentLines.join('\n');
  return { title, content: processedContent };
}

function addAnchorsToHeadings(html) {
  return html.replace(/<h([1-6])>(.+?)<\/h\1>/g, (match, level, text) => {
    const slug = slugify(text);
    return `
      <h${level} id="${slug}" class="heading-with-link">
        <span class="copy-link" data-slug="${slug}" title="Copy link to section">🔗</span>
        <a href="#${slug}" class="heading-anchor">${text}</a>
      </h${level}>
    `;
  });
}

function setupCopyLinks() {
  document.querySelectorAll('.copy-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const slug = e.target.dataset.slug;
      const url = `${window.location.origin}${window.location.pathname}#${slug}`;
      navigator.clipboard.writeText(url).then(() => {
        // Show feedback
        const originalTitle = e.target.title;
        e.target.title = 'Copied!';
        e.target.style.opacity = '1';
        setTimeout(() => {
          e.target.title = originalTitle;
          e.target.style.opacity = '';
        }, 1500);
      });
    });
  });
}

// Function to handle portfolio page translations
window.applyPageTranslations = function(locale) {
    loadPortfolio(locale);
}; 

async function loadPortfolio(locale) {
  // If no locale is provided, check URL query parameter
  if (!locale) {
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    locale = langParam || document.documentElement.lang || 'en';
  }

  try {
    const fileName = locale === 'fr' ? 'portfolio-fr.md' : 'portfolio.md';
    const response = await fetch(`./${fileName}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const markdown = await response.text();
    const { title, content } = parseMarkdown(markdown);

    const portfolioContent = document.querySelector('.portfolio-content');
    const parsedContent = marked.parse(content);
    const contentWithAnchors = addAnchorsToHeadings(parsedContent);
    
    portfolioContent.innerHTML = `
      <h2 id="${slugify(title)}" class="heading-with-link">
        <span class="copy-link" data-slug="${slugify(title)}" title="Copy link to section">🔗</span>
        <a href="#${slugify(title)}" class="heading-anchor">${title}</a>
      </h2>
      ${contentWithAnchors}
    `;

    hljs.highlightAll();
    setupCopyLinks();
  } catch (error) {
    console.error('Error loading portfolio:', error);
    const portfolioContent = document.querySelector('.portfolio-content');
    portfolioContent.innerHTML = '<p>Error loading portfolio content. Please try again later.</p>';
  }
}

// Load portfolio content when the page loads
document.addEventListener('DOMContentLoaded', loadPortfolio); 