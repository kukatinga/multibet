#!/usr/bin/env python3
"""
Simple redesign script that copies design from one page to others
"""

import os
import glob
import re

def main():
    print("=" * 60)
    print("SIMPLE REDESIGN SCRIPT")
    print("=" * 60)
    
    # Find all HTML files
    all_files = glob.glob('**/*.html', recursive=True)
    print(f"Found {len(all_files)} HTML files")
    
    if not all_files:
        print("❌ No HTML files found!")
        return
    
    # Use the first HTML file as template
    template_file = all_files[0]
    print(f"Using template: {template_file}")
    
    # Read template
    with open(template_file, 'r', encoding='utf-8', errors='ignore') as f:
        template = f.read()
    
    processed = 0
    errors = 0
    
    for filepath in all_files:
        if filepath == template_file:
            continue
            
        print(f"\nProcessing: {filepath}")
        
        try:
            # Read current file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create backup
            backup = filepath + '.backup'
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else "MULTIBET Article"
            
            # Extract description
            desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
            description = desc_match.group(1) if desc_match else ""
            
            # Extract date
            date_match = re.search(r'<span>([A-Za-z]+ \d{1,2}, \d{4})</span>', content)
            date = date_match.group(1) if date_match else ""
            
            # Extract image
            img_match = re.search(r'<img src="([^"]+)"[^>]*class="[^"]*object-cover[^"]*"', content)
            image = img_match.group(1) if img_match else "https://i.imgur.com/2H9nodm.jpg"
            
            # Extract category
            cat_match = re.search(r'<a href="/category/([^/]+)/"[^>]*>([^<]+)</a>', content)
            if cat_match:
                category_slug = cat_match.group(1)
                category_name = cat_match.group(2)
            else:
                category_slug = "reviews"
                category_name = "Reviews"
            
            # Start with template
            new_content = template
            
            # Replace metadata
            new_content = re.sub(r'<title>.*?\|\s*MULTIBET</title>', f'<title>{title} | MULTIBET</title>', new_content)
            new_content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{description}"', new_content)
            new_content = re.sub(r'<span>([A-Za-z]+ \d{1,2}, \d{4})</span>', f'<span>{date}</span>', new_content)
            new_content = re.sub(r'<img src="[^"]*"[^>]*class="w-full h-auto object-cover', f'<img src="{image}" alt="{title}" class="w-full h-auto object-cover', new_content)
            
            # Replace category
            new_content = re.sub(r'<a href="/category/[^"]*/"[^>]*>([^<]+)</a>', 
                               f'<a href="/category/{category_slug}/" class="inline-flex items-center gap-2 px-4 py-1.5 bg-brand-red/10 text-brand-red rounded-full text-sm font-semibold hover:bg-brand-red hover:text-white transition-all">{category_name}</a>', 
                               new_content)
            
            # Set active navigation
            if category_slug == "reviews":
                new_content = re.sub(r'<a href="/category/reviews/" class="[^"]*"', '<a href="/category/reviews/" class="text-brand-red font-semibold"', new_content)
                new_content = re.sub(r'<a href="/category/predictions/" class="[^"]*"', '<a href="/category/predictions/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_content)
                new_content = re.sub(r'<a href="/category/news/" class="[^"]*"', '<a href="/category/news/" class="text-gray-700 hover:text-brand-red font-medium transition-colors"', new_content)
            
            # Write new file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            processed += 1
            print(f"  ✅ Updated: {title[:50]}...")
            
        except Exception as e:
            errors += 1
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Done! Updated: {processed}, Errors: {errors}")

if __name__ == '__main__':
    main()
