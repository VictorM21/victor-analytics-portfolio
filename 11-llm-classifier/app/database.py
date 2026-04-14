import sqlite3
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.getenv("DB_PATH", "predictions.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                description     TEXT    NOT NULL,
                category        TEXT    NOT NULL,
                confidence      REAL    NOT NULL,
                flagged_for_review INTEGER NOT NULL DEFAULT 0,
                reasoning       TEXT,
                latency_ms      REAL,
                timestamp       TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON predictions(timestamp)
        """)
        conn.commit()


def log_prediction(data: dict):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO predictions
                (description, category, confidence, flagged_for_review,
                 reasoning, latency_ms, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["description"],
                data["category"],
                data["confidence"],
                int(data["flagged_for_review"]),
                data.get("reasoning", ""),
                data.get("latency_ms", 0),
                data.get("timestamp", datetime.utcnow().isoformat()),
            ),
        )
        conn.commit()


def get_recent_predictions(hours: int = 24) -> list[dict]:
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM predictions WHERE timestamp >= ? ORDER BY timestamp DESC",
            (since,),
        ).fetchall()
    return [dict(r) for r in rows]
