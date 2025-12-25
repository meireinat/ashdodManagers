#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סקריפט להכנת הקבצים לפרסום
יוצר תיקייה עם כל הקבצים הנדרשים לפרסום
"""

import os
import shutil

def prepare_deployment():
    """הכנת קבצים לפרסום"""
    
    # שם התיקייה לפרסום
    deploy_dir = "deploy"
    
    # יצירת תיקייה חדשה
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # רשימת הקבצים להעתקה
    files_to_copy = [
        "presentation_v2.html",
        "בוט הנמל החכם.mp3",
        "asdod_port_logo_official.png"
    ]
    
    # העתקת קבצים
    copied_files = []
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            copied_files.append(file)
            print(f"✓ הועתק: {file}")
        else:
            print(f"✗ לא נמצא: {file}")
    
    # שינוי שם קובץ HTML ל-index.html (אופציונלי)
    html_file = os.path.join(deploy_dir, "presentation_v2.html")
    if os.path.exists(html_file):
        index_file = os.path.join(deploy_dir, "index.html")
        shutil.copy2(html_file, index_file)
        print(f"✓ נוצר גם: index.html")
    
    # יצירת קובץ README
    readme_content = """# מצגת אינטראקטיבית - נמל אשדוד

## קבצים נדרשים:
- presentation_v2.html (או index.html)
- בוט הנמל החכם.mp3
- asdod_port_logo_official.png

## הוראות פרסום:

### GitHub Pages:
1. צור מאגר חדש ב-GitHub
2. העלה את כל הקבצים מהתיקייה deploy
3. לך להגדרות > Pages
4. בחר branch: main, folder: / (root)
5. שמור - הקישור יהיה זמין תוך כמה דקות

### Netlify:
1. לך ל-https://app.netlify.com/drop
2. גרור את כל התיקייה deploy
3. קבל קישור מיידי

### Vercel:
1. התקן: npm i -g vercel
2. בתיקייה deploy: vercel
3. עקוב אחר ההוראות

### Firebase Hosting:
1. התקן: npm i -g firebase-tools
2. בתיקייה deploy: firebase init hosting
3. firebase deploy
"""
    
    readme_path = os.path.join(deploy_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ נוצר: README.md")
    
    print(f"\n✅ הושלם! כל הקבצים נמצאים בתיקייה: {deploy_dir}")
    print(f"\n📁 קבצים שהועתקו ({len(copied_files)}):")
    for file in copied_files:
        print(f"   - {file}")
    
    return deploy_dir

if __name__ == "__main__":
    prepare_deployment()

