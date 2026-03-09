"""
Launcher for Real-time Pipeline
Run this to start all components
"""

import subprocess
import threading
import time
import os
import sys

def run_producer():
    """Run the click producer"""
    print("🚀 Starting producer...")
    subprocess.run([sys.executable, "producer/click_producer.py"])

def run_consumer():
    """Run the click consumer"""
    print("👀 Starting consumer...")
    subprocess.run([sys.executable, "consumer/click_consumer.py"])

def run_dashboard():
    """Run the dashboard server"""
    print("📊 Starting dashboard server...")
    subprocess.run([sys.executable, "dashboard/app.py"])

if __name__ == "__main__":
    print("="*60)
    print("REAL-TIME PIPELINE LAUNCHER")
    print("="*60)
    print("\nOptions:")
    print("1. Run all components")
    print("2. Run producer only")
    print("3. Run consumer only")
    print("4. Run dashboard only")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == "1":
        print("\n🚀 Starting all components...")
        threading.Thread(target=run_producer, daemon=True).start()
        time.sleep(1)
        threading.Thread(target=run_consumer, daemon=True).start()
        time.sleep(1)
        threading.Thread(target=run_dashboard, daemon=True).start()
        
        print("\n✅ All components started!")
        print("📊 Dashboard: http://localhost:5000")
        print("\nPress Ctrl+C to stop...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
    
    elif choice == "2":
        run_producer()
    elif choice == "3":
        run_consumer()
    elif choice == "4":
        run_dashboard()
    else:
        print("Goodbye!")