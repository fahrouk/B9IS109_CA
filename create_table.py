import sqlite3

def create_table():
    conn = sqlite3.connect('users.db')
    print("Connected to database successfully")

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compname TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE, 
                    password TEXT NOT NULL,
                    addr1 TEXT NOT NULL, 
                    addr2 TEXT, 
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    zipcode TEXT NOT NULL
                )''')
    print("Created table userd successfully!")

    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compname TEXT NOT NULL,
                    creators_email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    zipcode TEXT NOT NULL,
                    startdate DATE NOT NULL,
                    duedate DATE NOT NULL,
                    image_data BLOB,
                    pdf_data BLOB 
                )''')
    print("Created table invoices successfully!")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
