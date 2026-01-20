import redis
import time

# חיבור ל-Redis
r = redis.Redis(host='my-db', port=6379, decode_responses=True)

print("Simulator started: Adding background detections with full details...")

while True:
    try:
        # 1. קידום המונה ב-1 בכל פעם
        count = r.incr('camera_samples')
        
        # 2. יצירת חותמת זמן
        timestamp = time.strftime('%d/%m %H:%M:%S')
        
        # 3. יצירת רשומה מפורטת שכוללת גם את המונה וגם את הזמן
        history_entry = f"דגימה #{count} | {timestamp}"
        
        # 4. דחיפת הרשומה המפורטת לרשימה ב-Redis
        r.lpush('camera_history', history_entry) 
        r.ltrim('camera_history', 0, 9) # שומר את ה-10 האחרונים
        
        # הדפסה ללוג של הקונטיינר כדי שתוכל לעקוב ב-SSH
        print(f"✅ Simulated: {history_entry}")
        
        # מחכה 5 שניות בין דגימה לדגימה
        time.sleep(5) 
    except Exception as e:
        print(f"Error in simulator: {e}")
        time.sleep(10)