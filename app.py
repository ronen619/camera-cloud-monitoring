from flask import Flask, render_template_string, jsonify
import redis
import datetime

app = Flask(__name__)

# חיבור ל-Redis
r = redis.Redis(host='my-db', port=6379, decode_responses=True)

@app.route('/')
def index():
    # דף הבית רק מציג את המבנה, ה-JavaScript יעשה את השאר
    html_template = """
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>מערכת ניטור AI & זיהוי פנים</title>
        <style>
            body { background-color: #1a1a2e; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: auto; }
            .card { background-color: #16213e; padding: 25px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); border: 1px solid #0f3460; margin-bottom: 20px; }
            
            /* עיצוב כרטיס הזהות */
            .identity-card { border-right: 8px solid #2ecc71; transition: all 0.5s ease; }
            .high-priority { border-right-color: #e74c3c; animation: pulse 2s infinite; }
            
            .name-label { font-size: 18px; color: #95a5a6; margin: 0; }
            .person-name { font-size: 42px; font-weight: bold; color: #fff; margin: 10px 0; }
            .badge { padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: bold; text-transform: uppercase; }
            .bg-owner { background-color: #27ae60; }
            .bg-unauthorized { background-color: #c0392b; }
            
            .count { font-size: 60px; color: #f1c40f; font-weight: bold; }
            .btn { background-color: #e74c3c; color: white; border: none; padding: 12px 25px; border-radius: 10px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            .btn:hover { background-color: #c0392b; transform: translateY(-2px); }
            
            /* עיצוב רשימת ההיסטוריה */
            .history-container { text-align: right; background: #0f3460; padding: 15px; border-radius: 15px; margin-top: 20px; }
            .history-item { border-bottom: 1px solid #1a1a2e; padding: 8px; font-size: 14px; font-family: monospace; }
            .history-item:last-child { border: none; }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
                70% { box-shadow: 0 0 0 20px rgba(231, 76, 60, 0); }
                100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
            }
        </style>
        <script>
            function updateData() {
                fetch('/get_data')
                    .then(response => response.json())
                    .then(data => {
                        // עדכון המונה והזמן
                        document.getElementById('counter').innerText = data.count;
                        document.getElementById('time').innerText = data.time;
                        
                        // עדכון השם והזהות
                        document.getElementById('person-name').innerText = data.last_person;
                        const roleBadge = document.getElementById('role-badge');
                        roleBadge.innerText = data.role;
                        
                        // שינוי עיצוב לפי סוג הדמות
                        const idCard = document.getElementById('id-section');
                        if (data.priority === 'High') {
                            idCard.classList.add('high-priority');
                            roleBadge.style.backgroundColor = '#e74c3c';
                        } else {
                            idCard.classList.remove('high-priority');
                            roleBadge.style.backgroundColor = '#27ae60';
                        }

                        // עדכון רשימת ההיסטוריה
                        const historyList = document.getElementById('history-list');
                        historyList.innerHTML = '';
                        data.history.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'history-item';
                            div.innerText = '🔍 ' + item;
                            historyList.appendChild(div);
                        });
                    });
            }
            
            function resetCounter() {
                fetch('/reset_data').then(() => updateData());
            }

            setInterval(updateData, 2000);
        </script>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ מרכז ניטור ובקרת כניסה AI</h1>
            
            <div id="id-section" class="card identity-card">
                <p class="name-label">דמות שזוהתה לאחרונה:</p>
                <div id="person-name" class="person-name">טוען...</div>
                <span id="role-badge" class="badge bg-owner">טוען...</span>
            </div>

            <div class="card">
                <div class="count" id="counter">0</div>
                <p>סך כל אירועי המערכת</p>
                <p class="status">זמן סנכרון אחרון: <span id="time">...</span></p>
                <button onclick="resetCounter()" class="btn">איפוס נתונים</button>
            </div>

            <div class="history-container">
                <h3 style="margin-top:0">📜 לוג אירועים (Cloud History):</h3>
                <div id="history-list">
                    </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/get_data')
def get_data():
    # 1. שליפת המונה הקיים
    count = r.get('camera_samples') or 0
    
    # 2. שליפת נתוני ה-AI החדשים מה-Redis
    person = r.get('last_detected_person') or "No detection"
    role = r.get('detection_role') or "N/A"
    priority = r.get('alert_priority') or "Low"
    
    # 3. שליפת רשימת ההיסטוריה (10 האחרונים)
    history = r.lrange('camera_history', 0, 9)
    
    # 4. זמן שרת נוכחי (כמו שהיה לך קודם)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    # 5. החזרת ה-JSON המורחב
    return jsonify(
        count=count, 
        time=current_time,
        last_person=person,
        role=role,
        priority=priority,
        history=history
    )

@app.route('/reset_data')
def reset_data():
    r.set('camera_samples', 0)
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
