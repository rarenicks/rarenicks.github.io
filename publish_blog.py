import os
import re
import datetime
import argparse
import markdown

# Setup
BLOG_DIR = "blog"
DRAFTS_DIR = os.path.join(BLOG_DIR, "drafts")
TEMPLATE_PATH = os.path.join(BLOG_DIR, "templates", "post_template.html")
INDEX_PATH = os.path.join(BLOG_DIR, "index.html")

def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Simple frontmatter parsing
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2]
            for line in raw_fm.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip()
    
    return frontmatter, body

def publish_post(draft_filename):
    draft_path = os.path.join(DRAFTS_DIR, draft_filename)
    if not os.path.exists(draft_path):
        print(f"Error: Draft '{draft_filename}' not found in {DRAFTS_DIR}")
        return

    print(f"Processing {draft_filename}...")
    meta, body = parse_markdown(draft_path)
    
    # Convert MD to HTML
    html_content = markdown.markdown(body, extensions=['fenced_code', 'codehilite'])
    
    # Read Template
    with open(TEMPLATE_PATH, 'r') as f:
        template = f.read()
    
    # Fill Template
    output_html = template.replace('{{ title }}', meta.get('title', 'Untitled'))
    output_html = output_html.replace('{{ description }}', meta.get('description', ''))
    output_html = output_html.replace('{{ date }}', meta.get('date', datetime.date.today().strftime('%b %d, %Y')))
    output_html = output_html.replace('{{ category }}', meta.get('category', 'Technology'))
    output_html = output_html.replace('{{ content_html }}', html_content)
    
    # Write Output
    slug = draft_filename.replace('.md', '.html')
    output_path = os.path.join(BLOG_DIR, slug)
    with open(output_path, 'w') as f:
        f.write(output_html)
    
    print(f"Successfully created {output_path}")
    update_index(meta, slug)

def update_index(meta, slug):
    # This is a simple implementation that prepends the new link to the blog grid
    # A more robust solution would be to parse the HTML and insert it properly
    print("Note: Automated index updating requires Beautiful Soup or regex magic.")
    print(f"Please manually add the link to blog/index.html:\n")
    print(f"""
    <a href="{slug}" class="blog-card">
        <span class="blog-date">{meta.get('date')}</span>
        <h3>{meta.get('title')}</h3>
        <p>{meta.get('description')}</p>
        <span class="text-accent text-mono" style="font-size: 0.8rem;">{meta.get('category')}</span>
    </a>
    """)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish a blog post from markdown draft.")
    parser.add_argument("draft", help="Filename of the draft in blog/drafts/ (e.g., my_post.md)")
    args = parser.parse_args()
    
    publish_post(args.draft)
