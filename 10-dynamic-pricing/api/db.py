import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'predictions.db')

def init_db():
    """Initialize the SQLite database table for storing predictions."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            product_id TEXT,
            current_price REAL,
            competitor_price REAL,
            recommended_price REAL,
            lower_ci REAL,
            upper_ci REAL,
            expected_profit REAL,
            risk REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_prediction(data):
    """Insert a prediction record into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions (
            timestamp, product_id, current_price, competitor_price,
            recommended_price, lower_ci, upper_ci, expected_profit, risk
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        data['product_id'],
        data['current_price'],
        data.get('competitor_price'),
        data['recommended_price'],
        data['lower_ci'],
        data['upper_ci'],
        data['expected_profit'],
        data['risk']
    ))
    conn.commit()
    conn.close()

def get_stats():
    """Return basic statistics from the predictions table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM predictions")
    total = c.fetchone()[0]
    c.execute("SELECT AVG(expected_profit) FROM predictions")
    avg_profit = c.fetchone()[0]
    conn.close()
    return total, avg_profit
