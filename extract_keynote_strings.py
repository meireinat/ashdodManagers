#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract text from Keynote using strings command and create HTML
"""

import subprocess
import re
import html

def extract_text_with_strings(key_file):
    """Extract text using macOS strings command"""
    try:
        result = subprocess.run(['strings', key_file], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8',
                              errors='ignore')
        
        all_text = result.stdout
        
        # Filter Hebrew text
        hebrew_pattern = re.compile(r'[א-ת][א-ת\s\w\.,:;!?()\-•]*')
        hebrew_texts = hebrew_pattern.findall(all_text)
        
        # Remove duplicates and short strings
        unique_texts = []
        seen = set()
        for text in hebrew_texts:
            text = text.strip()
            if len(text) > 3 and text not in seen:
                seen.add(text)
                unique_texts.append(text)
        
        return unique_texts
        
    except Exception as e:
        print(f"שגיאה בחילוץ טקסט: {e}")
        return []

def organize_slides(texts):
    """Organize texts into slides"""
    slides = []
    
    # Try to identify slide boundaries
    # Look for patterns that might indicate slide titles
    current_slide = {'title': '', 'body': []}
    
    for text in texts:
        # If text is short and looks like a title
        if len(text) < 100 and not current_slide['title']:
            current_slide['title'] = text
        else:
            current_slide['body'].append(text)
            
            # If we have enough content, start a new slide
            if len(current_slide['body']) >= 5:
                slides.append(current_slide)
                current_slide = {'title': '', 'body': []}
    
    # Add last slide
    if current_slide['title'] or current_slide['body']:
        slides.append(current_slide)
    
    # If we don't have enough slides, split by content
    if len(slides) < 3:
        slides = []
        for i, text in enumerate(texts):
            if i % 5 == 0:
                slides.append({'title': text if len(text) < 100 else '', 'body': []})
            else:
                if slides:
                    slides[-1]['body'].append(text)
    
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
            for paragraph in slide_data['body'][:10]:  # Limit to 10 paragraphs per slide
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
    key_file = "2.key"
    output_file = "presentation_2key.html"
    
    print(f"מחלץ טקסט מ-{key_file}...")
    texts = extract_text_with_strings(key_file)
    
    print(f"נמצאו {len(texts)} מחרוזות טקסט")
    
    if texts:
        print("\nדוגמאות לטקסט שנמצא:")
        for i, text in enumerate(texts[:10]):
            print(f"  {i+1}. {text[:80]}...")
        
        slides_data = organize_slides(texts)
        print(f"\nנוצרו {len(slides_data)} שקופיות")
        create_html_presentation(slides_data, output_file)
    else:
        print("לא נמצא טקסט. נסה לייצא את המצגת ל-PDF או PowerPoint תחילה.")


