"""
Fixed Dashboard Server - Based on Working Simple Server
Author: Victor Makanju
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import random
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Initialize SocketIO with same settings as working server
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    ping_timeout=60,
    ping_interval=25,
    logger=True
)

# Data storage
data = {
    'total_clicks': 0,
    'unique_users': 0,
    'rate': 0,
    'pages': {},
    'devices': {},
    'countries': {}
}

def generate_data():
    """Generate realistic-looking data"""
    pages_list = ['home', 'products', 'cart', 'checkout', 'search']
    devices_list = ['mobile', 'desktop', 'tablet']
    countries_list = ['USA', 'Canada', 'UK', 'Germany', 'France']
    
    while True:
        # Update data
        data['total_clicks'] += random.randint(5, 15)
        data['unique_users'] = data['total_clicks'] // 10
        data['rate'] = random.randint(8, 12)
        
        # Update pages
        data['pages'] = {page: random.randint(10, 100) for page in pages_list}
        
        # Update devices
        data['devices'] = {device: random.randint(20, 80) for device in devices_list}
        
        # Update countries
        data['countries'] = {country: random.randint(5, 50) for country in countries_list}
        
        # Broadcast to all clients
        socketio.emit('metrics_update', data)
        print(f"📤 Sent update: {data['total_clicks']} clicks")
        
        time.sleep(2)

@app.route('/')
def index():
    """Serve the dashboard"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for initial data"""
    return data

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('✅ Client connected')
    emit('connected', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('❌ Client disconnected')

if __name__ == '__main__':
    # Start data generator
    thread = threading.Thread(target=generate_data, daemon=True)
    thread.start()
    print("✅ Data generator started")
    
    print("="*60)
    print("🚀 Server starting at http://127.0.0.1:5001")
    print("="*60)
    
    socketio.run(app, debug=True, host='127.0.0.1', port=5001)