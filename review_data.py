import sqlite3

def init_review_db():
    conn = sqlite3.connect('mess_data.db')  # or create a new one like reviews.db
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mess_name TEXT NOT NULL,
            review TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
