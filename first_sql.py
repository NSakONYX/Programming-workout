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



#dodawanie danych do tabeli (zasady bezpieczeństwa)
"""
Nigdy nie wklejaj zmiennych bezpośrednio do stringa SQL (np. przez f-stringi), 
bo otwiera to drogę do ataku SQL Injection i błędów formatowania. 
Używaj znaków zapytania ?, a dane przekazuj jako krotkę (tuple).
"""

ticker = "PLTR"
cena_zakupu = 170.02
ilosc_akcji = 100

zapytanie_insert = "INSERT INTO trades (symbol,price,volume) VALUES (?,?,?)"
dane_do_wstawienia = (ticker, cena_zakupu, ilosc_akcji)

cursor.execute(zapytanie_insert, dane_do_wstawienia)
conn.commit()


