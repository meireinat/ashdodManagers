#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Keynote to PDF/PPTX and extract content
"""

import subprocess
import os

def export_keynote_to_pdf(key_file):
    """Export Keynote to PDF using AppleScript"""
    abs_path = os.path.abspath(key_file)
    pdf_path = abs_path.replace('.key', '.pdf')
    
    script = f'''
tell application "Keynote"
    activate
    open POSIX file "{abs_path}"
    delay 3
    
    set pdfPath to POSIX file "{pdf_path}"
    export front document as "PDF" to pdfPath
    delay 2
    close front document
end tell
'''
    
    try:
        print("מייצא את המצגת ל-PDF...")
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"✓ הייצוא הושלם: {pdf_path}")
            return pdf_path
        else:
            print(f"שגיאה: {result.stderr}")
            return None
    except Exception as e:
        print(f"שגיאה: {e}")
        return None

if __name__ == "__main__":
    key_file = "2.key"
    pdf_file = export_keynote_to_pdf(key_file)
    
    if pdf_file and os.path.exists(pdf_file):
        print(f"\n✓ קובץ PDF נוצר: {pdf_file}")
        print("עכשיו אפשר לחלץ את התוכן מה-PDF")
    else:
        print("\nלא הצלחתי לייצא ל-PDF")
        print("\nאפשרות אחרת:")
        print("1. פתח את המצגת ב-Keynote")
        print("2. בחר File > Export To > PowerPoint או PDF")
        print("3. שמור את הקובץ")
        print("4. אני אחלץ את התוכן מהקובץ שיצרת")


