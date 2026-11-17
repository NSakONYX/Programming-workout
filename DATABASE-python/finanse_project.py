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
            
            df = pd.DataFrame(dictionary)
            df.to_sql('raw_trades', conn, if_exists='append', index=False)
            
        conn.close()
        print("Zainicjalizowano baze danych")    
        

if __name__ == '__main__':
    setup = InicializePandas()