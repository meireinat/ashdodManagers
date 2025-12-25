#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update logo in all HTML files to use the real Ashdod Port logo
"""

import re
import os

def update_logo_in_html(file_path, logo_url):
    """Update logo in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if logo exists
    if 'class="logo"' not in content:
        print(f"  לא נמצא לוגו ב-{file_path}")
        return False
    
    # Replace SVG logo with image logo
    # Find the logo div and replace its content
    logo_pattern = r'(<div class="logo">.*?</div>)'
    
    new_logo_html = f'''    <div class="logo">
        <img src="{logo_url}" alt="לוגו נמל אשדוד" />
    </div>'''
    
    if re.search(logo_pattern, content, re.DOTALL):
        content = re.sub(logo_pattern, new_logo_html, content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    else:
        print(f"  לא נמצא לוגו SVG ב-{file_path}")
        return False

if __name__ == "__main__":
    html_files = [
        "presentation_v2.html",
        "presentation_2key.html",
        "presentation_v1.html",
        "presentation.html"
    ]
    
    # Use Wikimedia Commons direct URL (always use online version for reliability)
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/%D7%9C%D7%95%D7%92%D7%95_%D7%A0%D7%9E%D7%9C_%D7%90%D7%A9%D7%93%D7%95%D7%93.jpg/512px-%D7%9C%D7%95%D7%92%D7%95_%D7%A0%D7%9E%D7%9C_%D7%90%D7%A9%D7%93%D7%95%D7%93.jpg"
    print(f"משתמש בלוגו מ-Wikimedia Commons")
    
    print("\nמעדכן לוגו בכל קבצי ה-HTML...")
    
    for html_file in html_files:
        try:
            if update_logo_in_html(html_file, logo_url):
                print(f"✓ עודכן לוגו ב-{html_file}")
            else:
                print(f"  דולג על {html_file}")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם!")

