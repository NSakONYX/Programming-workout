import sqlite3
import pandas as pd
from trades_dictionary import make_dict


class InicializePandas:
    def __init__(self):
        
        dictionary = make_dict()
        
        with sqlite3.connect('trades_database.db') as conn:
            cursor = conn.cursor()
            
            database = """
                CREATE TABLE IF NOT EXISTS raw_trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    price REAL,
                    volume INTEGER,
                    status TEXT
                )
            """
            
            cursor.execute(database)
            
            cursor.execute("SELECT COUNT(*) FROM raw_trades")
            ilosc_wierszy = cursor.fetchone()[0]
            
            if ilosc_wierszy == 0:
                print("Baza jest pusta. Generuję i dodaję 500 nowych transakcji...")
                dictionary = make_dict()
                df = pd.DataFrame(dictionary)
                df.to_sql('raw_trades', conn, if_exists='append', index=False)
            else:
                print(f"Baza posiada już {ilosc_wierszy} rekordów. Pomijam generowanie.")
            
        
        print("Zainicjalizowano baze danych")  
        conn.close()
        
        
        
    def analyze_portfolio(self):
        with sqlite3.connect('trades_database.db') as conn:
            
            df = pd.read_sql_query("SELECT * FROM raw_trades", conn)
            df.set_index('id', inplace=True)
            df = df[df['status'] != 'failed']
            df = df[df['status'] != 'rejected']
            
            #mozna tez df = df[~df['status'].isin(['failed', 'rejected'])]
            
            print("Wyciagnieto czyste dane:")
            print(df.head())
            
            
            return df
        conn.close()
            




if __name__ == '__main__':
    setup = InicializePandas()
    czyste_dane = setup.analyze_portfolio()


    czyste_dane['trade_value'] = czyste_dane['price'] * czyste_dane['volume']
    

    raport = czyste_dane.groupby('symbol').agg({
        'volume': 'sum',         # Sumujemy wszystkie kupione akcje
        'trade_value': 'sum',    # Sumujemy wydane dolary
        'price': 'mean'          # Wyliczamy średnią cenę zakupu
    })
    
    # Zaokrąglamy wyniki do 2 miejsc po przecinku dla czytelności
    raport = raport.round(2)
    
    print("\n--- RAPORT PORTFELA ---")
    print(raport)
    

    with sqlite3.connect('trades_database.db') as conn:
        raport.to_sql('portfolio_summary', conn, if_exists='replace')
        print("\nZapisano raport do tabeli 'portfolio_summary'!")