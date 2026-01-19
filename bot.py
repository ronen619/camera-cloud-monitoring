import os
import telebot
import redis
import time
import threading
from telebot import types

# הגדרות חיבור
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
r = redis.Redis(host='my-db', port=6379, decode_responses=True, socket_connect_timeout=5, socket_timeout=5)

try:
    r.ping()
    print("✅ Successfully connected to Redis")
except Exception as e:
    print(f"⚠️ Redis connection failed, but bot will continue: {e}")

# --- Handlers ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_status = types.KeyboardButton('📊 סטטוס מערכת')
    btn_reset = types.KeyboardButton('🔄 איפוס מונה')
    # --- עדכון 2.א: הוספת הכפתור החדש ---
    btn_history = types.KeyboardButton('📋 5 דגימות אחרונות')
    
    # הוספת שלושת הכפתורים לממשק
    markup.add(btn_status, btn_reset, btn_history)
    bot.reply_to(message, "אהלן רונן! אני מוכן. בחר פעולה מהתפריט למטה:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📊 סטטוס מערכת')
def status_btn_handler(message):
    try:
        count = r.get('camera_samples') or 0
        timestamp = time.strftime('%H:%M:%S')
        text = f"📊 *סטטוס מצלמות*\nדגימות ב-Redis: {count}\nזמן: {timestamp}"
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת נתונים: {e}")

@bot.message_handler(func=lambda message: message.text == '🔄 איפוס מונה')
def reset_btn_handler(message):
    try:
        r.set('camera_samples', 0)
        # איפוס גם של רשימת ההיסטוריה ב-Redis
        r.delete('camera_history')
        bot.reply_to(message, "✅ המונה וההיסטוריה אופסו בהצלחה ל-0!")
    except Exception as e:
        bot.reply_to(message, f"שגיאה באיפוס: {e}")

# --- עדכון 2.ב: הוספת ה-Handler של ההיסטוריה ---
@bot.message_handler(func=lambda message: message.text == '📋 5 דגימות אחרונות')
def history_btn_handler(message):
    try:
        # שליפת 5 האיברים האחרונים שהסימולטור הכניס לרשימה
        history = r.lrange('camera_history', 0, 4)
        
        if not history:
            bot.reply_to(message, "אין עדיין דגימות רשומות בהיסטוריה.")
            return

        text = "📸 *היסטוריית דגימות אחרונות:*\n\n"
        for i, ts in enumerate(history, 1):
            text += f"{i}. 🕒 `{ts}`\n"
            
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת היסטוריה: {e}")

@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"DEBUG: Received message: {message.text}", flush=True)

# --- Background Monitor ---

def monitor_redis_changes():
    MY_CHAT_ID = 770737566 
    THRESHOLD = 10 
    INTERVAL = 30 # בדיקה כל חצי דקה כדי לראות תוצאות מהר יותר
    
    try:
        last_count = int(r.get('camera_samples') or 0)
    except:
        last_count = 0
        
    print(f"📢 MONITOR START: Initial count is {last_count}. Waiting for {last_count + THRESHOLD}...", flush=True)

    while True:
        try:
            current_count = int(r.get('camera_samples') or 0)
            diff = current_count - last_count
            
            # השורה הזו היא ה"עיניים" שלנו בתוך הטרמינל
            print(f"🔍 [DEBUG] Current: {current_count}, Last: {last_count}, Diff: {diff} (Target: {THRESHOLD})", flush=True)

            if diff >= THRESHOLD:
                print(f"🔔 THRESHOLD REACHED! Sending message to {MY_CHAT_ID}", flush=True)
                message = f"🔔 *סיכום דגימות חדשות*\nנוספו: {diff} דגימות\nסה''כ בשרת: {current_count}"
                bot.send_message(MY_CHAT_ID, message, parse_mode='Markdown')
                last_count = current_count
            
            time.sleep(INTERVAL) 
        except Exception as e:
            print(f"⚠️ Monitor Error: {e}", flush=True)
            time.sleep(10)

# --- Startup ---

print("🚀 Starting Background Monitor...", flush=True)
monitor_thread = threading.Thread(target=monitor_redis_changes, daemon=True)
monitor_thread.start()

print("🚀 Starting Bot Polling...", flush=True)
try:
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
except Exception as e:
    print(f"❌ Polling crashed: {e}", flush=True)