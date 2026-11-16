import sqlite3

#tworzenie bazy danych i tabeli
conn = sqlite3.connect('trading_data.db')


#utworzenie 'kursora'
cursor = conn.cursor()

#komenda SQL
tworzenie_tabeli = """
    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price REAL NOT NULL,
        volume INTEGER,
        trade_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
cursor.execute(tworzenie_tabeli)

#zatwierdzenie zmian
conn.commit()
