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



#1-dodawanie danych do tabeli (zasady bezpieczeństwa)
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

cursor.execute(zapytanie_insert, dane_do_wstawienia) #cursor przyjmuje 1 albo 2 argumenty. 1 obowiazkowy z komenda i 2 opcjonalny z danymi
conn.commit()


#conn.fetchall()
"""
Kiedy wykonujesz zapytanie SELECT, baza danych odszukuje odpowiednie wiersze, 
ale nie przesyła ich od razu do zmiennej w Pythonie. Zamiast tego kursor ustawia 
się na początku odszukanych wyników (trochę jak wskaźnik na początek bloku pamięci).

Metoda .fetchall() ("przynieś wszystko") to polecenie, które każe kursorowi 
zassać wszystkie znalezione wiersze naraz i zapisać je w pamięci RAM Pythona w formie listy.

Wynikiem działania .fetchall() jest zawsze lista krotek. Każda krotka w liście 
reprezentuje jeden wiersz z bazy danych, a jej elementy to kolumny.
"""

#2-Odczyt danych z tabeli
cursor.execute("SELECT * FROM trades WHERE symbol = ?", ("PLTR",)) #? w stringu oznacza miejsce jakiejs zmiennej

wyniki = cursor.fetchall()
for wiersz in wyniki:
    # wiersz to krotka: (1, 'PLTR', 45.5, 100)
    print(f"ID: {wiersz[0]} | Ticker: {wiersz[1]} | Cena: {wiersz[2]}$ | Ilość: {wiersz[3]}")

conn.close() #zamkniecie połaczenia z baza danych