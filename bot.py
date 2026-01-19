import os
import telebot
import redis
import time
import threading
from telebot import types

# הגדרות חיבור - הגדלנו מעט את ה-Timeout ליציבות
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
    markup.add(btn_status, btn_reset)
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
        bot.reply_to(message, "✅ המונה אופס בהצלחה ל-0!")
    except Exception as e:
        bot.reply_to(message, f"שגיאה באיפוס: {e}")

@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"DEBUG: Received message: {message.text}", flush=True)

# --- Background Monitor ---

def monitor_redis_changes():
    MY_CHAT_ID = 770737566 
    THRESHOLD = 10 
    INTERVAL = 60 
    
    try:
        last_count = int(r.get('camera_samples') or 0)
    except:
        last_count = 0
        
    print(f"📢 Monitor updated: Alert every {THRESHOLD} samples, checking every {INTERVAL}s", flush=True)

    while True:
        try:
            current_count = int(r.get('camera_samples') or 0)
            diff = current_count - last_count

            if diff >= THRESHOLD:
                message = f"🔔 *סיכום דגימות חדשות*\nנוספו: {diff} דגימות\nסה''כ בשרת: {current_count}"
                bot.send_message(MY_CHAT_ID, message, parse_mode='Markdown')
                last_count = current_count
            
            time.sleep(INTERVAL) 
        except Exception as e:
            print(f"⚠️ Monitor Error: {e}", flush=True)
            time.sleep(20)

# --- Startup ---

print("🚀 Starting Background Monitor...", flush=True)
monitor_thread = threading.Thread(target=monitor_redis_changes, daemon=True)
monitor_thread.start()

print("🚀 Starting Bot Polling...", flush=True)
try:
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
except Exception as e:
    print(f"❌ Polling crashed: {e}", flush=True)