"""
Click Producer - Generates real-time click data
Author: Victor Makanju
"""

import time
import json
import random
from datetime import datetime
import os
import signal
import sys

class ClickProducer:
    def __init__(self):
        self.pages = ['home', 'products', 'product_detail', 'cart', 'checkout', 'search']
        self.devices = ['mobile', 'desktop', 'tablet']
        self.browsers = ['chrome', 'safari', 'firefox', 'edge']
        self.countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia']
        self.running = False
        self.click_count = 0
        self.start_time = time.time()
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create filename with timestamp
        self.filename = f"data/clicks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Initialize JSON file
        try:
            with open(self.filename, 'w') as f:
                f.write('[\n')
            print(f"📁 Created file: {self.filename}")
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            sys.exit(1)
        
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Received interrupt signal. Stopping producer...")
        self.stop()
        sys.exit(0)
    
    def generate_click(self):
        """Generate a single click event"""
        self.click_count += 1
        return {
            'click_id': self.click_count,
            'timestamp': datetime.now().isoformat(),
            'user_id': random.randint(1, 1000),
            'page': random.choice(self.pages),
            'device': random.choice(self.devices),
            'browser': random.choice(self.browsers),
            'country': random.choice(self.countries),
            'duration': round(random.uniform(5, 300), 2)
        }
    
    def save_click(self, click):
        """Save click to file"""
        try:
            with open(self.filename, 'a') as f:
                f.write(json.dumps(click) + ',\n')
        except Exception as e:
            print(f"⚠️ Error saving click: {e}")
    
    def start(self):
        """Start generating clicks"""
        self.running = True
        print(f"🚀 Producer started - generating 10 clicks/second")
        print(f"📊 Press Ctrl+C to stop")
        print("-" * 50)
        
        try:
            while self.running:
                click = self.generate_click()
                self.save_click(click)
                
                # Print progress every 50 clicks
                if self.click_count % 50 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.click_count / elapsed if elapsed > 0 else 0
                    print(f"📈 Generated {self.click_count} clicks ({rate:.1f}/sec)")
                
                time.sleep(0.1)  # 10 clicks per second
                
        except KeyboardInterrupt:
            print("\n\n🛑 Keyboard interrupt received...")
            self.stop()
        except Exception as e:
            print(f"\n❌ Error in producer: {e}")
            self.stop()
    
    def stop(self):
        """Stop producer and fix JSON file"""
        self.running = False
        elapsed = time.time() - self.start_time
        rate = self.click_count / elapsed if elapsed > 0 else 0
        
        print(f"\n📊 Producer stopped after {self.click_count} clicks")
        print(f"⏱️  Runtime: {elapsed:.1f} seconds")
        print(f"⚡ Average rate: {rate:.1f} clicks/second")
        
        # Fix JSON file (remove trailing comma and add closing bracket)
        try:
            with open(self.filename, 'rb+') as f:
                # Go to end minus 3 chars (to remove ",\n")
                f.seek(-3, 2)
                f.truncate()
                f.write(b'\n]')
            print(f"✅ Data saved to: {self.filename}")
        except Exception as e:
            print(f"⚠️ Could not finalize JSON file: {e}")
            print(f"💾 Raw data still in: {self.filename}")

if __name__ == '__main__':
    producer = ClickProducer()
    producer.start()