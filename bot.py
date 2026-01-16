import os
import telebot
import redis
import time
from telebot import types  # <--- זה הכלי שיוצר את הכפתורים

# הגדרות חיבור
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
r = redis.Redis(host='my-db', port=6379, decode_responses=True, socket_connect_timeout=5)

# 1. פקודת ההתחלה - יוצרת את הכפתורים
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # יצירת לוח המקשים
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # הגדרת הכפתורים
    btn_status = types.KeyboardButton('📊 סטטוס מערכת')
    btn_reset = types.KeyboardButton('🔄 איפוס מונה')
    
    # הוספת הכפתורים ללוח
    markup.add(btn_status, btn_reset)
    
    bot.reply_to(message, "אהלן רונן! אני מוכן. בחר פעולה מהתפריט למטה:", reply_markup=markup)

# 2. טיפול בלחיצה על "סטטוס מערכת"
@bot.message_handler(func=lambda message: message.text == '📊 סטטוס מערכת')
def status_btn_handler(message):
    try:
        count = r.get('camera_samples') or 0
        timestamp = time.strftime('%H:%M:%S')
        text = f"📊 *סטטוס מצלמות*\nדגימות ב-Redis: {count}\nזמן: {timestamp}"
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת נתונים: {e}")

# 3. טיפול בלחיצה על "איפוס מונה" (בונוס!)
@bot.message_handler(func=lambda message: message.text == '🔄 איפוס מונה')
def reset_btn_handler(message):
    try:
        r.set('camera_samples', 0)
        bot.reply_to(message, "✅ המונה אופס בהצלחה ל-0!")
    except Exception as e:
        bot.reply_to(message, f"שגיאה באיפוס: {e}")

# הפקודה הישנה לגיבוי
# @bot.message_handler(commands=['status'])
# def send_status_cmd(message):
#    status_btn_handler(message)

# 4. פונקציית הדיבאג החדשה - שתולה כאן! 
# היא תדפיס ללוג כל הודעה שלא נתפסה למעלה
@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"DEBUG: Received message: '{message.text}' from user {message.from_user.id}")

print("Checking connection to Telegram...")
try:
    # ניסיון למשוך את פרטי הבוט משרתי טלגרם
    info = bot.get_me()
    print(f"Success! Bot is online: @{info.username}")
except Exception as e:
    # אם הטוקן שגוי או שיש חסימה, זה יודפס כאן
    print(f"ERROR: Connection failed: {e}")

print("Bot with Remote Control buttons is starting...")
bot.infinity_polling(skip_pending=True)

print("Bot is starting to poll...")
try:
    # שימוש ב-polling פשוט עם העלאת שגיאות (none_stop=True)
    bot.polling(none_stop=True, interval=0, timeout=20)
except Exception as e:
    print(f"CRITICAL ERROR during polling: {e}")
