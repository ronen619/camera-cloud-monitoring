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
        <title>מערכת ניטור AI</title>
        <style>
            body { background-color: #2c3e50; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; padding: 20px; }
            .card { background-color: #34495e; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 10px 20px rgba(0,0,0,0.3); border: 1px solid #455a64; }
            .count { font-size: 80px; color: #2ecc71; font-weight: bold; margin: 20px 0; transition: all 0.3s ease; }
            .btn { background-color: #e74c3c; color: white; border: none; padding: 12px 25px; font-size: 18px; border-radius: 8px; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #c0392b; transform: scale(1.05); }
            .status { color: #bdc3c7; font-size: 14px; }
        </style>
        <script>
            // פונקציה שמושכת נתונים בלי לרענן את הדף
            function updateData() {
                fetch('/get_data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('counter').innerText = data.count;
                        document.getElementById('time').innerText = data.time;
                    });
            }
            
            // פונקציית איפוס חלקה
            function resetCounter() {
                fetch('/reset_data').then(() => updateData());
            }

            // הפעלה כל 2 שניות
            setInterval(updateData, 2000);
        </script>
    </head>
    <body>
        <div class="card">
            <h1>מערכת ניטור מצלמות AI</h1>
            <p class="status">זמן דגימה אחרון: <span id="time">טוען...</span></p>
            <div id="counter" class="count">0</div>
            <p>הנתונים נשלפים ב-Real-time משרת ה-Redis בענן</p>
            <button onclick="resetCounter()" class="btn">איפוס מונה מצלמה</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/get_data')
def get_data():
    # כאן אנחנו מקדמים את המונה ומחזירים JSON
    count = r.get('camera_samples')
    if count is None:
        count = 0
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return jsonify(count=count, time=current_time)

@app.route('/reset_data')
def reset_data():
    r.set('camera_samples', 0)
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
