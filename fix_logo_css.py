#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix logo CSS in all HTML files - remove unused .logo-text style
"""

import re

def fix_logo_css(file_path):
    """Remove unused logo-text CSS"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove .logo-text CSS if exists
    logo_text_pattern = r'\.logo-text\s*\{[^}]*\}'
    if re.search(logo_text_pattern, content):
        content = re.sub(logo_text_pattern, '', content)
        
        # Also ensure .logo img has border-radius
        if '.logo img' in content and 'border-radius' not in content.split('.logo img')[1].split('}')[0]:
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
    
    print("מתקן CSS של לוגו...")
    
    for html_file in html_files:
        try:
            if fix_logo_css(html_file):
                print(f"✓ תוקן {html_file}")
            else:
                print(f"  {html_file} כבר תקין")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם!")


