import sqlite3

def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def insert_db(original_url, hashed_url):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO Urls (original_url, hashed_url) VALUES (?, ?)', (original_url, hashed_url,))
    conn.commit()
    conn.close()

def read_db(hashed_url):
    conn = connect_db()
    urls = conn.execute('SELECT * FROM Urls WHERE hashed_url= (?)', (hashed_url,)).fetchall()
    url = urls[0]['original_url'] if len(urls) > 0 else ''
    conn.close()
    return url