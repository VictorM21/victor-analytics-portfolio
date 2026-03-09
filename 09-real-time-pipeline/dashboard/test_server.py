"""
Ultra Simple Test Server
Run this first to verify WebSocket works
"""

from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Simple HTML page for testing
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
    <h1>WebSocket Connection Test</h1>
    <div id="status">Disconnected</div>
    <div id="counter">0</div>
    
    <script>
        const socket = io('http://127.0.0.1:5002');
        
        socket.on('connect', () => {
            document.getElementById('status').innerHTML = '✅ CONNECTED';
            document.getElementById('status').style.color = 'green';
        });
        
        socket.on('disconnect', () => {
            document.getElementById('status').innerHTML = '❌ DISCONNECTED';
            document.getElementById('status').style.color = 'red';
        });
        
        socket.on('counter', (data) => {
            document.getElementById('counter').innerHTML = data.value;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

def send_counter():
    """Send counter updates every second"""
    count = 0
    while True:
        count += 1
        socketio.emit('counter', {'value': count})
        print(f"Sent counter: {count}")
        time.sleep(1)

if __name__ == '__main__':
    # Start counter thread
    threading.Thread(target=send_counter, daemon=True).start()
    
    print("="*60)
    print("🚀 Test server starting on port 5002")
    print("📊 Open http://127.0.0.1:5002")
    print("="*60)
    
    socketio.run(app, debug=True, host='127.0.0.1', port=5002)