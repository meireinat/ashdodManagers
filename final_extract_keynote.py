#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final attempt to extract content from Keynote automatically
"""

import subprocess
import os
import html

def extract_keynote_final(key_file):
    """Extract content using improved AppleScript"""
    abs_path = os.path.abspath(key_file)
    
    script = f'''
tell application "Keynote"
    activate
    open POSIX file "{abs_path}"
    delay 5
    
    set slideCount to count of slides of front document
    set slideContents to {{}}
    
    repeat with slideNum from 1 to slideCount
        set slideText to ""
        try
            -- Try to get all text from slide
            set slideText to text of slide slideNum of front document
        end try
        
        -- If empty, try getting from text boxes
        if slideText is "" then
            try
                set textItems to every text item of slide slideNum of front document
                repeat with textItem in textItems
                    set slideText to slideText & return & (text of textItem as string)
                end repeat
            end try
        end if
        
        set end of slideContents to slideText
    end repeat
    
    return slideContents
end tell
'''
    
    try:
        print("מחלץ תוכן מהמצגת...")
        print("אנא המתן - Keynote פותח את המצגת...")
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"תוצאה: {len(output)} תווים")
            
            # Parse the output
            # AppleScript returns items separated by commas or newlines
            texts = []
            if output:
                # Split by return (newline in AppleScript)
                parts = output.split('\n')
                for part in parts:
                    part = part.strip()
                    if part and part != ',':
                        # Remove quotes if present
                        part = part.strip('"').strip("'")
                        if part:
                            texts.append(part)
            
            return texts
        else:
            print(f"שגיאה: {result.stderr}")
            return []
    except Exception as e:
        print(f"שגיאה: {e}")
        return []

def create_html_with_content(texts, output_file):
    """Create HTML with extracted content"""
    
    slides = []
    for i, text in enumerate(texts):
        if text and text.strip():
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            slide = {
                'title': lines[0] if lines and len(lines[0]) < 100 else f'שקופית {i+1}',
                'body': lines[1:] if len(lines) > 1 else lines
            }
            slides.append(slide)
        else:
            slides.append({'title': f'שקופית {i+1}', 'body': []})
    
    # Use the same HTML template from before
    html_content = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מצגת אינטראקטיבית</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial Hebrew', 'David', 'Gisha', 'Miriam', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #141414;
            direction: rtl;
            overflow: hidden;
            height: 100vh;
        }}
        
        .presentation-wrapper {{
            width: 100%;
            height: 100vh;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .presentation-container {{
            width: 95%;
            height: 90vh;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        
        .slide-container {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px;
            overflow-y: auto;
        }}
        
        .slide {{
            max-width: 1000px;
            width: 100%;
            padding: 50px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            display: none;
            opacity: 0;
            transform: scale(0.95);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .slide.active {{
            display: block;
            opacity: 1;
            transform: scale(1);
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            0% {{ opacity: 0; transform: translateX(50px) scale(0.95); }}
            100% {{ opacity: 1; transform: translateX(0) scale(1); }}
        }}
        
        .slide-title {{
            font-size: 52px;
            font-weight: bold;
            background: linear-gradient(135deg, #003366 0%, #0066CC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 40px;
            padding-bottom: 25px;
            border-bottom: 4px solid #0066CC;
            text-align: right;
        }}
        
        .slide-body {{
            font-size: 26px;
            color: #2c3e50;
            line-height: 2;
            text-align: right;
        }}
        
        .slide-body p {{
            margin-bottom: 25px;
            padding-right: 20px;
            transition: all 0.3s ease;
        }}
        
        .slide-body p:hover {{
            padding-right: 30px;
            border-right: 3px solid #0066CC;
        }}
        
        .controls {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px 40px;
            border-radius: 50px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .btn {{
            background: linear-gradient(135deg, #003366 0%, #0066CC 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            font-family: 'Arial Hebrew', Arial, sans-serif;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0, 51, 102, 0.3);
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
        }}
        
        .btn:disabled {{
            background: #cccccc;
            cursor: not-allowed;
        }}
        
        .slide-counter {{
            position: fixed;
            top: 30px;
            left: 30px;
            background: linear-gradient(135deg, #003366 0%, #0066CC 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            z-index: 1000;
        }}
        
        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 5px;
            background: linear-gradient(90deg, #0066CC, #003366);
            transition: width 0.4s ease;
            z-index: 1001;
        }}
    </style>
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    <div class="slide-counter" id="slideCounter"></div>
    
    <div class="presentation-wrapper">
        <div class="presentation-container">
            <div class="slide-container">
"""
    
    for idx, slide in enumerate(slides):
        slide_class = "active" if idx == 0 else ""
        html_content += f'                <div class="slide {slide_class}" id="slide{idx}">\n'
        html_content += f'                    <h1 class="slide-title">{html.escape(slide["title"])}</h1>\n'
        html_content += '                    <div class="slide-body">\n'
        for para in slide['body']:
            html_content += f'                        <p>{html.escape(para)}</p>\n'
        html_content += '                    </div>\n'
        html_content += '                </div>\n'
    
    html_content += """            </div>
        </div>
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
                    setTimeout(() => slide.classList.add('active'), 50);
                }
            });
            document.getElementById('slideCounter').textContent = `${currentSlide + 1} / ${totalSlides}`;
            document.getElementById('progressBar').style.width = `${((currentSlide + 1) / totalSlides) * 100}%`;
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
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
                e.preventDefault();
                nextSlide();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                e.preventDefault();
                previousSlide();
            }
        });
        
        updateSlide();
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ דף HTML נוצר: {output_file}")

if __name__ == "__main__":
    key_file = "2.key"
    output_file = "presentation_2key.html"
    
    texts = extract_keynote_final(key_file)
    
    if texts:
        print(f"\n✓ נמצאו {len(texts)} שקופיות!")
        for i, text in enumerate(texts[:3]):
            print(f"  שקופית {i+1}: {text[:60]}...")
        create_html_with_content(texts, output_file)
    else:
        print("\nלא הצלחתי לחלץ את התוכן אוטומטית.")
        print("\nהפתרון הכי פשוט:")
        print("1. פתח את המצגת 2.key ב-Keynote")
        print("2. בחר File > Export To > PowerPoint")
        print("3. שמור את הקובץ")
        print("4. אני אחלץ את התוכן מהקובץ PowerPoint שיצרת")
        
        # Create empty template
        create_html_with_content([], output_file)


