import redis
import time
import random

# חיבור ל-Redis - שים לב: שמרנו על 'my-db' כדי שהדוקר יעבוד!
r = redis.Redis(host='my-db', port=6379, decode_responses=True)

# רשימת דמויות לסימולציה של זיהוי פנים
PEOPLE = [
    {"name": "Ronen Gilboa", "role": "Owner", "priority": "Low"},
    {"name": "Alma", "role": "Family", "priority": "Low"},
    {"name": "Unknown Guest", "role": "Unauthorized", "priority": "High"},
    {"name": "Delivery Person", "role": "Service", "priority": "Medium"}
]

print("🚀 AI Simulator started: Combined Motion & Face Recognition...")

while True:
    try:
        # 1. בחירת דמות רנדומלית
        detection = random.choice(PEOPLE)
        
        # 2. קידום המונה (שמרנו על השם camera_samples מהקוד המקורי שלך)
        count = r.incr('camera_samples')
        
        # 3. יצירת חותמת זמן
        timestamp = time.strftime('%d/%m %H:%M:%S')
        
        # 4. יצירת רשומה מפורטת שכוללת את השם שזוהה
        # זה יופיע ברשימת ה-10 האחרונים שלך
        history_entry = f"#{count} | {detection['name']} | {timestamp}"
        
        # 5. עדכון ההיסטוריה ב-Redis (כמו בקוד המקורי שלך)
        r.lpush('camera_history', history_entry) 
        r.ltrim('camera_history', 0, 9) 
        
        # 6. עדכון מפתחות ה-AI (לשימוש עתידי בדאשבורד)
        r.set('last_detected_person', detection['name'])
        r.set('detection_role', detection['role'])
        r.set('alert_priority', detection['priority'])

        print(f"✅ Simulated: {history_entry} ({detection['role']})")
        
        # מחכה 5 שניות
        time.sleep(5) 
        
    except Exception as e:
        print(f"Error in simulator: {e}")
        time.sleep(10)