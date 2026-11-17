"""
Obiektowy mini-projekt:
system zarządzający bazą danych klientów sklepu

kolumny: id, user_name, user_surname, user_email, join_date 

metody do zaimplementowania:
-add
-delete
-clear_table
-print_colum
-print_table


Zarządzanie stanem (UPDATE): Zaimplementuj metodę update_email(self, id, new_email), żeby przećwiczyć modyfikowanie istniejących rekordów.

Architektura relacyjna (CRM): Stwórz drugą tabelę services, połączoną kluczem obcym (Foreign Key) z users.id. Pozwoli to śledzić historię usług dla konkretnego klienta – idealne środowisko pod modelowanie realnego biznesu, np. przypisywanie do klienta zleceń na pranie ekstrakcyjne, czyszczenie parowe tapicerki czy renowację plastików w konkretnym modelu auta.

System autoryzacji: Dodaj kolumnę na hasło i wykorzystaj bibliotekę bcrypt (lub wbudowane hashlib), aby haszować hasła przed wykonaniem INSERT. Świetna wprawka, jeśli ten moduł miałby w przyszłości służyć do logowania użytkowników do terminala analitycznego.

Wyszukiwarka wzorców (LIKE): Metoda search_users(self, keyword), używająca w SQL operatora LIKE '%keyword%'. Pozwala odnaleźć klienta w bazie, znając tylko fragment jego maila albo początek nazwiska.

Wdrożenie "Soft Delete": Zmiana struktury tabeli tak, by zaimplementować mechanizm miękkiego usuwania, o którym rozmawialiśmy, zabezpieczający historię operacji przed permanentnym skasowaniem komendą DELETE.
"""

import sqlite3
import unittest
import os

class UsersDatabase:
    def __init__(self, name):
        '''
        W inicjalizatorze tworzymy baze danych i tabele, której nazwę określamy w konstruktorze ()  
        id - user_name - user_surname - user_email - join_date
        '''
        self.file_name = f"{name}.db"
        
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            make_table = """
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                user_surname TEXT NOT NULL,
                user_email TEXT UNIQUE NOT NULL,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(make_table)
            conn.commit()
        conn.close()
    
    
    def add(self, USER_NAME, USER_SURNAME, USER_EMAIL): 
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            insert = "INSERT INTO users (user_name,user_surname,user_email) VALUES (?,?,?)"
            values = (USER_NAME,USER_SURNAME,USER_EMAIL)
            
            cursor.execute(insert,values)
            conn.commit()
        conn.close()
            
    
    def delete_id(self, id):
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            command = "DELETE FROM users WHERE id = ?"
            

            cursor.execute(command, (id,))
            conn.commit()
        conn.close()
            
            
    def delete_user(self, name, surname, email):
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            command = "DELETE FROM users WHERE user_name = ? AND user_surname = ? AND user_email = ?"
            values = (name,surname,email)
            
            cursor.execute(command,values)
            conn.commit()
        conn.close()

    def clear_table(self):
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            command = "DELETE FROM users"
            cursor.execute(command)
            conn.commit()


    def print_table(self):
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            command = "SELECT * FROM users"
            cursor.execute(command)
            
            wyniki = cursor.fetchall()
            for wiersz in wyniki:
                print(f"ID: {wiersz[0]} | NAME: {wiersz[1]} | SURNAME: {wiersz[2]} | EMAIL: {wiersz[3]} | DATE: {wiersz[4]}")
        conn.close()
        
        


class TestUsersDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db_name = "test_baza"
        self.db = UsersDatabase(self.test_db_name)

    def tearDown(self):
        import gc
        gc.collect() # Wymusza zamknięcie wszystkich wiszących w pamięci uchwytów
        
        if os.path.exists(f"{self.test_db_name}.db"):
            os.remove(f"{self.test_db_name}.db")

    def test_add_user(self):
        self.db.add("Jan", "Kowalski", "jan@test.com")
        with sqlite3.connect(f"{self.test_db_name}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_email = 'jan@test.com'")
            user = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "Jan")
        self.assertEqual(user[2], "Kowalski")

    def test_delete_id(self):
        self.db.add("Anna", "Nowak", "anna@test.com")
        with sqlite3.connect(f"{self.test_db_name}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE user_email = 'anna@test.com'")
            user_id = cursor.fetchone()[0]
        conn.close()
            
        self.db.delete_id(user_id)
        
        with sqlite3.connect(f"{self.test_db_name}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            deleted_user = cursor.fetchone()
        conn.close()
            
        self.assertIsNone(deleted_user)

    def test_clear_table(self):
        self.db.add("A", "B", "1@test.com")
        self.db.add("C", "D", "2@test.com")
        self.db.clear_table()
        
        with sqlite3.connect(f"{self.test_db_name}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
        conn.close()
            
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()