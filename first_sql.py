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




#3-jak sie to robi w praktyce

def dodaj_transakcje(symbol, price, volume):
    '''Funkcja dodająca transakcje do bazy danych'''
    # Blok 'with' automatycznie zarządza połączeniem
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO trades (symbol, price, volume) VALUES (?, ?, ?)",
            (symbol, price, volume)
        )
        conn.commit()
        
dodaj_transakcje("NVDA", 135.20, 50)
dodaj_transakcje("TSLA", 210.00, 15)

def usun_transakcje(id):
    with sqlite3.connect('trading_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM trades WHERE id = ?",
            (id,)
        )
        conn.commit()
        
usun_transakcje(2)


#DODATKOWE FUNKCJE
"""
1. Row Factory (Zwracanie słowników zamiast krotek)
Domyślnie .fetchall() zwraca krotki, co zmusza Cię do pamiętania indeksów 
(np. wiersz[2] to cena). W Pythonie wystarczy jedna linijka, żeby kursor 
zaczął zwracać obiekty, z których czytasz dane po nazwach kolumn.
"""

conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT symbol, price FROM trades")

for wiersz in cursor.fetchall():
    print(wiersz["symbol"], wiersz["price"]) # Znacznie czytelniejsze inżynieryjnie
    
"""
2. Przechwytywanie wyjątków bazy danych (Error Handling)
Baza danych często odrzuca zapytania (np. próbujesz dodać duplikat do kolumny
oznaczonej jako UNIQUE albo nastąpił timeout blokady pliku). Umiejętności SQL
tu nie pomogą – musisz po stronie Pythona zabezpieczyć kod blokiem try-except,
żeby błąd nie wysypał całego terminala.
"""

try:
    cursor.execute("INSERT INTO portfolio (symbol) VALUES (?)", ("NVDA",))
    conn.commit()
except sqlite3.IntegrityError:
    print("Ten walor już istnieje w portfelu!")
    
"""
3. Bezpośrednie wpięcie w Pandas (Klucz w backtestingu i tradingu)
Jeśli pracujesz z danymi rynkowymi i szeregami czasowymi, pisanie pętli for, żeby
przepisać dane z SQL do struktur obliczeniowych, mija się z celem. Pythonowa biblioteka
Pandas posiada wbudowaną metodę, która jednym strzałem wykonuje komendę SQL i pakuje
wynik prosto do szybkiej tabeli DataFrame.
"""

"""
import pandas as pd

with sqlite3.connect('trading_data.db') as conn:
    # Jeden strzał: wykonuje SQL i tworzy gotowy do analityki obiekt DataFrame
    df = pd.read_sql_query("SELECT * FROM trades WHERE symbol = 'BTC'", conn)

# Od razu możesz liczyć np. średnią cenę:
srednia_cena = df['price'].mean()
"""

"""
4. Ostateczny poziom: ORM (Object-Relational Mapping)
W dużych, czysto obiektowych projektach (zgodnych z duchem Clean Code) w ogóle
przestaje się pisać surowe stringi SQL. Zamiast tego używa się narzędzi takich
jak SQLAlchemy. Mapujesz tabele na klasy Pythona, a biblioteka sama pod spodem
tłumaczy Twoje operacje na obiektach na najwydajniejszy kod SQL.
"""

"""
# Zamiast pisać zapytania SQL, operujesz na czystym Pythonie:
nowa_transakcja = Trade(symbol="PLTR", price=45.5, volume=100)
session.add(nowa_transakcja)
session.commit()

# Pobieranie danych:
wyniki = session.query(Trade).filter(Trade.symbol == "PLTR").all()
"""