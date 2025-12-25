#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all HTML files with real Ashdod Port logo from Wikimedia
"""

import re
import os

def update_logo_with_image(file_path, logo_path):
    """Update logo to use real image"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find logo div and replace SVG with image
    logo_pattern = r'(<div class="logo">.*?</div>)'
    
    # Use Wikimedia Commons direct URL (always use online version)
    # Try different possible URLs
    logo_src = "https://upload.wikimedia.org/wikipedia/commons/4/4a/%D7%9C%D7%95%D7%92%D7%95_%D7%A0%D7%9E%D7%9C_%D7%90%D7%A9%D7%93%D7%95%D7%93.jpg"
    
    new_logo_html = f'''    <div class="logo">
        <img src="{logo_src}" alt="לוגו נמל אשדוד" />
    </div>'''
    
    if re.search(logo_pattern, content, re.DOTALL):
        content = re.sub(logo_pattern, new_logo_html, content, flags=re.DOTALL)
        
        # Update CSS to work with img instead of svg
        if '.logo svg' in content:
            content = content.replace('.logo svg', '.logo img')
            # Add border-radius back
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
    
    logo_file = "asdod_port_logo_real.jpg"
    
    print("מעדכן לוגו אמיתי של נמל אשדוד...")
    
    for html_file in html_files:
        try:
            if update_logo_with_image(html_file, logo_file):
                print(f"✓ עודכן {html_file}")
            else:
                print(f"  לא נמצא לוגו ב-{html_file}")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם!")

