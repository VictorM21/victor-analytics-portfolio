"""
Ultra Simple Server - Guaranteed to Work
Author: Victor Makanju
Run this file directly
"""

from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import time
import threading
import random

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Initialize SocketIO with minimal settings
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    ping_timeout=60,
    ping_interval=25,
    logger=True
)

# Simple HTML template
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Dashboard</title>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f2f5; text-align: center; }
        .stats { display: flex; justify-content: center; gap: 20px; margin: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .value { font-size: 36px; font-weight: bold; color: #667eea; margin: 10px 0; }
        .connected { color: green; }
        .disconnected { color: red; }
    </style>
</head>
<body>
    <h1>📊 Simple Real-time Dashboard</h1>
    <h2 id="status" class="disconnected">❌ Disconnected</h2>
    
    <div class="stats">
        <div class="card">
            <div class="value" id="counter1">0</div>
            <div>Counter 1</div>
        </div>
        <div class="card">
            <div class="value" id="counter2">0</div>
            <div>Counter 2</div>
        </div>
        <div class="card">
            <div class="value" id="counter3">0</div>
            <div>Counter 3</div>
        </div>
    </div>

    <script>
        const socket = io('http://127.0.0.1:5002', {
            transports: ['websocket'],
            reconnection: true,
            reconnectionAttempts: 10,
            timeout: 10000
        });
        
        socket.on('connect', () => {
            document.getElementById('status').innerHTML = '✅ Connected';
            document.getElementById('status').className = 'connected';
            console.log('✅ Connected to server');
        });
        
        socket.on('disconnect', () => {
            document.getElementById('status').innerHTML = '❌ Disconnected';
            document.getElementById('status').className = 'disconnected';
            console.log('❌ Disconnected from server');
        });
        
        socket.on('update', (data) => {
            console.log('📊 Received:', data);
            document.getElementById('counter1').textContent = data.c1;
            document.getElementById('counter2').textContent = data.c2;
            document.getElementById('counter3').textContent = data.c3;
        });
    </script>
</body>
</html>
"""

# Counter
c1, c2, c3 = 0, 0, 0

@app.route('/')
def index():
    return render_template_string(HTML)

def background_updater():
    """Update counters every second"""
    global c1, c2, c3
    while True:
        c1 = random.randint(1, 100)
        c2 = random.randint(1, 100)
        c3 = random.randint(1, 100)
        socketio.emit('update', {'c1': c1, 'c2': c2, 'c3': c3})
        print(f"📤 Sent update: {c1}, {c2}, {c3}")
        time.sleep(2)

if __name__ == '__main__':
    # Start background thread
    thread = threading.Thread(target=background_updater, daemon=True)
    thread.start()
    print("✅ Background updater started")
    
    print("="*60)
    print("🚀 Server starting at http://127.0.0.1:5002")
    print("📊 Open in browser and check console")
    print("="*60)
    
    # Run on port 5002 to avoid conflicts
    socketio.run(app, debug=True, host='127.0.0.1', port=5002)