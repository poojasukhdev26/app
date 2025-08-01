import sqlite3

conn = sqlite3.connect('mess_data.db')  # same name as in your app
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS mess (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mess_name TEXT NOT NULL,
        owner_name TEXT NOT NULL,
        location TEXT NOT NULL,
        mobile TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("✅ Table 'mess' created successfully in mess_data.db.")
