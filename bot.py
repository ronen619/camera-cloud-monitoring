import os
import telebot
import redis
import time
from telebot import types  # <--- זה הכלי שיוצר את הכפתורים

# הגדרות חיבור
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
r = redis.Redis(host='my-db', port=6379, decode_responses=True, socket_connect_timeout=1, socket_timeout=1)

try:
    r.ping()
    print("✅ Successfully connected to Redis")
except Exception as e:
    print(f"⚠️ Redis connection failed, but bot will continue: {e}")
    
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

# 4. פונקציית הדיבאג החדשה - שתולה כאן! 
# היא תדפיס ללוג כל הודעה שלא נתפסה למעלה
@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"DEBUG: Received message: {message.text}", flush=True)
   
import threading

# פונקציה שרצה ברקע ובודקת את Redis
def monitor_redis_changes():
    # הגדרת ה-ID שלך (מהלוגים המוקדמים)
    MY_CHAT_ID = 770737566 
    
    # אתחול המונה האחרון שהכרנו
    try:
        last_count = int(r.get('camera_samples') or 0)
    except:
        last_count = 0
        
    print(f"📢 Monitoring thread started. Initial count: {last_count}", flush=True)

    while True:
        try:
            # שליפת המונה הנוכחי
            current_count = int(r.get('camera_samples') or 0)

            # אם המונה גדל - יש דגימה חדשה!
            if current_count > last_count:
                diff = current_count - last_count
                message = f"📸 *התראה: זוהתה דגימה חדשה!*\nמספר דגימות נוספות: {diff}\nסה''כ ב-Redis: {current_count}"
                
                # שליחת הודעה יזומה מהבוט אליך
                bot.send_message(MY_CHAT_ID, message, parse_mode='Markdown')
                
                # עדכון המונה האחרון
                last_count = current_count
            
            # המתנה של 5 שניות בין בדיקה לבדיקה
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠️ Monitor Error: {e}", flush=True)
            time.sleep(10)

# הפעלת התהליך ברקע לפני שמתחילים את ה-Polling
monitor_thread = threading.Thread(target=monitor_redis_changes, daemon=True)
monitor_thread.start()


# בדיקת חיבור לפני שמתחילים
print("Checking connection to Telegram...", flush=True)
try:
    info = bot.get_me()
    print(f"✅ Success! Bot is online: @{info.username}", flush=True)
except Exception as e:
    print(f"❌ ERROR: Connection failed: {e}", flush=True)

print("🚀 Bot is starting to poll now...", flush=True)

try:
    # infinity_polling דואג שהבוט ינסה להתחבר מחדש גם אם יש שגיאת רשת
    # skip_pending=True יגרום לבוט להתעלם מכל הודעות העבר ה"תקועות" ולהגיב רק להודעות חדשות מהרגע הזה
    bot.infinity_polling(skip_pending=True)
except Exception as e:
    print(f"⚠️ CRITICAL ERROR: {e}", flush=True)
