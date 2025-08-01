import sqlite3

def create_db():
    conn = sqlite3.connect('mess_data.db')  # ✅ Database name fixed
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mess_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mess_name TEXT,
            owner_name TEXT,
            location TEXT,
            mobile TEXT UNIQUE,
            otp TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()
