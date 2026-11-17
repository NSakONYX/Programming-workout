import sqlite3
import pandas as pd

#podpinanie sie pod baze trades
with sqlite3.connect('trading_data.db') as conn:
    df = pd.read_sql_query("SELECT * FROM trades", conn) #df - obiekt DataFrame
    
#1. Szybki look na baze (5 pierwszych wierszy)
print(df.head())
print("\n\n")

# 2. Inspekcja techniczna (typy danych, zużycie pamięci RAM, brakujące wartości)
print(df.info())
print("\n\n")

# 3. Wyciągnięcie jednej kolumny jako obiektu Series
symbole = df['symbol']
print(symbole)
print("\n\n")

# 4. Filtrowanie samych wierszzy (odpowiednik WHERE, ale działający w pamięci podręcznej)
# Zwraca tylko wiersze, gdzie nazwisko to Kowalski
PLTR_ROWS = df[df['symbol'] == 'PLTR']
print(PLTR_ROWS)
print("\n\n")

"""
Krytyczna zasada Pandas: Jeśli chcesz wyciągnąć jedną kolumnę, piszesz df['id']. 
Ale jeśli chcesz wyciągnąć dwie lub więcej, musisz przekazać je jako listę, 
stąd biorą się podwójne nawiasy: df[['id', 'symbols']].
"""
#5. Filtrowanie konkretnych kolumn
PLTR_INDEXES = df.loc[df['symbol']=='PLTR',['id','symbol']]
print(PLTR_INDEXES)

"""
#teraz jeszcze kilka przykładów z .iloc
# 1. Konkretny wiersz (zwraca wszystkie kolumny dla tego wiersza)
pierwszy_wiersz = df.iloc[0] 
setny_wiersz = df.iloc[99]

# 2. Konkretna komórka (np. 1. wiersz, 3. kolumna)
komorka = df.iloc[0, 2] 

# 3. Przedział wierszy (slicing)
pierwsze_piec = df.iloc[0:5]  # Wyciąga wiersze o pozycjach 0, 1, 2, 3, 4

# 4. Wycinanie w obu osiach (wiersze i kolumny naraz)
# Wyciąga wiersze 10-19, ale tylko z pierwszych dwóch kolumn (np. id i symbol)
wycinek = df.iloc[10:20, 0:2] 

# 5. Wyciągnięcie konkretnych rzędów i kolumn (nie po kolei)
wybiorczo = df.iloc[[0, 5, 10], [0, 3]] # Wiersze 0, 5, 10 z kolumn 0 i 3
"""

#--------------------------------------------------------------------------
#tworzenie nowej kolumny 'is_True' i dla kazdego wiersza ustawiamy True
df['is_active']=True 

#wyciąganie kolumny/kolumn
symbole = df['symbol']
id_symbole = df[['id','symbol']]#!Podwójne nawiasy!

print(df.loc[10,['symbol','price']]) #szuka 10 wiersza (liczac od 0) i wypisuje z niego symbol i cene

#to robimy zeby to patrzyło po naszej kolumnie id TYLKO TRZEBA NA NOWO OTWORZYC with sqlite3.connect...
df = pd.read_sql_query("SELECT * FROM trades", conn)
# Ustawiamy kolumnę 'id' jako główny system nawigacyjny tabeli
df.set_index('id', inplace=True)
# Teraz to zadziała tak, jak początkowo zakładałeś (wyciągnie TSLA)
print(df.loc[10, ['symbol', 'price']])

#LUB KLASYCZNIE
df[df['id'] == 10]

# Zmienia cenę tylko dla konkretnego rekordu o indeksie 10
df.loc[10, 'price'] = 250.0
# Szuka wszystkich wierszy NVDA i zmienia w nich flagę na False
df.loc[df['symbol'] == 'NVDA', 'is_active'] = False

# Przelicza cały wolumen w tabeli jednym ruchem procesora
df['volume'] = df['volume'] * 2

df.drop('is_active', axis=1, inplace=True)

# Alternatywnie, możesz użyć wbudowanego polecenia Pythona:
del df['is_active']


'''
Podczas obróbki danych rzadko pisze się pętle z funkcją drop(), by 
wykasować wiele rekordów. Zamiast tego w Pandasie stosuje się tak 
zwane "negatywne filtrowanie". Nadpisujesz po prostu obecną tabelę 
danymi, które spełniają odwrotny warunek.
'''


# Fizycznie "usuwa" spółkę PLTR z pamięci RAM, zachowując całą resztę (!=)
df = df[df['symbol'] != 'PLTR']