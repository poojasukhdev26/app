import sqlite3

# Remove duplicate menus for the same mess and date, keeping only the latest (highest id)
def cleanup_menu_duplicates():
    conn = sqlite3.connect('menu_data.db')
    c = conn.cursor()
    # Find all duplicate (mess_name, date) pairs
    c.execute('''
        SELECT mess_name, date, MAX(id) as max_id
        FROM menus
        GROUP BY mess_name, date
    ''')
    keep_ids = set(row[2] for row in c.fetchall())
    # Delete all rows not in keep_ids
    c.execute('SELECT id FROM menus')
    all_ids = set(row[0] for row in c.fetchall())
    delete_ids = all_ids - keep_ids
    if delete_ids:
        c.executemany('DELETE FROM menus WHERE id = ?', [(i,) for i in delete_ids])
        print(f"Deleted {len(delete_ids)} duplicate menu entries.")
    else:
        print("No duplicates found.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    cleanup_menu_duplicates()
