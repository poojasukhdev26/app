import sqlite3
from datetime import date

# ✅ Initialize the menu database with necessary columns
def init_menu_db():
    conn = sqlite3.connect('menu_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mess_name TEXT,
            date TEXT,
            breakfast TEXT,
            lunch TEXT,
            dinner TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Save a menu entry (breakfast, lunch, dinner) to the DB
def save_menu(mess_name, date_value, breakfast, lunch, dinner):
    conn = sqlite3.connect('menu_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO menus (mess_name, date, breakfast, lunch, dinner)
        VALUES (?, ?, ?, ?, ?)
    ''', (mess_name, date_value, breakfast, lunch, dinner))
    conn.commit()
    conn.close()

# ✅ Fetch today's menu entries from DB
def get_today_menu():
    today = date.today().isoformat()
    conn = sqlite3.connect('menu_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT mess_name, breakfast, lunch, dinner FROM menus WHERE date = ?
    ''', (today,))
    data = c.fetchall()
    conn.close()
    return data


