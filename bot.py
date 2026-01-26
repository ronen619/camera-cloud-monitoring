import os
import telebot
import redis
import time
import threading
import datetime
from telebot import types

# הגדרות חיבור
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
r = redis.Redis(host='my-db', port=6379, decode_responses=True, socket_connect_timeout=5, socket_timeout=5)

try:
    r.ping()
    print("✅ Successfully connected to Redis")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")

# --- Handlers ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_status = types.KeyboardButton('📊 סטטוס מערכת')
    btn_reset = types.KeyboardButton('🔄 איפוס מונה')
    btn_history = types.KeyboardButton('📋 10 דגימות אחרונות')
    
    markup.add(btn_status, btn_reset, btn_history)
    bot.reply_to(message, "אהלן רונן! מערכת ה-AI המעודכנת מוכנה. בחר פעולה:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📊 סטטוס מערכת')
def status_btn_handler(message):
    try:
        count = r.get('camera_samples') or 0
        # שליפת נתוני הזיהוי החדשים
        person = r.get('last_detected_person') or "אין זיהוי"
        role = r.get('detection_role') or "N/A"
        
        timestamp = time.strftime('%H:%M:%S')
        text = (f"📊 *סטטוס מערכת חכמה*\n\n"
                f"👤 זוהה לאחרונה: *{person}*\n"
                f"🏷️ תפקיד: {role}\n"
                f"🔢 סה''כ דגימות: {count}\n"
                f"🕒 זמן עדכון: {timestamp}")
        
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת נתונים: {e}")

@bot.message_handler(func=lambda message: message.text == '🔄 איפוס מונה')
def reset_btn_handler(message):
    try:
        r.set('camera_samples', 0)
        r.delete('camera_history')
        # איפוס נתוני זיהוי
        r.set('last_detected_person', "None")
        r.set('detection_role', "N/A")
        
        bot.reply_to(message, "✅ המערכת אופסה: המונה, ההיסטוריה והזיהויים נוקו.")
    except Exception as e:
        bot.reply_to(message, f"שגיאה באיפוס: {e}")

@bot.message_handler(func=lambda message: message.text == '📋 10 דגימות אחרונות')
def history_btn_handler(message):
    try:
        history = r.lrange('camera_history', 0, 9)
        if not history:
            bot.reply_to(message, "אין עדיין דגימות רשומות בהיסטוריה.")
            return

        text = "📸 *היסטוריית זיהויים אחרונה:*\n\n"
        for i, entry in enumerate(history, 1):
            text += f"{i}. `{entry}`\n"
            
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת היסטוריה: {e}")

# --- Background Monitor (התראות חכמות) ---

def monitor_redis_changes():
    MY_CHAT_ID = 770737566 
    THRESHOLD = 200 
    INTERVAL = 15  # בדיקה תכופה יותר כדי לתפוס זיהויים בזמן
    
    try:
        last_count = int(r.get('camera_samples') or 0)
    except:
        last_count = 0
        
    print(f"📢 Monitor started: Alert every {THRESHOLD} samples", flush=True)

    while True:
        try:
            current_count = int(r.get('camera_samples') or 0)
            diff = current_count - last_count

            if diff >= THRESHOLD:
                # שליפת פרטי האדם שגרם להתראה
                person = r.get('last_detected_person') or "Unknown"
                role = r.get('detection_role') or "Guest"
                priority = r.get('alert_priority') or "Low"

                if priority == "High":
                    message = (f"🚨 *התראת אבטחה דחופה*\n\n"
                               f"👤 דמות לא מורשית: *{person}*\n"
                               f"⚠️ סטטוס: {role}\n"
                               f"📈 מונה חריגות: {current_count}")
                else:
                    message = (f"✅ *עדכון פעילות שגרתי*\n\n"
                               f"👤 זוהה: *{person}*\n"
                               f"📝 תפקיד: {role}\n"
                               f"🔢 סה''כ דגימות: {current_count}")

                bot.send_message(MY_CHAT_ID, message, parse_mode='Markdown')
                last_count = current_count
            
            time.sleep(INTERVAL) 
        except Exception as e:
            print(f"⚠️ Monitor Error: {e}", flush=True)
            time.sleep(20)

# הפעלה
print("🚀 Starting Background Monitor...", flush=True)
threading.Thread(target=monitor_redis_changes, daemon=True).start()

print("🚀 Starting Bot Polling...", flush=True)
bot.infinity_polling(skip_pending=True)