# הוראות פרסום ל-GitHub Pages

## שלב 1: יצירת מאגר ב-GitHub

1. לך ל: https://github.com/new
2. שם המאגר: `ניהול-תרגיל-מסכם` (או כל שם אחר)
3. בחר: **Public**
4. **אל תסמן** "Initialize with README"
5. לחץ על "Create repository"

## שלב 2: חיבור המאגר המקומי ל-GitHub

העתק והדבק את הפקודות הבאות בטרמינל:

```bash
cd "/Users/smartpo/development/projects/ניהול תרגיל מסכם"

# החלף [שם-משתמש] בשם המשתמש שלך ב-GitHub
git remote add origin https://github.com/[שם-משתמש]/ניהול-תרגיל-מסכם.git

# דחיפה ל-GitHub
git push -u origin main
```

## שלב 3: הפעלת GitHub Pages

1. לך למאגר ב-GitHub: `https://github.com/[שם-משתמש]/ניהול-תרגיל-מסכם`
2. לחץ על **Settings** (בתפריט העליון)
3. גלול למטה ל-**Pages** (בתפריט השמאלי)
4. תחת **Source**:
   - בחר **Branch: main**
   - בחר **Folder: / (root)**
5. לחץ על **Save**
6. המתן 1-2 דקות

## שלב 4: גישה למצגת

הקישור יהיה:
```
https://[שם-משתמש].github.io/ניהול-תרגיל-מסכם/deploy/presentation_v2.html
```

או:
```
https://[שם-משתמש].github.io/ניהול-תרגיל-מסכם/deploy/index.html
```

## קבצים שפורסמו:

- ✅ `deploy/presentation_v2.html` - המצגת הראשית
- ✅ `deploy/index.html` - דף פתיחה (אותה מצגת)
- ✅ `deploy/בוט הנמל החכם.mp3` - מוזיקת רקע
- ✅ `deploy/asdod_port_logo_official.png` - לוגו נמל אשדוד

## פתרון בעיות:

### אם יש שגיאה ב-push:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### אם צריך לעדכן קבצים:
```bash
git add .
git commit -m "עדכון קבצים"
git push
```

### אם צריך לשנות את שם המאגר:
```bash
git remote set-url origin https://github.com/[שם-משתמש]/[שם-מאגר-חדש].git
git push -u origin main
```

