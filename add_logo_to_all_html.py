#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Ashdod Port logo to all HTML presentation files
"""

import re

def add_logo_to_html(file_path):
    """Add logo to HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if logo already exists
    if 'class="logo"' in content:
        print(f"  לוגו כבר קיים ב-{file_path}")
        return False
    
    # Add logo CSS before closing </style>
    logo_css = """
        .logo {
            position: fixed;
            top: 30px;
            right: 30px;
            z-index: 1000;
            width: 120px;
            height: auto;
            opacity: 0.9;
            transition: all 0.3s ease;
        }
        
        .logo:hover {
            opacity: 1;
            transform: scale(1.05);
        }
        
        .logo svg {
            filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.2));
        }
"""
    
    # Add logo HTML after <body>
    logo_html = """
    <div class="logo">
        <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <circle cx="60" cy="60" r="55" fill="#003366" opacity="0.1"/>
            <path d="M60 20 L80 50 L100 50 L75 70 L85 100 L60 80 L35 100 L45 70 L20 50 L40 50 Z" fill="#003366"/>
            <circle cx="60" cy="60" r="8" fill="#0066CC"/>
            <text x="60" y="105" font-family="Arial Hebrew" font-size="12" fill="#003366" text-anchor="middle" font-weight="bold">נמל אשדוד</text>
        </svg>
    </div>
"""
    
    # Add CSS
    if '</style>' in content:
        content = content.replace('</style>', logo_css + '\n    </style>')
    
    # Add HTML - find body tag and add after it
    body_pattern = r'(<body[^>]*>)'
    if re.search(body_pattern, content):
        # Add after body tag, before first div
        content = re.sub(
            body_pattern,
            r'\1' + logo_html,
            content,
            count=1
        )
    else:
        # Fallback - add after <body>
        content = content.replace('<body>', '<body>' + logo_html)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    html_files = [
        "presentation_v2.html",
        "presentation_2key.html",
        "presentation_v1.html",
        "presentation.html"
    ]
    
    print("מוסיף לוגו נמל אשדוד לכל קבצי ה-HTML...")
    
    for html_file in html_files:
        try:
            if add_logo_to_html(html_file):
                print(f"✓ נוסף לוגו ל-{html_file}")
            else:
                print(f"  דולג על {html_file} (כבר קיים)")
        except Exception as e:
            print(f"  שגיאה ב-{html_file}: {e}")
    
    print("\n✓ הושלם!")


