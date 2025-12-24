#!/bin/bash
# סקריפט לפרסום ל-GitHub

echo "🚀 מתחיל תהליך פרסום ל-GitHub..."
echo ""

# בדיקה אם יש remote
if git remote | grep -q origin; then
    echo "✓ Remote כבר קיים"
    git remote -v
else
    echo "⚠️  אין remote מוגדר"
    echo ""
    echo "אנא צור מאגר חדש ב-GitHub:"
    echo "1. לך ל: https://github.com/new"
    echo "2. צור מאגר חדש (למשל: ניהול-תרגיל-מסכם)"
    echo "3. אל תסמן 'Initialize with README'"
    echo "4. העתק את הפקודה הבאה:"
    echo ""
    echo "   git remote add origin https://github.com/[שם-משתמש]/[שם-מאגר].git"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

# דחיפה ל-GitHub
echo ""
echo "📤 דוחף קבצים ל-GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ הצלחה! המאגר פורסם ל-GitHub"
    echo ""
    echo "🌐 להפעלת GitHub Pages:"
    echo "1. לך ל-GitHub > Settings > Pages"
    echo "2. בחר branch: main"
    echo "3. בחר folder: / (root)"
    echo "4. שמור"
    echo ""
    echo "הקישור יהיה: https://[שם-משתמש].github.io/[שם-מאגר]/deploy/"
else
    echo ""
    echo "❌ שגיאה בדחיפה. בדוק את ההגדרות."
fi

