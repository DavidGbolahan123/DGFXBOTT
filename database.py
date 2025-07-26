# database.py

import sqlite3
import os
from config import DATABASE_PATH, DB_TABLES

def init_database():
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()

        # Create signal_logs table
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {DB_TABLES["signals"]} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                timeframe TEXT,
                direction TEXT,
                score REAL,
                sl_price REAL,
                tp_price REAL,
                rr_ratio REAL,
                status TEXT,
                trend TEXT
            )
        ''')

        # Create trades table for win/loss tracking
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {DB_TABLES["trades"]} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                result TEXT,
                pnl REAL,
                entry REAL,
                exit REAL,
                sl REAL,
                tp REAL
            )
        ''')

        # Create bot_health table
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {DB_TABLES["bot_health"]} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                status TEXT,
                notes TEXT
            )
        ''')

        conn.commit()
        conn.close()

def insert_signal_log(signal_data):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''
        INSERT INTO {DB_TABLES["signals"]} 
        (timestamp, symbol, timeframe, direction, score, sl_price, tp_price, rr_ratio, status, trend)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', signal_data)
    conn.commit()
    conn.close()

def insert_trade_result(trade_data):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''
        INSERT INTO {DB_TABLES["trades"]}
        (timestamp, symbol, result, pnl, entry, exit, sl, tp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', trade_data)
    conn.commit()
    conn.close()

def insert_bot_health(status_data):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''
        INSERT INTO {DB_TABLES["bot_health"]}
        (timestamp, status, notes)
        VALUES (?, ?, ?)
    ''', status_data)
    conn.commit()
    conn.close()

def fetch_all_signals():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''SELECT * FROM {DB_TABLES["signals"]} ORDER BY timestamp DESC''')
    data = c.fetchall()
    conn.close()
    return data

def fetch_all_trades():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''SELECT * FROM {DB_TABLES["trades"]} ORDER BY timestamp DESC''')
    data = c.fetchall()
    conn.close()
    return data

def fetch_bot_health():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(f'''SELECT * FROM {DB_TABLES["bot_health"]} ORDER BY timestamp DESC LIMIT 1''')
    data = c.fetchone()
    conn.close()
    return data
