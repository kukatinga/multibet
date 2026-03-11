#!/usr/bin/env python3
"""
Apply the perfect design from first page to all others while preserving their content
Run: python3 apply_design.py
"""

import os
import re
import glob
from datetime import datetime

# Read the perfect design page (your first template)
with open('when-bundles-run-out-the-game-doesnt-stop-sportpesa-kenyas-ussd-casino-is-changing-how-kenyans-play.html', 'r', encoding='utf-8') as f:
    PERFECT_DESIGN = f.read()

def extract_page_content(html):
    """
    Extract ONLY the unique content from a page
    Returns: (title, description, category, date, image, article_content)
    """
    
    # Extract title (remove "| MULTIBET" if present)
    title_match = re.search(r'<title>(.*?)(?:\s*\|\s*MULTIBET)?</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ''
    
    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
    description = desc_match.group(1) if desc_match else ''
    
    # Extract category
    cat_match = re.search(r'<a href="/category/([^/]+)/"[^>]*>([^<]+)</a>', html)
    if cat_match:
        category_slug = cat_match.group(1)
        category_name = cat_match.group(2)
    else:
        # Try to determine from URL or content
        if '/reviews/' in html:
            category_slug, category_name = 'reviews', 'Reviews'
        elif '/predictions/' in html:
            category_slug, category_name = 'predictions', 'Predictions'
        elif '/news/' in html:
            category_slug, category_name = 'news', 'News'
        else:
            category_slug, category_name = 'reviews', 'Reviews'
    
    # Extract date
    date_match = re.search(r'<span>([A-Za-z]+ \d{1,2}, \d{4})</span>', html)
    date = date_match.group(1) if date_match else ''
    
    # Extract featured image
    img_match = re.search(r'<img src="([^"]+)"[^>]*class="[^"]*object-cover[^"]*"', html)
    image = img_match.group(1) if img_match else 'https://i.imgur.com/2H9nodm.jpg'
    
    # EXTRACT THE MAIN ARTICLE CONTENT - THIS IS THE KEY PART
    # Look for the article content div
    content_match = re.search(r'<div class="article-content[^>]*>(.*?)</div>\s*<div class="flex items-center justify-between', html, re.DOTALL)
    
    if not content_match:
        # Try alternative patterns
        content_match = re.search(r'<div class="article-content[^>]*>(.*?)</div>\s*<div class="bg-gray-50 rounded-xl', html, re.DOTALL)
    
    if not content_match:
        # Last resort: get everything between article tags and clean it up
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if article_match:
            article_content = article_match.group(1)
            # Remove title, meta, image sections
            article_content = re.sub(r'<div class="mb-4">.*?</div>', '', article_content, flags=re.DOTALL)
            article_content = re.sub(r'<h1[^>]*>.*?</h1>', '', article_content, flags=re.DOTALL)
            article_content = re.sub(r'<div class="flex flex-wrap items-center.*?</div>', '', article_content, flags=re.DOTALL)
            article_content = re.sub(r'<div class="relative mb-8.*?</div>', '', article_content, flags=re.DOTALL)
            article_content = re.sub(r'<div class="flex items-center justify-between.*?share.*?</div>', '', article_content, flags=re.DOTALL)
            article_content = re.sub(r'<div class="bg-gray-50 rounded-xl p-6 flex gap-4.*?</div>', '', article_content, flags=re.DOTALL)
            content = article_content.strip()
        else:
            content = '<p>Content could not be extracted</p>'
    else:
        content = content_match.group(1).strip()
    
    # Clean up the content
    # Remove any stray script tags
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    
    return {
        'title': title,
        'description': description,
        'category_slug': category_slug,
        'category_name': category_name,
        'date': date,
        'image': image,
        'content': content
    }

def generate_table_of_contents(content):
    """Generate TOC from h2 headings"""
    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
    if len(headings) < 2:
        return ''
    
    # Clean headings and add IDs
    toc_items = []
    for i, heading in enumerate(headings, 1):
        clean_heading = re.sub(r'<[^>]+>', '', heading).strip()
        heading_id = re.sub(r'[^a-zA-Z0-9]+', '-', clean_heading.lower()).strip('-')
        
        # Add ID to the original h2 tag
        content = re.sub(f'<h2[^>]*>{re.escape(heading)}</h2>', 
                        f'<h2 id="{heading_id}">{clean_heading}</h2>', 
                        content)
        
        toc_items.append(f'''
                <a href="#{heading_id}" class="toc-link block text-gray-700 hover:text-brand-red transition-colors text-sm font-medium" data-num="{i}">{clean_heading}</a>''')
    
    toc_html = f'''
                <!-- Table of Contents -->
                <div class="bg-gray-50 rounded-xl p-6 my-8 border border-gray-200">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-display font-bold text-lg text-gray-900">Table of Contents</h3>
                        <button onclick="toggleToc()" class="text-sm text-brand-red font-medium hover:underline">Hide</button>
                    </div>
                    <nav id="toc" class="space-y-3">
                        {''.join(toc_items)}
                    </nav>
                </div>'''
    
    return toc_html, content

def create_page_from_design(page_data, toc_html, updated_content):
    """Create a new page using the perfect design but with this page's content"""
    
    # Start with the perfect design
    new_page = PERFECT_DESIGN
    
    # Replace all the content
    new_page = new_page.replace('When bundles run out, the game doesn\'t stop- SportPesa Kenya\'s USSD Casino is changing how Kenyans play', page_data['title'])
    new_page = new_page.replace('Every Kenyan mobile user knows the moment. You\'re ready to do something now then the bundles are low, the network drags, or your phone decides today is not', page_data['description'])
    new_page = new_page.replace('Reviews', page_data['category_name'])
    new_page = new_page.replace('href="/category/reviews/"', f'href="/category/{page_data["category_slug"]}/"')
    new_page = new_page.replace('December 18, 2025', page_data['date'])
    new_page = new_page.replace('https://i.imgur.com/2H9nodm.jpg', page_data['image'])
    
    # Set active navigation state
    if page_data['category_slug'] == 'reviews':
        new_page = re.sub(r'<a href="/category/reviews/" class="[^"]*"', '<a href="/category/reviews/" class="text-brand-red font-semibold"', new_page)
        new_page = re.sub(r'<a href="/category/predictions/" class="[^"]*"', '<a href="/category/predictions/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
        new_page = re.sub(r'<a href="/category/news/" class="[^"]*"', '<a href="/category/news/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
    elif page_data['category_slug'] == 'predictions':
        new_page = re.sub(r'<a href="/category/reviews/" class="[^"]*"', '<a href="/category/reviews/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
        new_page = re.sub(r'<a href="/category/predictions/" class="[^"]*"', '<a href="/category/predictions/" class="text-brand-red font-semibold"', new_page)
        new_page = re.sub(r'<a href="/category/news/" class="[^"]*"', '<a href="/category/news/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
    elif page_data['category_slug'] == 'news':
        new_page = re.sub(r'<a href="/category/reviews/" class="[^"]*"', '<a href="/category/reviews/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
        new_page = re.sub(r'<a href="/category/predictions/" class="[^"]*"', '<a href="/category/predictions/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_page)
        new_page = re.sub(r'<a href="/category/news/" class="[^"]*"', '<a href="/category/news/" class="text-brand-red font-semibold"', new_page)
    
    # Replace the article content
    content_pattern = r'<div class="article-content text-lg">.*?<div class="flex items-center justify-between py-6 border-t'
    content_replacement = f'<div class="article-content text-lg">{updated_content}</div>\n\n                <!-- Share -->\n                <div class="flex items-center justify-between py-6 border-t'
    new_page = re.sub(content_pattern, content_replacement, new_page, flags=re.DOTALL)
    
    # Insert TOC if we have one
    if toc_html:
        # Insert after featured image
        new_page = re.sub(r'(<div class="relative mb-8 rounded-2xl overflow-hidden group">.*?</div>)', 
                         r'\1' + toc_html, new_page, flags=re.DOTALL)
    
    return new_page

def main():
    print("=" * 70)
    print("APPLYING PERFECT DESIGN TO ALL PAGES (PRESERVING CONTENT)")
    print("=" * 70)
    
    processed = 0
    skipped = 0
    errors = 0
    
    for filepath in glob.glob('**/*.html', recursive=True):
        # Skip the template page itself and category pages
        if filepath == 'when-bundles-run-out-the-game-doesnt-stop-sportpesa-kenyas-ussd-casino-is-changing-how-kenyans-play.html':
            continue
        if filepath in ('index.html', 'apply_design.py'):
            continue
        if '/category/' in filepath.replace('\\', '/'):
            continue
        
        print(f"\n📄 Processing: {filepath}")
        
        try:
            # Read the current page
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                old_html = f.read()
            
            # Extract its unique content
            page_data = extract_page_content(old_html)
            
            if not page_data['content'] or page_data['content'] == '<p>Content could not be extracted</p>':
                print(f"  ⚠️  Could not extract content, skipping")
                skipped += 1
                continue
            
            # Generate TOC from content
            toc_html, updated_content = generate_table_of_contents(page_data['content'])
            
            # Create new page with perfect design
            new_html = create_page_from_design(page_data, toc_html, updated_content)
            
            # Create backup
            backup_path = filepath + '.design.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(old_html)
            
            # Write new page
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            processed += 1
            print(f"  ✅ Applied design to: {page_data['title'][:60]}...")
            if toc_html:
                print(f"     📚 Added Table of Contents")
            
        except Exception as e:
            errors += 1
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ COMPLETE!")
    print(f"   Pages redesigned: {processed}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors: {errors}")
    print(f"   Backup files created with .design.backup extension")
    print("=" * 70)

if __name__ == '__main__':
    main()
