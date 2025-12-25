#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all logos to use official Ashdod Port logo
"""

import re

def fix_logo(file_path):
    """Fix logo in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace any logo img src
    # Replace Wikimedia URL or any other URL with local file
    patterns = [
        (r'src="https://upload\.wikimedia\.org[^"]*"', 'src="asdod_port_logo_official.png"'),
        (r'src="https://www\.ashdodport\.co\.il[^"]*logo[^"]*"', 'src="asdod_port_logo_official.png"'),
        (r'src="asdod_port_logo[^"]*"', 'src="asdod_port_logo_official.png"'),
    ]
    
    changed = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changed = True
    
    # Also fix the div structure if needed
    if '<div class="logo">' in content and '            <div class="logo">' in content:
        content = content.replace('            <div class="logo">', '    <div class="logo">')
    
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

if __name__ == "__main__":
    html_files = [
        "presentation_v2.html",
        "presentation_2key.html",
        "presentation_v1.html",
        "presentation.html"
    ]
    
    print("מתקן לוגו בכל הקבצים...")
    
    for html_file in html_files:
        try:
            if fix_logo(html_file):
                print(f"✓ תוקן {html_file}")
            else:
                print(f"  {html_file} כבר תקין")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם!")


