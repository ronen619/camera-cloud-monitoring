FROM python:3.9-slim

# יצירת תיקייה עבור הפרויקט בתוך המכולה
WORKDIR /app

# 1. העתקת רשימת הקניות (requirements.txt) והתקנה שלהן
# זה יתקין גם את flask, גם את redis וגם את הספריה של טלגרם
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. העתקת כל הקבצים של הפרויקט (כולל app.py ו-bot.py) לתוך השרת
COPY . .

# ברירת מחדל (ה-docker-compose שלנו כבר יודע להחליף את זה לכל שירות)
CMD ["python", "app.py"]
