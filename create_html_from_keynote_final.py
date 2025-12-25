#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create HTML from Keynote using AppleScript extraction
"""

import subprocess
import re
import html
import json

def extract_keynote_with_applescript(key_file):
    """Extract content using AppleScript"""
    script = f'''
tell application "Keynote"
    activate
    open POSIX file "{key_file}"
    delay 2
    
    set slideCount to count of slides of front document
    set slideData to {{}}
    
    repeat with i from 1 to slideCount
        set slideText to ""
        try
            set slideText to text of slide i of front document
        end try
        set end of slideData to slideText
    end repeat
    
    return slideData
end tell
'''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Parse the result
            output = result.stdout.strip()
            # AppleScript returns list as comma-separated with quotes
            texts = re.findall(r'"([^"]*)"', output)
            return texts
        else:
            print(f"שגיאה: {result.stderr}")
            return []
    except subprocess.TimeoutExpired:
        print("התהליך נמשך יותר מדי זמן")
        return []
    except Exception as e:
        print(f"שגיאה: {e}")
        return []

def organize_slides(texts):
    """Organize texts into slides"""
    slides = []
    
    for text in texts:
        if text.strip():
            # Split by newlines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            slide = {
                'title': lines[0] if lines and len(lines[0]) < 100 else '',
                'body': lines[1:] if len(lines) > 1 else lines
            }
            
            slides.append(slide)
    
    return slides

def create_html_presentation(slides_data, output_file):
    """Create professional HTML presentation"""
    
    html_content = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מצגת - Keynote</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial Hebrew', 'David', 'Gisha', 'Miriam', Arial, sans-serif;
            background: linear-gradient(135deg, #f5f8fa 0%, #ffffff 100%);
            color: #141414;
            direction: rtl;
            overflow: hidden;
            height: 100vh;
        }
        
        .presentation-container {
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .slide-container {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            margin: 20px;
            border-radius: 8px;
            overflow-y: auto;
        }
        
        .slide {
            max-width: 1200px;
            width: 100%;
            padding: 60px;
            background: #ffffff;
            border: 2px solid #dce6f0;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 51, 102, 0.1);
            display: none;
            animation: fadeIn 0.5s ease-in;
        }
        
        .slide.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .slide-title {
            font-size: 48px;
            font-weight: bold;
            color: #003366;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #0066CC;
            text-align: right;
            line-height: 1.3;
        }
        
        .slide-body {
            font-size: 24px;
            color: #141414;
            line-height: 1.8;
            text-align: right;
        }
        
        .slide-body p {
            margin-bottom: 20px;
        }
        
        .controls {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 30px;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .btn {
            background: #003366;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-family: 'Arial Hebrew', Arial, sans-serif;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .btn:hover {
            background: #0066CC;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4);
        }
        
        .btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .slide-counter {
            position: fixed;
            top: 30px;
            left: 30px;
            background: rgba(0, 51, 102, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            z-index: 1000;
        }
        
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: #0066CC;
            transition: width 0.3s ease;
            z-index: 1001;
        }
    </style>
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    <div class="slide-counter" id="slideCounter"></div>
    
    <div class="presentation-container">
        <div class="slide-container">
"""
    
    # Add slides
    for idx, slide_data in enumerate(slides_data):
        slide_class = "active" if idx == 0 else ""
        html_content += f'            <div class="slide {slide_class}" id="slide{idx}">\n'
        
        if slide_data.get('title'):
            html_content += f'                <h1 class="slide-title">{html.escape(slide_data["title"])}</h1>\n'
        
        if slide_data.get('body'):
            html_content += '                <div class="slide-body">\n'
            for paragraph in slide_data['body']:
                if paragraph.strip():
                    html_content += f'                    <p>{html.escape(paragraph)}</p>\n'
            html_content += '                </div>\n'
        else:
            html_content += '                <div class="slide-body">\n'
            html_content += f'                    <p>שקופית {idx + 1}</p>\n'
            html_content += '                </div>\n'
        
        html_content += '            </div>\n'
    
    html_content += """        </div>
    </div>
    
    <div class="controls">
        <button class="btn" id="prevBtn" onclick="previousSlide()">← הקודם</button>
        <button class="btn" id="nextBtn" onclick="nextSlide()">הבא →</button>
    </div>
    
    <script>
        const slides = document.querySelectorAll('.slide');
        let currentSlide = 0;
        const totalSlides = slides.length;
        
        function updateSlide() {
            slides.forEach((slide, index) => {
                slide.classList.remove('active');
                if (index === currentSlide) {
                    slide.classList.add('active');
                }
            });
            
            document.getElementById('slideCounter').textContent = `${currentSlide + 1} / ${totalSlides}`;
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
            
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
        }
        
        function nextSlide() {
            if (currentSlide < totalSlides - 1) {
                currentSlide++;
                updateSlide();
            }
        }
        
        function previousSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                updateSlide();
            }
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                nextSlide();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                previousSlide();
            } else if (e.key === 'Home') {
                currentSlide = 0;
                updateSlide();
            } else if (e.key === 'End') {
                currentSlide = totalSlides - 1;
                updateSlide();
            }
        });
        
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            const diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    nextSlide();
                } else {
                    previousSlide();
                }
            }
        });
        
        updateSlide();
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ קובץ HTML נוצר: {output_file}")

if __name__ == "__main__":
    import os
    
    key_file = os.path.abspath("2.key")
    output_file = "presentation_2key.html"
    
    print(f"מחלץ תוכן מ-Keynote...")
    print("שים לב: Keynote יפתח אוטומטית")
    
    texts = extract_keynote_with_applescript(key_file)
    
    if texts:
        print(f"נמצאו {len(texts)} שקופיות")
        slides_data = organize_slides(texts)
        create_html_presentation(slides_data, output_file)
        print("✓ הושלם בהצלחה!")
    else:
        print("לא נמצא תוכן. ודא ש-Keynote מותקן וניתן לגשת אליו.")


