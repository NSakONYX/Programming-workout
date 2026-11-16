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
"""

import sqlite3

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
    
    
    def add(self, USER_NAME, USER_SURNAME, USER_EMAIL): 
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            insert = "INSERT INTO users (user_name,user_surname,user_email) VALUES (?,?,?)"
            values = (USER_NAME,USER_SURNAME,USER_EMAIL)
            
            cursor.execute(insert,values)
            conn.commit()
            
    
    def delete_id(self, id):
        with sqlite3.connect(self.file_name) as conn:
            cursor = conn.cursor()
            
            command = "DELETE FROM users WHERE id = ?"
            

            cursor.execute(command, (id,))
            conn.commit()
            
            
    def delete_user(self, name, surname, email):
        with sqlite3.connect(self.file_name) as conn:
                cursor = conn.cursor()
                
                command = "DELETE FROM users WHERE user_name = ? AND user_surname = ? AND user_email = ?"
                values = (name,surname,email)
                
                cursor.execute(command,values)
                conn.commit()

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

