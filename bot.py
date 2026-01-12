import os
import telebot
import redis
import time

# הגדרות חיבור (שים לב ל-host שתואם לשלך)
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
r = redis.Redis(host='my-db', port=6379, decode_responses=True)

@bot.message_handler(commands=['status'])
def send_status(message):
    try:
        # מושך את אותו המונה שהאתר שלך משתמש בו
        count = r.get('camera_samples') or 0
        timestamp = time.strftime('%H:%M:%S')
        text = f"📊 *סטטוס מערכת מהענן*\n" \
               f"מספר דגימות ב-Redis: {count}\n" \
               f"זמן עדכון: {timestamp}"
        bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"שגיאה: {e}")

print("Bot is starting...")
bot.infinity_polling()
