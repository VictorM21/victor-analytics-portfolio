"""
Click Consumer - Processes real-time click data
Author: Victor Makanju
"""

import json
import time
import os
import glob
from collections import defaultdict
import threading
import signal
import sys

class ClickConsumer:
    def __init__(self):
        self.metrics = {
            'total_clicks': 0,
            'unique_users': set(),
            'pages': defaultdict(int),
            'devices': defaultdict(int),
            'countries': defaultdict(int),
            'click_timestamps': []
        }
        self.running = False
        self.last_file = None
        self.last_position = 0
        self.lock = threading.Lock()
        
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Received interrupt signal. Stopping consumer...")
        self.stop()
        sys.exit(0)
    
    def get_latest_file(self):
        """Find the most recent click file"""
        try:
            files = glob.glob('data/clicks_*.json')
            if not files:
                return None
            return max(files, key=os.path.getctime)
        except Exception as e:
            print(f"Error finding files: {e}")
            return None
    
    def process_file(self):
        """Process new clicks from the latest file"""
        try:
            current_file = self.get_latest_file()
            if not current_file:
                return
            
            # If it's a new file, reset position
            if current_file != self.last_file:
                self.last_file = current_file
                self.last_position = 0
                print(f"📁 Processing new file: {current_file}")
            
            try:
                with open(current_file, 'r') as f:
                    f.seek(self.last_position)
                    new_content = f.read()
                    self.last_position = f.tell()
                    
                    if new_content:
                        self.process_content(new_content)
            except Exception as e:
                print(f"Error reading file: {e}")
                
        except Exception as e:
            print(f"Error in process_file: {e}")
    
    def process_content(self, content):
        """Process new JSON content"""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and line not in ['[', ']']:
                # Remove trailing comma if present
                if line.endswith(','):
                    line = line[:-1]
                
                try:
                    click = json.loads(line)
                    self.process_click(click)
                except json.JSONDecodeError:
                    # Skip invalid JSON
                    pass
                except Exception as e:
                    print(f"Error processing click: {e}")
    
    def process_click(self, click):
        """Process a single click"""
        try:
            with self.lock:
                self.metrics['total_clicks'] += 1
                self.metrics['unique_users'].add(click.get('user_id', 0))
                self.metrics['pages'][click.get('page', 'unknown')] += 1
                self.metrics['devices'][click.get('device', 'unknown')] += 1
                self.metrics['countries'][click.get('country', 'unknown')] += 1
                self.metrics['click_timestamps'].append(time.time())
                
                # Keep only last 100 timestamps
                if len(self.metrics['click_timestamps']) > 100:
                    self.metrics['click_timestamps'].pop(0)
        except Exception as e:
            print(f"Error in process_click: {e}")
    
    def get_current_rate(self):
        """Calculate current clicks per second"""
        try:
            with self.lock:
                if len(self.metrics['click_timestamps']) < 2:
                    return 0
                time_window = self.metrics['click_timestamps'][-1] - self.metrics['click_timestamps'][0]
                if time_window > 0:
                    return len(self.metrics['click_timestamps']) / time_window
                return 0
        except Exception:
            return 0
    
    def get_metrics(self):
        """Get current metrics"""
        try:
            with self.lock:
                return {
                    'total_clicks': self.metrics['total_clicks'],
                    'unique_users': len(self.metrics['unique_users']),
                    'pages': dict(sorted(self.metrics['pages'].items(), 
                                         key=lambda x: x[1], reverse=True)),
                    'devices': dict(self.metrics['devices']),
                    'countries': dict(sorted(self.metrics['countries'].items(),
                                            key=lambda x: x[1], reverse=True)),
                    'rate': round(self.get_current_rate(), 1)
                }
        except Exception as e:
            print(f"Error getting metrics: {e}")
            return {
                'total_clicks': 0,
                'unique_users': 0,
                'pages': {},
                'devices': {},
                'countries': {},
                'rate': 0
            }
    
    def start(self):
        """Start consuming clicks"""
        self.running = True
        print("👀 Consumer started - watching for clicks...")
        print("-" * 50)
        
        try:
            while self.running:
                self.process_file()
                time.sleep(0.5)  # Check every 0.5 seconds
                
        except KeyboardInterrupt:
            print("\n\n🛑 Keyboard interrupt received...")
            self.stop()
        except Exception as e:
            print(f"\n❌ Error in consumer: {e}")
            self.stop()
    
    def stop(self):
        """Stop consumer"""
        self.running = False
        try:
            metrics = self.get_metrics()
            print(f"\n📊 Consumer stopped after processing {metrics['total_clicks']} clicks")
            print(f"👥 Unique users: {metrics['unique_users']}")
        except Exception as e:
            print(f"\n📊 Consumer stopped (error getting final metrics: {e})")

if __name__ == '__main__':
    consumer = ClickConsumer()
    consumer.start()