#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all HTML files with official Ashdod Port logo from their website
"""

import re
import os

def update_logo_official(file_path):
    """Update logo to use official logo from Ashdod Port website"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find logo div and replace with official logo
    logo_pattern = r'(<div class="logo">.*?</div>)'
    
    # Use official logo - try local file first, then website URL
    logo_file = "asdod_port_logo_official.png"
    if os.path.exists(logo_file):
        logo_url = logo_file
    else:
        logo_url = "https://www.ashdodport.co.il/_catalogs/masterpage/AshdodPort/images/logo_big.png"
    
    new_logo_html = f'''    <div class="logo">
        <img src="{logo_url}" alt="לוגו נמל אשדוד" />
    </div>'''
    
    if re.search(logo_pattern, content, re.DOTALL):
        content = re.sub(logo_pattern, new_logo_html, content, flags=re.DOTALL)
        
        # Update CSS to work with img
        if '.logo svg' in content:
            content = content.replace('.logo svg', '.logo img')
            # Add border-radius if not exists
            if 'border-radius' not in content.split('.logo img')[1].split('}')[0]:
                content = content.replace(
                    '.logo img {',
                    '.logo img {\n            border-radius: 8px;'
                )
        
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
    
    print("מעדכן לוגו רשמי של נמל אשדוד מהאתר...")
    
    for html_file in html_files:
        try:
            if update_logo_official(html_file):
                print(f"✓ עודכן {html_file}")
            else:
                print(f"  לא נמצא לוגו ב-{html_file}")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם! הלוגו הרשמי מהאתר של נמל אשדוד נוסף.")

