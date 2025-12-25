#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract content from Keynote (.key) file and create HTML presentation
Keynote files are zip archives containing XML files
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import html

def extract_keynote_content(key_file):
    """Extract text content from Keynote file"""
    slides_data = []
    
    try:
        # Keynote files are zip archives
        with zipfile.ZipFile(key_file, 'r') as zip_ref:
            # List all files
            file_list = zip_ref.namelist()
            
            # Look for preview or data files
            print("מחפש קבצי תוכן...")
            
            # Try to find slide data
            for file_name in file_list:
                if 'preview' in file_name.lower() or 'data' in file_name.lower():
                    print(f"  נמצא: {file_name}")
            
            # Extract and parse index file
            try:
                index_data = zip_ref.read('Index/Document.iwa')
                print("  נמצא קובץ Index/Document.iwa")
            except:
                pass
            
            # Try to extract text from preview
            try:
                preview_data = zip_ref.read('preview.jpg')
                print("  נמצא תמונה preview")
            except:
                pass
            
            # Look for XML files
            xml_files = [f for f in file_list if f.endswith('.xml') or f.endswith('.iwa')]
            print(f"  נמצאו {len(xml_files)} קבצי XML/IWA")
            
            # Try to read slide data
            # Keynote stores slides in Index/Slide.iwa files
            slide_files = [f for f in file_list if 'Slide' in f and f.endswith('.iwa')]
            print(f"  נמצאו {len(slide_files)} קבצי שקופיות")
            
            # For now, return empty structure - we'll need to parse the binary format
            # Keynote .iwa files are in a proprietary binary format
            
    except Exception as e:
        print(f"שגיאה בקריאת הקובץ: {e}")
        return []
    
    return slides_data

def create_html_from_keynote(key_file, output_file):
    """Create HTML from Keynote file"""
    print(f"מעבד קובץ Keynote: {key_file}")
    
    # Try alternative approach - use command line tools if available
    # On macOS, we can try to export or use textutil
    
    # For now, create a template HTML that can be filled manually
    # or we can try to use macOS automation
    
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
            <div class="slide active" id="slide0">
                <h1 class="slide-title">טוען תוכן...</h1>
                <div class="slide-body">
                    <p>מעבד את קובץ Keynote...</p>
                </div>
            </div>
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
            }
        });
        
        updateSlide();
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"נוצר קובץ HTML בסיסי: {output_file}")
    print("הערה: קובצי Keynote דורשים כלים מיוחדים לחילוץ תוכן")
    print("נסה לייצא את המצגת ל-PDF או PowerPoint תחילה")

if __name__ == "__main__":
    import sys
    
    key_file = "2.key"
    output_file = "presentation_2key.html"
    
    # Try to extract content
    slides_data = extract_keynote_content(key_file)
    
    # Create HTML
    create_html_from_keynote(key_file, output_file)


