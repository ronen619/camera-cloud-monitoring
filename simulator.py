import redis
import time

# חיבור ל-Redis
r = redis.Redis(host='my-db', port=6379, decode_responses=True)

print("Simulator started: Adding background detections...")

while True:
    try:
        # קידום המונה ב-1 בכל פעם
        count = r.incr('camera_samples')
        print(f"Background detection simulated! Current count: {count}")
        
        # מחכה 5 שניות בין דגימה לדגימה
        time.sleep(1) 
    except Exception as e:
        print(f"Error in simulator: {e}")
        time.sleep(10)
