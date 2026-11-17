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