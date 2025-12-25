#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix logo CSS in all HTML files - change img to svg
"""

import re

def fix_logo_css(file_path):
    """Fix logo CSS to work with SVG"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace .logo img with .logo svg
    if '.logo img' in content:
        content = content.replace('.logo img', '.logo svg')
        # Remove border-radius as it's not needed for SVG
        content = re.sub(r'border-radius:\s*8px;?\s*', '', content)
        
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


