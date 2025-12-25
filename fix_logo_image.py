#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix logo image - replace with working SVG logo
"""

import re

def fix_logo_image(file_path):
    """Replace logo image with working SVG"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find logo div and replace image with SVG
    logo_pattern = r'(<div class="logo">.*?</div>)'
    
    new_logo_html = '''    <div class="logo">
        <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="portGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#003366;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#0066CC;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="60" cy="60" r="55" fill="url(#portGradient)" opacity="0.15"/>
            <!-- Anchor/Ship symbol -->
            <path d="M60 25 L75 45 L90 45 L70 65 L80 90 L60 75 L40 90 L50 65 L30 45 L45 45 Z" fill="url(#portGradient)" stroke="#003366" stroke-width="1.5"/>
            <!-- Circle center -->
            <circle cx="60" cy="60" r="6" fill="#0066CC"/>
            <!-- Waves -->
            <path d="M20 85 Q30 80, 40 85 T60 85 T80 85 T100 85" stroke="#0066CC" stroke-width="2" fill="none" opacity="0.6"/>
            <path d="M25 95 Q35 90, 45 95 T65 95 T85 95 T95 95" stroke="#0066CC" stroke-width="1.5" fill="none" opacity="0.4"/>
            <!-- Text -->
            <text x="60" y="110" font-family="Arial Hebrew, David, Arial" font-size="11" fill="#003366" text-anchor="middle" font-weight="bold">נמל אשדוד</text>
        </svg>
    </div>'''
    
    if re.search(logo_pattern, content, re.DOTALL):
        content = re.sub(logo_pattern, new_logo_html, content, flags=re.DOTALL)
        
        # Also update CSS to work with SVG
        if '.logo img' in content:
            content = content.replace(
                '.logo img {',
                '.logo svg {'
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
    
    print("מתקן לוגו - מחליף ל-SVG שעובד בוודאות...")
    
    for html_file in html_files:
        try:
            if fix_logo_image(html_file):
                print(f"✓ עודכן {html_file}")
            else:
                print(f"  לא נמצא לוגו ב-{html_file}")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם! הלוגו עכשיו SVG שעובד בוודאות.")


