import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  session_id TEXT, 
                  role TEXT, 
                  content TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def add_message(session_id, role, content):
    if not os.path.exists(DB_PATH):
        init_db()
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chats (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (session_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(session_id, limit=10):
    if not os.path.exists(DB_PATH):
        return []
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chats WHERE session_id=? ORDER BY id DESC LIMIT ?", 
              (session_id, limit))
    rows = c.fetchall()
    conn.close()
    
    # Return chronologically
    return [{"role": r[0], "content": r[1]} for r in rows][::-1]
